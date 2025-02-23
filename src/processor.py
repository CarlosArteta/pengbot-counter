import os
from pathlib import Path
import torch
import torchvision as tv
import scipy.io
import scipy.ndimage 
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from . import penguin_counter_model as pcm


class FolderProcessor:
    """
    A class to process a folder of images and count the number of penguins in each image.
    """
    def __init__(self, model_path, average_image_path, device):
        self.model = pcm.penguinCounterNet(model_path, average_image_path, device)
        self.model.eval()
        self.images = []
    
    def process_folder(self, folder_path, image_extension='jpg', output_folder_suffix='_count'):
        """
        Process a folder of images and count the number of penguins in each image.
        
        Parameters:
        folder_path (str): The path to the folder containing the images to process.
        """
        folder_path = Path(folder_path)
        if not folder_path.is_dir():
            raise NotADirectoryError(f"Input path is not a directory: {folder_path}")
        
        self.images = list(folder_path.glob(f'*.{image_extension}'))
        if len(self.images) == 0:
            raise FileNotFoundError(f"No images found in input folder: {folder_path}")
        
        output_folder_path = Path(folder_path.__str__() + '_count')
        output_folder_path.mkdir(exist_ok=True)
        output_csv_path = output_folder_path / f'count-{datetime.today().strftime("%Y-%m-%d")}.csv'
        output_df = pd.DataFrame(columns=['image_name', 'count'])
        
        # Print summary of processing task
        print('\n === Folder Processor === \n')
        print(f"Processing {len(self.images)} images in folder: {folder_path}")
        print(f"Output folder: {output_folder_path}")
        print(f"Model path: {self.model.model_path}") 
        print(f"Average image path: {self.model.average_image_path}")
        print('\n ======================== \n')

        for image_path in tqdm(self.images):
            output_density_path = output_folder_path / f'{image_path.stem}.mat'
            if output_density_path.is_file():
                tqdm.write(f"Skipping image {image_path.name}: output file already exists")
                continue
            pred_density = self.process_image(image_path)
            count = pred_density.sum()
            output_df = pd.concat(
                [output_df if not output_df.empty else None, pd.DataFrame({'image': image_path.name, 'count': count}, index=[0])], 
                ).reset_index(drop=True)
            scipy.io.savemat(output_density_path, {'density': pred_density.squeeze()}, do_compression=True)
            output_df.to_csv(output_csv_path, index=False)
    
    def process_image(self, image_path):
        """
        Process a single image and count the number of penguins in the image.
        
        Parameters:
        image_path (str): The path to the image to process.
        """
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError(f"Input image file not found: {image_path}")
        
        im = tv.io.read_image(image_path).type(torch.float32)
        avg_im = scipy.ndimage.zoom(self.model.average_image, np.array(im.size()) / self.model.average_image.shape)
        im = im - torch.tensor(avg_im)
        im = im.to(self.model.device)
        with torch.inference_mode():
            _, pred_density = self.model(im)

        return pred_density.detach().cpu().numpy()
