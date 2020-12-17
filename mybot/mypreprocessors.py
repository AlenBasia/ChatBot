"""
Statement pre-processors.
"""
def final_sigma(statement):
    '''
    Αν ο χρήστης πληκτρολογήσει "σ" στο τέλος μιας λέξης το αντικαθιστά με "ς".
    '''
    
    data = statement.text.split()
    text = ""
    
    for word in data:
        if word[-1]=="σ":
            word = word[:-1] + "ς" 
        text = text + word + " "
    statement.text = text
    
    return statement


def remove_questionmark(statement):
    '''
    Αν η πρόταση έχει στο τέλος ερωτηματικό, τότε το αφαιρεί
    '''
    
    data = statement.text
    if data.endswith(";") or data.endswith("?"):
        data = data[:-1]
    statement.text = data
    
    return statement
"""
def remove_accents(statement):
    '''
    Antikathista ta grammata pou exoun tonous se grammata xwris tonous
    '''
    import unicodedata
    
    text = ''.join(c for c in unicodedata.normalize('NFD', statement.text)
                  if unicodedata.category(c) != 'Mn')

    statement.text = str(text)

    print("Remove_accents: ", statement.text)

    return statement


def to_lowercase(statement):
    '''
    Converts all letters to lowercase
    '''

    statement.text = statement.text.lower()

    print("To_lowercase: ", statement.text)
    return statement

"""
