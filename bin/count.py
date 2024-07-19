#!/usr/bin/env python3

import os
import argparse
import yaml
import warnings
from src import processor


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Pengbot counter'
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='YAML file with the required paths'
    )

    config_arg = parser.parse_args()

    with open(config_arg.config, 'r') as config_fp:
        config = yaml.safe_load(config_fp)

    # validate arguments
    if not os.path.exists(config['model_path']):
        raise FileNotFoundError(f"Model file not found: {config['model_path']}")

    if not os.path.exists(config['average_image_path']):
        raise FileNotFoundError(f"Average image file not found: {config['average_image_path']}")
    
    if not os.path.exists(config['input_data_path']):
        raise FileNotFoundError(f"Input dicrectory not found: {config['input_data_path']}")
    
    if config['device'] not in ['cpu', 'cuda']:
        raise ValueError(f"Device must be either 'cpu' or 'cuda'")
    
    return config

def main():
    config = parse_cli_args()
    proc = processor.FolderProcessor(
        model_path=config['model_path'], 
        average_image_path=config['average_image_path'], 
        device=config['device']
    )
    proc.process_folder(
        folder_path=config['input_data_path'], 
        image_extension=config['image_extension'], 
        output_folder_suffix=config['output_folder_suffix']
    )
