from math import sin, pi

class Passive():
  def __init__(self, sets, repeats, restTime, rom, speed) -> None:
    self.sets = sets
    self.repeats = repeats
    self.restTime = restTime
    self.rom = rom
    self.speed = speed
      
  def SineGenereator(self, time):
    amp = self.rom / 2
    bias = - amp
    Per = 4 * amp / self.speed
    self.Sine = amp * sin ((2*pi/Per) * time + pi/2) + bias
    
  def SetRep(self, Time, Pos, Repeats_Desired, Sets_Desired, Stop_Time_i, Set_i, F_i, Count_i):
    [Flag, Output, Stop_Time_o, Set_o, F_o, Count_o]
    F_o=F_i
    Count_o=Count_i
    Set_o=Set_i
    Stop_Time_o=Stop_Time_i

    if -2<Pos and Pos<+2:
        F_o=1
    elif -self.rom -2 < Pos and Pos < -self.rom + 2:
        F_o=2

    if F_o==1 and F_i==2:
        Count_o=Count_i+1

    if Count_o == Repeats_Desired:
        if Set_i<Sets_Desired:
            Set_o=Set_i+1
        Count_o=0
        Stop_Time_o=Time

    if Set_o>=Sets_Desired:
        Set_o=Sets_Desired

    if (Set_i>=Sets_Desired or Time-Stop_Time_i < self.restTime):
        Output=0
        self.flag=1
    else:
        Output= self.Sine
        self.flag=0
        
  def TimerReset(self, Time_I):
    Time_O = Time_I + 0.001

    if self.flag == 1:
        Time_O = 0
        
  def IncrementalPID(self, error, P_max, P_old):
    [PID_Output, P]
    P = P_old + 0.0001

    if P >= P_max:
        P = P_max

    PID_Output = P * error
    
  def SafetyFunction(self, Time, Theta_Sat_Pos, Theta_Sat_Neg, Input, Theta, Run_Time_old):
    [Output, Run_Time]
    Run_Time = Run_Time_old + 0.001

    if Theta > Theta_Sat_Pos:
        Output = 0
    elif Theta < Theta_Sat_Neg:
        Output = 0
    else:
        Output = Input

    if Run_Time > Time - 5:
        Output = 0.01*(-Theta)