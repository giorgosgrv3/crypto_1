from secrets import randbelow, randbits
from Crypto.Util.number import getPrime
from utils import *


''' ---- SAME AS 4b FOR NOW, ATTACK BELOW --- '''


L=20
#p_list, n_list to build the canon form
p_list=[] #contains the primes
n_list=[] # contains the primes to the power of k = each n_i
coeff_list=[] #contains the coefficients n_{i-1}^n (mod ni)

while(len(p_list))<L:
    p=getPrime(256) #random 256bit prime
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


''' ---------- IMPLEMENTATION OF THE ATTACK (4c) ---------- '''
print("\n\n -- Initiating the attack --")

#we said that each server holds s_i = r_ni[n_{i-1}^n * x]
# therefore the attacker solves s_i congr n_{i-1}^n * x (mod n_i) for each server i
recovered_xi = []

for i in range(L):
    #now solve for x_i congr x (mod n_i)
    xi = solve_linear_congruence(coeff_list[i],server_content[i],n_list[i]) # n_{i-1}^n*x congr s_i (mod n_i)
    recovered_xi.append(xi)

#now we have a system of congruences, we use CRT to find x
x_reconstructed = solve_crt(recovered_xi, n_list, n)
    
# VERIFYYYY
if x_reconstructed == x_true:
    print("Reconstructed secret x MATCHES the original secret x")
else:
    print("Reconstructed secret x DOES NOT MATCH the original x")