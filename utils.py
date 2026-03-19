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