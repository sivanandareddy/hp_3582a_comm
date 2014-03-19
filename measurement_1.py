'''
Created on 19-Mar-2014

@author: sivananda
'''
import hp_3582a
import time
import peakdetect
import prettytable;

def main():
    dev = hp_3582a.hp_3582a();
    dev.preset();       #preset the device
    time.sleep(0.5)     #delay of 0.5 secs
    dev.set_span(8);    #set span now set to 250Hz
    time.sleep(0.5)     #delay of 0.5 secs
    dev.autoset_sensitivity();  #auto set the sensitivty of channel
    time.sleep(0.5)     #delay of 0.5 secs
    dev.set_averaging(mode = "RMS", no_of_samples=4);   #set averaging
    time.sleep(5);      #delay of 0.5 secs
    data = dev.get_spectrum();  #get the spectrum data to find peaks
    ##!!!!!! WARNING: Peakdetection algoritam was not written by me !!!!!!!##
    ##!!!!!!          make sure it is working well before using it  !!!!!!!##
    peak_data = peakdetect.peakdetect(data, lookahead = 2); #peak detection
    max_peaks = peak_data[0]; #considering only the max peak and discarding mins
    dev.set_scale("linear") #change scale from 10 dB/div to linear
    for peaks in max_peaks:
        #print peaks;
        peaks.append(dev.freq_calc(peaks[0]));  #calculate freq cooresp.. to index
        dev.set_marker(peaks[2]);   #set marker at that peak
        time.sleep(3);              #delay of 3 secs
        mark_val = dev.get_marker_data()[0];    #get marker value in volts
        peaks.append(mark_val);     #append marker value to the list
        time.sleep(0.75);           #delay of 0.75 secs
        print peaks;                #print the peak info after reading each peak
    #preperation for consolidated report
    table = prettytable.PrettyTable(["Index","in dB", "Freq", "in V"]);
    for peaks in max_peaks:
        table.add_row(peaks);
    print table;
    return

if __name__ == "__main__":
    main()