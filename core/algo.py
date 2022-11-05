import numpy
from procrustes import permutation

from helper import timer_func


class Permuter:
    """"
    Parent class for all the methods
    """
    perm = None
    def __init__(self, archi:list[int], model_width):
        self.loss = None
        self.archi = archi
        self.model_width = model_width


class ActivationMethod(Permuter):
    def __init__(self, archi, model_width) -> None:
        super().__init__(archi, model_width)

    def _layer_wise(self, act_a, act_b)->numpy.ndarray:
        """
        Model B is considered to be permuted

        :param act_a: Activation of Model a layer in the model
        :type act_a: numpy.ndarray

        :param act_b: Activation of Model b layer in the model
        :type act_b: torch.Tensor

        :return: permutation matrix for the corresponding layer
        :rtype: numpy.ndarray
        """
        # Note that the procrustes algorithm works with the form
        
        res = permutation(act_b.T, act_a).T
        self.loss = res.get('error')
        return res.get('t').T
    
    @timer_func("Activation method")
    def get_permuation(self, model_a_act, model_b_act):
        """
        Get's layer wise permutation matrix
        
        :param model_a_act: Activations of all layers of model A
        :type model_a_act: numpy.ndarray
        
        :param model_b_act: Activations of all layers of model B
        :type model_b_act: numpy.ndarray
        
        :return: List of permutation matrix
        :rtype: list[numpy.ndarray]
        """
        if not (isinstance(model_a_act, numpy.ndarray) and isinstance(model_b_act, numpy.ndarray)):
            raise TypeError("Activations must be numpy array")
        
        if model_a_act.shape == model_b_act.shape:
            raise Exception(f"Model architecture don't match: model_a has {len(model_a_act)} layers and model_b has {len(model_b_act)}")
        
        
        self.perm = [
            self._layer_wise(act_a=act_a, act_b= act_b)
            for act_a, act_b in zip(model_a_act, model_b_act)
            ]
        
        return self.perm

    def get_loss(self):
        """
        Gets loss value of the operation

        :return: Loss 
        :rtype: float
        """
        return self.loss

class GreedyAlgorithm(Permuter):
    def __init__(self, archi: list[int], model_width) -> None:
        """
        _summary_

        :param archi: _description_
        :type archi: list[int]
        :param model_width: _description_
        :type model_width: _type_
        """
        super().__init__(archi, model_width)
    
    def get_permutation(self, model_a, model_b):
        """
        Generate permutation for the weights of model B

        :param model_a: Model A
        :type model_a: torch.nn
        
        :param model_b: Model B
        :type model_b: torch.nn
        
        :return: List of permutation of each layer
        :rtype: 
        """
    
        
        return numpy.zeros((2,2))