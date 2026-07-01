import pyperclip 

def add_bullet_point():
    text = pyperclip.paste().split('\n')

    for i in range(len(text)):
        text[i] = "- " + text[i]

    new_text = "\n".join(text)
    pyperclip.copy(new_text)

add_bullet_point()

"""Okay that is fine
I am okay """

