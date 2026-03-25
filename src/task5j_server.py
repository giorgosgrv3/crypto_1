import socket
import json
from secrets import randbits,randbelow
import utils 

def run_server():
    n = randbits(4096)  # 4096-bit modulus 
    t = 100             # Challenge repetitions 
    database = {}   # we now make it a dict, to store username -> y for the user 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen()
    print("Server listening on 127.0.0.1:8080...")

    while True:
        conn, addr = server_socket.accept()
        try:
            while True:
                conn.sendall(b"Please press 1 for Registration, 2 for Login or 3 for Exit:\n")
                choice = conn.recv(1).decode().strip()

                match choice:
                    case '1':
                        # send the modulus n. 
                        conn.sendall(n.to_bytes(512,"big")) # (4096 bits / 8 = 512 bytes)

                        message = conn.recv(2048)
                        username_bytes, y_bytes = message.split(b"||", 1)
                        username = username_bytes.decode().strip()
                        y = int.from_bytes(y_bytes, "big")

                        database[username] = y
                        print(f"Registered user {username} with valid y FOUND")
                        conn.sendall(b"Registered\n")

                    case '2':
                        message = conn.recv(2048)
                        username_bytes, y_bytes = message.split(b"||", 1)
                        username = username_bytes.decode().strip()
                        y = int.from_bytes(y_bytes, "big")
                        
                        if username not in database or database[username] != y:
                            conn.sendall(b"Fail\n")
                            continue
                        
                        conn.sendall(f"{t}\n".encode()) # Send number of challenges 
                    
                        success = True

                        for _ in range(t):
                            # Receive b from client
                            b_bytes = conn.recv(512)
                            if b_bytes:
                                b = int.from_bytes(b_bytes,"big")

                                # Send random challenge c 
                                c = randbelow(2) # c belongs to Z_2 so is either 0 or 1
                                conn.sendall(c.to_bytes(1,"big"))

                                # Receive d from client
                                d_bytes= conn.recv(512)
                                d = int.from_bytes(d_bytes,"big")
                        
                                # Verify: d^2 ≡ b * y^c (mod n) 
                                checking = ((d % n)*(d % n)) % n
                                target = (b * (y if c == 1 else 1)) % n

                                if checking != target: #if a challenge fails, send "Fail" and break
                                    conn.sendall(b"Fail\n")
                                    success = False
                                    break

                                if _ < t-1: #only send "Again" if it is NOT the last iteration of t
                                    conn.sendall(b"Again\n") 
                                else: # if it IS the last iteration of t, send "Success"
                                    conn.sendall(b"Success\n")
                    
                    case '3': 
                        break
                    
                    case _:
                        break

                
        except Exception as e:
            print(f"Connection closed: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    run_server()