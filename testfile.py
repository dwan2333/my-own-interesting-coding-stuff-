def printbox(symbol, width, height):
    if width < 2:
        raise Exception("Width has to be bigger or equal to 2")
    if height < 2:
        raise Exception("Height has to be bigger or equal to 2")
    
    for y in range(height):
        for x in range(width):
            print(symbol, end = '')
        print()


        
        
print(printbox("*",3,3))

    
    