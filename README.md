# pengbot-counter
Tool to count penguins in images as presented using the work in  [Arteta, Carlos, Victor Lempitsky, and Andrew Zisserman. "Counting in the wild" ECCV 2016](https://www.robots.ox.ac.uk/~vgg/publications/2016/Arteta16/arteta16.pdf) 

## Installation
Clone the git repository
```
git clone https://github.com/CarlosArteta/pengbot-counter.git
```
 
Create a Python virtual enviroment
```
cd pengbot-counter
python3 -m venv venv_pengbot_counter
```

Install the package
```
source venv_pengbot_counter/source/bin/activate
pip install torch==2.3.1 torchvision==0.18.1 --index-url https://download.pytorch.org/whl/cu118
pip install .
```

Download model
```
wget https://drive.google.com/file/d/1Qi-EuqGNiQ9WKpXXFpET6wGLCM9bZagX/view?usp=sharing
wget https://drive.google.com/file/d/1Qi-EuqGNiQ9WKpXXFpET6wGLCM9bZagX/view?usp=sharing
```

(Optional) Run tests
```
pip install pytest
pytest 
```

## Usage
Activate the python virtual environment 
```
source venv_pengbot_counter/source/bin/activate
```

Edit a configuration file; for example: `pengbot-counter/example/config_AITCb2014a.yaml`

Call the tool with the edited config file:
```
pengbot-counter --config example/config_AITCb2014a.yaml
```