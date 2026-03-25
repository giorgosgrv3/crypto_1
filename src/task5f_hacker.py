import json
import socket
from secrets import randbelow
from utils import efficient_pow,get_gcd


def run_hacker():

    with open("etc/intercepted_data.json", "r") as f:
        intercepted = json.load(f)

    n, y, t, b_list, c_list, d_list = intercepted

    attempts = 0
    while True:
        attempts += 1
        hacker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hacker_sock.connect(('127.0.0.1', 8080))

        hacker_sock.recv(1024)

        hacker_sock.sendall(b"2") # Login
        hacker_sock.sendall(y.to_bytes(512, "big"))
        
        t = int(hacker_sock.recv(1024).decode())
        impersonation_success = True
        
        for _ in range(t):

            #guess c=0, send b=a^2 % n
            while True:
                a=randbelow(n)
                if get_gcd(a,n)==1:
                    break
            b = efficient_pow(a, 2, n)
            hacker_sock.sendall(b.to_bytes(512, "big"))
            
            c_actual = int.from_bytes(hacker_sock.recv(1), "big")

            if c_actual == 0:
                # here, since c=0 then d=r_n(ax^c) is just a % n = a since a is co prime with n
                hacker_sock.sendall(a.to_bytes(512, "big"))
                hacker_sock.recv(1024) # "Again"

            else:
                # Guess failed, send dummy d and retry login 
                hacker_sock.sendall(b"\x00" * 512)
                impersonation_success = False
                break
        
        if impersonation_success:
            print(f"Success! Unauthorized access gained after {attempts} attempts.")
            break
        

if __name__ == "__main__":
    run_hacker()