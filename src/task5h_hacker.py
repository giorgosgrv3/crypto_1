import socket
import json
from secrets import randbelow
from utils import get_gcd

with open("etc/intercepted_data.json", "r") as f:
    intercepted = json.load(f)

n = intercepted[0]
y = intercepted[1]

hacker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hacker_sock.connect(('127.0.0.1', 8080))

#prompt sent from server, receive it
prompt = hacker_sock.recv(1024).decode()
print(f"{prompt}\n")
print(" -- automatically choosing '2' - Login")
hacker_sock.sendall(b"2")

# present the intercepted y, from the client that ran right before
hacker_sock.sendall(y.to_bytes(512, "big"))
resp = hacker_sock.recv(1024).decode()
if resp != "Fail":
    t = int(resp)
    print(f"-- server accepted the intercepted y. starting {t} rounds of challenges")

    for i in range(t):
        while True:
            a = randbelow(n)
            if get_gcd(a,n)==1:
                break
        b = ((a%n) * (a%n)) % n

        hacker_sock.sendall(b.to_bytes(512, "big"))
        c_bytes = hacker_sock.recv(1)  
        hacker_sock.sendall(a.to_bytes(512, "big"))

        status = hacker_sock.recv(1024).decode()

        if status == "Fail":
            print(f"round {i+1} failed (this shouldn't have happened)")
            break
        elif status == "Success":
            print("-- we have logged in as the user.\n")
            print("Hello, friend. Hello, friend? That's lame. Maybe I should give you a name. But that's a slippery slope. You're only in my head. ")
            break
else:
    print("Server didn't find the y. (run client again)")