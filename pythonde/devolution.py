import numpy as np
from numpy.random import random

class DEvolution(object):
    """
    Differential evolution optimization (DE)
    Parameters:
        f:           The function to be optimized (Objective Function)
        bounds:      The bounds on optimization parameters
        nPopulation: The population size
        F :          The difference amplification factor (optional)
        CR :         The cross-over probability (optional)
        seed :       The seed for the random number generator (optional)
        minimize:    If True the function "f" will be minimized esle maximized (optional)
    """
    def __init__(self, f, bounds, nPopulation, F = 0.5, CR = 0.5, seed = None, minimize = True):

        self.func = f
        self.nPopulation = nPopulation

        self.bounds = np.asarray(bounds)
        self.lowerBound = np.tile(self.bounds[:, 0], [self.nPopulation, 1])
        self.boundRange = np.tile(self.bounds[:, 1] - self.bounds[:, 0], [self.nPopulation, 1])

        self.nParameters = (self.bounds).shape[0]
        self.nDimension = (self.bounds).shape[0]

        self.F = F
        self.CR = CR
        self.m = 1 if minimize else -1
        self._minIndex = None

        if seed:
            np.random.seed(seed)
        self.seed = seed

        self._population = np.asarray(self.lowerBound + random([self.nPopulation, self.nParameters]) * self.boundRange)
        self._fitness    = np.zeros(self.nPopulation)

        self._trialPopulation  = np.zeros_like(self._population)
        self._trialFitness  = np.zeros_like(self._fitness)

        self._iterationNum = 0
        self._extFitness = None

    @property
    def Population(self):
        """The population vector"""
        return self._population

    @property
    def MinimumIndex(self):
        """The index of best solution in the population vector"""
        return self._minIndex

    @property
    def MinimumPoint(self):
        """The optimized solution"""
        return self._population[self._minIndex, :]

    @property
    def MinimumValue(self):
        """The value of f (objective function) at the optimized location"""
        return self._fitness[self._minIndex]

    def Optimize(self, maxGen):
        """Starts the optimization process"""
        for tmp in self(maxGen): pass
        return self._population[self._minIndex, :], self._fitness[self._minIndex]

    def __call__(self, maxGen = None):
        return self._iterate(maxGen)

    def _iterate(self, maxGen):
        """Iterating the optimization algorithm for maxGen generations"""
        # Automatic handling between Generator/Coroutine/Normal modes of operation
        while (((type(maxGen) == int) and (maxGen > 0)) or (maxGen == None)):

            # Initializing the fitness vectors
            if (self._iterationNum == 0):
                for i in range(self.nPopulation):
                    self._extFitness = (yield self._population[i,:])
                    if (self._extFitness is None): break
                    self._fitness[i] = self.m * self._extFitness
                self._iterationNum += 1
            else:
                for i in range(self.nPopulation):
                    self._extFitness = (yield self._trialPopulation[i,:])
                    if (self._extFitness is None): break
                    self._trialFitness[i] = self.m * self._extFitness
                self._iterationNum += 1

            # Check if the optimizer is used in coroutine mode
            if (self._extFitness is not None):

                if (self._iterationNum > 1):
                    mask = self._trialFitness < self._fitness
                    self._population[mask, :] = self._trialPopulation[mask, :]
                    self._fitness[mask] = self._trialFitness[mask]

                    self._minIndex = np.argmin(self._fitness)

                for j in range(self.nPopulation):

                    rnds = (random(3) * self.nPopulation).astype(int);
                    while rnds[0] in [j]:
                        rnds[0] = int(random() * self.nPopulation)
                    while rnds[1] in [j, rnds[0]]:
                        rnds[1] = int(random() * self.nPopulation)
                    while rnds[2] in [j, rnds[0], rnds[1]]:
                        rnds[2] = int(random() * self.nPopulation)

                    v = self._population[rnds[0], :] + self.F * (self._population[rnds[1], :] - self._population[rnds[2], :]);
                    u = np.zeros_like(v)
                    randb = random(self.nDimension);
                    for index, value in enumerate(randb):
                        if value <= self.CR:
                            u[index] = v[index]
                        else:
                            u[index] = self._population[j, index]

                    rnbr = int(random() * self.nDimension)
                    u[rnbr] = v[rnbr]

                    # Applying constraints on the population vector
                    for index, val in enumerate(u):
                        if (val < self.bounds[index][0]):
                            u[index] = self.bounds[index][0]
                        elif (val > self.bounds[index][1]):
                            u[index] = self.bounds[index][1]

                    self._trialPopulation[j, :] = u;

            # Check if the optimizer is used in normal mode
            elif (maxGen != None):

                maxGen -= 1
                if (self._iterationNum == 1):
                    for i in range(self.nPopulation):
                        self._fitness[i] = self.m * self.func(self._population[i, :])

                for j in range(self.nPopulation):

                    rnds = (random(3) * self.nPopulation).astype(int);
                    while rnds[0] in [j]:
                        rnds[0] = int(random() * self.nPopulation)
                    while rnds[1] in [j, rnds[0]]:
                        rnds[1] = int(random() * self.nPopulation)
                    while rnds[2] in [j, rnds[0], rnds[1]]:
                        rnds[2] = int(random() * self.nPopulation)

                    v = self._population[rnds[0], :] + self.F * (self._population[rnds[1], :] - self._population[rnds[2], :]);
                    u = np.zeros_like(v)
                    randb = random(self.nDimension);
                    for index, value in enumerate(randb):
                        if value <= self.CR:
                            u[index] = v[index]
                        else:
                            u[index] = self._population[j, index]

                    rnbr = int(random() * self.nDimension)
                    u[rnbr] = v[rnbr]

                    # Applying constraints on the population vector
                    for index, val in enumerate(u):
                        if (val < self.bounds[index][0]):
                            u[index] = self.bounds[index][0]
                        elif (val > self.bounds[index][1]):
                            u[index] = self.bounds[index][1]

                    self._trialPopulation[j, :] = u;

                for i in range(self.nPopulation):
                    self._trialFitness[i] = self.m * self.func(self._trialPopulation[i, :])

                mask = self._trialFitness < self._fitness
                self._population[mask, :] = self._trialPopulation[mask, :]
                self._fitness[mask] = self._trialFitness[mask]

                self._minIndex = np.argmin(self._fitness)
