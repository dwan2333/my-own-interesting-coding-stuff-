inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
dragon_loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']

def display_inventory(ivt):
    print('Inventory:')
    count = 0
    for k,v in ivt.items():
        print(v, k)
        count += v
    print(f"Total number of items : {count}")


def add_to_inventory(ivt, loot):
    for i in loot:
        if i in ivt:
            ivt[i] += 1
        else:
            ivt.setdefault(i,1)
    return ivt

new_invt = add_to_inventory(inventory, dragon_loot)
print(new_invt)
display_inventory(new_invt)

    

