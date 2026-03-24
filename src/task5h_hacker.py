import socket
import json
from secrets import randbelow

# 1. Load the stolen public info from the previous interception
with open("etc/intercepted_data.json", "r") as f:
    intercepted = json.load(f)

# We only need the public modulus n and the user's public key y
n = intercepted[0]
y = intercepted[1]
t = intercepted[2]
print(t)

# 2. Connect to the server to perform the unauthorized login
hacker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hacker_sock.connect(('127.0.0.1', 8080))

# 3. Navigate the menu to Login
prompt = hacker_sock.recv(1024).decode()
hacker_sock.sendall(b'2') # Select Login

# 4. Identify as the victim using the stolen 'y'
hacker_sock.sendall(y.to_bytes(512, "big"))
resp = hacker_sock.recv(1024).decode()

if resp != "Fail":
    print(f"Server accepted y. Starting {t} rounds of forged proof...")
    
    for i in range(t):
        # BYPASS LOGIC: We don't know x, so we pick a and b first.
        a = randbelow(n)
        b = (a * a) % n # b = r_n[a^2]
        
        # Send commitment
        hacker_sock.sendall(b.to_bytes(512, "big"))
        
        # Receive challenge (which we know will be c=0)
        c_bytes = hacker_sock.recv(1)
        
        # Respond with d=a. 
        # Since c=0, the server checks: d^2 == b * y^0 => a^2 == b.
        hacker_sock.sendall(a.to_bytes(512, "big"))
        
        status = hacker_sock.recv(1024).decode()
        if status == "Fail":
            print(f"Round {i} failed unexpectedly.")
            break

    final_result = hacker_sock.recv(1024).decode()
    print(f"Hacker Login Result: {final_result}")
else:
    print("Victim y not found in database.")

hacker_sock.close()