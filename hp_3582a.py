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
    def __init__(self):
        self.dev = Gpib.Gpib(0,11);
    def preset(self):
        self.dev.write("PRS\r\n");
    def __del__(self):
        self.dev.clear()
    def check_device(self):
        self.preset();
        print ("Check the device presetted or not");
    def command(self,command_str):
        self.dev.write(command_str+"\r\n");
    def get_spectrum(self,no_of_points = 256):
        self.command("LDS");
        self.spec_str = self.dev.read(256*10);
        temp = self.spec_str.split(",")
        output = [float(var) for var in temp];
        return output;
        return ()