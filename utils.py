def extended_euclidean(a:int, b:int):
        if a<b:
            a, b = b, a

        x_prev, x_curr = 1, 0
        y_prev, y_curr = 0, 1

        while b!=0:
            q = a//b
            r = a-q*b

            if abs(r-b)<abs(r):
                q=q+1
                r=r-b

            #print(f"{a} = {q}*{b} + {r}")

            x = x_prev-q*x_curr
            y = y_prev-q*y_curr

            if r<0: #this is to handle a sign inconsistency in case that the negative remainder is selected
                x=-x
                y=-y
            
            a, b = b, abs(r)

            x_prev, x_curr = x_curr, x
            y_prev, y_curr = y_curr, y

        return a, x_prev, y_prev