# -*- coding: utf-8 -*-

class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self): 
        """Implementação do pre-processamento do bad caracter rule"""
        self.occ = {} #cria dicionário
        for c in self.alphabet: #adiciona ao dicionario todas as letras do alfabeto com valor -1
            self.occ[c] = -1
        for i in range(len(self.pattern)):
            self.occ[self.pattern[i]] = i #altera no dicionario a letra no pattern para valor i
     
    def process_gsr(self): #2 casos: sufixo ocorre de novo no padrao, ou um sufixo do match é parte do prefixo do padrao
        """Implementação do pre-processamento do good suffix rule"""
        self.f = [0] * (len(self.pattern) + 1) #abrir uma lista de 0's com o tamanho do padrao
        self.s = [0] * (len(self.pattern) + 1) #abrir uma lista de 0's com o tamanho do padrao
        i = len(self.pattern)
        j = i + 1 #define o i e j pelo comprimento do padrão
        self.f[i] = j #altera o ultimo elemento da lista f para o valor de j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i-1] != self.pattern[j-1]: #lista s, lista que significa o numero de casas que pode avançar caso não encaixe no padrao
                if self.s[j] == 0:
                    self.s[j] = j-i
                j = self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j
        j = self.f[0]    
        for i in range(0, len(self.pattern)): #quando definido como 0 alterar para o valor de j mais recente, que significa passar o restante da cadeia.
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
                   
    def search_pattern(self, text):
        res = []
        i = 0 #posição na sequencia
        while i <= (len(text) - len(self.pattern)): #para começar a correr a sequencia
            j = len(self.pattern) - 1 #posição no padrão
            while j >= 0 and self.pattern[j] == text[j + i]: #continuar a correr enquanto houver match
                j = j -1 
            if j < 0:
                res.append(i)
                i = i + self.s[0] #avançar para i "casas" para a frente como j<0 significa que deu match com um padrão
            else:
                c = text[j + i]
                i += max(self.s[j+1],j - self.occ[c]) #avançar uma sequencia dependo do GSR e BCR
        return res

def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))
    
if __name__ == "__main__":
    test()


# result: [5, 13, 23, 37]
            
