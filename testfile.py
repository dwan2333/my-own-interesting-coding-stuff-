import time

indent = True
while True:
    
    if indent == True:
        for i in range(1,8):
            print(i * " " + "*******")
        indent = False 

    else:
        for i in range(6,-1,-1):
            print(i * " " + "*******")
        indent = True


    
    