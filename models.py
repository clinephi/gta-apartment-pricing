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

# REFERENCE
# conv2d( in_channels, out_ch, k, stride, pad )
# maxpool2d( k, stride )
# ConvTranspose2d( in, out, k, pad, out_pad )

class Autoencoder( nn.Module ):
    def __init__(self):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 30, 11, stride=4),
            nn.ReLU(),
            # nn.MaxPool2d( 3,2 ), # Max pool layer.
            nn.Conv2d(30, 60, 5, padding=2),
            nn.ReLU(),
            # nn.MaxPool2d(3, 2),  # Max pool layer.
            nn.Conv2d(60, 90, 3, padding=1),
            nn.ReLU(),
            # nn.Conv2d(15, 1, 3, padding=1),
            # nn.ReLU(),
            # nn.MaxPool2d( 3,2 )
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(90, 60, 3, padding=1 ),
            nn.ReLU(),
            nn.ConvTranspose2d(60,30,5, padding=2 ),
            nn.ReLU(),
            nn.ConvTranspose2d(30, 3, 11, stride=4),
            nn.Sigmoid()
        )
    def forward(self, x):
        x = self.encode(x)
        x = self.decode(x)
        return x



