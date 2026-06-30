def printbox(symbol, width, height):
    if width < 2:
        raise Exception("Width has to be bigger or equal to 2")
    if height < 2:
        raise Exception("Height has to be bigger or equal to 2")
    
    print(symbol * width)
    for i in range(height-2):
        print(symbol + ' ' * (width-2) + symbol)
    print(symbol * width)

print(printbox('*',5,4))


        
        


    
    