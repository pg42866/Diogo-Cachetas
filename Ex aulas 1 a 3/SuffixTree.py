class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
        self.seq = ''
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p, sufnum):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p)-1:
                    self.add_node(node, p[pos], sufnum)
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1
    
    def suffix_tree_from_seq(self, text):
        self.seq = text
        seq = text + "$"  
        for i in range(len(seq)):
            self.add_suffix(seq[i:], i)
            
    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else: return None
        return self.get_leafes_below(node)
        

    def get_leafes_below(self, node):
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

    def nodes_below(self, node): #ex1a
        res = []
        if node in self.nodes.keys(): #verfifica a existencia de nodes
            for x in self.nodes[node][1].values():
                res.append(x) #cria a lista com os valores dos nodes
            for n in res:
                for y in self.nodes[n][1].values():
                    res.append(y) #acrescenta os valores obtidos
            return res 
        else:
            return None

    def matches_prefix(self, prefix): #ex1b
        res = []
        padrao = self.find_pattern(prefix) #guarda os nodes do padrao na variavel
        seq = self.seq #seq inicial
        if padrao is None:
            return None
        else:
            for i in padrao: #itera os nodes do padrao
                psblt = len(seq) - i # nº possibilidades
                tam = len(prefix) #variavel para armazenar o tamanho atual da hipotese
                while tam <= psblt:
                    res.append(seq[i:i + tam]) #adiciona a lista res o excerto da seq entre o valor iterado (i) e i+tam
                    tam += 1 #adiciona sempre mais um para fechar o ciclo
        return set(res)

#  def largestCommonSubstring (self): #ex2


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))
    print (st.nodes_below(0))
    #print(st.matches_prefix("TA"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print(st.find_pattern("TA"))
    print(st.repeats(2,2))

test()
#print()
#test2()
