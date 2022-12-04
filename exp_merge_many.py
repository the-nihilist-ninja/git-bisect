import copy
from functools import reduce
import pprint
from config import _STASH_PATH, DEVICE, LAMBDA_ARRAY, TEST, TRAIN
from models.mlp import LAYER_NAMES, MLP, WEIGHT_PERM_LOOKUP
import torch
from models.utils import cifar10_loader
from permuter._algo import WeightMatching
from permuter.common import combine_models, get_losses
from permuter.mlp import permute_model
import  numpy as np




def combine_many_models(*models:MLP):
    """
    Combine multiple models

    :param model1: Model 1
    :type model1: torch.nn.Module
    :param model2: Model 2
    :type model2: torch.nn.Module
    :param lam: Lambda value in linear interpolation way
    :type lam: float
    :return: Combined model
    :rtype: torch.nn.Module
    """
    # Creating dummy model
    combined_model = copy.deepcopy(models[0]).to(DEVICE)
    combined_model_sd = combined_model.state_dict()
    list_sd = [model.state_dict() for model in models ]
    

    for key in combined_model_sd.keys():
        combined_model_sd[key] = (1/len(models)) * reduce(lambda x,y: torch.add(x, y), [sd[key] for sd in list_sd])

    combined_model.load_state_dict(combined_model_sd)
    return combined_model

def get_permuted_model(model1, model2):
    weight_matcher = WeightMatching(arch=LAYER_NAMES, perm_lookup=WEIGHT_PERM_LOOKUP)
    perm_dict = weight_matcher.evaluate_permutation(
            m1_weights=model1.state_dict(), m2_weights=model2.state_dict()
        )
    permuted_model = permute_model(model=model2,  perm_dict=perm_dict)
    return permuted_model

if __name__ == "__main__":
    
    models = list()
    NUM_MODELS = 5
    for i in range(NUM_MODELS):
        m = MLP().to(DEVICE)
        m.load_state_dict(torch.load(_STASH_PATH.joinpath(f"mlp{i+1}_512_20.pth")))
        models.append(m)
    
    # Getting permutation_dict for each model
    _permutation_model = [
        get_permuted_model(models[0], models[j])
        for j in range(1,NUM_MODELS)
        ]
    
    
    train_loader, test_loader, _ = cifar10_loader(batch_size=128)
    
    def _generate_models(model1: torch.nn.Module, model2: torch.nn.Module) -> tuple:
        """
        Internal function to ensure temporary tensors gets erased

        :param _model2: Model 2
        :type _model2: torch.nn.Module
        :return: Result dictionary
        :rtype: dict[str, np.ndarray]
        """
        _models = list()
        for lam in LAMBDA_ARRAY:
            tmp = combine_models(model1=model1, model2=model2, lam=lam)
            tmp.eval()
            _models.append(tmp)
        _res = {
            TRAIN: get_losses(
                data_loader=train_loader,
                combined_models=_models,
            ),
            TEST: get_losses(
                data_loader=test_loader,
                combined_models=_models,
            ),
        }
        pprint.pprint(_res)
        return max(_res[TRAIN]) - 0.5*(_res[TRAIN][0] + _res[TRAIN][-1]), max(_res[TEST]) - 0.5*(_res[TEST][0] + _res[TEST][-1])
    
    print(_generate_models(models[0], _permutation_model[0]))
    print(_generate_models(models[0], _permutation_model[1]))
    print(_generate_models(models[0], _permutation_model[2]))
    print(_generate_models(models[0], _permutation_model[3]))
    print(_generate_models(_permutation_model[0], _permutation_model[1]))
    print(_generate_models(_permutation_model[1], _permutation_model[2]))
    print(_generate_models(_permutation_model[2], _permutation_model[3]))
    print("Done !")
    