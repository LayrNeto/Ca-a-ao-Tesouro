#@title Funções geradores de imagem
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from collections import defaultdict
import heapq


def print_mapa(grid, caminho=[], title=""):
    """
    Esta função gera uma representação visual do mapa usando matplotlib.
    """
    cores = [
        "#9c5a3c",  # Nada
        "#3d1e10",  # Obstaculo
        "#FFCA00",  # Tesouro
        "#EBCF87",  # Caminho
        "#EBAD87"   # Lama
    ]

    grid_cores = {
        '.': 0,  # Vazio
        '#': 1,  # Obstaculo
        'I': 0,  # Inicio
        'T': 2,  # Tesouro
        '*': 3,  # Caminho
        'L': 4   # Lama
    }

    # cria um colormap personalizado
    cmap = ListedColormap(cores)

    n, m = len(grid), len(grid[0])
    map_visual = np.zeros((n, m))

    # Conte quantas vezes cada célula é visitada no caminho
    path_indices = defaultdict(list)

    for idx, pos in enumerate(caminho):
        path_indices[pos].append(idx)

    for i in range(n):
        for j in range(m):
            # Altera as cores das celulas que estao no caminho
            if (i, j) in caminho:
                if grid[i][j] == 'I':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == 'T':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == '.':
                    map_visual[i][j] = grid_cores['*']
                elif grid[i][j] == 'L':
                    map_visual[i][j] = grid_cores['*']
                else:
                    map_visual[i][j] = grid_cores[grid[i][j]]
            else:
                map_visual[i][j] = grid_cores.get(grid[i][j], 0)

    if title:
        plt.title(title)
    # Plota o mapa
    plt.imshow(map_visual, cmap=cmap, vmin=0, vmax=len(cores) - 1)

    # Adicionar anotações de texto a cada célula
    for i in range(n):
        for j in range(m):
            # Exibir o indice do caminho no canto inferior direito se a celula estiver no caminho
            if (i, j) in path_indices:
                index = ", ".join(map(str, path_indices[(i, j)]))
                plt.text(j + 0.35, i + 0.35, index, ha='right', va='bottom', color='red', fontsize=4)
                plt.text(j, i, grid[i][j], ha='center', va='center', color='black', fontsize=12, fontweight='bold')
            else:
               plt.text(j, i, grid[i][j], ha='center', va='center', color='white', fontsize=12, fontweight='bold')

    plt.grid(which='both', color='black', linestyle='-', linewidth=2)
    plt.xticks(np.arange(-0.5, m, 1), [])
    plt.yticks(np.arange(-0.5, n, 1), [])

    # Mostra o mapa
    plt.show()


def print_caminho(grid, caminho, title=""):
    """
    Esta função recebe uma matriz e um caminho como argumentos e mostra o caminho percorrido na matriz.
    """
    # Cria uma copia da grade para evitar modificar a original
    grid_copia = [linha[:] for linha in grid]

    # Marque o caminho com '*'
    for (x, y) in caminho:
        if grid_copia[x][y] == '.':  # Marca apenas celulas vazias
            grid_copia[x][y] = '*'

    print_mapa(grid_copia, caminho, title)


def busca_custo_uniforme(grid, pos_inicial, pos_tesouro):
    visitados = set()
    fila = []  
    caminho = {} 

    heapq.heappush(fila, (0, pos_inicial))
    caminho[pos_inicial] = None  

    linhas = len(grid)
    colunas = len(grid[0])

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    while fila:
        custo_atual, pos_atual = heapq.heappop(fila)
        x_atual, y_atual = pos_atual


        if pos_atual == pos_tesouro:
            caminho_encontrado = []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual = caminho[pos_atual]
            caminho_encontrado.reverse()
            return caminho_encontrado

        if pos_atual in visitados:
            continue

        visitados.add(pos_atual)

        for x, y in direcoes:
            x_adjacente, y_adjacente = x_atual + x, y_atual + y

            # Se o nó adjacente está dentro do escopo de valores e ainda não foi visitado
            if (0 <= x_adjacente < linhas) and (0 <= y_adjacente < colunas) and ((x_adjacente, y_adjacente) not in visitados):
                if grid[x_adjacente][y_adjacente] != '#':
                    if grid[x_adjacente][y_adjacente] == 'L':
                        custo_novo = custo_atual + 5  
                    else: 
                        custo_novo = custo_atual + 1 
                        
                    heapq.heappush(fila, (custo_novo, (x_adjacente, y_adjacente)))
                    if (x_adjacente, y_adjacente) not in caminho or custo_novo < custo_atual:
                        caminho[(x_adjacente, y_adjacente)] = pos_atual

    return []


