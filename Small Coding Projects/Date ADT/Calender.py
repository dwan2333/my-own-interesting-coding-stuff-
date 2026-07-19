from Date import Date


# function to prinnout a calendar with input as Date (any date)
def printCalendar(d):


    date = Date(d.month(), 1, d.year())
    print(f'{d.monthName():>13} {d.year()}')
    print(f'Su  Mo  Tu  We  Th  Fr  Sa')
    start_position_index = date.dayOfWeek()  #[0,1,2,3,4,5,6] ---> [1,5,9,12,15,19,25]
    start_positions = [5,9,13,17,21,25,1]   # the sequence determines the position of depending on the input for dayOfWeek() method 
    real_position = start_positions[start_position_index]

    
    for i in range(1,date.numDays()+1):

        # start position for the calendar , the number one while is not located at the last position of the calendar with with real_position == 25
        if i == 1 and real_position != 25:
            print(" " * real_position + f'{i}', end = '')
            real_position += 4 
            continue

        # start position for the calendar where position is at 25 
        if i == 1 and real_position == 25:
            print(f'{i:>26}')
            real_position = 1
            continue

        # when the numbers are near the ending of the calendar on Sat. Real position gets reset to start at beginning
        if real_position == 25:
            real_position = 1
            print(f'{i:>4}')

        # printing the regular calendar numbers range from 1 to 24 in real_positions 
        else:
            if real_position == 1:
                print(f'{i:>2}', end= '')
            else:
                print(f'{i:>4}', end = '')
            real_position += 4



            
        




