import pyperclip, re

text = pyperclip.paste() 

phone_number_match = re.compile(r''' # optional country code 
                                (\d{3}) # leading three number 
                                (-|\.|\b)  # seperator 
                                (\d{3}) # body number
                                (-|\.|\b) # seperator 
                                (\d{4})
                                    ''', re.VERBOSE)

text = "858-308-2978 , +1 858 308 2978, 858.308.2978"

print(phone_number_match.findallmatch(text))




                
