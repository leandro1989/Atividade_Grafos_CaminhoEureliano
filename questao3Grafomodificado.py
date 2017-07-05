# -*- coding: utf-8 -*-
from pip.cmdoptions import no_binary

from grafo123 import Grafo
n = ["a", "b", "c", "d"]
a = {"a1":"a-b", "a2":"b-c", "a3":"c-d", "a4":"d-a" }
grafo = Grafo(N=n, A=a);
matriz = grafo.colocaMatriz(a, n)

matriz2 = [[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]]

def naoAdjacente(n, matriz):
    listaNaoAdjacente = []
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == 0:
                listaNaoAdjacente.append(n[i]+"_"+n[j])
    print(listaNaoAdjacente)

def existeLaco(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if (i == j and matriz[i][j] == 1):
                return True
    return False

def verificaParalelo(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == matriz[j][i]:
                return True
    return False

def verificaGrau(matriz, vertice, n):
    indiceVertice = n.index(vertice)
    return matriz[indiceVertice].count(1)

def grafoCompleto(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if (j > i) and matriz[i][j] == 0:
                return False
    return True

def conexo(matriz, listaDeConbinacao):
    '''esta e a funcao principal para a questao do grafo ser conexo ou nao
    usando as funcoes arestaExistente(), procura(), conbinacoes()'''
    for k in range(len(matriz)):
        arestaAdja = arestaExistente(matriz, k)
        for i in range(len(arestaAdja[1])):
            if [arestaAdja[0], arestaAdja[1][i]] in listaDeConbinacao:
                del(listaDeConbinacao[listaDeConbinacao.index([arestaAdja[0], arestaAdja[1][i]])])
                if len(listaDeConbinacao) == 0:
                    return True

    for j in range(len(listaDeConbinacao)):
        if procura(listaDeConbinacao[j][1],listaDeConbinacao[j][0]) == True:
            listaDeConbinacao[j] = '#'

    if listaDeConbinacao.count("#") == len(listaDeConbinacao):
        return True
    else: return False
    
def procura(indiceDeProcura,procurado, procuradoAnterior = -1):
    '''procura um caminho de um no qualquer a outro, tambem e utilizada para
    procurar ciclos'''
    a = False
    l = arestaExistente(matriz,indiceDeProcura,procuradoAnterior)
    if procurado in l[1]:
        a = True
        return a
    else:
        try:
            novoIndiceDeProcura = l[1][0]
        except:
            return a
        procuradoAnterior = l[0]
        del(l[1][0])
        a = procura(indiceDeProcura=novoIndiceDeProcura,procurado=procurado, procuradoAnterior=procuradoAnterior)
    return a

def conbinacoes(matriz):
    '''retorna uma matriz com todas as conbinacoes possiveis de ligacoes entre os nos
    OBS.: nao retorna as ligacoes e sim as possibilidades de ligacoes'''
    conbinacao = []
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if i is not j and [j,i] not in conbinacao:
                conbinacao.append([i,j])
    return conbinacao

def arestaExistente(matriz, index, numeroHaSerRetirado=-1):
    '''funcao cuja finalidade e retornar uma matriz cuja sua representatividade e relacionar
    os vertices ligados EX.: o indice 0 e passado pelo parametro index dai entao e retornado
    todos os vertices em que 0 esta ligado diretamente
    retornando algo do tipo [0,[1,2,3,...n]] onde 0 e passado por parametro e [1,2,3,...n] sao
    os vertices ligados a 0'''
    arestaExiste = [index,[]]
    for i in range(len(matriz)):
        if matriz[index][i] == 1:
            arestaExiste[1].append(i)
        if matriz[i][index] == 1:
            arestaExiste[1].append(i)
    if numeroHaSerRetirado in arestaExiste[1]:
        try:
            del(arestaExiste[1][arestaExiste[1].index(numeroHaSerRetirado)])
        except:
            print()
    return arestaExiste

def caminhoAresta(valor, listacaminho, listaindex,tamanho, i=1):
    '''esta funcao usa de outras 4 funcoes ( tiraRepetido(), excluiRepetido(),
        engrauraUm() e salva Caminho) onde sua finalidade e engraurar o caminho de
        tamanho aleatorio passado pelo parametro tamanho'''
    if i == len(listaindex):
        return
    if valor[1] == listaindex[i][0]:
        if len(listacaminho) is not tamanho:
            tiraRepetido(listacaminho, valor, listaindex[i])
            excluirepetido(listacaminho)
        caminhoAresta(listaindex[i], listacaminho, listaindex,tamanho,i+1)
    caminhoAresta(valor, listacaminho, listaindex,tamanho, i+1)
    return

def tiraRepetido(lista, valor1, valor2):
    ''' esta funcao recebe uma lista e dois valores (valor1 e valor2)
        dai entao checa se valor1 ou valor2 estao na lista caso estejam
        nao inseri o valor que ja esteja na lista'''
    if valor1 not in lista:
        lista.append(valor1)
    if valor2 not in lista:
        lista.append(valor2)

def excluirepetido(lista):
    '''este trecho de codigo como o nome diz exclui o repetido recebendo uma lista
    como parametro... substitui o primeiro item repetido por ["-","-"] depois o exclui'''
    for i in range(len(lista)-1):
        if lista[i][0] == lista[i+1][0]:
            lista[i] = ["-","-"]
    for i in range(len(lista)):
        try:
            if lista[i] == ["-","-"]:
                del(lista[i])
        except:
            continue

def engrauraUM(matriz):
    '''esta funcao salva os indices de todas as arestas, ou seja, salva
    os indices onde tem 1'''
    listaIndex = []
    existeLigacao = 1
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == existeLigacao:
                listaIndex.append([i,j])
    return listaIndex

def salvaCaminho(x,y,n):
    '''retorna algo do tipo "A¹-A²" sendo A¹ e A² vertices '''
    return  n[x]+"-"+n[y]

def ligacao(matriz):
    ligacao = []
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == 1:
                ligacao.append([i,j])

    return ligacao

def criaMatriz(matriz1):
    matriz = []
    for i in range(len(matriz1)):
        matriz.append([])
        for j in range(len(matriz1)):
            matriz[i].append(None)
    return matriz

def max(pos_1, pos_2):
    if pos_1 != pos_2 or (pos_1 == 1 and pos_2 == 1):
        return 1
    return 0

def clone(matriz):
    matrizClone = criaMatriz(matriz)
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] != 1:
                matrizClone[i][j] = 0
            else: matrizClone[i][j] = 1
    return matrizClone

def warshall(matriz_adjacencia):
    E = clone(matriz_adjacencia)
    for i in range(len(E)):
        for j in range(len(E)):
            if E[j][i] == 1:
                for k in range(len(E)):
                    E[j][k] = max(E[j][k],E[i][k])
    return E

def transposta(matriz):
    matriz_transposta = criaMatriz(matriz)
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            matriz_transposta[i][j] = matriz[j][i]
    return matriz_transposta


def nosGrauImpar(matriz):
    grau = 0
    matriz_transposta = transposta(matriz)
    nosImpar = []
    for i in range(len(matriz)):
        grau += matriz[i].count(1)
        grau += matriz_transposta[i].count(1)
        if grau % 2 != 0:
            nosImpar.append(i)
        grau = 0

    return nosImpar

def euleriano(matriz):
    ligacaos = ligacao(matriz)
    nosInpar = nosGrauImpar(matriz)
    proximoNo = None
    caminho = []
    if nosInpar == 2:
        caminho = [nosInpar[0]]
        proximoNo = nosInpar[0]
    i = 0
    if conexo(matriz,conbinacoes(matriz)) == True:
        while ligacaos != [["#","#"]]*len(ligacaos):
            if len(nosInpar) == 0:
                caminho.append(ligacaos[i][0])
                caminho.append(ligacaos[i][1])
                proximoNo = ligacaos[i][1]
                ligacaos[i] = ["#","#"]
                while ligacaos != [["#","#"]]*len(ligacaos):
                    if proximoNo == ligacaos[i][0]:
                        caminho.append(ligacaos[i][1])
                        proximoNo = ligacaos[i][1]
                        ligacaos[i] = ["#", "#"]
                        i = -1

                    elif proximoNo == ligacaos[i][1]:
                        caminho.append(ligacaos[i][0])
                        proximoNo = ligacaos[i][0]
                        ligacaos[i] = ["#", "#"]
                        i = -1

                    i += 1

            elif len(nosInpar) == 2:
                if proximoNo == ligacaos[i][0]:
                    proximoNo = ligacaos[i][1]
                    caminho.append(ligacaos[i][1])
                    ligacaos[i] = ["#","#"]
                    i=-1
                elif proximoNo == ligacaos[i][1]:
                    proximoNo = ligacaos[i][0]
                    caminho.append(ligacaos[i][0])
                    ligacaos[i] = ["#", "#"]
                    i=-1
            i += 1
    return caminho

for i in range(len(matriz)):
    for j in range(len(matriz)):
        print(matriz[i][j], end=" ")
    print('')

print("-----------------------------")
#print(ligacao(matriz))
for i in range(len(matriz2)):
    e = warshall(matriz2)
    print(e[i])

print("-----------------------------")
for i in range(len(matriz2)):
    print(matriz2[i])