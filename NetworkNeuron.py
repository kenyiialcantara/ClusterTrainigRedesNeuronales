
import random
import math

class RNA:

    def __init__(self, ci_, co_, cs_):
        self.ci = ci_
        self.co = co_
        self.cs = cs_
        self.rand = random.Random()
        
        self.xin = []  
        self.xout = []  
        
        self.y = []
        self.s = []
        self.g = []
        self.w = []
        self.c = [0, 0, 0]  # capas de datos
        
        self.c[0] = self.ci
        self.c[1] = self.co
        self.c[2] = self.cs
        
        for _ in range(self.co + self.cs):
            self.y.append(0)
            self.s.append(0)
            self.g.append(0)
            
        for _ in range(self.ci * self.co + self.co * self.cs):
            self.w.append(self.get_random())
    
    def get_random(self):
        return self.rand.random() * 2 - 1  # [-1;1[
    
    def fun(self, d):
        return 1 / (1 + math.exp(-d))
    
    def print_x_ingreso(self):
        for i in range(len(self.xin)):
            for j in range(len(self.xin[i])):
                print("xingreso[{}, {}]={}".format(i, j, self.xin[i][j]))
        print()
    
    def print_x_y_salida(self):
        for i in range(len(self.xout)):
            for j in range(len(self.xout[i])):
                print("xsalida[{}, {}]={}".format(i, j, self.xout[i][j]))
    
    def print_y(self):
        for i in range(len(self.y)):
            print("y[{}]={}".format(i, self.y[i]))
    
    def print_w(self):
        for i in range(len(self.w)):
            print("w[{}]={}".format(i, self.w[i]))
    
    def prints(self):
        for i in range(len(self.s)):
            print("s[{}]={}".format(i, self.s[i]))
    
    def print_g(self):
        for i in range(len(self.g)):
            print("g[{}]={}".format(i, self.g[i]))
    
    def entrenamiento(self, inp, sal, veces):
        self.xin = inp
        self.xout = sal
        
        for _ in range(veces):
            for i in range(len(self.xin)):
                self.entreno(i)
        return self.w
    
    def entreno(self, cii):
        ii = 0
        pls = 0
        ci = cii
        
        # entrenamiento
        # Ida
        # capa1
        ci = cii
        ii = 0
        pls = 0
        for i in range(self.c[1]):
            for j in range(self.c[0]):
                pls += self.w[ii] * self.xin[ci][j]
                ii += 1
            self.s[i] = pls
            self.y[i] = self.fun(self.s[i])
            pls = 0
        
        # capa2
        pls = 0
        ii = self.c[0] * self.c[1]
        for i in range(self.c[2]):
            for j in range(self.c[1]):
                pls += self.w[ii] * self.y[j]
                ii += 1
            self.s[i + self.c[1]] = pls
            self.y[i + self.c[1]] = self.fun(self.s[i + self.c[1]])
            pls = 0
        
        # Vuelta
        # capa2 g
        for i in range(self.c[2]):
            self.g[i + self.c[1]] = (self.xout[ci][i] - self.y[i + self.c[1]]) * self.y[i + self.c[1]] * (1 - self.y[i + self.c[1]])
        
        # capa1 g
        pls = 0
        for i in range(self.c[1]):
            for j in range(self.c[2]):
                pls += self.w[self.c[0] * self.c[1] + j * self.c[1] + i] * self.g[self.c[1] + j]
            self.g[i] = self.y[i] * (1 - self.y[i]) * pls
            pls = 0
        
        # capa2 w
        ii = self.c[0] * self.c[1]
        for i in range(self.c[2]):
            for j in range(self.c[1]):
                self.w[ii] = self.w[ii] + self.g[i + self.c[1]] * self.y[j]
                ii += 1
        
        # capa1 w
        ii = 0
        for i in range(self.c[1]):
            for j in range(self.c[0]):
                self.w[ii] = self.w[ii] + self.g[i] * self.xin[ci][j]
                ii += 1

        
    
    
