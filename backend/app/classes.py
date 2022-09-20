from torch import nn,flatten
import torch
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(1,6,25,padding="same"),
                                nn.ReLU(),
                                nn.MaxPool2d(2,2))
        self.conv2 = nn.Sequential(nn.Conv2d(6,9,15,padding="same"),
                                nn.ReLU(),
                                nn.MaxPool2d(2,2))
        self.conv3 = nn.Sequential(nn.Conv2d(9,12,5,padding="same"),
                                nn.ReLU(),
                                nn.MaxPool2d(2,2))
        self.fc = nn.Sequential(nn.Linear(108,100),
                                nn.ReLU(),
                                nn.Linear(100,80),
                                nn.ReLU(),
                                nn.Linear(80,10))

    def forward(self, x):
        x = x.reshape(-1,1,28,28)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = flatten(x,1)
        x= self.fc(x)
        return x

def load_model():
    mod = Model()
    checkpoint = torch.load("model2.ckpt")
    modw = checkpoint["state_dict"]
    for k in list(modw):
        modw[k.replace("model.","")] = modw.pop(k)
    print("loaded correctly")
    mod.load_state_dict(checkpoint["state_dict"])
    print("evaluating")
    mod.eval()
    return mod
