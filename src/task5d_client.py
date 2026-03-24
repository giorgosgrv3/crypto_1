import socket
from secrets import randbelow
from utils import get_gcd

def run_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 8080))
    
    # Storage for user triple
    x, y, n = None, None, None
    

    while True:
        prompt = client_sock.recv(1024).decode()
        print("\n",prompt)
        choice = input("> ")
        client_sock.sendall(choice.encode())

        match choice:

            case '1': # Registration
                n_bytes = client_sock.recv(4096)
                if n_bytes:
                    n=int.from_bytes(n_bytes,"big")
                    x = randbelow(n) # Secret x 
                    y = ((x % n)*(x % n)) % n # Public y =r_n[x^2]
                    client_sock.sendall(y.to_bytes(512,"big"))
                    print(client_sock.recv(1024).decode()) #receive Registered! 

            case '2': # Login
                if x is None:
                    print("Register first!")
                    client_sock.sendall(b"0") # Dummy y to fail
                    continue
                
                client_sock.sendall(y.to_bytes(512,"big"))
                resp = client_sock.recv(1024).decode()
            
                if resp == "Fail":
                    print("Login Failed at start.")
                    continue
            
                t = int(resp)
                login_success = True
                for _ in range(t):
                    while True:
                        a=randbelow(n)
                        if get_gcd(a,n)==1:
                            break
                    b =  ((a % n)*(a % n)) % n #b =r_n[a^2]
                    client_sock.sendall(b.to_bytes(512,"big"))
                
                    # 2. Receive challenge c 
                    c_bytes = client_sock.recv(1)
                    c = int.from_bytes(c_bytes,"big")
                
                    # 3. Compute d = a * x^c (mod n) 
                    d = (a * (x if c == 1 else 1)) % n
                    client_sock.sendall(d.to_bytes(512,"big"))
                
                    status = client_sock.recv(1024).decode()
                    if status == "Fail":
                        login_success = False
                        break
            
                final_status = client_sock.recv(1024).decode()
                print(f"Login Result: {final_status}")

            case '3':
                break

if __name__ == "__main__":
    run_client()