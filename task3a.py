from secrets import randbelow , randbits
from utils import extended_euclidean


def keygen(M):
    a=randbelow(M)
    b=randbelow(M)
    c=randbelow(M)
    d=randbelow(M)
    return a,b,c,d

def encrypt(m1,m2,keys,M):

    a,b,c,d = keys
    r1=(a*m1+b*m2) % M
    r2=(c*m1+d*m2) % M

    return r1,r2

def decrypt(r1,r2,keys,M):

    a,b,c,d = keys
    det=(a*d)-(b*c)
    gcd,t,y = extended_euclidean(det,M)

    print(f"gcd =",gcd)
    print(f"x=",t)
    print(f"y=",y)
    

    m1_hat = ((d*r1-b*r2)*t) % M
    m2_hat = ((a*r2-c*r1)*t) % M

    return m1_hat,m2_hat

if __name__ == "__main__":
    M=15
    m1=10
    m2=12
    keys=keygen(M)
    r1,r2 = encrypt(m1,m2,keys,M)
    m1_hat,m2_hat = decrypt(r1,r2,keys,M)

    print(f"Original messages:",m1," ",m2)
    print(f"Encrypted messages:",r1," ",r2)
    print(f"Decrypted messages:",m1_hat," ",m2_hat)