# pengbot-counter
Tool to count penguins in images as presented using the work in  [Arteta, Carlos, Victor Lempitsky, and Andrew Zisserman. "Counting in the wild" ECCV 2016](https://www.robots.ox.ac.uk/~vgg/publications/2016/Arteta16/arteta16.pdf) 

## Installation 
Clone the git repository
```
git clone https://github.com/CarlosArteta/pengbot-counter.git
```

Download the model and normalization image from the following URLs:
```
# Model:
https://drive.google.com/file/d/1Qi-EuqGNiQ9WKpXXFpET6wGLCM9bZagX/view?usp=sharing
# Average image for input normalization:
https://drive.google.com/file/d/1n74wK0yq8p7_GBTMM1KvnKUFuUsUzf5G/view?usp=sharing
```

Create a Python virtual enviroment
```
cd pengbot-counter
python3 -m venv venv_pengbot_counter
```

Acitvate the virtual enviroment 
```
# In Linux:
source venv_pengbot_counter/source/bin/activate

# In Windows:
./venv_pengbot_counter/Scripts/activate
```

Install the package
```
python -m pip install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu118
python -m pip install .
```

(Optional) Run tests
```
python -m pip install pytest
pytest 
```

## Usage
Acitvate the virtual enviroment 
```
# In Linux:
source venv_pengbot_counter/source/bin/activate

# In Windows:
./venv_pengbot_counter/Scripts/activate
```

Edit a configuration file; for example, the one in `pengbot-counter/example/config_AITCb2014a.yaml`

Call the tool with the edited config file:
```
cd pengbot-counter
python bin/count.py --config "example/config_AITCb2014a.yaml"
```