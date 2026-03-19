from secrets import randbelow , randbits
from utils import extended_euclidean,solve_linear_congruence,get_gcd


def keygen(M):

    Zm = range(M)
    Tm =[]

    for i in Zm:
        gcd,_,_=extended_euclidean(i,M)
        if gcd == 1:
            Tm.append(i)

    idx = randbelow(len(Tm)) #take a random index of Tm
    k = Tm[idx] #now we have a k picked from the co-primes of M

    coin1 = randbelow(2) #takes values 0 or 1
    coin2 = randbelow(2)

    if coin1 == 0:
        a=randbelow(M)
        d=randbelow(M)
        if coin2 == 0:
            while True:
                b=randbelow(M)
                #2.3.2 
                if (a*d-k) % get_gcd(b,M) == 0: 
                    c =solve_linear_congruence(b,(a*d-k),M)
                    break
        else:
            while True:
                c=randbelow(M)
                if   (a*d-k) % get_gcd(c,M) == 0:
                    b =solve_linear_congruence(c,(a*d-k),M)
                    break   


    else:
        b=randbelow(M)
        c=randbelow(M)
        if coin2 == 0:
            while True:
                a=randbelow(M)
                if  (k + b*c) % get_gcd(a,M) == 0:
                    d =solve_linear_congruence(a,(k + b*c),M)
                    break
        else:
            while True:
                d=randbelow(M)
                if  (k + b*c) % get_gcd(d,M) == 0:
                    a =solve_linear_congruence(d,(k + b*c),M)
                    break   
   
    return a,b,c,d

def encrypt(m1,m2,keys,M):

    a,b,c,d = keys
    r1=(a*m1+b*m2) % M
    r2=(c*m1+d*m2) % M

    return r1,r2

def decrypt(r1,r2,keys,M):

    a,b,c,d = keys
    k=(a*d)-(b*c)

    t=solve_linear_congruence(k,1,M)

    m1_hat = ((d*r1-b*r2)*t) % M
    m2_hat = ((a*r2-c*r1)*t) % M

    return m1_hat,m2_hat

if __name__ == "__main__":
    M=11
    keys=keygen(M)
    print(keys)
    r1,r2 = encrypt(1,2,keys,M)
    m1,m2 = decrypt(r1,r2,keys,M)

    print(m1)
    print(m2)