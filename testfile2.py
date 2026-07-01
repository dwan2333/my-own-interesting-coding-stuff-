import pyperclip, re

text = pyperclip.paste() 

phone_number_match = re.compile(r'''(?:\+?\d[-\.\s])? # optional country code 
                                \d{3} # leading three number 
                                [-\.\s]  # seperator 
                                \d{3} # body number
                                [-\.\s] # seperator 
                                \d{4} # tailing number
                                ''', re.VERBOSE)

text = "858-308-2978 , +1 858 308 2978, 858.308.2978"

print(phone_number_match.findall(text))




                
