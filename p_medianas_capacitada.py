import math
import heapq
import random

DEBUG = False


def pop_random(values):
    return values.pop(random.randrange(len(values)))

def get_random(values):
    return values[random.randrange(len(values))]

class PriorityQueueIndividuo:
    def __init__(self, elements=[]):
        self.elements = []
        for element in elements:
            self.put(element)

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)

    def peak(self, n):
        return heapq.nsmallest(n, self.elements)

    def size(self):
        return len(self.elements)


class Vertice:
    def __init__(self, coordenada, capacidade, demanda):
        self.coordenada = coordenada
        self.demanda = demanda
        self.capacidade = capacidade

    def __str__(self):
        return "Vertice({}, {}, {})".format(
            str(self.coordenada),
            str(self.capacidade),
            str(self.demanda)
        )

    def __repr__(self):
        return self.__str__()


class Mediana:
    def __init__(self, vertice, conjunto=set([])):
        self.vertice = vertice
        self.conjunto = conjunto
        self.__distancias = {}
        self.__demanda = 0
        self.__distancia_total = 0
        if len(conjunto) != 0:
            for v in conjunto:
                self.__demanda += v.demanda
                self.__distancia_total += self.distancia(self.vertice, v)

    def __str__(self):
        return "Mediana({}: {})".format(str(self.vertice), str(self.conjunto))

    def __repr__(self):
        return self.__str__()

    def adicionar_vertice(self, v):
        self.conjunto.add(v)
        self.__demanda += v.demanda
        self.__distancia_total += self.distancia(self.vertice, v)

    def capacidade(self, v1):
        return self.vertice.capacidade >= (self.demanda_atual() + v1.demanda)

    def demanda_atual(self):
        return self.__demanda

    def distancia(self, v1, v2):
        aresta = (v1, v2)
        if not aresta in self.__distancias:
            xa, ya = v1.coordenada
            xb, yb = v2.coordenada
            self.__distancias[aresta] = math.sqrt(
                math.pow((xa - xb), 2) + math.pow((ya - yb), 2))
        return self.__distancias[aresta]

    def distancia_total(self):
        return self.__distancia_total


class Individuo:
    def __init__(self, medianas=[]):
        self.medianas = medianas
        self.__aptidao = -1

    def fitness(self):
        if self.__aptidao < 0:
            for mediana in self.medianas:
                self.__aptidao += mediana.distancia_total()

        return self.__aptidao

    def __lt__(self, other):
        return (self.fitness() < other.fitness())

    def __le__(self, other):
        return (self.fitness() > other.fitness())

    def __cmp__(self, other):
        return ((self.fitness() > other.fitness()) - (self.fitness() < other.fitness()))

    def __str__(self):
        return "Invididuo({}, {})".format(len(self.medianas), str(self.fitness()))

    def __repr__(self):
        return self.__str__()


class Populacao:
    def __init__(self, individuos=[]):
        self.individuos = PriorityQueueIndividuo(individuos)

    def __str__(self):
        return "População({})".format(self.individuos.size())

    def __repr__(self):
        return self.__str__()

    def melhor(self):
        return self.individuos.peak(1)[0]

    def tamanho(self):
        return self.individuos.size()

    def melhores(self, n):
        return self.individuos.peak(n)


