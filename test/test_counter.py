import pytest
from pathlib import Path
import numpy as np
from src.penguin_counter_model import penguinCounterNet
import torch
import torchvision as tv
import scipy.io

TEST_IM_PATH = (Path(__file__).parent.parent / "test/testdata/AITCb2015a_0001.JPG").absolute()
TEST_DENSITY_PATH = (Path(__file__).parent.parent / "test/testdata/AITCb2015a_0001.mat").absolute()
MODEL_PATH = (Path(__file__).parent.parent / "static/penguinCounterNetReduced.pth").absolute() 
AVG_IM_PATH = (Path(__file__).parent.parent / "static/penguinCounterAvgIm.mat").absolute() 

def test_penguinCounterNet():
    im = tv.io.read_image(TEST_IM_PATH)
    density = scipy.io.loadmat(TEST_DENSITY_PATH)['density']
    model = penguinCounterNet(MODEL_PATH, AVG_IM_PATH)
    model.eval()
    with torch.no_grad():
        pred_mask, pred_density = model(im)
    # assert that the predicted density map is close to the reference desntiy map
    assert np.allclose(pred_density.numpy(), density, atol=1e-2)
    

    
