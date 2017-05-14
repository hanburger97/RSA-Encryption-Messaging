#1. Extended gcd
#2. Modular inverse, if it exists
#3. Extras: Coprime list, Euler's Totient function Phi

## NOTE. Python's builtin  pow(x,n,m) is better (faster) than 'pow(x,n) % m' BUT:
### requires n >=0

def gcd(a,b):
    """Returns the greatest common divisor of a,b
    using the classic Euclidean Algorithm"""
    
    while b != 0:
        a,b = b, a%b
    return a

#Iterative Extended GCD algorithm
def egcd(a, b):
     """Returns a triple (d, x, y), such that
     ax + by = d = gcd(a, b)
     """
    #Initialize
     x,y, u,v = 1,0, 0,1 #now four simultaneous assignments
     
     while b != 0:
        q = a//b
        m, n = x-u*q, y-v*q
        x,y, u,v = u,v, m,n
        a,b = b, a%b
        
     gcd = a 
     return gcd, x, y
        
def modinv(a, m): 
    gcd, x, y = egcd(a, m) 
    if gcd != 1:
        print(a,'not invertible mod',m)
        print('Please generate another key pair')
        return None # modular inverse does not exist 
    else: 
        return x % m



# **** Extras ***
def coprime (a,b):
    return gcd(a,b) == 1

def coprime_list(n):
    ans = [k for k in range(1,n) if coprime(k,n)]
    return ans

# Euler's "totient" function Greek-Phi uppercase:
# (Brute force, inefficient for large n)

# Efficient sol in special case(by Math/Number_Theory):
## 1. if n = prime number p, then phi(n) = p-1
## 2. if n = p*q with p, q primes, then phi(n) = (p-1)*(q-1)
##  Case 2. is used in CRYPTOGRAPHY, RSA Encryption/Decryption.
### (GOOD Project Topic!)

def Phi(n):
    """Euler's Totient function:
    The number of integers between 1 and n-1 which are
    coprime with n """
    
    return len(coprime_list(n))

def isPrime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True

    # Testing

if __name__ == '__main__':
    n = 2017 #Edit at will 
    print("Phi(",n,") = ",Phi(n),sep = "")
    print('*'*10+'\n')

    n = 15 #Change this at will for your own test runs
    
    L = coprime_list(n)
    print("Coprime list of {} = ".format(n))
    print(L,'\n')
    print("Phi({}) = {}".format(n,len(L)),'\n')
    
    # Modular Multiplication table  in L
    print("\tMultiplication table mod {0} in Coprime list of {0} ".format(n))
    print('\t'+'-'*60)
    
    for a in L:
        print("\t{:>3}|".format(a), end = ' ')
        for b in L:
            print("{:>3}".format((a*b)% n), end=' ')
        print()

    
 


