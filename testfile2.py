import random,time

width = int(input('Could you please choosed the width of the matrix: '))
matrix_line = [0] * width
density = float(input('Could you please type in an real number x so that 0 < x < 1: '))

while True:
    for i in range(len(matrix_line)):
        if random.random() < density and matrix_line[i] == 0: 
            matrix_line[i] = (random.randint(0,12))
        if matrix_line[i] != 0:
            print(random.randint(0,1), end = " ")
            matrix_line[i] -= 1 
        else:
            print(' ', end = ' ')
        time.sleep(0.01)
    print()




    

