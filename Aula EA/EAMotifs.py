from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            multifit = self.motifs.scoreMult(sol)
            ind.setFitness(fit)
            ind.setMultiFitness(multifit)


class EAMotifsReal (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.mottifes = MotifFinding() #iniciar o MotifFiding
        self.motifs.readFile(filename, "dna") #vai guardando as seqs
        indsize = self.motifs.motifSize * len(self.motifs.alphabet) #tamanho vai ser um vetor da pwm, linhas(alfabeto) e colunas(motif)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        low = 0
        up = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize, low, up, [])

    def v_pwm(self, v): #transformar em pwm
        tam_mot = self.motifs.motifSize #tamanho motif
        tam_alf = len(self.motifes.alphabet) #tamanho alfabeto
        pwm = createMatZeros(tam_alf, tam_mot) #criar pwm de zeros tendo em conta os parametros acima
        for a in range(0, len(v), tam_alf): #correr o vetor em incrementos de tamanho do alfabeto
                id_col = int(a / tam_alf) #indice vai incrementar em 1, int porque decimal não pode entrar na matriz
                col = v[a : a + tam_alf] #splicing (de tamanho do alfabeto) no vetor
                soma = sum(col) #soma dos elementos retirados
                for b in range(tam_alf): #correr as linhas da pwm
                    pwm,[b][id_col] = col[b] / soma #para cada linha da coluna do ciclo anterior adicionar o valor respetivo
        return pwm
    
    def probabSeq(self, seq): #probabilidade de apenas uma seq tendo em conta a pwm
        res = 1.0
        for a in range(self.motifs.motifSize): #corre o motif
            linha = self.motifs.alphabet.index(seq[a]) #vê qual a linha a usar tendo em conta o analfabeto
            res *= self.motifs.pwm[linha][a] #multiplica o valor pelo valor guardado anterior
        return res #probabilidade da seq ter sido gerada pela pwm

    def mostProbableSeq(self, seq):
        maxi = -1.0
        max_ind = -1
        for a in range(len(seq) - self.motifs.motifSize): #corre enquanto o motif cabe na seq
            prob = self.probabSeq(seq[a : a + self.motifs.motifSize]) #probabilidade de cada seq
            if prob > maxi: #maior valor de probabilidade
                maxi = prob
                max_ind = a
        return max_ind
   
    def evaluate(self, indivs):
        for a in range(len(indivs)):  # para cada individuo
            ind = indivs[a]  # atribuir cada individuo
            gen = ind.getGenes()  # retira os "genes" desse individuo, que neste caso sao os valores que vao compor a pwm
            self.motifs.pwm = self.v_pwm(gen)  # construir a pwm a partir do vetor
            k = MyMotifs(pwm = self.motifs.pwm, alphabet = self.motifs.alphabet)  # iniciar MyMotifs com a pwm criada e alfabeto 
            pos = []  # vetor de posições iniciais
            for seq in self.motifs.seqs:  # para cada sequencia que está guardada
                prob = k.mostProbableSeq(seq)  # calcular o indice da sequencia mais provavel de acordo com a pwm 
                pos.append(prob)  # adicionar esse indice ao vetor das posições iniciais
            fit = self.motifs.score(pos)  # ver o score 
            ind.setFitness(fit)  # associar ao individuo
            ### Calcular o score multiplicativo sem atualizar a pwm
            multifit = self.motifs.scoreMult(pos, self.motifs.pwm)  # não queremos que a pwm seja atualizada ao fazer o score multiplo, por isso dá-mos como parametro a pwm que acabamos de criar atraves da função v_pwm
            ind.setMultiFitness(multifit)  # e associamos o valor do score multiplicativo a esse individuo da mesma maneira que se fez para o score



def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt", 2)
    ea.run()
    ea.printBestSolution()


test1()
# test2()
