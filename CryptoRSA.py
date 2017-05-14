
from NumTheoryBasics import modinv

alphabet = "$ABCDEFGHIJKLMNOPQRSTUVWXYZ "
p, q = 2**31 - 1, 216895849601 # two large primes

#The Public Key (e,n)
n = p*q
e = 2017 #prime! so clearly co-prime to n - IRRELEVANT!
# Want e coprime to Phi!


#The Private Key (d, phi)
phi = (p-1)*(q-1) #Euler's Totient function of n

#Important check: e and phi must be coprime
# gcd(e,phi) == 1 # True
# So e is INVERTIBLE modulo phi:

d = modinv(e,phi)

#Check: (e*d)%phi == 1)



def word_to_num(wd):
    L = [str(ord(c)) for c in wd]
    return eval(''.join(L))

def num_to_word(num):
    ns = str(num)
    res = []

    while ns:
        res.append(ns[:2])
        ns = ns[2:]
    res = [eval(st) for st in res]
    to_letters = [chr(ordnum) for ordnum in res]
    
    return ''.join(to_letters)

def encrypt(word):
    # Your code goes here
    pass #this will change with your code

def decrypt(num):
    # Your code goes here
    pass


# Shell session of Test Case
if __name__ == '__main__':
    M0 = "HELLO"
    M = word_to_num(M0) #original, plaintext message.
##    >>> #Bob sends M to Alice after encrypting it with the Public Key (e,n)
##    >>> #(People other than Bob can do this too, as they know (e,n)
##    >>> #With probability very near 100%, M is coprime to n (99.99999995297281%)
##    
    #The encrypted message, transmitted through a public channel:
    print("Plaintext message:", M0)   

    E = pow(M,e,n) #284589552001883805621
    print("Encrypted message transmitted by Bob to Alice:\n",E)
    # Alice decrypts E using the private key d.
    # Private because only Alice (and her trusted friends) know p, or q (or phi!)

    D = pow(E,d,n) # 7269767679
    print("Message numerically  decrypted by Alice:",D)
    M_prime = num_to_word(D) #'HELLO'
    print("Decrypted message converted back to text:",M_prime)
    
        



