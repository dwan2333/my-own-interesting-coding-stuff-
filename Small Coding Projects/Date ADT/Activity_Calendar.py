
from DateADT import Date as Date
class ActivitiesCalendar:

    def __init__(self, dateFrom, dateTo):

        # making sure that dateFrom must precede dateTo and that both date do not overlap for the same day 
        assert dateFrom._julianDay < dateTo._julianDay \
            , 'Your starting date must be later than your ending date !'
        if dateFrom.month() == dateTo.month(): 
            assert dateFrom.day() != dateTo.day() \
                , 'You can not have overlapping day and month !'

        self._dateFrom = dateFrom 
        self._dateTo = dateTo
        self.activity_storage = dict()

        for i in range(dateFrom._julianDay, dateTo._julianDay + 1):
            self.activity_storage.setdefault(self._toGregorian(i), '')


    # function used to convert julianDay into regular Gregorian for display 
    def _toGregorian(self, julianday ):
        A = julianday + 68569
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

        

    # add given activity decribition to the calendar for the given date 
    def addActivity(self, date, activity):
        try:
            self.activity_storage.update({date._toGregorian(): activity})
        except KeyError:
            return 'Your date is not inside the calendar range'

    # return the string that describes the activity for the given date return None if not exists
    def getActivity(self, date):
        if self.activity_storage[date._toGregorian()] == '':
            return None
        else:
            return self.activity_storage[date._toGregorian()]

    # display a standard output for all activities for the given
    def displayMonth(self, month):

        # filter out the incorrect month  
        key = [date for date, activity in self.activity_storage.items()]
        key = list(filter(lambda x: x[0] == month, key)) 
        

        print(f'Here are the list of activities happening throughout {Date(month,1,2004).monthName()}:')
        for date in key: 
            if self.getActivity(Date(date[0], date[1], date[2])) != None:
                print(f'{date[0]:02d} - {date[1]:02d} - {date[2]:04d} ------> {self.getActivity(Date(date[0], date[1], date[2]))}')




act = ActivitiesCalendar(Date(7,1,2026), Date(8,1,2026))

act.addActivity(Date(7,2,2026), 'Soccer')
act.addActivity(Date(7,22,2026), 'Watch World Cup')
act.addActivity(Date(7,15,2026), 'Play CSGO')

act.displayMonth(7)








        




