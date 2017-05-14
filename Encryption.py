import random

from NumTheoryBasics import modinv, isPrime

LPRIMES = [i for i in range(1000, 2018) if isPrime(i)]
SPRIMES = [i for i in range(214748364,214749364) if isPrime(i)] #global pool of primes

def smallPrimeGenerator():
     return random.choice(LPRIMES) #randomly selects a prime


def largePrimeGenerator():
    return random.choice(SPRIMES)

def cypher(z): #Either transform text to its ordinals or number to character
    if type(z) is str:
        z = z.upper()
        L = [str(ord(c)) for c in z]
        joined = ''.join(L)
        ev = eval(joined)
        return ev
    elif type(z) is int:
        ns = str(z)
        res = []
        while ns:
            res.append(ns[:2])
            ns = ns[2:]
        res = [eval(st) for st in res]
        to_letters = [chr(ordnum) for ordnum in res]

        return ''.join(to_letters)

class User(object):
    def __init__(self, name):
        self.name = name

        #self.generateKeyPairs()
        self.__publicKey = None
        self.__n = None
        self.__e = None
        self.__phi = None
        self.__d = None
        self.__n = None

    def __dict__(self):#prevent user from peaking into other instance's private attributes
        print('You are not authorized to see this')
        return None

    def generateKeyPairs(self): #generates a public and private keys
        self.__publicKey = self.__genPublicKey()
        self.__privateKey = self.__genPrivateKey()
        print(self.publicKey)

    def __genPrivateKey(self):
        if not self.__phi: #generated in previous step to conceal p and q
            print('Ooops there was an error please try again')
        self.__d = modinv(self.__e, self.__phi) #since (e*d)mod phi = 1; d = modinv(e,phi)
        return {'d':self.__d, 'phi':self.__phi}

    def __genPublicKey(self):
        #In order to conceal p and q, we use local scope only
        p, q = largePrimeGenerator(), largePrimeGenerator()
        self.__phi = (p-1) * (q-1) # by Euler's Totien Function
        self.__n = p * q
        self.__e = smallPrimeGenerator()
        return {'e': self.__e, 'n': self.__n}

    @property #returns a getter for private attribute public key
    def publicKey(self):
        return self.__publicKey


    def sendMessage(self, other, msg):
        try:
            assert type(msg) is str #making sure the msg input is string
            if not(self.publicKey and other.publicKey) :
                raise NoKey('Either your own key or your recipient key is missing, please run user.generateKeyPairs()')

            res = []
            while msg:
                word = msg[:5]
                res.append(self.encrypt(other, word))
                msg = msg[5:]
            return res

        except AssertionError:
            print('Your input type must be string')

    def receiveMessage(self, other, C):
        try:
            assert type(C) is list#making sure the encrypted input is an array of numbers
            res = []
            for c in C:
                res.append(self.decrypt(other, c))
            outp = ''.join(res)
            print("Decrypted message: {} //End of message with signature from {}".format(outp, other.name))

        except AssertionError:
            print('Make sure your input is correct or that you have used user.sendMessage(recipient, message) correctly')


    def encrypt(self, other,word):
        try:
            assert type(other) == User
            if len(word) > 5:
                print('You can only encrypt maximum 5 string characters at once')
                return None
            M = cypher(word)
            k2 = other.publicKey
            k1 = self.publicKey
            n2 = k2['n']
            e2 = k2['e']
            n1 = k1['n']
            if ( n1 < n2):#check cases because not perfect symmetry with signature RSA
                S1 = pow(M, self.__privateKey['d'], n1)
                C1 = pow(S1, e2, n2)
                return C1
            elif( n2 < n1):
                S1 = pow(M, e2, n2)
                C1 = pow(S1, self.__privateKey['d'], n1)
                return C1
            elif(n1 == n2):
                print('Please generate another key pair, this one is deprecated')
                return None
        except AssertionError:
            raise RecipientNotUser("the recipient must an User, try declaring using newUser = User('userName')")

    def decrypt(self, other, C):
        try:
            assert type(other) == User
            k2 = other.publicKey
            k1 = self.publicKey
            n2 = k2['n']
            e2 = k2['e']
            n1 = k1['n']
            if (n1 > n2): #Need to change sign since we flipped U1 and U2 (always in terms of U1 POV)
                S = pow(C, self.__privateKey['d'], n1)
                M = pow(S, e2, n2)
                return cypher(M)
            elif(n1 < n2):
                S = pow(C, e2, n2)
                M = pow(S, self.__privateKey['d'], n1)
                return cypher(M)
        except AssertionError:
            raise RecipientNotUser("Your first argument should be the sender who must an User, try declaring using newUser = User('userName')")

class NoKey(Exception):
    def __init__(self, message):
        super().__init__(message)

class RecipientNotUser(Exception):
    def __init__(self, message):
        super().__init__(message)

if __name__ == '__main__':
    a = User('Alice')
    b = User('Bob')
    a.generateKeyPairs()
    b.generateKeyPairs()
    y = b.sendMessage(a,'Hey there i hope you are doing well Lorem Ipsum Porem')
    z = a.sendMessage(b,'Herro')
    a.receiveMessage(b, y)
    b.receiveMessage(a, z)
