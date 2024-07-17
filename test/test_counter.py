import pytest
from pathlib import Path
import numpy as np
from src.penguin_counter_model import penguinCounterNet
import torch
import torchvision as tv
import scipy.io
import scipy.ndimage 

TEST_IM_PATH = (Path(__file__).parent.parent / "test/testdata/AITCb2015a_0001.JPG").absolute()
TEST_DENSITY_PATH = (Path(__file__).parent.parent / "test/testdata/AITCb2015a_0001.mat").absolute()
MODEL_PATH = (Path(__file__).parent.parent / "static/penguinCounterNetReduced.pth").absolute() 
AVG_IM_PATH = (Path(__file__).parent.parent / "static/penguinCounterAvgIm.mat").absolute() 

def test_density_sum():
    im = tv.io.read_image(TEST_IM_PATH).type(torch.float32)
    density = scipy.io.loadmat(TEST_DENSITY_PATH)['density']
    model = penguinCounterNet(MODEL_PATH, AVG_IM_PATH)
    model.eval()
    avg_im = scipy.ndimage.zoom(model.avg_image, np.array(im.size()) / model.avg_image.shape)
    im = im - torch.tensor(avg_im)
    with torch.inference_mode():
        pred_mask, pred_density = model(im) 
    assert torch.allclose(pred_density.sum(), torch.tensor(density.sum()), atol=1e-2)
    

    
