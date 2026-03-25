import socket
from secrets import randbelow
from hashlib import sha512
from utils import get_gcd

def get_x_from_pwd(password, n):
    password_bytes = password.encode()
    total_bytes = b"" #initial empty byte string, to accumulate the final bytes
    for i in range(8):
        i_bytes = i.to_bytes(4, "big") #convert i to 4 bytes
        total_bytes += sha512(i_bytes + password_bytes).digest() #concatenate and hash
    
    x = int.from_bytes(total_bytes, "big") #convert the final bytes to an integer
    return x % n

def recv_line(sock): #this is to prevent more than one recv() calls being gulped by one recv()
    data = b""
    while not data.endswith(b"\n"): #read each line until \n, this means that the server has to end everything in \n !!!
        data += sock.recv(1) #build "data" one byte at a time, until we hit the \n
    return data[:-1].decode() #throw out the \n, and decode


def run_client():
    n = None
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 8080))

    while True:
        prompt = recv_line(client_sock)
        print(prompt)
        choice = input("> ")
        client_sock.sendall(choice.encode())

        match choice:

            case '1': # Registration
                n_bytes = client_sock.recv(512)
                if n_bytes:
                    n=int.from_bytes(n_bytes,"big")

                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    
                    x = get_x_from_pwd(password, n) # Secret x 
                    y = ((x % n)*(x % n)) % n # Public y =r_n[x^2]
                    
                    #testing sending pair (username,y) as one, without using two separate sendall()
                    message = username.encode() + b"||" + y.to_bytes(512, "big")
                    client_sock.sendall(message)
                    print(recv_line(client_sock)) #receive Registered! 

            case '2': # Login
                if n is None:
                    print("Register first!")
                    msg_to_fail = b"0" + b"||" + (0).to_bytes(512, "big")
                    client_sock.sendall(msg_to_fail) # Dummy y to fail
                    continue
                
                username = input("Username: ")
                password = input("Password: ")

                x = get_x_from_pwd(password, n)
                y = ((x % n)*(x % n)) % n # Public y =r_n[x^2]
                
                #testing sending pair (username,y) as one, without using two separate sendall()
                message = username.encode() + b"||" + y.to_bytes(512, "big")
                client_sock.sendall(message)
                
                resp = recv_line(client_sock)
            
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
                
                    status = recv_line(client_sock)

                    if status == "Fail":
                        login_success = False
                        break
                    elif status == "Success":
                        print("Login Result: Success")
                        login_success = True
                        break
                    # else status == "Again", in which case we continue normally

            case '3':
                break

if __name__ == "__main__":
    run_client()