def busca_gulosa(grid, pos_inicial, pos_tesouro):
    visitados = set()
    fila = []  
    caminho = {} 

    def heuristica(pos):
        return abs(pos[0] - pos_tesouro[0]) + abs(pos[1] - pos_tesouro[1])
    
    heapq.heappush(fila, (heuristica(pos_inicial), pos_inicial))
    caminho[pos_inicial] = None  

    linhas = len(grid)
    colunas = len(grid[0])

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    while fila:
        _, pos_atual = heapq.heappop(fila)
        x_atual, y_atual = pos_atual


        if pos_atual == pos_tesouro:
            caminho_encontrado = []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual = caminho[pos_atual]
            caminho_encontrado.reverse()
            return caminho_encontrado

        if pos_atual in visitados:
            continue

        visitados.add(pos_atual)

        for x, y in direcoes:
            x_adjacente, y_adjacente = x_atual + x, y_atual + y

            # Se o nó adjacente está dentro do escopo de valores e ainda não foi visitado
            if (0 <= x_adjacente < linhas) and (0 <= y_adjacente < colunas) and ((x_adjacente, y_adjacente) not in visitados):
                if grid[x_adjacente][y_adjacente] != '#':
                    pos_adjacente = (x_adjacente, y_adjacente)                        
                    heapq.heappush(fila, (heuristica(pos_adjacente), pos_adjacente))
                   
                    if pos_adjacente not in caminho:
                        caminho[pos_adjacente] = pos_atual

    return []   
        


def busca_a_estrela(grid, pos_inicial, pos_tesouro):
    visitados = set()
    fila = []  
    caminho = {} 

    def manhattan(pos):
        return abs(pos[0] - pos_tesouro[0]) + abs(pos[1] - pos_tesouro[1])
    
    heapq.heappush(fila, (manhattan(pos_inicial), 0, pos_inicial))
    caminho[pos_inicial] = (0, None)

    linhas = len(grid)
    colunas = len(grid[0])

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]


    while fila:
        _, custo_acumulado, pos_atual = heapq.heappop(fila)
        x_atual, y_atual = pos_atual


        if pos_atual == pos_tesouro:
            caminho_encontrado = []
            while pos_atual is not None:
                caminho_encontrado.append(pos_atual)
                pos_atual = caminho[pos_atual][1]
            caminho_encontrado.reverse()
            return caminho_encontrado

        if pos_atual in visitados:
            continue

        visitados.add(pos_atual)

        for x, y in direcoes:
            x_adjacente, y_adjacente = x_atual + x, y_atual + y

            if (0 <= x_adjacente < linhas) and (0 <= y_adjacente < colunas):
                if grid[x_adjacente][y_adjacente] != '#':
                    if grid[x_adjacente][y_adjacente] == 'L':
                        custo_novo = custo_acumulado + 5  
                    else: 
                        custo_novo = custo_acumulado + 1 

                    pos_adjacente = (x_adjacente, y_adjacente)                        
                    heuristica_adjacente = manhattan(pos_adjacente)

                    total = heuristica_adjacente + custo_acumulado

                    if pos_adjacente not in caminho or custo_novo < caminho[pos_adjacente][0]:
                        caminho[pos_adjacente] = (custo_novo, pos_atual)
                        heapq.heappush(fila, (total, custo_novo, pos_adjacente))
    
    return []   


def main():
    mapa = [
        ['I', '#', '.', '#', 'L', 'L', 'T'],
    ['.', '#', '.', '#', 'L', '#', '.'],
    ['.', '#', '.', '#', 'L', '#', '.'],
    ['.', '#', '.', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '.', '.', '#', '.', '.', '.'],
    ]
    
    posicao_inicial = tuple(map(int, input("Digite a posição inicial (X Y): ").split()))
    posicao_tesouro = tuple(map(int, input("Digite a posição do tesouro (X Y): ").split()))

    caminho_bcu = busca_custo_uniforme(mapa, posicao_inicial, posicao_tesouro)
    caminho_gulosa = busca_gulosa(mapa, posicao_inicial, posicao_tesouro)
    caminho_a_estrela = busca_a_estrela(mapa, posicao_inicial, posicao_tesouro)

    print_caminho(mapa, caminho_bcu, "Custo uniforme")
    print_caminho(mapa, caminho_gulosa, "Gulosa")
    print_caminho(mapa, caminho_a_estrela, "A*")
  
main()

