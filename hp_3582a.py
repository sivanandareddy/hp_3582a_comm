'''
Created on 18-Mar-2014

@author: sivananda
'''
import Gpib;
import time;
import numpy as np;

class hp_3582a:
    '''
    @summary: This class will make easy of remote commands on the HP 3582A
              Spectrum analyser
    '''
    np = 256;
    def __init__(self):
        self.dev = Gpib.Gpib(0,11);
        self.no_of_points = self.np;    #no of points in spectrum
        self.span = 8;                  #set span to 250 Hz
        self.span_list = [0, 1, 2.5, 5, 10, 25, 50, 
                          100, 250, 500, 1000, 2500, 
                          5000, 10000, 25000];   #different span settings available
        self.scale = {'A': 1,'B': 1};
        self.sens_list = ["CAL","30V, +30 dBV", "10V, +20dBV",
                          "3V, +10dBV","1V, +0dBV","0.3V, -10dBV", 
                          "0.1V, -20dBV", "30mV, -30dBV", 
                          "10mV, -40dBV", "3mV, -50dBV"]
    def preset(self):
        self.command("PRS");  #preset device 
        print ("Device is presetted")
        
    def __del__(self):
        self.dev.clear();
    
    def check_device(self):
        self.preset();
        print ("Check the device presetted or not");
    
    def command(self,command_str):
        self.dev.write(command_str+"\r\n");
    
    def get_spectrum(self,no_of_points = np):
        '''
        
        '''
        self.no_of_points = no_of_points;
        self.command("LDS");
        self.spec_str = self.dev.read(no_of_points*10);
        temp = self.spec_str.split(",")
        output = [float(var) for var in temp];
        return output;
    
    def set_marker(self,freq):
        '''
        @summary: sets marker to a given frequency
        @param freq: this parameter can be float or int
        '''
        self.marker_on();   #turn on marker
        self.command("MF");     #marker set frequency mode
        self.marker_freq = freq;
        freq_int = int(freq*(self.no_of_points - 6)/self.span_list[self.span])
        self.marker_freq_int = freq_int;
        freq_str = str(freq_int);
        self.command("MP "+freq_str); #set marker to the requested frequency
        freq_str_prn = str(int(freq_int*self.span_list[self.span]/(self.no_of_points - 6)));
        print ("Current marker position: "+freq_str_prn+"Hz")        
        return ;
    
    def freq_calc(self,data_pos):
        '''
        @summary: to calculate the freq of the data point in the spectrum data
        @param data_pos: This is the position of the data in the list
        @return: returns the freqency corresponding to the data position 
        '''
        return data_pos*self.span_list[self.span]/(self.no_of_points - 6);
        
    def set_span(self,span_number = 8):
        '''
        @summary: sets the span
        @param span_number: select the span number according to the following list
        none => 0, 1 => 1, 2 => 2.5, 3 => 5, 4 => 10, 5 => 25, 6 => 50, 
        7 => 100, 8 => 250, 9 => 500, 10 => 1000, 11 => 2500, 12 => 5000, 
        13 => 10000, 14 =>25000
        @example:
        set_span(13) #for span frequency 10kHz
        '''
        self.command("MD 2");
        self.command("SP "+str(span_number));
        self.span = span_number;
    
    def set_passband_shape(self,shape = "Flattop"):
        '''
        @summary: sets the pass band shape
        @param: Take the parameter "Flattop","Hanning",or "Uniform" anything else will
        be considered as Flattop
        @example:
        set_passband_shape("Flattop");
        '''
        if shape[0] == "F" or shape[0] == "f":
            shape_int = 1;
        elif shape[0] == "H" or shape[0] == "h":
            shape_int = 2;
        elif shape[0] == "U" or shape[0] == "u":
            shape_int = 3;
        else:
            shape_int = 1;
        self.command("PS "+ str(shape_int));
    
    def marker_on(self):
        '''
        @summary: turns on marker
        '''
        self.command("MN 1");
    
    def marker_off(self):
        '''
        @summary: truns off marker
        '''
        self.command("MN 0")
        
    def status(self):
        self.command("LST0");
        return (format(ord(self.dev.read(1)),"#010b"));
    
    def set_sensitivity(self,scale_no = 2,ch = 'A'):
        '''
        @summary: Sets the sensitvity of channel A
            +----------+--------------+
            | scale_no | Sensitivity  |
            +----------+--------------+
            |    2     | 30V, +30 dBV |
            |    3     | 10V, +20dBV  |
            |    4     |  3V, +10dBV  |
            |    5     |  1V, +0dBV   |
            |    6     | 0.3V, -10dBV |
            |    7     | 0.1V, -20dBV |
            |    8     | 30mV, -30dBV |
            |    9     | 10mV, -40dBV |
            |    10    | 3mV, -50dBV  |
            +----------+--------------+
        '''
        if ch == "A" or ch == "a":
            self.command("AS " + str(scale_no));
            self.scale['A'] = scale_no;
            print ("Sensitivity on ch: "+ ch +" "+self.sens_list[self.scale[ch]-1]);
        elif ch == "B" or ch == "b":
            self.command("BS " + str(scale_no));
            self.scale['B'] = scale_no;
            print ("Sensitivity on ch: "+ ch +" "+self.sens_list[self.scale[ch]-1]);
    
    def autoset_sensitivity(self,ch = 'A'):
        scale_no = 2;
        self.scale[ch] = scale_no;
        self.set_sensitivity(2, ch);
        while(1):
            time.sleep(1)
            if self.is_overloaded(ch):
                break;
            else:
                scale_no = scale_no + 1;
                self.scale[ch] = scale_no;
                if scale_no > 10:
                    print ("Maximum sensitivity has been reached");
                    break
                else:
                    self.set_sensitivity(scale_no, ch)
        scale_no = scale_no - 1;
        self.scale[ch] = scale_no;
        self.set_sensitivity(scale_no, ch)
        print ("Autoset Sensitivity on ch: "+ ch +" "+self.sens_list[self.scale[ch]-1]);
        return ;
    
    def is_overloaded(self,ch = 'A'):
        '''
        @summary: This function finds whether the particular channel is overloaded
        or not. if overloaded it returns true else false
        '''
        if ch == 'A' or ch == 'a':
            for x in range(0,4):
                status_byte = self.status();
                time.sleep(0.5);
            if status_byte[-3] == '1':
                return True;
            else:
                return False;
        if ch == 'B' or ch == 'b':
            for x in range(0,4):
                status_byte = self.status();
                time.sleep(0.5);
            if status_byte[-4] == '1':
                return True;
            else:
                return False;
    
    def set_averaging(self,mode = "RMS", no_of_samples = 4):
        '''
        @summary: To set averaging mode 
        @param mode: "RMS" or "TIME" or "PEAK" are the valid inputs
        @param no_of_samples: 4, 8, 16, 32, 64, 128, 256 are valid inputs
        '''
        self.avg_mode = {"RMS":2,"TIME":3,"PEAK":4}
        self.command("AV "+str(self.avg_mode[mode]));
        if no_of_samples > 256:
            no_of_samples = 256;    #upper limit of the samples for averaging
        if no_of_samples < 4:
            no_of_samples = 4;      #lower limit of the samples for averaging
        nu = int(no_of_samples/4);
        nu = int(np.log2(nu)) + 1;
        nu_temp = nu;
        sh = int(nu/4);
        if sh == 1:
            nu = nu % 4;
        self.command("SH "+str(sh));
        self.command("NU "+str(nu));
        print ("Averaging is turned on; Mode = " + mode + 
               ";\nNumber of samples for averaging " + str(int(pow(2,nu_temp+1))));
        return;
    
    def averaging_off(self):
        '''
        @summary: Turns off the averaging mode
        '''
        self.command("AV 1");
        print ("Averaging mode is truned off")
        return ;
    
    def set_scale(self,scale = "10 dB/div"):
        '''
        @summary: Sets the scale to linear or dB
        @param scale: "LINEAR" or "10 dB/div" or "2 dB/div"
        are the acceptable inputs
        '''
        self.scale_list = {"linear":1,"10 db/div":2, "2 db/div":3}
        s = self.scale_list[scale.lower()];
        self.command("SC "+str(s));
        print ("Current scale is "+scale+" scale mode "+str(s));
        
    def get_marker_data(self):
        '''
        @summary: to get the marker position and value
        @returns the marker position in the frist of list, 
        value in the second of list
        '''
        self.command("LMK");
        data = self.dev.read(21)
        value = float(data[0:10]);
        freq = float(data[12:20]);
        return [value, freq]