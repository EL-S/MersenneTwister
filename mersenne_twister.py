def lowest_w_bits(a):
    mask = (1 << 64)-1

    b = bin(a & mask)
    return int(b, 2)

class random:
    w = 64
    n = 312
    m = 156
    r = 31
    a = 0xB5026F5AA96619E9
    u = 29
    d = 0x5555555555555555
    s = 17
    b = 0x71D67FFFEDA60000
    t = 37
    c = 0xFFF7EEE000000000
    l = 43
    index = n
    f = 6364136223846793005
    lower_mask = (1 << r) - 1
    upper_mask = lowest_w_bits(~lower_mask)


    def __init__(self, seed):
        self.state = [0] * random.n
        self.seed_mt(seed)
        
    def seed_mt(self, seed):
        self.index = random.n
        self.state[0] = seed
        for i in range(1,random.n):
            first_section = self.state[i-1] >> (random.w-2)
            second_section = self.state[i-1]
            third_section = random.f * (second_section ^ first_section)
            fourth_section = third_section + i
            
            self.state[i] = lowest_w_bits(fourth_section)

    def extract_number(self):
        if self.index >= random.n:
            if self.index > random.n:
                seed = 5489
                self.seed_mt(seed)
            self.twist()

        y = self.state[self.index]
        y = y ^ ((y >> random.u) & random.d)
        y = y ^ ((y << random.s) & random.b)
        y = y ^ ((y << random.t) & random.c)
        y = y ^ (y >> random.l) # L not 1

        self.index = self.index + 1
        return lowest_w_bits(y)

    def twist(self):
        for i in range(0,random.n):
            x = (self.state[i] & random.upper_mask) + (self.state[(i+1) % random.n] & random.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ random.a
            self.state[i] = self.state[(i+random.m) % random.n] ^ xA
        self.index = 0

object_r = random(0)

while True:
    number = object_r.extract_number()
    print(number/((2**64)-1))
