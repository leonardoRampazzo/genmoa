import math
import heapq
import random
from copy import deepcopy
from pprint import pprint
DEBUG = False

def pop_random(values):
    return values.pop(random.randrange(len(values)))

def get_random(values):
    return values[random.randrange(len(values))]

def distancia_euclidianea(p1, p2):    
    xa, ya = p1
    xb, yb = p2
    return math.sqrt(math.pow((xa - xb), 2) + math.pow((ya - yb), 2))

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
            self.__distancias[aresta] = distancia_euclidianea(v1.coordenada, v2.coordenada)
        return self.__distancias[aresta]

    def distancia_total(self):
        return self.__distancia_total


class Individuo:
    def __init__(self, medianas=[]):
        self.medianas = medianas

    def fitness(self):        
        aptidao = 0
        for mediana in self.medianas:
            aptidao += mediana.distancia_total()
        return aptidao

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
    
    def gerar_individuo(self, medianas):
        for v in self.vertices:
            if v not in medianas:
                melhor_mediana = None
                melhor_distancia = 9999999
                for mediana in medianas:
                    distancia = distancia_euclidianea(v.coordenada, mediana.vertice.coordenada)
                    if ((distancia < melhor_distancia)
                            and mediana.capacidade(v)):
                        melhor_distancia = distancia
                        melhor_mediana = mediana

                if melhor_mediana != None:
                    melhor_mediana.conjunto.add(v)

        return Individuo(medianas)
                
    def crossover(self, pai, mae):
        pai = deepcopy(pai)
        mae = deepcopy(mae)
        numero_medianas = len(pai.medianas)

        if (random.random() < self.pcross_over):              
            medianas_filho_1 = pai.medianas[:numero_medianas//2] + mae.medianas[numero_medianas//2:]
            medianas_filho_2 = mae.medianas[:numero_medianas//2] + pai.medianas[numero_medianas//2:]

            return (medianas_filho_1, medianas_filho_2)
        return (pai.medianas, mae.medianas)

    def mutacao(self, medianas):    
        if (random.random() < self.pmutacao):
             medianas_mutacao = medianas[:]
             nova_mediana = Mediana(get_random(self.vertices))
             while (nova_mediana in medianas_mutacao):
                 nova_mediana = Mediana(get_random(self.vertices))            
                         
             pop_random(medianas_mutacao)
             medianas_mutacao.append(nova_mediana)                                                
             return medianas_mutacao

        return medianas

    def reproduzir(self, selecionados):
        filhos = []
        size_selecionados = len(selecionados)
        for i in range(0, size_selecionados):
            pai = selecionados[i]
            if i == size_selecionados - 1:
                mae = selecionados[0]
            else:
                mae = selecionados[i + 1] if (i %
                                             2 == 0) else selecionados[i - 1]
            
            medianas_filho_1, medianas_filho_2 = self.crossover(pai, mae)
            medianas_filho_1 = self.mutacao(medianas_filho_1)
            medianas_filho_2 = self.mutacao(medianas_filho_2)
                        
            individuo_1 = self.gerar_individuo(medianas_filho_1)
            individuo_2 = self.gerar_individuo(medianas_filho_2)

            filhos.append(individuo_1)
            filhos.append(individuo_2)

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
            pprint(populacao.individuos.elements)

        melhor = populacao.melhor()
        print("Melhor inicial", melhor)
        while not self.parar():
            self.geracao += 1
            if DEBUG:
                print("População ")
                pprint(populacao.individuos.elements)
            selecionados = self.executar_torneio(populacao)            
            if DEBUG:
                print("Selecionados ")
                pprint(selecionados)
            
            filhos = self.reproduzir(selecionados)            
            if DEBUG:
                print("Filhos")
                pprint(filhos)                            

            queue = PriorityQueueIndividuo(filhos)            
            melhor_filho = queue.get()
            if DEBUG:
                print("Melhor filho ", melhor_filho)            
            
            if melhor_filho.fitness() < melhor.fitness():
                melhor = melhor_filho
            
            print("Melhor ", melhor)
            populacao = Populacao(selecionados + filhos)
            
        if DEBUG:
            print("População final", populacao)        
            pprint(populacao.individuos.elements)
        return melhor

if (__name__ == "__main__"):            
    linhas = open('teste2', 'r').readlines()        
    primeiralinha = linhas.pop(0).split()
        
    numero_de_pontos = int(primeiralinha[0])
    numero_medianas = int(primeiralinha[1])        
    vertices = []

    while linhas:                        
        x, y, capacidade, demanda = linhas.pop(0).split()        
        vertices.append(Vertice((int(x), int(y)), int(capacidade), int(demanda)))

    random.seed(10)    
    tamanho_populacao = 10
    quantidade_torneio = 9
    maximo_geracoes = 1000
    pcross_over = 0.90
    pmutacao = 0.5

    ag = AlgoritmoGenetico(
        vertices,
        tamanho_populacao,
        quantidade_torneio,
        maximo_geracoes,
        pcross_over,
        pmutacao
    )
        
    print("Melhor solução AG: ", ag.solucionar(numero_medianas))

