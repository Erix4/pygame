import random
import numpy as np

INPUT_NUM = 5
HIDDEN_NUM = 1
OUTPUT_NUM = 2

class Brain:
    def __init__(self, *args):
        if(len(args) > 1):
            self.genome = args[0]#list of tuples: input, ouput, weight
            self.biases = args[1]#dict of biases for outputs and hidden nodes
        else:
            self.genome = []
            self.biases = {}
            for x in range(args[0]):
                self.genome.append((random.randint(0, INPUT_NUM + HIDDEN_NUM - 1),
                            random.randint(INPUT_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM - 1),
                            random.uniform(-1, 1)))
            for x in range(INPUT_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM):
                self.biases[x] = random.uniform(-1, 1)
        #0-3 are inputs, 4-5 are hidden nodes, 6-10 are outputs
        #
        self.tracework = {}#diction from output to connection info
        for x in range(INPUT_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM):
            self.tracework[x] = ([], [])#input, weight
            for gene in self.genome:
                if gene[1] == x:
                    self.tracework[x][0].append(gene[0])
                    self.tracework[x][1].append(gene[2])
        #
        self.stored = {}
        for x in range (INPUT_NUM, INPUT_NUM + HIDDEN_NUM):
            self.stored[x] = 0
        #
        #print(self.tracework)
        #print(self.weights)
    #
    def forward(self, inputs):
        outputs = []
        for x in range(INPUT_NUM + HIDDEN_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM):
            outputs.append(self.eval(x, inputs))
        #
        return outputs
    #
    def eval(self, node, inputs, visited=[]):
        sum = 0
        for x in range(len(self.tracework[node][0])):#loop through the number of inputs to this node
            inp = self.tracework[node][0][x]
            weight = self.tracework[node][1][x]
            if(inp < INPUT_NUM):#node input is a native input
                sum += inputs[inp] * weight
            elif(inp == node or inp in visited):#node input is itself, must be a hidden node
                sum += self.stored[inp] * weight
            else:#node input is hidden node that is not itself
                visited.append(inp)
                sum += self.eval(inp, inputs, visited) * weight
        #
        value = np.tanh(sum + self.biases[node])
        if node >= INPUT_NUM and node < INPUT_NUM + HIDDEN_NUM:
            self.stored[node] = value
        #
        return value# squash sum to 
    #
    def mutate(self):
        new_genome = self.genome
        new_biases = self.biases
        #
        if (random.random() > 0.5):
            new_gene_num = random.randint(0, len(new_genome) - 1)
            old_gene = new_genome[new_gene_num]
            match random.randint(0, 4):
                case 0:#input
                    new_genome[new_gene_num] = (random.randint(0, INPUT_NUM + HIDDEN_NUM - 1), old_gene[1], old_gene[2])
                case 1:#output
                    new_genome[new_gene_num] = (old_gene[0], random.randint(INPUT_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM - 1), old_gene[2])
                case 2 | 3 | 4:#weight
                    new_genome[new_gene_num] = (old_gene[0], old_gene[1], random.uniform(-1, 1))
        else:
            new_biases[random.randint(INPUT_NUM, INPUT_NUM + HIDDEN_NUM + OUTPUT_NUM - 1)] = random.uniform(-1, 1)
        #
        return [new_genome, new_biases]
    #
    def __str__(self):
        buildString = ""
        for gene in self.genome:
            buildString += str(gene[0]) + " -- " + str(np.round(gene[2], 3)) + " --> " + str(gene[1]) + "\n"
        #
        buildString += "--\n"
        #
        for bias in self.biases:
            buildString += str(bias) + ": " + str(np.round(self.biases[bias], 3)) + "\n"
        #
        return buildString