'''
Created on 18-Mar-2014

@author: sivananda
'''
import Gpib

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
                          5000, 10000, 25000]   #different span settings available
    def preset(self):
        self.dev.write("PRS\r\n");  #preset device 
        
    def __del__(self):
        self.dev.clear()
    def check_device(self):
        self.preset();
        print ("Check the device presetted or not");
    def command(self,command_str):
        self.dev.write(command_str+"\r\n");
    def get_spectrum(self,no_of_points = np):
        self.no_of_points = no_of_points;
        self.command("LDS");
        self.spec_str = self.dev.read(no_of_points*10);
        temp = self.spec_str.split(",")
        output = [float(var) for var in temp];
        return output;
    def set_marker(self,freq):
        self.command("MN 1");
        self.command("MF");
        self.marker_freq = freq;
        freq_int = int(freq*(self.no_of_points - 6)/self.span_list[self.span])
        self.marker_freq_int = freq_int;
        freq_str = str(freq_int);
        self.command("MP "+freq_str);        
        return("")
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