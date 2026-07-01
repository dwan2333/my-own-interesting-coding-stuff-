inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def display_inventory(ivt):
    print('Inventory:')
    count = 0
    for k,v in ivt.items():
        print(v, k)
        count += v
    print(f"Total number of items : {count}")


display_inventory(inventory)

    

