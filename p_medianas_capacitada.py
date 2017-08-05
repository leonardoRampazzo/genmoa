import math

class Vertice:
    def __init__(self, coordenada, demanda, capacidade):        
        self.coordenada = coordenada
        self.demanda = demanda
        self.capacidade = capacidade

class Mediana:
    def __init__(self, vertice, conjunto):        
        self.vertice = vertice
        self.conjunto = conjunto
        self.__distancias = {}        

    def distancia(self, v1, v2):
        aresta = (v1, v2)
        if not aresta in self.__distancias:
            xa, ya = v1.coordenada
            xb, yb = v2.coordenada
            self.__distancias[aresta] = math.sqrt(math.pow((xa - xb), 2) + math.pow((ya - yb), 2))        
        return self.__distancias[aresta]

    def somar_distancia(self):        
        self.__soma = 0
        for vc in self.conjunto:
            self.__soma += self.distancia(self.vertice, vc)
        return self.__soma       
        
    def cardinalidade(self):
        return len(self.conjunto)

        
m1 = Mediana(
    Vertice((1, 1), 120, 1),
    [
        Vertice((2, 2), 120, 15),
        Vertice((3, 3), 120, 7)
    ]
)

m2 = Mediana(
    Vertice((4, 4), 120, 15),
    [
        Vertice((1, 4), 120, 2),
        Vertice((4, 1), 120, 8)
    ]

)
print(m1.vertice.coordenada)
print(m1.somar_distancia())
print(m2.vertice.coordenada)
print(m2.somar_distancia())

medianas = [m1, m2]

"""
for v1 in g.vertices:
    print(v1.coordenada)
    for v2 in g.vertices:
        print(v2.coordenada)
        print(g.distancia(v1, v2))
"""