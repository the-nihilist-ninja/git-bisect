from functools import partial

import torch
from torch import nn

from models.utils import hook_func


class MLP(nn.Module):
  '''
    Multilayer Perceptron.
  '''
  def __init__(self) -> None:
    super().__init__()
    self.layer_1 = nn.Linear(32 * 32 * 3, 512)
    self.relu_layer_1 = nn.ReLU()
    self.layer_2 = nn.Linear(512, 512)
    self.relu_layer_2 = nn.ReLU()
    self.layer_3 = nn.Linear(512, 512)
    self.relu_layer_3 = nn.ReLU()
    self.layer_4 = nn.Linear(512,10)


  def forward(self, x):
    """
    _summary_

    :param x: Input variable
    :type x: torch.Tensor
    
    :return: predicted output
    :rtype: torch.Tensor
    """
    y = torch.flatten(x, 1)
    y = self.layer_1(y)
    y = self.relu_layer_1(y)
    y = self.layer_2(y)
    y = self.relu_layer_2(y)
    y = self.layer_3(y)
    y = self.relu_layer_3(y)
    y = self.layer_4(y)
            
    return y


def register_hook(mlp_inst:MLP, activations_dict:dict) -> None:
  """
  Function to register hook

  :param mlp_inst: _description_
  :type mlp_inst: MLP
  :param activations_dict: _description_
  :type activations_dict: dict
  """
  for name, layer in mlp_inst.named_modules():
    if name.startswith('layer'):
      layer.register_forward_hook(hook=partial(hook_func, activations_dict, name))
      