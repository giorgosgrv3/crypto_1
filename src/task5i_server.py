import socket
from secrets import randbits,randbelow
import utils 

def run_server():
    n = randbits(4096)  # 4096-bit modulus 
    t = 100             # Challenge repetitions 
    database = set()    # Stores registered 'y' values 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen()
    print("Server listening on 127.0.0.1:8080...")

    while True:
        conn, addr = server_socket.accept()
        try:
            while True:
                conn.sendall(b"\nPlease press 1 for Registration, 2 for Login or 3 for Exit: ")
                choice = conn.recv(1).decode().strip()

                match choice:
                    case '1':
                        # send the modulus n. 
                        conn.sendall(n.to_bytes(512,"big")) # (4096 bits / 8 = 512 bytes)
                        y_bytes = conn.recv(512) 
                        if y_bytes:
                            y = int.from_bytes(y_bytes, "big") # recv returns bytes, so we pass it directly to from_bytes
                            database.add(y) #store y to db
                            print(database)
                            conn.sendall(b"Registered") 
                    case '2':
                        y_bytes = conn.recv(512)
                        if y_bytes:
                            y = int.from_bytes(y_bytes, "big")
                            if y not in database:
                                conn.sendall(b"Fail")
                                continue
                        
                            conn.sendall(str(t).encode()) # Send number of challenges 
                    
                            success = True
                            for _ in range(t):

                                # Receive b from client
                                b_bytes = conn.recv(512)
                                if b_bytes:
                                    b = int.from_bytes(b_bytes,"big")

                                    # Send random challenge c 
                                    c = 1 # -- this is theee ONLY difference from (5h) server
                                    conn.sendall(c.to_bytes(1,"big"))


                                # Receive d from client
                                d_bytes= conn.recv(512)
                                d = int.from_bytes(d_bytes,"big")
                        
                                # Verify: d^2 ≡ b * y^c (mod n) 
                                checking = ((d % n)*(d % n)) % n
                                target = (b * (y if c == 1 else 1)) % n

                                if checking != target: #if a challenge fails, send "Fail" and break
                                    conn.sendall(b"Fail")
                                    success = False
                                    break

                                if _ < t-1: #only send "Again" if it is NOT the last iteration of t
                                    conn.sendall(b"Again") 
                                else: # if it IS the last iteration of t, send "Success"
                                    conn.sendall(b"Success")
                                        
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