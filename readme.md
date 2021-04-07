# Computational Music Creativity Final Project 

## Introduction
"Hear What You Do Not See" is a project carried out within the scope of the Computational Music Creativity class at Pompeu Fabra University in 2021. The theoretical inspiration of this project lies at the intersection of cognitive related notions, and a reflection on the idea of eventalism: synesthesia, information processing and randomness. The system extracts entropy measures from an image provided by the user. It then builds a sound module composed of several synthesizers (including granulars). Each instrument's parameters and melodic behaviour are dynamically responding to the information extracted from the image.


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
      --samples-dir-1 TEXT          First samples directory
      --samples-dir-2 TEXT          Second samples directory
      --samples-dir-3 TEXT          Third samples directory
      --samples-dir-4 TEXT          Fourth samples directory
      --mask-size INTEGER           Size of the mask for entropy extraction
      --nb-grn INTEGER              Number of granular synths
      --nb-clouds INTEGER           Number of cloud synths
      --MIDDLE INTEGER              Middle midi note played by pitched intstruments
      --STD INTEGER                 Standard dev. midi note played by pitched intstruments
      --shuffle BOOLEAN             Shuffle the entropy values (if not, the mask moves from top left to bottom right of the image)
      --record BOOLEAN              Record the performance
      --normalize BOOLEAN           Normalize extracted entropy values
      --verbose INTEGER             Print instruments playing at each time-step
      --help
```
