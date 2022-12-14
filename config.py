from pathlib import Path

import numpy
import torch

TIME_FLAG = False
WEIGHT = "weight"
BIAS = "bias"
FEATURES = "features"
CLASSIFIER = "classifier"
NAIVE_MATCH = "NaiveMatching"
ACT_MATCH = "ActivationMatching"
WEIGHT_MATCH = "WeightMatching"
STE_MATCH = "STEstimator"

TRAIN = "Train"
TEST = "Test"

MLP_RESULTS_PATH = Path("Mlp_results.pkl")
VGG_RESULTS_PATH = Path("Vgg_results.pkl")

_STASH_PATH = Path("stash")
_STASH_PATH.mkdir(exist_ok=True, parents=True)

MLP_MODEL1_PATH = _STASH_PATH.joinpath("mlp1_512_40.pth")
MLP_MODEL2_PATH = _STASH_PATH.joinpath("mlp2_512_40.pth")
VGG_MODEL1_PATH = _STASH_PATH.joinpath("vgg16_bn_100_100.pth")
VGG_MODEL2_PATH = _STASH_PATH.joinpath("vgg16_bn1_100_100.pth")

MLP_PERM_PATH = _STASH_PATH.joinpath("mlp_perm")
MLP_PERM_PATH.mkdir(exist_ok=True, parents=True)

VGG_PERM_PATH = _STASH_PATH.joinpath("vgg_perm")
VGG_PERM_PATH.mkdir(exist_ok=True, parents=True)

CUDA_AVAILABLE = torch.cuda.is_available()
DEVICE = torch.device("cuda" if CUDA_AVAILABLE else "cpu")

LAMBDA_ARRAY = numpy.linspace(start=0, stop=1, num=21, dtype=numpy.float32)
