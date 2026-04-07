import random as r
import string

def key_generator():
    l = list(string.ascii_lowercase)
    num = list("1234567890")
    l1 = l.copy()
    num1 = num.copy()
    key = []
    cipher = {}

    n = 25
    for i in range(26):
        rint = r.randint(0,n)
        key.append(l[rint])
        l.pop(rint)
        n -= 1
    del l

    n1 = 9
    for i in range(10):
        rint = r.randint(0,n1)
        key.append(num[rint])
        num.pop(rint)
        n1 -= 1
    del num

    for i in range(26):
        k = l1[i]
        v = key[i]
        cipher[k] = v

    for i in range(10):
        k = num1[i]
        v = key[i+26]
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
        elif i.isdigit():
            for k,v in dict(cipher).items():
                    if i == k:
                        encrypted_message += str(v)
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
        elif i.isdigit():
            for k,v in dict(cipher).items():
                    if i == v:
                        decrypted_message += str(k)
        else:
            decrypted_message += i
    return decrypted_message
