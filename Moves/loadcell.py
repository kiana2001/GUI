# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
import csv
# Import the ADS1x15 module.
# import Adafruit_ADS1x15

class loadcell():
    def loadcell():
        # Create an ADS1115 ADC (16-bit) instance.
        # adc = Adafruit_ADS1x15.ADS1115()

        # Or create an ADS1015 ADC (12-bit) instance.
        #adc = Adafruit_ADS1x15.ADS1015()

        # Note you can change the I2C address from its default (0x48), and/or the I2C
        # bus by passing in these optional parameters:
        # adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=5)
        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        GAIN = 1

        # print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        # print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        # print('-' * 37)
        # Main loop.

        data = []
        reading_time = []
        milliseconds1 = int(round(time.time()*1000000))
        t = 0
        c = 0
        avg = 0
        values = []
        try:
            while True:
                # Read all the ADC channel values in a list.
                # values2 = [0]*4
                # values = [0]*4
                # for i in range(1):
                # Read the specified ADC channel using the previously set gain value.
                # values[i] = adc.read_adc(i, gain=GAIN)
                # Note you can also pass in an optional datanalogio not supported for this board.a_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = 
                # print('hello')
                time.sleep(0.005)
                ADC_Value = 1#(adc.read_adc(0, gain=GAIN, data_rate=860) - 19944)/6.232
                # print(ADC_Value)
                return ADC_Value
                data.append(ADC_Value)
                # print()
                # data.append(values[i])
                # values2[i] = adc.read_adc_difference(differential = 0, gain=1, data_rate=None)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
                # Print the ADC values.
                
                # print(values[1] / 16)
                # print('usual    =   ','| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
                # print('diffe    =   ','| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values2))
                # print(milliseconds-milliseconds1)
                # continue
                # value = adc.read_adc(0, gain=GAIN, data_rate=860)
                
                # data.append(value)
                # avg = avg + value
                # values.append(value) 
                # print(value, (values[-100:]))            
                
                # print((int(sum(values[-100:])/1000)/10.0) - 179)           
                #time.sleep(0.01)
                        
                # Pause for half a second.
                # time.sleep(0.1)


        except IOError as e:
            print('')
        
        except KeyboardInterrupt:
            print("ctrl + c:")
            print("Program end")
            
        with open('data.csv', 'w', newline='') as f:
            fileWriter = csv.writer(f)
            for d in data: fileWriter.writerow([d])
        print(sum(data)/len(data))

# print("do")
    
# with open('reading_time.csv', 'w', newline='') as f:
#     fileWriter = csv.writer(f)
#     for d in reading_time: fileWriter.writerow([d])
