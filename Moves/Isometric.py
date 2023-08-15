# import canopen
import time
# import ADS1263
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from . loadcell import loadcell

class Isometric(QObject):
    finished = pyqtSignal()
    M_i, Timer_i, F_i, Count_i, Set_i, Timer2, Run_Time_old = [0, 0, 0, 0, 0, 100, 0]

    # ADC = ADS1263.ADS1263()
    # if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
    #     exit()
    # ADC.ADS1263_SetMode(1)
    # ADC.ADS1263_SetDiffChannal(0)


    def Force_Loadcell(self):
        # while True:
        #     ADC_Value = ADC.ADS1263_GetChannalValue(0)
        #     if ADC_Value == "error":
        #         continue
        #     offset = 0.0577
        #     if(ADC_Value>>31 ==1):
        #         # print("ADC1 IN%d = -%lf %d" %(0, ((REF*2 - ADC_Value * REF / 0x80000000) - offset), milliseconds))  
        #         Force = (REF*2 - ADC_Value * REF / 0x80000000)
                
        #     else:
        #         Force = ADC_Value * REF / 0x7fffffff
        #     break
        # print(Force)
        return 10

    def Refrence_Generator(self, Force_Ref, Time_h, Theta1, Theta2, Theta3, Theta, Force):
        
        Velocity = 0
        # global M_i, Timer_i
        M_o = self.M_i
        Timer = self.Timer_i

        print('Holding Time = ',Timer)    #Timer for holding

        if Force_Ref < 0:
            Force=-Force
            Force_Ref=-Force_Ref

        if M_o == 0:
            Velocity = 0.01*(-Theta1 - Theta)
            if Force > Force_Ref and abs(-Theta1 - Theta) < 10:
                Timer = self.Timer_i + 0.0003
            else:
                Timer = 0
            if Timer > Time_h:
                M_o = 1

        if M_o == 1:
            #Timer = 5
            Velocity = 0.01*(-Theta2 - Theta) 
            if Force > Force_Ref and abs(-Theta2 - Theta) < 10:
                Timer = self.Timer_i + 0.0003
            else:
                Timer = 5
            if Timer > Time_h + 5:
                M_o = 2

        if M_o == 2:
            #Timer = 10
            Velocity = 0.01*(-Theta3 - Theta)
            if Force > Force_Ref and abs(-Theta3 - Theta) < 10:
                Timer = self.Timer_i + 0.0003
            else:
                Timer = 10
            if Timer > Time_h + 10:
                M_o = 0
        self.Timer_i = Timer
        self.M_i = M_o
        return Velocity

    def Set_Rep(self, Rest_Time, Pos, Ti2, Ti1, Input, Repeats_Desired, Sets_Desired):        
        F_o = self.F_i
        Count_o = self.Count_i
        Set_o = self.Set_i

        if -Ti1-5<Pos and Pos<-Ti1+5:
            F_o = 1
        elif -Ti2-5<Pos and Pos<-Ti2+5:
            F_o = 2

        if F_o == 1 and self.F_i == 2:
            Count_o = self.Count_i+1

        if Count_o == Repeats_Desired:
            if self.Set_i < Sets_Desired:
                Set_o = self.Set_i+1
            Count_o = 0
            self.Timer2 = 0
            
            
        print('set_i = ',self.Set_i)
        if Set_o >= Sets_Desired:
            Set_o = Sets_Desired

        if (self.Set_i >= Sets_Desired or self.Timer2 < Rest_Time):
            self.Timer2 += 0.0003
            if  self.Set_i >= Sets_Desired and -1 < Pos and Pos < 1:
                stop_while = 0
            Output = 0.01*(-Pos)
        else:
            Output = Input

        self.F_i = F_o
        self.Count_i = Count_o
        self.Set_i = Set_o

        return Output

    def Safety_Function(self, Time, Theta_Sat_Pos, Theta_Sat_Neg, Input, Theta):
        Run_Time = self.Run_Time_old + 0.001
        if Theta > Theta_Sat_Pos:
            Output = 0
        elif Theta < Theta_Sat_Neg:
            Output = 0
        else:
            Output = Input

        if Run_Time > Time - 5:
            Output = 0.01*(-Theta)
        self.Run_Time_old = Run_Time

        return Output

    def init_drive(self, node , network):
        node.nmt.state = 'PRE-OPERATIONAL'
        node.sdo['Controlword'].raw=128 #Clear_Error
        node.sdo['Controlword'].raw=0 #Switch_ON
        node.sdo['Controlword'].raw=6 #
        node.sdo['Controlword'].raw=7 # Init & Run
        node.sdo['Controlword'].raw=15#

        node.sdo['Modes of operation'].raw=3 #Velocity Mode

        # Read PDO configuration from node
        node.rpdo.read()
        node.tpdo.read()
        # Re-map TPDO[1]
        node.tpdo[1].clear()
        node.tpdo[1].add_variable('Position actual value')
        node.tpdo[1].add_variable('Velocity actual value')
        node.tpdo[1].enabled = True

        # Re-map TPDO[2]
        node.tpdo[2].clear()
        node.tpdo[2].add_variable('Torque actual value')
        # node.tpdo[2].add_variable('Velocity actual value')
        node.tpdo[2].enabled = True

        # Save new PDO configuration to node
        node.tpdo[1].save()
        node.tpdo[2].save()

        node.rpdo[1].clear()
        node.rpdo[1].add_variable('Target velocity')
        #node.rpdo[1].add_variable('Target velocity')
        node.rpdo[1].enabled = True
        node.rpdo.save()
        node.rpdo[1].start(0.005)

    def run(self, Rest_Time, Sets_Desired, Repeats_Desired, Force, Hold_Time, Theta1, Theta2, Theta3):
        # Start with creating a network representing one CAN bus
        network = canopen.Network()

        # Add some nodes with corresponding Object Dictionaries
        node1 = canopen.RemoteNode(1, '/home/physio/codes/Physio Robot/Physio_Robot_GUI/modules/Moves/ASDA_A2_1042sub980_C.eds')
        network.add_node(node1)

        network.connect(bustype='socketcan', channel='can0')
        
        self.init_drive(node1, network)
        print("all nodes are initiated")

        node1.nmt.state = 'OPERATIONAL'

        LoopTime = 0
        try:
            while True:
                Theta = node1.tpdo[1]['Position actual value'].raw *(360 / (1280000 * 25))
                # print('Pos', Theta)
                # Force = self.Force_Loadcell()
                Force = loadcell.loadcell()
                print(Force)
                # Force_Ref, Time_h, Theta1, Theta2, Theta3 = [Force, Hold_Time, Theta1, Theta2, Theta3]
                #Force
                Velocity = self.Refrence_Generator(5, 0.2, Theta1, Theta2, Theta3, Theta, Force)
                Velocity = self.Set_Rep(Rest_Time, Theta, Theta2, Theta1, Velocity, Repeats_Desired, Sets_Desired)
                # print('Vel = ', Velocity)
                # Time, Theta_Sat_Pos, Theta_Sat_Neg, Input = [100, 10, -80, Velocity]
                # Velocity = Safety_Function(Time, Theta_Sat_Pos, Theta_Sat_Neg, Input, Theta)
                
                node1.rpdo[1]['Target velocity'].raw = Velocity*10000
                # print('Loop Time = ',abs(LoopTime - time.time()))
                LoopTime = time.time()

        except KeyboardInterrupt:
            print("STOP!")
            node1.sdo['Controlword'].raw = 0
            network.disconnect()
        except Exception as e:
            print(e)
        finally:
            self.finished.emit()    
            node1.rpdo[1]['Target velocity'].raw = 0
            node1.sdo['Controlword'].raw = 0
            network.disconnect()
        
# with open("actualPosition.csv",'w') as f:
#     w = csv.writer(f)
#     for a in apos:
#         w.writerow([a])
