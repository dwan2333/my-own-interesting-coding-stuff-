from datetime import date
class Date :
    # Creates an object instance for the specified Gregorian date.
    def __init__( self, month = None, day = None, year = None):
        self._julianDay = 0
        assert self._isValidGregorian( month, day , year ), \
               "Invalid Gregorian date."
        if all([month == None, day == None, year == None]):
            month = date.today().month
            day = date.today().day
            year = date.today().year
        # The formula's first line, T = (M - 14) / 12, had to be changed
        # because Python's integer division differs from the mathematical
        # definition — see the warning below.
        tmp = 0
        if month < 3 :
            tmp = -1
        self._julianDay = day - 32075 + \
                          (1461 * (year + 4800 + tmp) // 4) + \
                          (367 * (month - 2 - tmp * 12) // 12) - \
                          (3 * ((year + 4900 + tmp) // 100) // 4)

    # Extracts the appropriate Gregorian date component.
    def month( self ):
        return (self._toGregorian())[0]     # M from (M, d, y)

    def day( self ):
        return (self._toGregorian())[1]     # D from (m, D, y)

    def year( self ):
        return (self._toGregorian())[2]     # Y from (m, d, Y)

    # Returns day of the week as an int between 0 (Mon) and 6 (Sun).
    def dayOfWeek( self ):
        month, day, year = self._toGregorian()
        if month < 3 :
            month = month + 12
            year = year - 1
        return ((13 * month + 3) // 5 + day + \
                year + year // 4 - year // 100 + year // 400) % 7

    # Returns the date as a string in Gregorian format.
    def __str__( self ):
        month, day, year = self._toGregorian()
        return "%02d/%02d/%04d" % (month, day, year)

    # Logically compares the two dates.
    def __eq__( self, otherDate ):
        return self._julianDay == otherDate._julianDay

    def __lt__( self, otherDate ):
        return self._julianDay < otherDate._julianDay

    def __le__( self, otherDate ):
        return self._julianDay <= otherDate._julianDay

    # ... the remaining methods (numDays, advanceBy, monthName, isLeapYear,
    #     _isValidGregorian) are left as exercises by the book ...

    # Returns the Gregorian date as a tuple: (month, day, year).
    def _toGregorian( self ):
        A = self._julianDay + 68569
        B = 4 * A // 146097
        A = A - (146097 * B + 3) // 4
        year = 4000 * (A + 1) // 1461001
        A = A - (1461 * year // 4) + 31
        month = 80 * A // 2447
        day = A - (2447 * month // 80)
        A = month // 11
        month = month + 2 - (12 * A)
        year = 100 * (B - 49) + year + A
        return month, day, year

    # return the current str month name 
    def monthName(self):
        month_list = ['January' , 'Febuary', 'March' , 'April', 'May' , 'June' , 'July', 'August', 'September' , 'October', 'November' , 'December']
        return month_list[self._toGregorian()[0]-1]

    # return Boolean Value to determine given date Leap year validity
    def isLeapYear(self):
        year = self._toGregorian()[2]
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return True
        else:
            return False 

    # return int for number of days in the month
    def numDays(self):
        if self.isLeapYear() and self._toGregorian()[0] == 2: 
            return 29
        elif self._toGregorian()[0] == 2:
            return 28
        else:
            days = [31,28,31,30,31,30,31,31,30,31,30,31]
            return days[self._toGregorian()[0] - 1]

    # add days to the current date
    def advanceBy(self, days):
        self._julianDay += days

    # return Boolean value to determine if user input is valid date
    def _isValidGregorian(self, month, day, year):

        if all([month == None, day == None, year == None]):
            return True
        if not all([type(month) == int, type(day) == int, type(year) == int]):
            return False 
        if not (month <= 12 and month > 0 ):
            return False 
        
        is_leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        max_days = 29 if is_leap and month == 2 else [31,28,31,30,31,30,31,31,30,31,30,31][month - 1]
        if not (day <= max_days and day > 0):
            return False 
        if year < 0:
            return False 
        return True 

    # return the str name of the week for the user date
    def dayOfWeekName(self): 
        week_names = ['Monday' , 'Tuesday', 'Wednsday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return week_names[self.dayOfWeek()]

    # return int for the total number of days passed given by the user date
    def dayOfYear(self):
        month, day, year = self._toGregorian()
        if self.isLeapYear():
            days = [31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            days = [31,28,31,30,31,30,31,31,30,31,30,31]
        return sum(days[:month-1]) + day 

    # return bool for whether the date is a weekday or not
    def isWeekday(self):
        return True if self.dayOfWeek() >= 5 else False

    # return str format for the user intended dividers
    def asGregorian(self, divchar = '/'):
        month,day,year = self._toGregorian()
        return f'{month}{divchar}{day}{divchar}{year}'

    # return bool to determine if the given date is Equinox (meaning they time are equal in day and night)
    def isEquinox(self):
        month, day, year = self._toGregorian()
        if (month == 3 and day == 20) or (month == 9 and day == 22):
            return True
        return False 

    # return bool to determine if the given date is Solastice (two day when sun reaches highest or lowest given two longest or shortest day)
    def isSolastice(self):
        month, day, year = self._toGregorian()
        if (month == 6 and day == 21) or (month == 12 and day == 21):
            return True
        return False






        


