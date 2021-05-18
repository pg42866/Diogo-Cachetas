# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                prefixo = pattern[0:q] + a #gera um prefixo de tamanho dos estados com base no prefixo do padrao
                self.transitionTable[(q,a)] = overlap(prefixo, pattern) #dá o comprimento do overlap max de s1 e s2              
       
    def printAutomata(self): #imprime o automato finito
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys(): #keys() permite ver as chaves do dict como lista
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable[(current,symbol)]
        
    def applySeq(self, seq): #dá o caminho dos estados previstos
        q = 0
        res = [q]
        for c in seq:
            q = self.nextState(q,c)
            res.append(q)
        return res
        
    def occurencesPattern(self, text): #dá o indice da ocorrencia do padrao
        q = 0 
        res = []
        for i in range(len(text)):
            q = self.nextState(q, text[i])
            if q == self.numstates-1:
                res.append(i-self.numstates+2)
        return res

def overlap(s1, s2):
    maxov = min(len(s1), len(s2)) #devolve o mais pequeno
    for i in range(maxov,0,-1): #range(start,stop,step)
        if s1[-i:] == s2[:i]: return i #se o sufixo de s1 for prefixo de s2 devolve a posição
    return 0 #para todo o caso devolvemos um zero 
               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]



