import pyperclip, re

text = pyperclip.paste() 

phone_number_match = re.compile(r'''(?:\+?\d[-\.\s])? # optional country code 
                                \d{3} # leading three number 
                                [-\.\s]  # seperator 
                                \d{3} # body number
                                [-\.\s] # seperator 
                                \d{4} # tailing number
                                ''', re.VERBOSE)


phone_number_match = phone_number_match.findall(text)

pyperclip.copy(" ".join(phone_number_match))






                