class AlgoritmoGenetico:
    def __init__    (self, vertices, tamanho_populacao,
                 quantidade_torneio, maximo_geracoes, pcross_over, pmutacao):
        self.tamanho_populacao = tamanho_populacao
        self.vertices = vertices
        self.quantidade_torneio = quantidade_torneio
        self.maximo_geracoes = maximo_geracoes
        self.pcross_over = pcross_over
        self.pmutacao = pmutacao

    def parar(self):
        return self.geracao > self.maximo_geracoes

    def gerar_populacao_inicial(self, numero_medianas):
        invididuos = []
        for j in range(self.tamanho_populacao):
            vertices = self.vertices[:]
            lista_medianas = []

            if(vertices):
                for i in range(numero_medianas):
                    vertice = vertices.pop(random.randrange(len(vertices)))
                    mediana = Mediana(vertice)
                    lista_medianas.append(mediana)

            indice = 0
            i = 0
            while(vertices and lista_medianas):
                v = vertices.pop(random.randrange(len(vertices)))

                if(lista_medianas[indice].capacidade(v)):
                    lista_medianas[indice].adicionar_vertice(v)           

                i += 1
                indice = (i % len(lista_medianas))
            
            individuo = Individuo(lista_medianas)
            invididuos.append(individuo)                    
        return Populacao(invididuos)

    def executar_torneio(self, populacao):
        return populacao.melhores(self.quantidade_torneio)
    
    def recalcular_vertices(self, individuo):
        return 
    def crossover(self, pai_1, pai_2):
        return (pai_1, pai_2)

    def mutacao(self, individuo):
        individuo_mutado = individuo
        if (pmutacao * random.randrange(100) > 1):
            nova_mediana = Mediana(get_random(self.vertices))
            while (nova_mediana in (individuo.medianas)):
                nova_mediana = Mediana(get_random(self.vertices))

            pop_random(individuo.medianas)
            individuo.medianas.append(nova_mediana)            
        return individuo_mutado

    def reproduzir(self, selecionados):
        filhos = []
        size_selecionados = len(selecionados)
        for i in range(0, size_selecionados):
            p1 = selecionados[i]
            if i == size_selecionados - 1:
                p2 = selecionados[0]
            else:
                p2 = selecionados[i + 1] if (i %
                                             2 == 0) else selecionados[i - 1]

            filho_1, filho_2 = self.crossover(p1, p2)
            filho_1 = self.mutacao(filho_1)
            filho_2 = self.mutacao(filho_2)

            filhos.append(filho_1)
            filhos.append(filho_2)
            if len(filhos) >= self.tamanho_populacao:
                break

        return filhos

    def solucionar(self, numero_medianas):
        if len(self.vertices) <= 0:
            return False

        self.geracao = 0    
        populacao = self.gerar_populacao_inicial(numero_medianas)
        if DEBUG:
            print("População inicial", populacao)        
        melhor = populacao.melhor()
        while not self.parar():
            self.geracao += 1
            selecionados = self.executar_torneio(populacao)
            if DEBUG:
                print("Selecionados ", selecionados)
            filhos = self.reproduzir(selecionados)
            if DEBUG:
                print("Filhos ", filhos)
            queue = PriorityQueueIndividuo(filhos)
            melhor_filho = queue.get()
            if DEBUG:
                print("Melhor filho ", melhor_filho)            
            if melhor.fitness() < melhor_filho.fitness():
                melhor = populacao.melhor()

            if DEBUG:
                print("Melhor ", melhor)

            populacao = Populacao(selecionados)
            
        if DEBUG:
            print("População final", populacao)        
        return melhor
            
if (__name__ == "__main__"):        
    random.seed()    
    linhas = open('teste', 'r').readlines()        
    primeiralinha = linhas.pop(0).split()
        
    numero_de_pontos = int(primeiralinha[0])
    numero_medianas = int(primeiralinha[1])        
    vertices = []

    while linhas:                        
        x, y, capacidade, demanda = linhas.pop(0).split()        
        vertices.append(Vertice((int(x), int(y)), int(capacidade), int(demanda)))

    tamanho_populacao = 4
    quantidade_torneio = 4
    maximo_geracoes = 1000
    pcross_over = 0.98
    pmutacao = 0.05
    
    ag = AlgoritmoGenetico(
        vertices,
        tamanho_populacao,
        quantidade_torneio,
        maximo_geracoes,
        pcross_over,
        pmutacao
    )
        
    print("Melhor solução AG: ", ag.solucionar(numero_medianas))