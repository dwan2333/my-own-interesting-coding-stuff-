while True:
    print('Who are you?')
    if (name := input('>')) != 'Joe':
        continue 
    print("Hello Joe, what's your password?")
    if (password := input('>')) != 'swordfish':
        break
print('Acess granted') 
