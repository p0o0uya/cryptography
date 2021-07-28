import secrets as sc

class modtools():

    def __init__(self):
        return None

    def halving(self, a, N):
        return (a*(N+1)//2)%N

    def isprime(self, a, k:int=20):
        # k is the number of random checks
        if a==2:
            return True
        if a==1 or a%2==0:
            return False
        c = a//2
        base = set((1, a-1))
        f    = base.copy()
        for pj in range(0, k):
            h = sc.randbelow(a-1)+1
            f.add(pow(h, c, a))
            f.add(pow(a-h, c, a))
            if not f==base:
                return False
        return True

    def isprime_a2(self, a):
        if a==2:
            return True
        if a==1 or a%2==0:
            return False
        r = sc.randbelow(a-1)+1
        if self.modinv(r, a)==self.modinvp(r, a):
            return True
        else:
            return False

    def modinv(self, a, p):
        # for general p
        lm, hm      = 1,0
        low, high   = a % p, p
        while low > 1:
            ratio   = high//low
            nm, new = hm-lm*ratio, high-low*ratio
            lm, low, hm, high = nm, new, lm, low
        return lm % p

    def modinvp(self, a, p):
        # for p prime
        return pow(a, p-2, p)

    def sqroot(self, a, p):
        if pow(a, (p - 1)//2, p) != 1:
            # print('{} is a quadratic non-residue modulo {}!'.format(a, p))
            return None
        s   = p - 1
        r   = 0
        while s%2==0:
            r += 1
            s //= 2
        #--------------------------------------#
        # finding the smallest quadratic non-residue
        n = 1
        while pow(n, (p - 1)//2, p) == 1:
            n += 1
        #--------------------------------------#
        m = pow(n, s, p)
        b = pow(a, s, p) # b has order dividing 2**(r - 1)
        u = 0
        while (pow(b, 2**u, p) != 1) & (u < r):
            u +=1
        x = pow(a, (s+1)//2, p)
        #--------------------------------------#
        # Starting the main loop
        while u != 0:
            b = (pow(m, 2**(r - u), p)*b)%p
            x = (pow(m, 2**(r - u - 1), p)*x)%p
            u = 0
            while (pow(b, 2**u, p) != 1) & (u < r):
                u +=1
        #--------------------------------------#
        # Final Check
        if pow(x, 2, p)==a:
            #print('proofed')
            return x
        else:
            print('something was wrong!')
            return None

    def rootdown(self, a, p):     
        k   = 0
        rtd = a
        while True:
            res = self.sqroot(rtd, p)
            if res:
                rtd = res
            else:
                print(k)
                break
            k += 1
            if k>1000:
                break
        return k

    def aretriplets(self, triplets, p):
        t1 = triplets[0]
        t2 = triplets[1]
        t3 = triplets[2]
        cond1 = (t1+t2+t3)%p==0
        cond2 = (t1*t2*t3)%p==pow(t1, 3, p)
        return cond1 & cond2  

    def sorter(self, T, base, p):
        if (not self.aretriplets(T, p)) | (not self.aretriplets(base, p)):
            print('T or base are not triplets!!')
            return None
        H    = [0]*3
        H[0] = (T[0]-base[0])%p
        H[1] = (T[1]-base[1])%p
        H[2] = (T[2]-base[2])%p
        if self.aretriplets(H, p):
            return T
        H    = [0]*3
        H[0] = (T[0]-base[0])%p
        H[1] = (T[2]-base[1])%p
        H[2] = (T[1]-base[2])%p
        if self.aretriplets(H, p):
            return [T[0], T[2], T[1]]
        print('Something Went Wrong')
        

    def theo2(self, x1, p):   #the other two of a triplet
        x1 = x1%p
        if x1%p==0:
            return None, 0

        w = pow(x1, 3, p)
        if pow(x1, 3, p)!=w:
            print("x1 is not a valid root of w!")
            return None, None
        a    = 1
        b    = x1
        c    = (self.modinvp(x1, p)*w)%p
        dlta = (pow(b, 2, p)-4*a*c)%p
        #eps  = pow(dlta, (p+1)//4, p)
        if dlta==0:
            print(x1)
            print(w)
        eps  = self.sqroot(dlta, p)
        x2   = (-b + eps)*self.modinvp(2*a%p, p)%p
        x3   = (-b - eps)*self.modinvp(2*a%p, p)%p
        #print("unofficial", x2, x3)
        T = [x1, x2, x3]
        if self.aretriplets(T, p):
            return T, sum(T)//p
        else:
            print("w is probably not a valid cube!")
            return None

if __name__ == "__main__":
    inst = modtools()
    print(inst.halving(7, 19))
    print(inst.isprime(37))
    for pj in range(1, 100):
        print(pj, inst.isprime(pj))
    print(inst.modinv(4, 17))
    print(inst.modinvp(4, 17))
    # p = 19
    # print(p%4)
    # for pj in range(1, p):
    #     print(pj, sqroot(pj, p))
    # P  = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    # N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    # print(N%4, P%4)
