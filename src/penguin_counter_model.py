import torch
import torch.nn as nn
import torchvision.transforms as tvt
from scipy.io import loadmat
import numpy as np


class PenguinCounterNet(nn.Module):

    def __init__(self, model_path, average_image_path, device='cpu'):
        super(PenguinCounterNet, self).__init__()
        self.average_image = np.empty([])
        self.density_multiplier = 1e4
        self.segmentation_th = 0.95
        self.horizontal_edge_remove = 30
        self.device = device
        self.model_path = model_path
        self.average_image_path = average_image_path
        self.conv1_1 = nn.Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu1_1 = nn.ReLU()
        self.conv1_2 = nn.Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu1_2 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=(1, 1), dilation=1, ceil_mode=True)
        self.conv2_1 = nn.Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu2_1 = nn.ReLU()
        self.conv2_2 = nn.Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu2_2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=(1, 1), dilation=1, ceil_mode=True)
        self.conv3_1 = nn.Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu3_1 = nn.ReLU()
        self.conv3_2 = nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu3_2 = nn.ReLU()
        self.conv3_3 = nn.Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu3_3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=(1, 1), dilation=1, ceil_mode=True)
        self.conv4_1 = nn.Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu4_1 = nn.ReLU()
        self.conv4_2 = nn.Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu4_2 = nn.ReLU()
        self.conv4_3 = nn.Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu4_3 = nn.ReLU()
        self.pool4 = nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=(1, 1), dilation=1, ceil_mode=True)
        self.conv5_1 = nn.Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu5_1 = nn.ReLU()
        self.conv5_2 = nn.Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu5_2 = nn.ReLU()
        self.conv5_3 = nn.Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        self.relu5_3 = nn.ReLU()
        self.pool5 = nn.MaxPool2d(kernel_size=[2, 2], stride=[2, 2], padding=(1, 1), dilation=1, ceil_mode=True)
        self.fc6 = nn.Conv2d(512, 4096, kernel_size=(7, 7), stride=(1, 1), padding=(3, 3))
        self.relu6 = nn.ReLU()
        self.fc7 = nn.Conv2d(4096, 4096, kernel_size=(1, 1), stride=(1, 1))
        self.relu7 = nn.ReLU()
        self.fc8 = nn.Conv2d(4096, 1, kernel_size=(1, 1), stride=(1, 1))
        self.deconv2 = nn.ConvTranspose2d(1, 1, kernel_size=(4, 4), stride=(2, 2), bias=False)
        self.skip4 = nn.Conv2d(512, 1, kernel_size=(1, 1), stride=(1, 1))
        self.deconv2bis = nn.ConvTranspose2d(1, 1, kernel_size=(4, 4), stride=(2, 2), bias=False)
        self.skip3 = nn.Conv2d(256, 1, kernel_size=(1, 1), stride=(1, 1))
        self.deconv8 = nn.ConvTranspose2d(1, 1, kernel_size=(16, 16), stride=(8, 8), bias=False)
        self.fc8_l = nn.Conv2d(4096, 1, kernel_size=(1, 1), stride=(1, 1))
        self.deconv2_l = nn.ConvTranspose2d(1, 1, kernel_size=(4, 4), stride=(2, 2), bias=False)
        self.deconv2bis_l = nn.ConvTranspose2d(1, 1, kernel_size=(4, 4), stride=(2, 2), bias=False)
        self.deconv8_l = nn.ConvTranspose2d(1, 1, kernel_size=(16, 16), stride=(8, 8), bias=False)

    def forward(self, input):
        input = input[:, self.horizontal_edge_remove:-self.horizontal_edge_remove, :]
        x1 = self.conv1_1(input)
        x2 = self.relu1_1(x1)
        x3 = self.conv1_2(x2)
        x4 = self.relu1_2(x3)
        x5 = self.pool1(x4)
        x6 = self.conv2_1(x5)
        x7 = self.relu2_1(x6)
        x8 = self.conv2_2(x7)
        x9 = self.relu2_2(x8)
        x10 = self.pool2(x9)
        x11 = self.conv3_1(x10)
        x12 = self.relu3_1(x11)
        x13 = self.conv3_2(x12)
        x14 = self.relu3_2(x13)
        x15 = self.conv3_3(x14)
        x16 = self.relu3_3(x15)
        x17 = self.pool3(x16)
        x18 = self.conv4_1(x17)
        x19 = self.relu4_1(x18)
        x20 = self.conv4_2(x19)
        x21 = self.relu4_2(x20)
        x22 = self.conv4_3(x21)
        x23 = self.relu4_3(x22)
        x24 = self.pool4(x23)
        x25 = self.conv5_1(x24)
        x26 = self.relu5_1(x25)
        x27 = self.conv5_2(x26)
        x28 = self.relu5_2(x27)
        x29 = self.conv5_3(x28)
        x30 = self.relu5_3(x29)
        x31 = self.pool5(x30)
        x32 = self.fc6(x31)
        x33 = self.relu6(x32)
        x35 = self.fc7(x33)
        x36 = self.relu7(x35)
        x38 = self.fc8(x36)
        x39 = self.deconv2(x38)
        x40 = self.skip4(x24)
        x41 = torch.add(x40, tvt.functional.center_crop(x39, x40.size()[1:]))
        x42 = self.deconv2bis(x41)
        x43 = self.skip3(x17)
        x44 = torch.add(x43, tvt.functional.center_crop(x42, x43.size()[1:]))
        prediction_s = self.deconv8(x44)
        prediction_s = tvt.functional.center_crop(prediction_s, input.size()[1:])
        x38_l = self.fc8_l(x36)
        x39_l = self.deconv2_l(x38_l)
        x41_l = torch.add(x40, tvt.functional.center_crop(x39_l, x40.size()[1:]))
        x42_l = self.deconv2bis_l(x41_l)
        x44_l = torch.add(x43, tvt.functional.center_crop(x42_l, x43.size()[1:]))
        prediction_l = self.deconv8_l(x44_l)
        prediction_l = tvt.functional.center_crop(prediction_l, input.size()[1:])
        prediction_s = prediction_s > self.segmentation_th
        # set prediction_s to 0 on the top and bottom of the image an amount of self.horizontal_edge_remove pixels
        prediction_s = tvt.functional.pad(prediction_s, (0, self.horizontal_edge_remove))
        prediction_l = tvt.functional.pad(prediction_l, (0, self.horizontal_edge_remove))
        # set density 0 outside the segmentation, and rescale density map
        prediction_l = prediction_l * prediction_s / self.density_multiplier
        return prediction_s, prediction_l

def penguinCounterNet(model_path, average_image_path, device='cpu'):
    """
    load imported model instance

    Args:
        model_path (str): path to model weights
        avg_image_path (str): path to average image used for normalization
    """
    model = PenguinCounterNet(model_path, average_image_path, device)
    state_dict = torch.load(model_path)
    model.load_state_dict(state_dict)
    average_image = loadmat(average_image_path)
    model = model.to(device)
    model.average_image = np.array(average_image['average_image'], dtype=np.float32).transpose(2, 0, 1)

    return model
