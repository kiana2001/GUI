class Passive():
    def __init__(self, time, restTime, sets, repeats, minROM = 0, maxROM = 30, speed = 10) -> None:
        self.time = time
        self.restTime = restTime
        self.sets = sets
        self.repeats = repeats
        self.minROM = minROM
        self.maxROM = maxROM
        self.speed = speed
        
    def print(self):
        print(self.time)