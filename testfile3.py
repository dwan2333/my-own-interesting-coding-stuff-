def make(name, *, color='red'):
    return f'{name}/{color}'

print(make('car','tesla' ,color='blue'))   # OK — passed by name
# make('car', 'blue')              # TypeError: color is keyword-only

