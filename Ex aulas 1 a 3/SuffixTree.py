class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
        self.seq1 = ""
        self.seq2 = ""
    
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
        self.seq1 = s1
        self.seq2 = s2
        seq1 = s1 + "$"
        seq2 = s2 + "#"
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], 0, i)  # i pos incial do sufixo na sequencia, 0 representa a seq 1
        for j in range(len(seq2)):
            self.add_suffix(seq2[j:], 1, j)  # j pos incial do sufixo na sequencia, 1 representa a seq 2
            
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

    def largestCommonSubstring (self): #ex2
        subseq = ""  # maior sequencia será guardada
        for x in range(len(self.seq1)):  # corre a primeira sequencia
            for y in range(len(self.seq2)):  # corre a segunda sequencia
                c = 1
                while x + c <= len(self.seq1) and y + c <= len(self.seq2):  # ciclo while que vai permitir aumentar a janela a analisar em ambas as sequencias
                    if self.seq1[x:x+c] == self.seq2[y:y+c]:  # se os caracteres deste splicing forem iguais de uma seq para a outra
                        if len(subseq) <= len(self.seq1[x:x+c]):  # e se o tamanho desse for maior ou igual que o tamanho da subsequencia já gravada
                            subseq = self.seq1[x:x+c]  # subsquencia comum passa a ser essa
                    c += 1  #corre até ficar maior que uma das seqs
        return subseq


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

def test3():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.nodes_below(0))

test()
#print()
#test2()
