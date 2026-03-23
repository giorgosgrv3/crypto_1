from secrets import randbelow, randbits
from Crypto.Util.number import getPrime
from utils import efficient_pow

L=20 #distinct authentication servers
'''p_list and n_list are used to build the canonical form'''
p_list=[] #contains the primes
n_list=[] # contains the primes to the power of k = each n_i
coeff_list=[] #contains the coefficients n_{i-1}^n (mod ni)

while(len(p_list))<L:
    p=getPrime(256) #get random 256bit prime
    if p not in p_list:
        p_list.append(p)
        k = randbelow(10)+1 #random exponent
        n_list.append(p**k)
        print(f"generated prime #{len(p_list)}")
print("-----------------")

n=1 #initialize n with neutral element (1)
for ni in n_list:
    n=n*ni

# ----- generate secret x ------
x_true = randbelow(n)
print("generated secret x")
print("-----------------")
# ------ what each server stores ------ 
# each server stores r_ni[n_{i-1}^n * x]

print("letting servers know their parts of the secret")
server_content=[]
for i in range(L):
    #get n_i and n_{i-1}
    ni = n_list[i]
    n_prev = n_list[i-1]

    # compute n_{i-1}^n (mod ni) efficiently
    n_prev_n = efficient_pow(n_prev,n,ni)
    coeff_list.append(n_prev_n)

    # compute n_{i-1}^n * x (mod ni)
    x_mod_ni = x_true%ni #property r_n[ab] = r_n[r_n[a]r_n[b]] for faster computation
    si = (n_prev_n * x_mod_ni) % ni
    server_content.append(si)

print("done with the servers")
print("-----------------")

# --------  party authentication process ---------
def auth_party(claimed_x, server_content_list, n_list, coeff_list):
    for i in range(L): #check with each server
        ni = n_list[i]
        n_prev = n_list[i-1]

        n_prev_n = coeff_list[i] #we have already computed this above, no need to compute again
        claimed_x_mod_ni = claimed_x % ni #property r_n[ab] = r_n[r_n[a]r_n[b]] aaagain
        si_claimed = (n_prev_n * claimed_x_mod_ni) % ni #calculate s_i with the CLAIMED x

        if si_claimed != server_content_list[i]:
            return False, i #auth failed at server i
        print(f"Server {i} accepted")
    return True, None # success for all servers

#testing CORRECT secret
print("\n --- Testing authentication with CORRECT secret ----")
success, fail_index = auth_party(x_true, server_content, n_list, coeff_list)
if success:
    print("ACCEPTED")
else:
    print(f"REJECTED at server {fail_index}")


# testing WRONG secret
print("\n --- Testing authentication with WRONG secret ----")
x_wrong = randbelow(n)
while x_wrong == x_true:
    x_wrong = randbelow(n)

success, fail_index = auth_party(x_wrong, server_content, n_list, coeff_list)

if success:
    print("ACCEPTED")
else:
    print(f"REJECTED at server {fail_index}")
    