def euclidean(a:int, b:int, decision:int):
    swapped = False #this variable is used only for the extended algorithm
    if a<b:
        a, b = b, a
        swapped = True
    
## ------------------- Simple euclidean -------------------
    # it isn't asked, but we did it to compare the printf's anyway
    if decision==0:
        while b!=0:
            q = a//b
            r = a-q*b
            print(f"{a} = {q}*{b} + {r}")
            a = b
            b = r
        return a

## ------------------- Accelerated standard -------------------
    elif decision==1:
        while b!=0:
            q = a//b
            r = a-q*b #or r=a%b, but for the sake of clarity

            if abs(r-b)<abs(r):
                q=q+1
                r=r-b
            print(f"{a} = {q}*{b} + {r}")
            a,b = b,abs(r)
        return a

## ------------------- Accelerated extended -------------------
    elif decision == 2:

        x_prev, x_curr = 1, 0
        y_prev, y_curr = 0, 1

        while b!=0:
            q = a//b
            r = a-q*b

            if abs(r-b)<abs(r):
                q=q+1
                r=r-b

            print(f"{a} = {q}*{b} + {r}")

            #from here on is the extended part, hopefully explained nicely in the report :)
            x = x_prev-q*x_curr
            y = y_prev-q*y_curr

            if r<0: #this is to handle a sign inconsistency in case that the negative remainder is selected
                x=-x
                y=-y
            
            a, b = b, abs(r)

            x_prev, x_curr = x_curr, x
            y_prev, y_curr = y_curr, y

        if swapped:
            return a, y_prev, x_prev
        return a, x_prev, y_prev
        

if __name__ == "__main__":
    print(" -------- Accelerated Euclidean Algorithm ---------")
    print("Provide two numbers, and then choose Extended or Standard mode for the algorithm \n (and don't be cheeky with the input, edge cases aren't handled :) )")
    a = int(input("a = "))
    b = int(input("b = "))

    print("\nNow choose\n0 for simple euclidean\n1 for accelerated standard\n2 for accelerated extended")
    decision = int(input("Selection: "))
    print("\n")

    if decision not in [0,1,2]:
        print("you are purposely trying to make me crash :(")
        exit()
    else:
        result = euclidean(a,b,decision)

        if decision == 2:
            gcd, x, y = result
            print(f"\n({a},{b}) = {gcd}")
            print(f"coefficients x = {x}, y = {y}")
            print(f"linear combination : {gcd} = {x}*{a} + {y}*{b}")
        else:
            print(f"({a},{b}) = {result}")

