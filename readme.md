# Computational Music Creativity Final Project 


## Content

1. Main.py: Main program. 

2. image_processing.py: Image processing program extracting features from a given image. 

3. sound_module.py: Sound module program. 

4. utils.py: Util functions used. 

5. Samples: Samples directory containing the samples used. To add new samples, the name should respect the following format : xxxx-Key-xxxx.wav. For example, you can add a male voice singing a C with the following name: male-C-voice.wav

6. Images: Images folder, no specific name format is required. 


## Use

1. Install the python requirements : 
```ShellSesion
    pip install -r requirements.txt
```

2. Make sure the samples and images directories are available.

3. Run main.py with the required arguments:
```ShellSesion
    python3 main.py --help
    Usage: main.py [OPTIONS] [IMAGE_PATH]

    Options:
      --samples-dir-1 TEXT
      --samples-dir-2 TEXT
      --samples-dir-3 TEXT
      --samples-dir-4 TEXT
      --mask-size INTEGER
      --nb-grn INTEGER
      --nb-clouds INTEGER
      --MIDDLE INTEGER
      --STD INTEGER
      --shuffle BOOLEAN
      --record BOOLEAN
      --normalize BOOLEAN
      --verbose INTEGER
      --help
```
