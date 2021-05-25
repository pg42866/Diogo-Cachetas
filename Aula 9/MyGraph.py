## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g   #atributo unico, é um dicionario 

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v]) #dá print para cada key (vertide) no dic

    ## get basic info

    def get_nodes(self): #devolve uma lista dos nodes aka vertices aka keys
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): #devolve as arestas numa lista de tuplos (origem, destino)
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self): #devolve o tamanho do grafo
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v): #adiciona um node aka vertice
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d): #adiciona uma aresta ao grafo, se um vertice nao existir, é adicionadp
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys(): #confirmar se o está no grafo
            self.add_vertex(o) #adicionar o
        if d not in self.graph.keys(): #confirmar se d está no grafo
            self.add_vertex(d) #adicionar d 
        if d not in self.graph[o]: #ver se d é um destino de o
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v): #devolver uma lista com os antecessores
        res = [] #criar lista
        for k in self.graph.keys(): #para cada node
            if v in self.graph[k]: #verificar se v é um destino do node
                res.append(k) #adicionar o node
        return res
    
    def get_adjacents(self, v): #devolve a lista de adjacentes de um node (dois nodes são adjacentes se um for o sucessor do outro)
        suc = self.get_successors(v) #sucesores
        pred = self.get_predecessors(v) #antecessores
        res = pred #lista toma os valores dos antecessores
        for p in suc: #para cada sucessor
            if p not in res:
                res.append(p) #se não estiver na lista é adicionado à mesma
        return res
        
    ## degrees    
    
    def out_degree(self, v): #devolve o grau de saída do node
        return len(self.graph[v])
    
    def in_degree(self, v): #devolve o grau de entrada do node
        return len(self.get_predecessors(v))
        
    def degree(self, v): #grau do node é dado pelo numero de arestas que lhe incidem
        return len(self.get_adjacents(v)) #conta as arestas
        
    def all_degrees(self, deg_type = "inout"): #calcula os graus de entrada e saída para todos os nodes
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys(): #para cada node
            if deg_type == "out" or deg_type == "inout": #se forem graus de saída ou de entrada e saída
                degs[v] = len(self.graph[v]) #adicionar o valor de graus de saída
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout": #se for grau de entrada ou de entrada e saída
            for v in self.graph.keys(): #para cada node do grafo
                for d in self.graph[v]: #para cada value desse node
                    if deg_type == "in" or v not in self.graph[d]: #se o grau for entrada ou o node não for um value de d
                        degs[d] = degs[d] + 1 #adicionar um ao value de d no dicionario
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):#devolve os 10 nos com maior grau
        if all_deg is None: 
            all_deg = self.all_degrees(deg_type) #vai buscar o dicionario de todos os graus
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True) #transforma o dicionario em lista e ordena do maior para o mais pequeno
        return list(map(lambda x:x[0], ord_deg[:top])) #devolve uma lista com os 10 nos
        
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"): #devolve a media dos graus
        degs = self.all_degrees(deg_type) #calcula os graus de entrada, saída ou ambos para todos os nodes
        return sum(degs.values()) / float(len(degs)) #calcula a media
        
    def prob_degree(self, deg_type = "inout"): #probabilidade de um grau existir no grafo
        degs = self.all_degrees(deg_type) #calculo dos graus de entrada, saída e ambos dos nós todos
        res = {} #criar dicionario
        for k in degs.keys(): #para todas as keys da lista
            if degs[k] in res.keys(): #se o value dessa key já estiver presente no dicionario
                res[degs[k]] += 1 #
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res    
    
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s, d):
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited: 
                    l.append((elem,dist+1))
                    visited.append(elem)
        return None
        
    def shortest_path(self, s, d):
        if s == d: return 0
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node,elem]
                elif elem not in visited: 
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0
        num_reachable = 0 #numero de 
        for k in self.graph.keys(): #para cada node
            distsk = self.reachable_with_dist(k) #lista das ligações existentes
            for _, dist in distsk:
                tot += dist #contagem das distancias
            num_reachable += len(distsk) #contagem das ligações entre todos os nodes
        meandist = float(tot) / num_reachable #media da distancia das ligações
        n = len(self.get_nodes()) #numero de nos
        return meandist, float(num_reachable)/((n-1)*n)
    
    def closeness_centrality(self, node): #
        dist = self.reachable_with_dist(node) #lista que tem os nodes todos e a distancia do node dado a cada um dos nos
        if len(dist)==0:
            return 0.0 #centralidade mais proxima é 0
        s = 0.0
        for d in dist: #para cada node
            s += d[1] #a distancia aumenta o valor da distancia do node a d
        return len(dist) / s #devolve a centralidade mais proxima -> todos os nodes com ligação ao node dado a dividir pela distancia total
        
    
    def highest_closeness(self, top = 10): #devolver 0 top 10 centralidades mais proximas
        cc = {} #criar um dicionario
        for k in self.graph.keys(): #para cada node
            cc[k] = self.closeness_centrality(k) #calcular a centralidade mais proxima desse node
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #tranformar o dicionario em lista e ordenar em ordem a centralidade mais proxima
        return list(map(lambda x:x[0], ord_cl[:top])) #devolver as a0 centralidades mais proximas
            
    
    def betweenness_centrality(self, node):
        total_sp = 0 #total de caminhos curtos existentes
        sps_with_node = 0 #caminhos curtos que passam pelo node dado
        for s in self.graph.keys(): #para todos os nodes
            for t in self.graph.keys(): 
                if s != t and s != node and t != node: #se o primeiro node for diferente do segundo e se os dois forem diferentes do node dado
                    sp = self.shortest_path(s, t) #calcula-se o caminho do node s ao t
                    if sp is not None: #se o caminho não for zero
                        total_sp += 1 #incrementa-se o numero de caminhos curtos 
                        if node in sp: #se o node dado estiver presente no caminho entre s e t
                            sps_with_node += 1 #incrementa-se o numero de caminhos que passam pelo node dado
        return sps_with_node / total_sp #devolve-se o valor da centralidade ->caminhos curtos que passam pelo node dado/caminhos curtos totais


    def highest_betweenness(self, top = 10): #devovler o top 10 centralidades betweenness
        cc = {}#criar dicionario
        for k in self.graph.keys(): #para todos os nodes
            cc[k] = self.betweenness_centrality(k) #calcular a centralidade desse node
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #tranformar em lista e ordenar em ordem a beteenness centrality
        return list(map(lambda x:x[0], ord_cl[:top])) #devolver o top 10


    def node_degree_centrality(self, v):
        alldegree = self.all_degrees()
        return alldegree[v]
                    
    
    ## cycles    
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited: 
                    l.append(elem)
                    visited.append(elem)
        return res       
    
    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res

    ## clustering
        
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): degs_k[degs[k]].append(k)
            else: degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck


def is_in_tuple_list(tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res

    
if __name__ == "__main__":
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))
    
    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))
