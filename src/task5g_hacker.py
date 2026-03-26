import json
import socket
from utils import solve_linear_congruence,get_gcd,efficient_pow
from secrets import randbelow

def run_hacker():

    with open("etc/intercepted_data.json", "r") as f:
        intercepted = json.load(f)

    n, y, t, b_list, c_list, d_list = intercepted

    #we find the first time the server asked for 0
    idx0 = c_list.index(0) 

    #the first time the server asked for 1
    idx1 = c_list.index(1) 

    #and now we know exactly which 'd' values to use
    a = d_list[idx0]
    ax = d_list[idx1]

    #we solve a*x = ax (mod n) 
    x_secret = solve_linear_congruence(a, ax, n)
    print(f"Extracted Secret x: {x_secret}")

    # Use extracted x to log in as the user
    hacker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hacker_sock.connect(('127.0.0.1', 8080))
    hacker_sock.recv(1024)
    hacker_sock.sendall(b"2")
    hacker_sock.sendall(y.to_bytes(512, "big"))
    
    t_rounds = int(hacker_sock.recv(1024).decode())

    for _ in range(t_rounds):
        #we can now behave like an honest client using x_secret
        while True:
            a_new=randbelow(n)
            if get_gcd(a,n)==1:
                break
        b =efficient_pow(a_new, 2, n)
        hacker_sock.sendall(b.to_bytes(512, "big"))
        c = int.from_bytes(hacker_sock.recv(1), "big")
        d = (a_new * (x_secret if c == 1 else 1)) % n
        hacker_sock.sendall(d.to_bytes(512, "big"))
        server_msg=hacker_sock.recv(1024).decode()

    if "Success" in server_msg: #we check only the response of the last iteration
        print(f"Final Result: Success (Secret extracted and verified!)")
            
    elif "Fail" in server_msg:
        print("Final Result: Fail")
            

if __name__ == "__main__":
    run_hacker()