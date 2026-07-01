import re 
number = re.compile(r'\d{3}-|\.|\s\d{3}')
text = '858 308 2978, 858 297'

print(number.findall(text))
    


        
        


    
    