import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)



lstm = nn.LSTM(3, 3)

a = 10