import math
import heapq
import random

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
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

class Populacao: 
    def __init__(self, individuos = []):        
        self.individuos = PriorityQueue
        for individuo in individuos:
            self.individuos.put(individuo)    

    def melhor(self):
        return self.individuos.peak(1)

    def tamanho(self):
        return self.individuos.size()

    def melhores(self, n):
        return self.individuos.peak(n)


class Selecao:
    def executarTorneio(populacao, quantidade):
        qtde_populacao = populacao.tamanho()
        qtde_participantes = qtde_populacao        
        if (qtde_populacao > quantidade):           
            qtde_participantes = (quantidade + random.randrange(qtde_populacao - quantidade))        
                               
        
        participantes = populacao.melhores(qtde_participantes);
        
        Comparator<Individuo> c = new Individuo();
        Arrays.sort(participantes, c);
        
        System.arraycopy(participantes, 0, vencedores, 0, quantidade);        
        return vencedores;
    }
}

class AlgoritmoGenetico:
    def __init__(self, vertices):        
        self.vertices = vertices
        self.geracao = 0        

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
        return Populacao()

    def parar(self):
        return True
    
    def solucionar(self):
        self.geracao = 0;                
        melhor_solucao = Individuo()
        populacao = self.gerar_populacao_inicial()                                                        
        melhor = populacao.melhor()                    
        while (not self.parar()):
            self.geracao += 1
            vencedores = []
            filhos = []
            
            vencedores = selecionador.executarTorneio(populacao, Util.QUANTIDADE_INDIVIDUOS_TORNEIO);            
            filhos = cruzamento.executar(vencedores, melhor != populacao.getIndividuo(0));
            filhos = mutacao.executar(filhos);                        
            populacao.atualizar(filhos);       
            if (this.tipoBuscaLocal == 1)
                populacao.setIndividuo(0, buscaLocal.firstFit(populacao.getIndividuo(0)));                                                          
            if (melhor != populacao.getIndividuo(0)){
                if (this.tipoBuscaLocal == 2)                
                    populacao.setIndividuo(0, buscaLocal.hillClimbing(populacao.getIndividuo(0)));           
                melhor = populacao.getIndividuo(0);
                this.printMelhorInvidivuo(populacao);
                this.repeticaoMelhor = 0;                
            } 
            else repeticaoMelhor++;            
        }

        this.printMelhorInvidivuo(populacao);
        return melhor;        
                
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