from modtools import modtools, sc

class secp256k1(modtools):
        
    P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1                  # The proven prime
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141    # Number of points in the field also prime
    Acurve = 0; Bcurve = 7                       # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
    Gx     = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Gy     = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    GPoint = (Gx,Gy)                             # This is our generator point. Trillions of dif ones possible

    def __init__(self):
        return None

    # Not true addition, invented for EC. Could have been called anything. This adds P and Q that are P=(xp, yp), Q=(xq,yq)
    def adding(self, xp, yp, xq:int=Gx, yq:int=Gy): 
        m  = ((yq-yp)*self.modinv(xq-xp,self.P))%self.P
        xr = (m*m-xp-xq) % self.P
        yr = (m*(xp-xr)-yp) % self.P
        return (xr, yr)

    # This is called point doubling, also invented for EC.
    def doubling(self, xp, yp):
        mNumer = 3*xp*xp+self.Acurve
        mDenum = 2*yp
        m      = (mNumer * self.modinv(mDenum,self.P)) % self.P
        xr     = (m*m-2*xp) % self.P
        yr     = (m*(xp-xr)-yp) % self.P
        return (xr, yr)

    def ecc(self, intg, xs:int=Gx, ys:int=Gy): # Double & add. Not true multiplication
        #if intg == 0 or intg >= N: raise Exception("Invalid SECP256K1 Private Key")
        bin_   = bin(intg)[2:]
        Qx, Qy = xs, ys
        for i in range (1, len(bin_)):
            Qx, Qy=self.doubling(Qx, Qy)
            if bin_[i] == '1':
                Qx, Qy = self.adding(Qx, Qy, xs, ys)
        return (Qx, Qy)

    def maskhalving(self, x, y):
        h = ecc((N+1)//2, x, y)
        return h


if __name__ == "__main__":
    inst = secp256k1()
    print(inst.ecc(1))
    Pi = inst.P + 2
    k = 0
    while True:
        if inst.isprime(Pi):
            k += 1
            print(Pi)
            print(Pi - inst.P)
            print(k)
            if not inst.isprime_a2(Pi):
                print("Coudn't double check!")
            # break
        Pi += 2


