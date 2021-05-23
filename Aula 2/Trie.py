# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1 #contador
        self.nodes[origin][symbol] = self.num #atribui a cada nuc uma edge
        self.nodes[self.num] = {} #abre um novo dicionário no dicionário
    
    def add_pattern(self, p):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node].keys(): #chave do dicionário, ou seja os nucleotidos
                self.add_node(node, p[pos]) #cria node com o numero, e nuc
            node = self.nodes[node][p[pos]] #dá a edge e o nucleotido
            pos += 1 #aumenta 1
            
    def trie_from_patterns(self, pats): #vai buscar os padroes
     for p in pats:
         self.add_pattern(p)
            
    def prefix_trie_match(self, text): 
        pos = 0
        match = ""
        node = 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys() :
                node = self.nodes[node][text[pos]]
                match += text[pos]
                if self.nodes[node] == {}: return match
                else: pos += 1
            else: return None
        return None
        
    def trie_matches(self, text): 
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m != None: res.append((i,m))
        return res
        
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()
