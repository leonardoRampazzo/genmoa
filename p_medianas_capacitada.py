import math
import heapq
import random


def pop_random(values):
    return values.pop(random.randrange(len(values)))


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
        return heapq.heappop(self.elements)[1]

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

    def __cmp__(self, other):
        return ((self.fitness() > other.fitness()) - (self.fitness() < other.fitness()))

    def __str__(self):
        return "Invididuo({}, {})".format(str(medianas), str(self.fitness()))

    def __repr__(self):
        return self.__str__()


class Populacao:
    def __init__(self, individuos=[]):
        self.individuos = PriorityQueueIndividuo(individuos)

    def __str__(self):
        return "População({})".format(str(self.individuos.elements))

    def __repr__(self):
        return self.__str__()

    def melhor(self):
        return self.individuos.peak(1)

    def tamanho(self):
        return self.individuos.size()

    def melhores(self, n):
        return self.individuos.peak(n)


class AlgoritmoGenetico:
    def __init__(self, vertices, tamanho_populacao,
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
        for i in range(self.tamanho_populacao):
            medianas = []
            vertices = self.vertices
            for j in range(numero_medianas):
                mediana = Mediana(pop_random(vertices))
                v = pop_random(vertices)
                while (vertices
                       and mediana.capacidade(v)):
                    if mediana.vertice != v:
                        mediana.adicionar_vertice(v)
                    v = pop_random(vertices)
                medianas.append(mediana)
            invididuos.append(Individuo(medianas))
        return Populacao(invididuos)

    def executar_torneio(self, populacao):
        return populacao.melhores(self.quantidade_torneio)

    def crossover(self, pai1, pai2):
        pass

    def mutacao(self, individuo):
        pass

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

            filho = self.crossover(p1, p2)
            filho = self.mutacao(filho)

            filhos.append(filho)
            if len(filhos) >= self.quantidade_torneio:
                break

        return filhos

    def solucionar(self, numero_medianas):
        if len(self.vertices) <= 0:
            return False

        self.geracao = 0
        print("População inicial")
        populacao = self.gerar_populacao_inicial(numero_medianas)
        print("População inicial", populacao)
        print("População inicial")
        melhor = populacao.melhor()
        while not self.parar():
            self.geracao += 1
            selecionados = self.executar_torneio(populacao)
            filhos = self.reproduzir(selecionados)

            queue = PriorityQueueIndividuo(filhos)
            melhor_filho = queue.get()

            if melhor.fitness() < melhor_filho.fitness():
                melhor = populacao.melhor()

            populacao = Populacao(selecionados)


if (__name__ == "__main__"):
    m1 = Mediana(Vertice((1, 1), 120, 1))
    m1.adicionar_vertice(Vertice((2, 2), 120, 15))
    m1.adicionar_vertice(Vertice((3, 3), 120, 7))

    m2 = Mediana(Vertice((4, 4), 120, 15))
    m2.adicionar_vertice(Vertice((1, 4), 120, 2))
    m2.adicionar_vertice(Vertice((4, 1), 120, 8))

    print(m1.vertice.coordenada)
    print(m1.distancia_total())
    print(m1.demanda_atual())
    print(m2.vertice.coordenada)
    print(m2.distancia_total())
    print(m2.demanda_atual())

    medianas = [m1, m2]

    vertices = [
        Vertice((1, 1), 120, 1),
        Vertice((2, 2), 120, 15),
        Vertice((3, 3), 120, 7),
        Vertice((4, 4), 120, 15),
        Vertice((1, 4), 120, 2),
        Vertice((4, 1), 120, 8),
    ]
    tamanho_populacao = 1
    quantidade_torneio = 100
    maximo_geracoes = 1000
    pcross_over = 0.98
    pmutacao = 0.05
    numero_medianas = 1

    ag = AlgoritmoGenetico(
        vertices,
        tamanho_populacao,
        quantidade_torneio,
        maximo_geracoes,
        pcross_over,
        pmutacao
    )

    print(ag.solucionar(numero_medianas))

    """
    for v1 in g.vertices:
        print(v1.coordenada)
        for v2 in g.vertices:
            print(v2.coordenada)
            print(g.distancia(v1, v2))
    """
