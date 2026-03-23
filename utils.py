def extended_euclidean(a: int, b: int):
    # Ensure a is the larger number
    swapped = False
    if a < b:
        a, b = b, a
        swapped = True

    x_prev, x_curr = 1, 0
    y_prev, y_curr = 0, 1

    while b != 0:
        q = a // b
        r = a % b  # Standard Euclidean remainder is safer here
        
        x = x_prev - q * x_curr
        y = y_prev - q * y_curr
        
        a, b = b, r
        x_prev, x_curr = x_curr, x
        y_prev, y_curr = y_curr, y

    # If we swapped initially, we must return coefficients in correct order
    if swapped:
        return a, y_prev, x_prev
    return a, x_prev, y_prev


def get_gcd(a:int, b:int):
    if a<b:
        a, b = b, a

## ------------------- Accelerated standard -------------------
        while b!=0:
            q = a//b
            r = a-q*b #or r=a%b, but for the sake of clarity

            if abs(r-b)<abs(r):
                q=q+1
                r=r-b
           # print(f"{a} = {q}*{b} + {r}")
            a,b = b,abs(r)
        return a



def solve_linear_congruence(a, b, n):
    # gcd = (a, n) 
    gcd, x_inv, _ = extended_euclidean(a, n)

    #  d must divide b 
    if b % gcd != 0:
        raise ValueError("No solution exists because (a, n) does not divide b.")

    #Base solution x0 
    # Multiply the inverse by (b/gcd) and reduce mod (n/gcd) to keep it small
    n_prime = n // gcd
    x0 = (x_inv * (b // gcd)) % n_prime

    return x0

def efficient_pow(base, exponent, modulus):
    """ calculate base^exponent (mod modulus) efficiently,
    using the algorithm from our notes (2.11, 2.12).
    """
    if modulus == 1:
        return 0

    #property 7a from 2.3 : r_n[a] congruent to a, mod n.
    result = 1 #initializing with neutral element
    base = base % modulus #ensure base is small

    while exponent > 0: #iterate all bits, from LSB to MSB
        if exponent % 2 == 1: #if odd, current bit=1, multiply into result. otherwise do not.
            result = (result * base) % modulus
        exponent >>= 1 #shift 1bit to the right
        base = (base * base) % modulus #square the base, happens every iteration no matter what
    return result

def mod_inverse(a, m):
    '''return the mod inverse of a (mod m)'''
    
    gcd, x, y = extended_euclidean(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    
    return x % m #ensure smallest remainder in Zm

def solve_crt(list_xi, list_ni, total_n):
    '''we apply the CRT to find a unique solution for a system of
    linear congruences'''
    x = 0
    # Build the solution using the CRT summation formula
    for i in range(len(list_ni)):
        ni = list_ni[i]
        xi = list_xi[i]
        
        # Mi = n/ni
        Mi = total_n // ni
        yi = mod_inverse(Mi, ni)
        #yi = solve_linear_congruence(Mi, 1, ni) would also work here but okay
        
        #computation of the secret, we apply mod n to keep it efficient
        x = (x + xi * Mi * yi) % total_n
        
    return x