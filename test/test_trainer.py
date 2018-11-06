import unittest
import torch
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import torchvision
from torch.optim import Adam
import torch.utils.data as data
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torchgan.metrics import *
from torchgan import *
from torchgan.models import *
from torchgan.losses import *
from torchgan.trainer import Trainer

def mnist_dataloader():
    train_dataset = dsets.MNIST(root='./mnist', train=True,
                                transform=transforms.Compose([transforms.Pad((2, 2)),
                                                              transforms.ToTensor(),
                                                              transforms.Normalize(mean=(0.5, 0.5, 0.5),
                                                                  std=(0.5, 0.5, 0.5))]), download=True)
    train_loader = data.DataLoader(train_dataset, batch_size=128, shuffle=True)
    return train_loader

class TestMetrics(unittest.TestCase):
    def test_trainer_dcgan(self):
        network_params = {
            "generator": {"name": DCGANGenerator, "args": {"out_channels": 1, "step_channels": 4}},
            "discriminator": {"name": DCGANDiscriminator, "args": {"in_channels": 1, "step_channels": 4}}
        }
        optim_params = {
            "optimizer_generator": {"name": Adam, "args": {"lr": 0.0002, "betas": (0.5, 0.999)}},
            "optimizer_discriminator": {"name": Adam, "args": {"lr": 0.0002, "betas": (0.5, 0.999)}},
        }
        losses_list = [MinimaxGeneratorLoss(), MinimaxDiscriminatorLoss()]
        trainer = Trainer(network_params, optim_params, losses_list,
                batch_size=128, sample_size=1, epochs=1, device=torch.device('cpu'))
        trainer(mnist_dataloader())

    def test_trainer_cgan(self):
        network_params = {
            "generator": {"name": ConditionalGANGenerator, "args": {"num_classes": 1,
                    "out_channels": 1, "step_channels": 4}},
            "discriminator": {"name": ConditionalGANDiscriminator, "args": {"num_classes": 1,
                    "in_channels": 1, "step_channels": 4}}
        }
        optim_params = {
            "optimizer_generator": {"name": Adam, "args": {"lr": 0.0002, "betas": (0.5, 0.999)}},
            "optimizer_discriminator": {"name": Adam, "args": {"lr": 0.0002, "betas": (0.5, 0.999)}},
        }
        losses_list = [MinimaxGeneratorLoss(), MinimaxDiscriminatorLoss()]
        trainer = Trainer(network_params, optim_params, losses_list,
                batch_size=128, sample_size=1, epochs=1, device=torch.device('cpu'))
        trainer(mnist_dataloader())
