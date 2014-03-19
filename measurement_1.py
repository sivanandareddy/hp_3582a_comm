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
    dev.set_span(8);    #set span of h
    time.sleep(0.5)
    dev.autoset_sensitivity();
    time.sleep(0.5)
    dev.set_averaging(mode = "RMS", no_of_samples=4);
    time.sleep(5);
    data = dev.get_spectrum();
    peak_data = peakdetect.peakdetect(data, lookahead = 2);
    max_peaks = peak_data[0];
    dev.set_scale("linear")
    for peaks in max_peaks:
        #print peaks;
        peaks.append(dev.freq_calc(peaks[0]));
        dev.set_marker(peaks[2]);
        time.sleep(3);
        mark_val = dev.get_marker_data()[0];
        peaks.append(mark_val);
        time.sleep(0.75);
        print peaks;
    table = prettytable.PrettyTable(["Index","in dB", "Freq", "in V"]);
    for peaks in max_peaks:
        table.add_row(peaks);
    print table;
    return

if __name__ == "__main__":
    main()