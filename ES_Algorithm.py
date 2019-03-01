import math
import random
import matplotlib.pyplot as plt
import time

from chromosome import chromosome


class ES:

    individuals = []
    individual_length = 0
    individual_count = 0
    min = []
    max = []
    iterations = 0
    child_count = 0
    func="rosenbrock"
    fitness_base = 0

    def __init__(self, individual_length, individual_count, min, max, iterations, child_count, fitness_base):

        self.fitness_base = fitness_base
        self.individual_length = individual_length
        self.individual_count = individual_count
        self.max = max
        self.min = min
        self.child_count = child_count
        self.iterations = iterations


    def initial_individual(self):

        for i in range(0, self.individual_count):
            self.individuals.append(chromosome(self.min, self.max, self.individual_length))

        return

    def recombination(self, chromosome1, chromosome2):

        child = chromosome(self.min, self.max, self.individual_length)
        x = []
        u = []
        z = []

        for i in range(0, self.individual_length):
            rand = random.uniform(0, 1)

            if (rand > 0.5):
                x.append(chromosome1.X[i])
                u.append(chromosome1.sigma[i])
                z.append(chromosome1.alpha[i])

            else:
                x.append(chromosome2.X[i])
                u.append(chromosome2.sigma[i])
                z.append(chromosome2.alpha[i])

        child.setX(x)
        child.sigma = u
        child.alpha = z
        child.fitness = self.getFitness(child)

        return child

    def parentSelection(self):

        parents = []

        rand1 = random.randint(0, self.individual_count - 1)
        rand2 = random.randint(0, self.individual_count - 1)

        while(rand2 == rand1):
            rand2 = random.randint(0, self.individual_count - 1)

        parents.append(self.individuals[rand1])
        parents.append(self.individuals[rand2])

        return parents


    def survivor_selection(self, childs):

        total = self.join(self.individuals, childs)
        # total2= sorted(total, key=lambda indiv: indiv.X, reverse=True)

        from operator import attrgetter
        total.sort(key=attrgetter('fitness'), reverse=False)

        new_individual = total[0:self.individual_count]

        return new_individual


    def run(self):

        result=[]
        self.initial_individual()
        iteration=0
        time1=time.time()
        time2=time1
        tmp = False

        while(iteration < self.iterations):
            iteration+=1

            # setFitness
            for i in range(0, self.individual_count):
                self.individuals[i].setFitness(self.getFitness(self.individuals[i]))

            childs = []

            while(len(childs) <= self.child_count):
                parents = self.parentSelection()
                childs.append(self.recombination(parents[0], parents[1]))

            self.individuals = self.survivor_selection(childs)
            # print("iteration: "+ str(iteration))
            res = self.findBest()
            # print(res)
            result.append(res)

            if( res <= self.fitness_base and tmp == False):
                time2 = time.time()
                tmp = True

            # print("***********")

        # print("runtime is: "+ str(time2-time1))
        # plt.plot(result)
        # plt.xlabel("iteration")
        # plt.ylabel("Error")
        # plt.show()

        return result


    def findBest(self):

        fitness = 0
        index = 0
        i = 0

        for elem in self.individuals:

            if (elem.fitness < fitness or i==0 ):
                fitness = elem.fitness
                index = i

            i+=1
        # print(self.individuals[index].X)
        return self.individuals[index].fitness


    def getFitness(self, chromosome):

        if(self.func=="rosenbrock"):
            sum = self.rosenbrock(chromosome)

        elif (self.func=="ackley"):
            sum = self.ackley(chromosome)

        return sum


    def rosenbrock (self, chromosome):

        sum = 0
        x = chromosome.X

        for i in range(0, self.individual_length - 1):
            sum += 100 * ((x[i + 1] - x[i] ** 2) ** 2) + (x[i] - 1) ** 2
        return sum

    def join (self, dataset1, dataset2):

        new=[]

        for elem in dataset1:
            new.append(elem)

        for elem in dataset2:
            new.append(elem)

        return new


    def ackley(self,chromosome):

        sum = 0
        x = chromosome.X
        cos = 0

        for i in range(0, self.individual_length-1):

            sum += x[i]**2
            cos += math.cos(2 * x[i] * math.pi)

        res = -20 * math.exp( -0.2 * math.sqrt(sum/self.individual_length)) \
              - math.exp(cos/self.individual_length) \
              + 20 + math.exp(1)

        if(res < 0):
            res *= -1

        return  res


