import socket
import json

with open("etc/intercepted_data.json", "r") as f:
    intercepted = json.load(f)

n = intercepted[0]
y = intercepted[1]
b_list = intercepted[3]
c_list = intercepted[4]
d_list = intercepted[5]

# this is where the entire attack relies:
# the attacker wants to find a single pair of (b,d) where c=1, and use it for ALL t challenges
replayed_b = None
replayed_d = None

for b, c, d in zip(b_list, c_list, d_list):
    if c == 1:
        replayed_b = b
        replayed_d = d
        print(" -- a valid (b,d) pair where c=1 was found (he's cooked)")
        break

hacker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hacker_sock.connect(('127.0.0.1', 8080))

# receive prompt from sevrer
prompt = hacker_sock.recv(1024).decode()
print(f"{prompt}\n")
print(" -- automatically choosing '2' - Login")
hacker_sock.sendall(b"2")

# present the intercepted y
hacker_sock.sendall(y.to_bytes(512, "big"))
resp = hacker_sock.recv(1024).decode()

if resp != "Fail":
    t = int(resp)
    print(f"-- server accepted the intercepted y. starting {t} rounds of challenges")

    for i in range(t):
        # Replay the same valid pair every round
        hacker_sock.sendall(replayed_b.to_bytes(512, "big"))

        c_bytes = hacker_sock.recv(1)
        c = int.from_bytes(c_bytes, "big")

        hacker_sock.sendall(replayed_d.to_bytes(512, "big"))

        status = hacker_sock.recv(1024).decode()

        if status == "Fail":
            print(f"round {i+1} failed. (this shouldnt have happened)")
            break
        elif status == "Again":
            print(f"round {i+1} successful")
        elif status == "Success":
            print("-- we have logged in as the user.\n")
            print("Hello, friend. Hello, friend? That's lame. Maybe I should give you a name. But that's a slippery slope. You're only in my head.")
            break
else:
    print("Server didn't find the y. (run client again)")