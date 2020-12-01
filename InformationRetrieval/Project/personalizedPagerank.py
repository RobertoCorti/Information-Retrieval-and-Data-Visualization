import json
import numpy as np
from scipy.sparse import csr_matrix

class PersonalizedPageRank:
    
    def __init__(self, graphFile, contentFile):
        self.graph_file = graphFile
        self.content_file = contentFile
        self.generate_graph()
        self.generate_contents()
        
    def generate_graph(self):
        with open(self.graph_file, 'r') as f:
            # We have the graph encoded as an adjacency list in a JSON file 
            g = json.load(f)
            # The data structure read from JSON is already "good enough" for us
        self.graph = g
        self.num_nodes = len(g.keys())
        
    def generate_contents(self):
        with open(self.content_file, 'r') as f:
            # We have the graph encoded as an adjacency list in a JSON file 
            c = json.load(f)
            # The data structure read from JSON is already "good enough" for us
        self.contents = c
        
    def compute_stochastic_matrix(self):
        # we make a dictionary saving for each key in the graph
        # the corresponding index in the matrix
        key_to_pos = dict(zip(self.graph.keys(), range(0,self.num_nodes)))
        row = []
        col = []
        data = []

        for key in self.graph.keys():
            for edge in self.graph[key]:
                row.append(key_to_pos[key])
                col.append(key_to_pos[edge])
                data.append(1/len(self.graph[key]))
        R = csr_matrix((data, (row, col)), shape=(self.num_nodes, self.num_nodes))
    
        self.R = R
    
    def generate_seed(self, topic):
        key_to_pos = dict(zip(self.graph.keys(), range(0,self.num_nodes)))
        seeds = np.zeros(self.num_nodes)

        for key in self.contents.keys():
            lower_key_content = [x.lower() for x in self.contents[key]]
            mask = [topic in x for x in lower_key_content]
            #if topic in lower_key_content:
            if any(mask):
                seeds[key_to_pos[key]] = 1

        if (np.sum(seeds)!=0):
            self.J = seeds/sum(seeds)
        else: 
            self.J = seeds
        
    def PersonalizedPageRank_iteration(self, x, alpha):
        P = (1 - alpha) * self.R
        x_prime = (P.T).dot(x) + alpha * self.J
        return x_prime
    
    def compute_PersonalizedPageRank(self, topic, alpha, epsilon):
        dictionary = {}
        # We compute the transition matrix without the teleportation
        self.compute_stochastic_matrix()
        # The jump vector is imply a vector of ones divided by its length
        self.generate_seed(topic)
        if (np.sum(self.J)==0):
            print('There are no pages related to '+topic)
            x = np.zeros(self.num_nodes)
            return x, dictionary
        #J = np.ones(n)/n
        # The starting point can be a uniform distribution across all nodes
        # x = np.ones(n)/n
        # ...or a random stochastic vector
        x = np.random.rand(self.num_nodes)
        x = x/x.sum()
        # We can now iterate until the norm one of the changes in the
        # last iteration goes below epsilon
        err = np.inf # initially infinity
        while (err > epsilon):
            x_new = self.PersonalizedPageRank_iteration(x, alpha)
            err = (abs(x_new - x)).sum()
            x = x_new
        for i, k in enumerate(self.graph.keys()):
            dictionary[k] = x[i]
        
        return x, dictionary