from Date import Date
import logging

def printCalendar(d):

    date = Date(d.month(), 1, d.year())
    print(f'{d.dayOfWeekName():>13} {d.year()}')
    print(f'Su  Mo  Tu  We  Th  Fr  Sa')
    start_position_index = date.dayOfWeek()+1  #[0,1,2,3,4,5,6] ---> [1,5,9,12,15,19,25]
    start_positions = [1,5,9,13,17,21,25]
    real_position = start_positions[start_position_index]

    
    for i in range(1,date.numDays()+1):


        if i == 1 and real_position != 25:
            print(" " * real_position + f'{i}', end = '')
            real_position += 4 
            continue

        if i == 1 and real_position == 25:
            print(f'{i:>26}')
            real_position = 1
            continue

        if real_position == 25:
            real_position = 1
            print(f'{i:>4}')

        else:
            if real_position == 1:
                print(f'{i:>2}', end= '')
            else:
                print(f'{i:>4}', end = '')
            real_position += 4


printCalendar(Date(8,1,2026))
            
        




