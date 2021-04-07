import numpy as np
import os
import random


# Onset dictionary for midi notes
onset_dict = {
    'A' : 33,
    'A#' : 34,
    'B' : 35,
    'C' : 36,
    'C#' : 37,
    'D' : 38,
    'D#' : 39,
    'E' : 40,
    'F' : 41,
    'F#' : 42,
    'G' : 43,
    'G#' : 44
    }
    
# Circle of fifths dictionary for random walk between keys
circle_of_fifths = {
        tuple(['A', 'major']) : [['D', 'major'],['E','major'], ['F#','minor']],
        tuple(['A#', 'major']) : [['D#', 'major'],['F#','major'], ['G','minor']],
        tuple(['B', 'major']) : [['F#', 'major'],['E','major'], ['G#','minor']],
        tuple(['C', 'major']) : [['F', 'major'],['G','major'], ['A','minor']],
        tuple(['C#', 'major']) : [['G#', 'major'],['F#','major'], ['D#','minor']],
        tuple(['D', 'major']) : [['G', 'major'],['A','major'], ['B','minor']],
        tuple(['D#', 'major']) : [['A#', 'major'],['G#','major'], ['C','minor']],
        tuple(['E', 'major']) : [['A', 'major'],['B','major'], ['C#','minor']],
        tuple(['F', 'major']) : [['C', 'major'],['A#','major'], ['D','minor']],
        tuple(['F#', 'major']) : [['C#', 'major'],['B','major'], ['D#','minor']],
        tuple(['G', 'major']) : [['C', 'major'],['D','major'], ['E','minor']],
        tuple(['G#', 'major']) : [['D#', 'major'],['C#','major'], ['F','minor']],
        tuple(['G#', 'major']) : [['D#', 'major'],['C#','major'], ['F','minor']],
        tuple(['A' , 'minor']) : [['D', 'minor'],['E','minor'], ['C','major']],
        tuple(['E' , 'minor']) : [['A', 'minor'],['B','minor'], ['G','major']],
        tuple(['B' , 'minor']) : [['E', 'minor'],['F#','minor'], ['D','major']],
        tuple(['F#' , 'minor']) : [['B', 'minor'],['C#','minor'], ['A','major']],
        tuple(['C#' , 'minor']) : [['F#', 'minor'],['G#','minor'], ['E','major']],
        tuple(['G#' , 'minor']) : [['C#', 'minor'],['D#','minor'], ['B','major']],
        tuple(['D#' , 'minor']) : [['G#', 'minor'],['C#','minor'], ['F#','major']],
        tuple(['A#' , 'minor']) : [['D#', 'minor'],['F','minor'], ['D#','major']],
        tuple(['F' , 'minor']) : [['A#', 'minor'],['C','minor'], ['G#','major']],
        tuple(['C' , 'minor']) : [['F', 'minor'],['G','minor'], ['D#','major']],
        tuple(['G' , 'minor']) : [['C', 'minor'],['D','minor'], ['A#','major']],
        tuple(['D' , 'minor']) : [['G', 'minor'],['A','minor'], ['F','major']]
}
    
# Steps to build major and minor keys
steps_major = [2, 4, 5, 7, 9, 11]
steps_minor = [2, 3, 5, 7, 8, 10]
    
    
def build_key(key):
    """
    Key building function

    :param key: Tuple containing note + mode
    :return list_notes: List of playable notes
    """
    root = key[0]
    scale = key[1]
    list_notes = []
    list_notes.append(root)
    list_onsets = list(onset_dict.keys())
    onset = list_onsets.index(root)
    if scale == 'major':
        for i in steps_major:
            note = list_onsets[(onset+i)%12]
            list_notes.append(note)
    elif scale == 'minor':
        for i in steps_minor:
            note = list_onsets[(onset+i)%12]
            list_notes.append(note)
    return list_notes
    
            
def build_chords(list_notes):
    """
    Chord building function

    :param list_notes: List of playable notes
    :return list_chords: List of playable chords
    """
    list_chords = []
    for i in range(len(list_notes)):
        nb = len(list_notes)
        list_chords.append([list_notes[i], list_notes[(i+2)%nb], list_notes[(i+4)%nb]])
    return list_chords
    
    
def build_chords(list_notes):
    """
    Chord building function

    :param list_notes: List of playable notes
    :return list_chords: List of playable chords
    """
    list_chords = []
    nb = len(list_notes)
    for i in range(len(list_notes)):
        # One note
        list_chords.append([list_notes[i]])
        # Perfect fifths
        list_chords.append([list_notes[i], list_notes[(i+4)%nb]])
        # Triads
        list_chords.append([list_notes[i], list_notes[(i+2)%nb], list_notes[(i+4)%nb]])
        # Seventh chords
        list_chords.append([list_notes[i], list_notes[(i+2)%nb], list_notes[(i+4)%nb], list_notes[(i+6)%nb]])
    return list_chords
    

def pitch_quantizer(pitch_class, onset_dict, inf, sup):
    """
    Chord building function

    :param pitch_class: Current key
    :param onset_dit: Dictionary of midi onsets
    :param inf: Lowest midi note
    :param sup: Highest midi note
    :return final_pitches: List of quantized pitches
    """
    final_pitches = []
    for key in pitch_class:
        note = onset_dict[key]
        final_pitches += [i for i in range(inf, sup) if (i-note) % 12 == 0]
    return final_pitches
    
    
def quantize(a, b):
    """
    Integers quantizing function

    :param a, b: Numbers
    """
    if a%b > a/2:
        return ((a//b)+1)*b
    else:
        return (a//b)*b


def random_chord(chords_list):
    """
    Random chord picking function

    :param chords_list: List of chords to choose from
    :return chords: Random chord from the list
    """
    return random.choice(chords_list)
    
    
def random_walk(current_key):
    """
    Random walk function

    :param current_key: Current key in the circle of fifths
    :return chords: Random neighbour within the circle
    """
    return random.choice(circle_of_fifths[current_key])
    

def select_sample_by_key(samples_dir, chords):
    """
    Sample selection by key

    :param samples_dir: Directory in which to search for samples
    :param chords: Chords allowed in the current key
    :return sample: Random choice from available samples
    """
    samples = []
    for file in os.listdir(samples_dir):
        if file.endswith('.wav'):
            if list(file.split('-')[-2]) in chords:
                samples.append(file)
    if len(samples)>0:
        return random.choice(samples)
    else:
        return None
        
        
def pdf(mean, std):
    """
    Gaussian distribution

    :param mean: Mean parameter of the law
    :param std: Std parameter of the law
    :return y_out: Normal distribution for x values (going from 0 to 100)
    """
    x = np.arange(100)
    y_out = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
    return y_out
        
        
def select_sample(samples_dir):
    """
    Sample selection (without key constraint)

    :param samples_dir: Directory in which to search for samples
    :return sample: Randomly chosen sample
    """
    samples = []
    for file in os.listdir(samples_dir):
        if file.endswith('.wav'):
            samples.append(file)
    return random.choice(samples)

        
        
def check_still_in_key(sample, chords):
    """
    Still in key check

    :param sample: Sample considered
    :param chords: playable chords from the key 
    :return boolean: If still in key or not
    """
    if sample:
        return list(sample.split('-')[-2]) in chords
    else:
        return False
