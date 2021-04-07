from pyo import *
from utils import *
import os
import random
import time
from collections import deque

class Sound_Module:
    
    def __init__(self, list_instruments, samples_dir_melody, samples_dir_voices,samples_dir_aggressive,samples_dir_beat, list_blocks, MIDDLE, STD, record=False, normalized=False):
        """
        Sound module initialization function

        :param samples_dir_melody: Directory containing melodic sound samples
        :param samples_dir_voices: Directory containing vocal sound samples
        :param samples_dir_aggressive: Directory containing aggressive sound samples
        :param samples_dir_beat: Directory containing rhythmic sound samples
        :param list_blocks: List of entropy values
        :param MIDDLE: Center of the midi notes played
        :param STD: Deviation of the midi notes played
        :param record: Boolean to activate recording or not
        :param normalized: Boolean to normalize the entropy values or not
        :return: an initialized sound module
        """
        self.MIDDLE = MIDDLE
        self.STD = STD
        self.s = Server().boot()
        self.home = os.path.expanduser('~')
        self.samples_dir_melody  = samples_dir_melody
        self.list_instruments = list_instruments
        self.samples_dir_voices = samples_dir_voices
        self.samples_dir_aggressive = samples_dir_aggressive
        self.samples_dir_beat = samples_dir_beat
        self.current_key = random.choice(list(circle_of_fifths.keys()))
        self.chords = build_chords(build_key(self.current_key))
        self.list_blocks = list_blocks
        self.TOTAL = len(list_blocks)
        self.path_record = os.path.join(os.path.expanduser("~"), "Desktop", "test.wav")
        self.record = record
        print('Instruments initialization ...')
        self.init_instruments()
        self.nb_instruments = len(list(self.instruments.keys()))
        self.init_thresholds(normalized)
        print('Conductor initialization ...')
        self.init_conductor()
        print('Melodic conductor initialization ...')
        self.init_melodic_conductor()
        print('Granular conductor initialization ...')
        self.init_grn_conductor()
        self.TIME_REACT = 0.1
        print('System ready ...')
        
        

    def start(self):
        """
        Sound module start function

        :param:
        :return:
        """
        # Starts the server
        self.s.start()
        # Activates the recording or not
        self.s.recordOptions(filename=self.path_record, fileformat=0, sampletype=1)
        if self.record:
            self.s.recstart()
        # Starts all the instruments
        self.start_all()
        
                        
    def stop(self):
        """
        Sound module stop function

        :param:
        :return:
        """
        # Stops the server
        self.s.stop()
        

    def init_particule(self):
        """
        Granular synth initialization function

        :param:
        :return: Dictionary containing 1) the out module (reverb); 2) the instrument; 3) list of previously selected samples;
                                       4) the table to read; 5) inner counter
        """
        dir = random.choice([self.samples_dir_melody, self.samples_dir_voices])
        sample = select_sample_by_key(dir, self.chords)
        sample_old = deque(maxlen=5)
        sample_old.append(sample)
        snd = SndTable()
        path = os.path.join(dir, sample)
        snd.setSound(path)
        end = snd.getSize() - self.s.getSamplingRate() * 0.25
        env = WinTable(7)
        pit = Noise(0, add=1)
        pososc = Sine(0.05).range(0, end)
        posrnd = Noise(mul=0.01, add=1)
        pos = pososc * posrnd
        pan = Noise(mul=0.5, add=0.5)
        cf = Sine(freq=0.07).range(75, 125)
        fcf = Choice(list(range(1, 40)), freq=150, mul=cf)
        grn = Particle2(
            table=snd,  # The table to read.
            env=env,  # The grain envelope.
            dens=50,  # The density of grains per second.
            pitch=pit,  # The pitch of the grain.
            pos=pos,  # The position of the grain in the table.
            dur=0.2,  # The duration of the grain in seconds.
            dev=0.005,  # The maximum deviation of the start time,
            pan=pan,  # The pan value of the grain.
            filterfreq=fcf,  # The filter frequency of the grain.
            filterq=20,  # The filter Q of the grain.
            filtertype=2,  # The filter type of the grain.
            chnls=2,  # The output number of streams of the granulator.
        )
        comp = Compress(grn, thresh=-20, ratio=4, risetime=0.005, falltime=0.10, knee=0.5, mul=0.8)
        b = Freeverb(comp, size=[0.9,0.9], damp=0.5, bal=0.4)
        return {'out':b, 'instrument':grn, 'list_samples':sample_old, 'snd':snd, 'count':0}
        
        
    def init_thresholds(self, normalized):
        """
        Entropy thresholds initialization function

        :param normalized: Boolean indicating whether the entropy is normalized or not
        :return:
        """
        if normalized:
            # Defines the step size, according to the number of instruments
            step_size = 100//self.nb_instruments
            # Defines the steps according to the corresponding percentiles
            step = np.percentile(self.list_blocks, step_size)
            self.thresholds = []
            for i in range(self.nb_instruments):
                self.thresholds.append(np.percentile(self.list_blocks, i*step_size))
            return
        else:
            step_size = int(100//self.nb_instruments)
            self.thresholds = []
            for i in range(self.nb_instruments):
                self.thresholds.append(i*step_size*0.01)
            return
        
        
    def get_instruments_playing(self, i):
        """
        Function returning current instruments playing

        :param i: index of the current entropy value (time-step)
        :return:
        """
        for instrument in list(self.conductor.keys()):
            if self.conductor[instrument][i] > 0:
                print(instrument, 'currently playing')
        return
    
        
    def init_particule2(self):
        """
        Granular synth initialization function n°2

        :param:
        :return: Dictionary containing 1) the out module (reverb); 2) the instrument; 3) list of previously selected samples;
                                       4) the table to read; 5) inner counter
        """
        snd_2 = SndTable()
        dir = random.choice([self.samples_dir_melody, self.samples_dir_voices])
        sound = select_sample_by_key(dir, self.chords)
        path_3 = os.path.join(dir, sound)
        sample_old = deque(maxlen=5)
        sample_old.append(sound)
        snd_2.setSound(path_3)
        end_2 = snd_2.getSize() - self.s.getSamplingRate() * 0.4
        env_2 = HarmTable()
        pos_2 = Phasor(snd_2.getRate()*.25, 0, snd_2.getSize())
        dns_2 = Randi(min=0, max=30, freq=0.01)
        pit_2 = Randi(min=0.99, max=1.01, freq=0.01)
        grn_2 = Granule(snd_2, env_2, dens=dns_2, pitch=pit_2, pos=pos_2, dur=1)
        comp = Compress(grn_2, thresh=-20, ratio=4, risetime=0.005, falltime=0.10, knee=0.5, mul=0.08)
        b_2 = Freeverb(comp, size=[0.5,0.5], damp=0.5, bal=0.1)
        return {'out':b_2, 'instrument':grn_2, 'list_samples':sample_old, 'snd':snd_2, 'count':0}
        
        
    def init_cloud(self):
        """
        Cloud synth initialization function

        :param:
        :return: Dictionary containing 1) the out module (reverb); 2) the instrument
        """
        pitches = pitch_quantizer(self.chords[0], onset_dict, 40, 80)
        mid = Choice(choice=pitches, freq=[10000, 10000])
        jit = Randi(min=0.993, max=1.007, freq=[10000, 10000])
        fr = MToF(mid, mul=jit)
        fd = Randi(min=0, max=0.01, freq=[10000, 10000])
        a = SineLoop(freq=fr, feedback=fd, mul=0)
        #d = Delay(a.mix(0), delay=[10,10], feedback=0.1)
        chor = Chorus(a, depth=[1,1], feedback=0.1, bal=0.1)
        #d = Disto(d, drive=.1, slope=.8)
        c_1 = Freeverb(chor, size=[0.5, 0.5], damp=0.5, bal=0.9)
        #c_2 = Freeverb(c_1, size=[0.5, 0.5], damp=0.7, bal=0.9)
        eq = Biquad(c_1, freq=fr+100, q=1, type=1)
        c = Freeverb(eq, size=[0.9, 0.9], damp=0.7, bal=0.4)
        #c = Freeverb(c_2, size=[0.9, 0.9], damp=0.7, bal=0.4)
        return {'out':c, 'instrument':a}
        
        
    def init_second_cloud(self):
        """
        Cloud synth initialization function n°2

        :param:
        :return: Dictionary containing 1) the out module (compressor); 2) the instrument
        """
        pitches_2mid = pitch_quantizer(self.chords[0], onset_dict, 40, 80)
        mid_2mid = Choice(choice=pitches_2mid, freq=[10, 10])
        jit_2mid = Randi(min=0.993, max=1.007, freq=[4, 4])
        fr_2mid = MToF(mid_2mid, mul=jit_2mid)
        fd_2mid = Randi(min=0, max=0.01, freq=[4, 4])
        sp_2mid = RandInt(max=20, freq=10000, add=0)
        amp_2mid = Sine(sp_2mid, mul=0.01, add=0)
        a_2mid = SineLoop(freq=fr_2mid, feedback=fd_2mid)
        d_2mid = Delay(a_2mid.mix(random.choice([0,1,2])), delay=[10,10], feedback=0.1)
        chor_2mid = Chorus(d_2mid, depth=[1,1], feedback=0.1, bal=0.1)
        c_1_2mid = Freeverb(a_2mid+d_2mid, size=[0.4, 0.4], damp=0.1, bal=0.3)
        #d = Disto(chor, drive=.5, slope=.8, mul=1)
        c_2mid = Freeverb(c_1_2mid, size=[0.9, 0.9], damp=0.2, bal=0.3)
        comp = Compress(c_2mid, thresh=-20, ratio=4, risetime=0.005, falltime=0.10, knee=0.5, mul=0.01)
        return {'out':comp, 'instrument':a_2mid}


    def init_bass(self):
        """
        Bass synth initialization function

        :param:
        :return: Dictionary containing 1) the out module (reverb); 2) the instrument
        """
        syn = SineLoop(freq=110, feedback=.07, mul=0.1)
        disto_bass = Disto(syn, drive=0.001, slope=.5)
        c_low = Freeverb(disto_bass, size=[0.5, 0.5], damp=0.7, bal=0.1)
        return {'out':c_low, 'instrument':syn}


    def init_instruments(self):
        """
        Instruments initialization function

        :param:
        :return:
        """
        # Creates the dictionary of instruments
        self.instruments = {}
        
        # Creates the required number of granulars
        for i in range(self.list_instruments[0]):
            if random.random()>0.5:
                self.instruments['grn_{}'.format(i)] = self.init_particule()
            else:
                self.instruments['grn_{}'.format(i)] = self.init_particule2()
        # Always creates a bass
        self.instruments['bass'] = self.init_bass()
        
        # Creates the required number of clouds
        for i in range(self.list_instruments[1]):
            if random.random()>0.4:
                self.instruments['cloud_{}'.format(i)] = self.init_cloud()
            else:
                self.instruments['cloud_second_{}'.format(i)] = self.init_second_cloud()
        return
        
        
    def start_all(self):
        """
        Instruments starting function

        :param:
        :return:
        """
        for keys, instrument in self.instruments.items():
            if keys == 'bass':
                self.restart([keys], 0.1, self.TIME_REACT)
            else:
                self.restart([keys], 0.3, self.TIME_REACT)
        return
        
        
    def shut(self, instruments, duration):
        """
        Instrument stopping function

        :param instruments: List of instrument names to stop
        :param duration: Time taken to shut one instrument down
        :return:
        """
        for i in instruments:
            # Calculates intermediate volume values (fadeout effect)
            fadeout = self.fadeout(self.instruments[i]['instrument'].mul)
            for value in fadeout:
                # Modifies the mul parameter of the instrument
                if 'grn' in i:
                    self.instruments[i]['out'].input.mul = float(value)
                else:
                    self.instruments[i]['instrument'].mul = float(value)
                time.sleep(duration)
            # Stops the instruments once its volume is at zero
            self.instruments[i]['out'].stop()
        return
        
        
    def restart(self, instruments, volume, duration):
        """
        Instrument restarting function

        :param instruments: List of instrument names to start
        :param volume: Volume at which the instrument will be raised
        :param duration: Time taken to restart an instrument
        :return:
        """
        for i in instruments:
            # Calculates intermediate volume values (fadein effect)
            fadein = self.fadein(volume)
            # Starts the instrument
            self.instruments[i]['out'].out()
            # Modifies the mul parameter of the instrument
            for value in fadein:
                if 'grn' in i:
                    self.instruments[i]['out'].input.mul = float(value)
                else:
                    self.instruments[i]['instrument'].mul = float(value)
                time.sleep(duration)
        return
    
    
    def fadeout(self, start_value):
        """
        Fadeout calculation function

        :param start_value: Volume value from which the fadeout starts
        :return values: List of 100 intermediate, equally spaced volume values going from start_value to zero
        """
        values = []
        for i in range(100):
            values.append(start_value-i*start_value/100)
        return values
        
        
    def fadein(self, end_value):
        """
        Fadein calculation function

        :param end_value: Volume value at which the fadein arrives
        :return values: List of 100 intermediate, equally spaced volume values going from zero to end_value
        """
        values = []
        for i in range(100):
            values.append(end_value-(100-i)*end_value/100)
        return values


    def fade_other(self, start, end):
        """
        Fadeother calculation function

        :param start: Volume value from which the fade starts
        :param end: Volume value at which the fade arrives
        :return values: List of 100 intermediate, equally spaced volume values going from strat to end
        """
        values = []
        step = np.abs(start-end)/100
        if start > end:
            for i in range(100):
                values.append(start-i*step)
            return values
        else:
            for i in range(100):
                values.append(start+i*step)
            return values
    
    
    def change_volume(self, start, end, instrument, duration):
        """
        Volume change function

        :param start: Volume value from which the fade starts
        :param end: Volume value at which the fade arrives
        :param instrument: Name of the instrument to modify
        :param duration: Duration taken to change the volume
        :return:
        """
        values = []
        # Calculates intermediate volume values
        values = self.fade_other(start, end)
        for value in values:
            # Changes the volume value
            if 'grn' in instrument:
                self.instruments[instrument]['out'].input.mul = float(value)
            else:
                self.instruments[instrument]['instrument'].mul = float(value)
            time.sleep(duration)
        return
        
        
    def change_effect(self, start, end, effect, duration):
        """
        Effect change function

        :param start: Effect value from which the fade starts
        :param end: Effect value at which the fade arrives
        :param effect: Name of the effect to modify
        :param duration: Duration taken to change the effect
        :return:
        """
        values = []
        values = self.fade_other(start, end)
        for value in values:
            effect = float(value)
            time.sleep(duration)
        return
    
        
    def build_conductor(self):
        """
        Conductor Assembling function

        :param:
        :return array: Array of size nb_instruments*nb_timesteps containing volume values for each instrument
        """
        # Initializes the array
        array = np.zeros((self.nb_instruments, len(self.list_blocks)))+np.round(random.choice(pdf(0, .1)),2)
        # For each entropy value
        for index in range(len(self.list_blocks)-1):
            entropy = self.list_blocks[index]
            # For each threshold value
            for i in range(len(self.thresholds)-1):
                # If entropy in an interval, number of instruments on that timestep = the index of that interval
                if entropy>self.thresholds[i] and entropy<self.thresholds[i+1]:
                    array[:,index+1] = self.build_next_step(array[:,index], i+1, index+1)
            if entropy>self.thresholds[-1]:
                array[:,index+1] = self.build_next_step(array[:,index], len(self.thresholds), index+1)
        return array
     
    
    def build_next_step(self, current_step, total_on, index):
        """
        Conductor Step Building function

        :param current_step: The volume values of all instruments at a certain time step
        :param total_on: The number of instruments playing needed
        :param index: Current index in the conductor
        :return answer: Array of size nb_instruments*1 containing the volume for the next time step based on the previous one and the current entropy value
        """
        # Finds the instruments currently playing
        current_on = list(np.where(current_step>0)[0])
        # Finds the instruments not playing
        current_off = list(np.where(current_step==0.)[0])
        # If we need to turn on more instruments
        if total_on > len(current_on):
            # We find how many
            needed = total_on - len(current_on)
            # We randomly choose among those that are off
            choices = random.sample(current_off, needed)
            answer = current_step.copy()
            # We set their volume to .4
            answer[choices] =.4
            return answer
        # If enough instruments are already playing
        elif total_on == len(current_on):
            answer = current_step.copy()
            # We return a copy of the current step
            return answer
        # If we need to shut instruments down
        elif total_on < len(current_on):
            # We count how many
            needed = len(current_on) - total_on
            # We randomly choose among the ones playing
            choices = random.sample(current_on, needed)
            answer = current_step.copy()
            # We set their volume to 0
            answer[choices] = 0
            return answer
            
            
    def post_process_conductor(self, array):
        """
        Conductor post-processing function

        :param array: Conductor array before post-processing step
        :return array: Post-processed conductor array
        """
        j_cloud = 100
        for i in range(len(array)):
            for j in range(2, len(array[i])):
                new_value = array[i,j]
                # Applies several post-processing operations (volume limiter etc ...)
                if list(self.instruments.keys())[i]=='bass' and new_value>0:
                    new_value = .2
                elif 'cloud_second' in list(self.instruments.keys())[i] and new_value>0:
                    new_value = .4
                elif 'cloud' in list(self.instruments.keys())[i] and new_value>0:
                    j_cloud = i
                    new_value = .2
                elif new_value>.6:
                    new_value = .4
                elif new_value>0:
                    new_value = random.choice([.1, .2, .3, .4])
                array[i,j] = new_value
        if j_cloud != 100:
            for i in range(len(array[0,:])):
                if len(np.where(array[:,i]>0)[0])==1 or len(np.where(array[:,i]>0)[0])==0:
                    array[j_cloud,i] = .1
        return array
                
                
    def init_conductor(self):
        """
        Conductor initialization function

        :param:
        :return:
        """
        # Converts the conductor array to a dictionary using instrument names as keys
        array = self.post_process_conductor(self.build_conductor())
        self.conductor = {}
        for i in range(len(array)):
            self.conductor[list(self.instruments)[i]] = array[i,:]
        return
        
        
    def read_conductor(self, i):
        """
        Conductor reading function

        :param i: current time-step
        :return:
        """
        for instrument in list(self.conductor.keys()):
            # For each instrument
            # Turns it off if needed
            if self.conductor[instrument][i] == 0 and self.conductor[instrument][i-1] > 0:
                self.shut([instrument], self.TIME_REACT)
            # Restarts it if needed
            elif self.conductor[instrument][i] > 0 and self.conductor[instrument][i-1] == 0 :
                self.restart([instrument], float(self.conductor[instrument][i]), self.TIME_REACT)
        return
        
    
    def print_volumes(self):
        """
        Volume printing function

        :param:
        :return:
        """
        # Prints the volume of every instrument
        for i in list(self.instruments.keys()):
            print('INSTRUMENT :', i)
            print('VOLUME :',self.instruments[i]['instrument'].mul)
        return
        
        
    def init_melodic_conductor(self):
        """
        Melodic conductor initialization function

        :param:
        :return:
        """
        self.melody_conductor = {}
        # Saves the current key the performance is in
        self.melody_conductor['key'] = [self.current_key]
        # Saves the list of possible chords from that key
        self.melody_conductor['chords'] = [self.chords]
        # Iterates over all the entropy values
        for i in range(1, len(self.list_blocks)):
            # If there is a high gap between two consecutive values (>.4)
            if np.abs(self.list_blocks[i]-self.list_blocks[i-1])>.4:
                # Chooses a new key
                next_key = random_walk(tuple(self.current_key))
                # Builds list of allowed chords
                next_chords =  build_chords(build_key(tuple(next_key)))
                self.melody_conductor['key'].append(next_key)
                self.melody_conductor['chords'].append(next_chords)
            # Otherwise, stays in the same key
            else:
                self.melody_conductor['key'].append(self.current_key)
                self.melody_conductor['chords'].append(self.chords)
        return
        
        
    def read_melodic_conductor(self, i):
        """
        Melodic conductor initialization function

        :param i: current time-step
        :return:
        """
        # Reads content from the melodic conductor at a given time-step
        self.current_key = self.melody_conductor['key'][i]
        self.chords = self.melody_conductor['chords'][i]
        return
    
    
    def update_cloud(self, i):
        """
        Cloud updating function
        
        :param i: current time-step
        :return:
        """
        # Chooses a random chord from the list of chords allowed
        chord = random_chord(self.chords)
        # Quantizes the pitch
        final_pitches = pitch_quantizer(chord, onset_dict, self.MIDDLE-self.STD-int(2*self.list_blocks[i]*self.STD), self.MIDDLE+self.STD+int(4*self.list_blocks[i]*self.STD))
        # Sets a pitch for the bass
        pitch_bass = random.choice(chord)
        # Quantizes the bass pitch
        bass = pitch_quantizer([pitch_bass], onset_dict, 48, 64)
        # Turns off the bass
        self.shut(['bass'], 0.005)
        # Changes its fequency
        self.instruments['bass']['instrument'].freq = bass[0]
        # Starts it again with the new frequency
        self.restart(['bass'], float(self.conductor['bass'][i]), 0.005)
        # For all the melodic instruments
        for instrument in list(self.instruments.keys()):
            if 'cloud' in instrument and self.conductor[instrument][i]>0:
                if 'second' in instrument:
                    final_pitches = [final_pitches[0]]
                # Random choice between the notes of a given chord
                mid = Choice(choice=final_pitches, freq=[10, 10])
                fr = MToF(mid, mul=1)
                # Sets the frequency of the instrument to that note
                self.instruments[instrument]['instrument'].freq = fr
        return
        
                
    def update_samples(self, instrument, i, dir, LIMIT):
        """
        Granular samples updating function
        
        :param instrument: Name of the instrument to modify
        :param i: Current time-step
        :param dir: Name of the directory in which to search for a new sample
        :param LIMIT: Time taken to update the sample
        :return:
        """
        # Find current sample of the instrument considered
        sample = self.instruments[instrument]['list_samples'][-1]
        # If instrument currently playing
        if self.conductor[instrument][i]>0:
            if dir in [self.samples_dir_voices, self.samples_dir_aggressive, self.samples_dir_beat]:
                # If the sample has not changed for a while
                if self.instruments[instrument]['count']>LIMIT:
                    # Looks for a sample that has not been selected lately
                    while (sample in self.instruments[instrument]['list_samples']):
                        sample = select_sample_by_key(dir, self.chords)
                        while(sample == None):
                            sample = select_sample_by_key(dir, self.chords)
                    if sample != None:
                        path = os.path.join(dir,sample)
                        # Shuts the instrument down to replace the sample
                        self.shut([instrument], 0.01)
                        self.instruments[instrument]['snd'].setSound(path)
                        self.instruments[instrument]['instrument'].table = self.instruments[instrument]['snd']
                        # Restarts the instrument with the new sample
                        self.restart([instrument], float(self.conductor[instrument][i]), self.TIME_REACT)
                    if sample.endswith('.wav'):
                        # Saves the name of the sample for later
                        self.instruments[instrument]['list_samples'].append(sample)
                        self.instruments[instrument]['count'] = 0
                    return
                else:
                    self.instruments[instrument]['count'] += 1
                    return
            else:
                # If the sample is not in key anymore, or has not changed for a while
                if (not check_still_in_key(sample, self.chords)) or self.instruments[instrument]['count']>LIMIT:
                    while (sample in self.instruments[instrument]['list_samples']):
                        sample = select_sample_by_key(dir, self.chords)
                        while(sample == None):
                            sample = select_sample_by_key(dir, self.chords)
                    if sample != None:
                        path = os.path.join(dir,sample)
                        self.shut([instrument], 0.01)
                        self.instruments[instrument]['snd'].setSound(path)
                        self.instruments[instrument]['instrument'].table = self.instruments[instrument]['snd']
                        self.restart([instrument], float(self.conductor[instrument][i]), self.TIME_REACT)
                    if sample.endswith('.wav'):
                        self.instruments[instrument]['list_samples'].append(sample)
                        self.instruments[instrument]['count'] = 0
                    return
                else:
                    self.instruments[instrument]['count'] += 1
                    return
            
            
    def update_time(self, i):
        """
        Time updating function
        
        :param i: Current time-step
        :return:
        """
        # Randomly assigns a duration for this time-step
        time = random.choice([self.list_blocks[i]*10, 2+(1-self.list_blocks[i])*10])
        print('Wait time = ', time, 's')
        return time
        
        
    def pick_from_list(self, choices, probabilities):
        """
        Returns a random element from a list with weighted probabilites
        
        :param choices: Elements to choose from
        :param probabilities: Probability of each element to be picked
        :return:
        """
        return np.random.choice(choices, 1, p=probabilities, replace=False)[0]

    
    def init_grn_conductor(self):
        """
        Granular conductor initialization function
        
        :param:
        :return:
        """
        self.grn_conductor = {}
        
        # Initializes fields for each granular synth
        for i in list(self.instruments.keys()):
            if "grn" in i:
                self.grn_conductor[i] = {}
                self.grn_conductor[i]['samples_file'] = []
                self.grn_conductor[i]['duration'] = []
                self.grn_conductor[i]['density'] = []
                self.grn_conductor[i]['reverb_wet'] = []
                
        # Defines the samples directories available
        choices = [self.samples_dir_melody, self.samples_dir_voices, self.samples_dir_beat, self.samples_dir_aggressive]
        # For each time-step
        for entropy in self.list_blocks:
            # Finds the threshold interval for the current time-step
            for i in range(len(self.thresholds)-1, 0, -1):
                if entropy>self.thresholds[i]:
                    # Defines the probabilities to choose each samples directory
                    probabilities = [1-entropy, 1-entropy, entropy, entropy]
                    # Normalizes the probability distribution
                    probabilities /= np.sum(probabilities)
                    # Random weighted choice from the list
                    choice = self.pick_from_list(choices, probabilities)
                    for grn in list(self.grn_conductor.keys()):
                        # Replaces samples directory with the newly selected one
                        self.grn_conductor[grn]['samples_file'].append(choice)
                        # Grain duration modification
                        self.grn_conductor[grn]['duration'].append(2-entropy/2)
                        # Grain density modification
                        self.grn_conductor[grn]['density'].append(150-(10+entropy)*entropy)
                        # Reverb modification
                        self.grn_conductor[grn]['reverb_wet'].append(1-entropy)
        return
                    
                    
    def read_grn_conductor(self,i):
        """
        Granular conductor reading function
        
        :param i: current time-step
        :return:
        """
        # For each granular instrument
        for name in list(self.grn_conductor.keys()):
            # Updates the samples directory
            self.update_samples(name, i, self.grn_conductor[name]['samples_file'][i], random.choice([2, 3, 4, 5, 6]))
            # Updates the parameters
            if i%5==0 and self.conductor[name][i]>0:
                self.instruments[name]['instrument'].dur = float(self.grn_conductor[name]['duration'][i])
                self.instruments[name]['instrument'].dens = float(self.grn_conductor[name]['density'][i])
                self.instruments[name]['out'].bal = float(self.grn_conductor[name]['reverb_wet'][i])
