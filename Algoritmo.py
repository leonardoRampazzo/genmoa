import random
import math
import heapq
import time
from pprint import pprint

# BLOCO DE CLASSES DO ESTADO E VARIÁVEIS
verticelist = []
entrada = []
passosSeq = []
populacao = []
listaCruzamento = []
tamPopulacao = 10
numTentativas = 0
solucaoBetter = True


class Vertice:
    def __init__(self, coordenada, capacidade, demanda):
        self.coordenada = coordenada
        self.capacidade = capacidade
        self.demanda = demanda        

    def __str__(self):
        return "Vertice({}, {}, {})".format(
            str(self.coordenada),
            str(self.capacidade),
            str(self.demanda)            
        )

    def __repr__(self):
        return self.__str__()

class Mediana:
    def __init__(self, vertice):
        self.vertice = vertice
        self.conjunto = set([])
        self.__distancias = {}
        self.__demanda = 0
        self.__distancia_total = 0

    def __str__(self):
        return "Mediana({}: {})".format(str(vertice), str(self.conjunto))

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

    def somar_distancia(self):
        return self.__distancia_total

    def cardinalidade(self):
        return len(self.conjunto)


class Individuo:
    def __init__(self, medianas=[]):
        self.medianas = medianas

    def fitness(self):
        aptidao = 0
        for mediana in self.medianas:
            aptidao += mediana.distancia_total

        return aptidao

    def get_medianas(self):
        return self.medianas


def geraPopulacao(verticelist):
    populacao = []

    for j in range(tamPopulacao):
        lista_medianas = []

        if(verticelist):
            for i in range(numero_medianas):
                vertice = verticelist.pop(random.randrange(len(verticelist)))
                mediana = Mediana(vertice)
                lista_medianas.append(mediana)

        indice = 0
        i = 0
        while(verticelist and lista_medianas):
            v = verticelist.pop(random.randrange(len(verticelist)))

            if(lista_medianas[indice].capacidade(v)):
                lista_medianas[indice].adicionar_vertice(v)
            else:
                lista_medianas[indice].pop()

            i += 1
            indice = (i % len(lista_medianas))
        
        individuo = Individuo(lista_medianas)
        populacao.append(individuo)
    
    return populacao

def selectRota(pPopulacao):
    vRandom1 = random.randrange(tamPopulacao // 2)
    vRandom2 = random.randrange(tamPopulacao // 2)

    if pPopulacao[vRandom1].custo() < pPopulacao[vRandom2].custo():
        return pPopulacao[vRandom1].caminho
    else:
        return pPopulacao[vRandom2].caminho


def geraCruzamento(pSolucaoA, pSolucaoB):
    global tamPopulacao
    global tamConjunto

    listaCruzamento = []
    contador = 0
    qtGeracoes = int(tamPopulacao * 0.8)
    tamanhoCorte = int(tamConjunto * 0.95)
    while contador < qtGeracoes:

        novoCaminho = pSolucaoA[:tamanhoCorte]
        qtAdicionados = 0
        for i in pSolucaoB:
            if qtAdicionados == (tamConjunto - tamanhoCorte):
                break
            if i not in novoCaminho:
                novoCaminho.append(i)
                qtAdicionados += 1

        novoCaminho = mutacaoCaminho(novoCaminho)  # Mutação
        cruzamento = Solucao()
        cruzamento.caminho = novoCaminho
        cruzamento = buscaLocal(cruzamento)  # Busca Local - First Improvement
        listaCruzamento.append(cruzamento)
        contador += 1

    return listaCruzamento


def mutacaoCaminho(pCaminho):
    p1 = random.randrange(tamConjunto - 1)
    p2 = random.randrange(p1, tamConjunto - 1)
    pCaminho[p1], pCaminho[p2] = pCaminho[p2], pCaminho[p1]
    return pCaminho


def geraVizinho(pCaminho, pContador):
    caminho = pCaminho[:]
    (caminho[pContador], caminho[pContador + 1]
     ) = (caminho[pContador + 1], caminho[pContador])
    return caminho


def buscaLocal(pCruzamento):
    i = 0
    vizinho = Solucao()
    for i in range(tamConjunto // 2):
        vizinho.caminho = geraVizinho(pCruzamento.caminho, i)
        if vizinho.custo() < pCruzamento.custo():
            pCruzamento = vizinho
            break

    return pCruzamento


def atualizaPopulacao(pPopulacao, pListaCruzamento):
    global solucaoBetter
    global numTentativas

    for cruzamento in pListaCruzamento:
        maior = heapq.nlargest(1, pPopulacao)[0]
        menor = pPopulacao[0]

        custoCruzamento = cruzamento.custo()
        if (custoCruzamento < maior.custo()):
            pPopulacao.remove(maior)
            heapq.heappush(pPopulacao, cruzamento)
            heapq.heapify(pPopulacao)

            if (custoCruzamento < menor.custo()):
                numTentativas = 0
            else:
                numTentativas += 1
        else:
            numTentativas += 1

        if (numTentativas == 700):
            solucaoBetter = False

    return pPopulacao


def obtemMenor(pPopulacao):
    return pPopulacao[0].custo()

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

    populacao = geraPopulacao(vertices)

    print(populacao)



    # Parte para enviar
    # primeiralinha = input()
    # primeiralinha = primeiralinha.split()

    # random.seed()

    # numero_de_pontos   = int(primeiralinha[0])
    # numero_de_medianas = int(primeiralinha[1])

    # entrada = []
    # verticelist = []

    # for i in range(numero_de_pontos):
    #     a = input()
    #     entrada.append(a)

    # for i in range(numero_de_pontos):
    #     vList = entrada[i].split()
    #     vertice = Vertice((float(vList[0]), float(vList[1])), int(vList[2]), int(vList[3]))
    #     verticelist.append(vertice)

