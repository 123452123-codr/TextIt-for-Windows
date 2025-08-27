import random as r

def key_generator():
    l = list("abcdefghijklmnopqrstuvwxyz")
    l1 = l.copy()
    key = []
    cipher = {}

    n = 25
    for i in range(26):
        rint = r.randint(0,n)
        key.append(l[rint])
        l.pop(rint)
        n -= 1
    del l

    for i in range(26):
        k = l1[i]
        v = key[i]
        cipher[k] = v
    
    return cipher
 
def encrypter(s,cipher):
    s_iter = str(s)
    encrypted_message = ""
    for i in s_iter:
        if i.isalpha():
            if i.isupper():
                for k,v in dict(cipher).items():
                    if i.lower() == k:
                        encrypted_message += str(v).upper()
            else:
                for k,v in dict(cipher).items():
                    if i == k:
                        encrypted_message += v
        else:
            encrypted_message += i
    return encrypted_message

def decrypter(s,cipher):
    s_iter = str(s)
    decrypted_message = ""
    for i in s_iter:
        if i.isalpha():
            if i.isupper():
                for k,v in dict(cipher).items():
                    if i.lower() == v:
                        decrypted_message += str(k).upper()
            else:
                for k,v in dict(cipher).items():
                    if i == v:
                        decrypted_message += k
        else:
            decrypted_message += i
    return decrypted_message
