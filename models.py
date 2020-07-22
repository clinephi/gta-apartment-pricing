# ANN ARCHITECTURE:
import torch.nn as nn
import torch.nn.functional as F

class ANN(nn.Module):
    def __init__(self):
        super(ANN, self).__init__()
        self.name = "test_ann"
        self.layer1 = nn.Linear(17, 10)
        self.layer2 = nn.Linear(10, 1)

    def forward(self, x):
        x = self.layer1( x )
        x = F.relu( x )
        x  = self.layer2( x )
        return x



