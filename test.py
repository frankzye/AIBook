import torch
import torch.nn as nn

line = nn.Linear(2, 4)

x = torch.rand(5, 2)

o = line(x)

print(x)
print(o)
