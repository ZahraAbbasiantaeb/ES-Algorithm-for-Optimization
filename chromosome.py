import math
import random
import numpy as np


class chromosome:

    X = []
    sigma = []
    alpha = []
    min = []
    max = []

    beta = (5 * math.pi) / 180
    theta2 = 0
    theta1 = 0
    threshold = 0
    fitness = 0.0

    def __init__(self, min, max, length):

        self.sigma = np.zeros(length)
        self.X = np.zeros(length)
        self.alpha = np.zeros(length)

        for i in range (0, length):

            self.X[i] = (random.uniform(min[i], max[i]))
            self.sigma[i] = random.uniform(0, 1)
            self.alpha[i] = random.uniform(0, math.pi)

        self.min = min
        self.max = max
        self.theta1 = 1 / math.sqrt(2 * (math.sqrt(length)))
        self.theta2 = 1/(math.sqrt(2*length))
        self.threshold =  0.00001

        return


    def setFitness(self, fitness):

        self.fitness = fitness

        return


    def mutate (self):

        length =  len(self.X)
        rand = random.uniform(0,1)
        rand2 = random.uniform(0,1)

        for i in range (0, length):

            self.sigma[i] = self.sigma[i] * math.exp(self.theta2 * rand + self.theta1 * random.uniform(0, 1))
            self.alpha[i] =  self.alpha[i] + self.beta * rand2

            if (self.sigma[i] < self.threshold):
                self.sigma[i] = self.threshold


            if (self.alpha[i]> math.pi or self.alpha[i]< -1 * math.pi):
                self.alpha[i] = self.alpha[i] - 2 * math.pi * math.sin(self.alpha[i])


        C_prim = np.cov(np.stack((self.alpha, self.sigma), axis=1))
        mean = np.zeros(length)
        random_c = np.random.multivariate_normal(mean, C_prim)

        for i in range (0, length):
            self.X[i] = self.X[i] + random_c[i]

        return


    def setX(self,x):

        self.X =x
        return