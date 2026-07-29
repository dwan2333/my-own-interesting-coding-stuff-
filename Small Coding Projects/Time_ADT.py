# Abstract Data Tyeps to show time 
class Time:

    # initialization of for time 
    def __init__(self, hours, minutes, seconds): 
        self.hours = hours 
        self.minutes = minutes 
        self.seconds = seconds 

    # returns hour part of the time 
    def hour(self):
        return self.hours 

    # return the seconds part of the time 
    def minutes(self):
        return self.minutes 

    # return seconds 
    def seconds(self):
        return self.seconds 

    # return number of seconds as a positive integer between this time and the Othertime 
    def numSeconds(self, otherTime):
        self_total = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        other_total = (otherTime.hours * 3600) + (otherTime.minutes * 60) + otherTime.seconds
        return abs(self_total - other_total)

    # determine if the time is ante meridiem or beofre midday 
    def isAm(self):
        return True if self.hours < 12 else False

    # determine if the time is post meridiem or after midday 
    def isPm(self):
        return True if self.hours > 12 else False 

    # Compare this time to otherTime to determine their logical ordering
    def comparable(self, otherTime): 
        self_total = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        other_total = (otherTime.hours * 3600) + (otherTime.minutes * 60) + otherTime.seconds
        
        if self_total < other_total:
            return -1 # This time is earlier
        elif self_total == other_total:
            return 0  # Both times are the exact same
        else:
            return 1  # This time is later

    # return a string representation of the time in 12 hour format hh:mm:ss 
    def toString(self):
        # set condition for hh if is hour is bigger than 12 
        if self.hours > 12: 
            hours = '0' + str(self.hours - 12) 
        else:
            hours = str(self.hours) 

        # set condition for mm if minute is less than 10 
        if self.minutes < 10:
            minutes = '0' + str(self.minutes)
        else:
            minutes = str(self.minutes)

        # set condition for ss if minute is less than 10
        if self.seconds < 10:
            seconds = '0' + str(self.seconds)
        else:
            seconds = str(self.seconds)

        return f'{hours}:{minutes}:{seconds}'



        
        

    