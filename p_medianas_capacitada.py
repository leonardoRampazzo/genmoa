import math

class Vertice:
    def __init__(self, coordenada, capacidade, demanda):        
        self.coordenada = coordenada
        self.demanda = demanda
        self.capacidade = capacidade

class Mediana:
    def __init__(self, vertice, conjunto = set([])):
        self.vertice = vertice
        self.conjunto = conjunto
        self.__distancias = {}
        self.__demanda = 0
        self.__distancia_total = 0        
        if len(conjunto) != 0:                    
            for v in conjunto:
                self.__demanda += v.demanda
                self.__distancia_total += self.distancia(self.vertice, v)

    def adicionar_vertice(self, v):
        self.conjunto.add(v)
        self.__demanda += v.demanda
        self.__distancia_total += self.distancia(self.vertice, v)

    def capacidade(self, v1):                
        return self.vertice.capacidade >= (self.demanda_atual + v1.demanda)

    def demanda_atual(self):
        return self.__demanda

    def distancia(self, v1, v2):
        aresta = (v1, v2)
        if not aresta in self.__distancias:
            xa, ya = v1.coordenada
            xb, yb = v2.coordenada
            self.__distancias[aresta] = math.sqrt(math.pow((xa - xb), 2) + math.pow((ya - yb), 2))
        return self.__distancias[aresta]

    def distancia_total(self):
        return self.__distancia_total

class Individuo:
    def __init__(self, medianas = []):
        self.medianas = medianas        

    def fitness(self):        
        aptidao = 0
        for mediana in self.medianas:
            aptidao += mediana.distancia_total

        return aptidao

class AlgoritmoGenetico:
    def __init__(self, vertices):
        self.medianas = set([])
        self.vertices = vertices
        self.valor_solucao = 0

    def gerar_nova_mediana(self, vertice, mediana):
        novo_conjunto = mediana.conjunto.discard(vertice)
        novo_conjunto.add(mediana.vertice)

        nova_mediana = Mediana(vertice)        
        for v in novo_conjunto:
            if not nova_mediana.capacidade(v):
                return None

            nova_mediana.adicionar_vertice(v)                            

        return nova_mediana
    
    def gerar_populacao_inicial(self):
        pass

    def solucao_melhor(self, valor):
        return valor < self.valor_solucao

    def solucionar(self):
        self.gerar_populacao_inicial()
        pass
                

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

    """
    for v1 in g.vertices:
        print(v1.coordenada)
        for v2 in g.vertices:
            print(v2.coordenada)
            print(g.distancia(v1, v2))
    """