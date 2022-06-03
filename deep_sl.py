
import torch.nn as nn
import torch.nn.functional as F


class Model_1(nn.Module):
    def __init__(self):
        super().__init__()
        self.softmax = nn.Softmax(dim=0)
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 46)
    
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.softmax(self.layer3(x))



class Model_2(nn.Module):
    def __init__(self):
        super().__init__()
        self.softmax = nn.Softmax(dim=0)
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 128)
        self.layer3 = nn.Linear(128, 128)
        self.layer4 = nn.Linear(128, 64)
        self.layer5 = nn.Linear(64, 32)
        self.layer6 = nn.Linear(32, 46)
    
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = F.relu(self.layer4(x))
        x = F.relu(self.layer5(x))
        return self.softmax(self.layer6(x))