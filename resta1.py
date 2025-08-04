
import pygame
import random
import copy

# --- Constantes do jogo ---
TAM_CELULA = 60
TAM_TAB = 7
LARGURA = ALTURA = TAM_CELULA * TAM_TAB
FPS = 10

# --- Cores ---
CINZA = (220, 220, 220)
AZUL = (0, 120, 255)
VERDE = (0, 200, 0)
FUNDO = (30, 30, 30)

# Direções possíveis: cima, baixo, esquerda, direita
DIRECTIONS = [(-2,0),(2,0),(0,-2),(0,2)]
FIRST_PLAY = [[(1, 3),(3, 3)]]

# Algoritmo genético
POP_SIZE = 60
SEQ_SIZE = 40
GENS = 100
MUT_RATE = 0.2
ELITISM = 5

# --- Funções de tabuleiro e jogo ---

# Mostra visualmente o estado atual do tabuleiro.
def desenhar_tabuleiro(tab):
    tela.fill((30, 30, 30))
    for i in range(7):
        for j in range(7):
            x = j * TAM_CELULA
            y = i * TAM_CELULA
            if tab[i][j] == -1:
                continue
            rect = pygame.Rect(x+5, y+5, TAM_CELULA-10, TAM_CELULA-10)
            pygame.draw.rect(tela, CINZA, rect, border_radius=8)
            if tab[i][j] == 1:
                pygame.draw.circle(tela, AZUL, rect.center, TAM_CELULA // 2 - 8)
            elif tab[i][j] == 0:
                pygame.draw.circle(tela, (0, 0, 0), rect.center, TAM_CELULA // 2 - 8)
    pygame.display.flip()
    clock.tick(FPS)

# Executa um movimento: remove pinos envolvidos e posiciona novo pino.
def atualizar_tabuleiro(tab, movimento):
    si, sj = movimento[0]
    i, j = movimento[1]
    tab[si][sj] = 0
    tab[(si+i)//2][(sj+j)//2] = 0
    tab[i][j] = 1

# Conta quantos pinos restam no tabuleiro
def contar_pinos(tab):
    return sum(cell == 1 for row in tab for cell in row)

# --- Tabuleiro Padrão ---

# Retorna o layout inicial do tabuleiro do jogo
X = -1
def tabuleiro_inicial():
    return [
        [X, X, 1, 1, 1, X, X],
        [X, X, 1, 1, 1, X, X],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [X, X, 1, 1, 1, X, X],
        [X, X, 1, 1, 1, X, X]
    ]

# Gera todos os movimentos válidos no estado atual do tabuleiro
# Analisa para cada célula se é possível mover nas direções permitidas
def movimentos_possiveis(tab):
    movimentos = []
    for i in range(7):
        for j in range(7):
            if tab[i][j] == 1:
                for dx, dy in DIRECTIONS:
                    ni, nj = i + dx, j + dy
                    mi, mj = i + dx//2, j + dy//2
                    if 0 <= ni < 7 and 0 <= nj < 7 and tab[ni][nj] == 0 and tab[mi][mj] == 1:
                        movimentos.append(((i, j), (ni, nj)))
    return movimentos

# --- Prioridade quadrantes laterais e proximidade ---

# Identifica se uma posição está nas bordas/laterais do tabuleiro
def quadrante_lateral(pos):
    i, j = pos
    return (j in [0,1,2] or j in [4,5,6] or i in [0,1,2] or i in [4,5,6])

# Verifica se o movimento está próximo ao anterior (para dar preferência a sequências contínuas)
def proximo_ao_anterior(pos, anterior, dist=2):
    if anterior is None:
        return True
    return abs(pos[0] - anterior[0]) <= dist and abs(pos[1] - anterior[1]) <= dist

# Seleciona um movimento priorizando quadrantes laterais e proximidade ao movimento anterior
# Utiliza aleatoriedade quando há múltiplas opções
def gerar_movimento_priorizado(tab, anterior=None):
    movs = movimentos_possiveis(tab)
    if not movs:
        return None
    laterais = [m for m in movs if quadrante_lateral(m[1])]
    proximos = [m for m in laterais if proximo_ao_anterior(m[1], anterior)]
    if proximos:
        return random.choice(proximos)
    elif laterais:
        return random.choice(laterais)
    else:
        proximos = [m for m in movs if proximo_ao_anterior(m[1], anterior)]
        if proximos:
            return random.choice(proximos)
        return random.choice(movs)

# --- Algoritmo Genético ---

# Cria um indivíduo (sequência de movimentos) de forma priorizada, usando as estratégias anteriores
def gerar_individuo_priorizado(tab):
    individuo = FIRST_PLAY
    t = copy.deepcopy(tab)
    anterior = None
    for _ in range(SEQ_SIZE):
        mov = gerar_movimento_priorizado(t, anterior)
        if mov:
            individuo.append(mov)
            atualizar_tabuleiro(t, mov)
            anterior = mov[1]
        else:
            break
    return individuo

# Executa a sequência de movimentos do indivíduo no tabuleiro e retorna a quantidade de pinos restantes (fitness)
def avaliar_individuo(tab, individuo):
    t = copy.deepcopy(tab)
    for mov in individuo:
        if mov in movimentos_possiveis(t):
            atualizar_tabuleiro(t, mov)
        else:
            break
    # Penalização: quanto menos pinos melhor
    return contar_pinos(t)

# Realiza cruzamento entre dois indivíduos, gerando um novo filho
def crossover(ind1, ind2):
    ponto = random.randint(1, min(len(ind1), len(ind2))-1) if min(len(ind1), len(ind2)) > 1 else 0
    filho = ind1[:ponto] + ind2[ponto:]
    return filho

# Aplica mutações nos movimentos do indivíduo com base na taxa de mutação, garantindo que os movimentos continuem válidos
def mutacao(individuo, tab):
    t = copy.deepcopy(tab)
    anterior = None
    for i, mov in enumerate(individuo):
        if random.random() < MUT_RATE:
            movs = movimentos_possiveis(t)
            if movs:
                novo_mov = gerar_movimento_priorizado(t, anterior)
                if novo_mov:
                    individuo[i] = novo_mov
        if individuo[i] in movimentos_possiveis(t):
            atualizar_tabuleiro(t, individuo[i])
            anterior = individuo[i][1]
        else:
            break
    return individuo

# Ciclo principal do algoritmo genético:
# - Inicialização da população
# - Avaliação e seleção dos melhores (elitismo)
# - Cruzamento e mutação para gerar nova população
# - Parada quando encontra solução ótima ou chega ao número máximo de gerações
# - Exibe histórico de evolução das gerações e melhor solução encontrada
def algoritmo_genetico():
    tab = tabuleiro_inicial()
    populacao = [gerar_individuo_priorizado(tab) for _ in range(POP_SIZE)]
    historico_melhor = []

    for gen in range(GENS):
        populacao = sorted(populacao, key=lambda x: avaliar_individuo(tab, x))
        nova_pop = populacao[:ELITISM]  # Elitismo
        while len(nova_pop) < POP_SIZE:
            pais = random.sample(populacao[:20], 2)
            filho = crossover(pais[0], pais[1])
            filho = mutacao(filho, tab)
            nova_pop.append(filho)
        populacao = nova_pop
        melhor = populacao[0]
        melhor_pinos = avaliar_individuo(tab, melhor)
        historico_melhor.append(melhor_pinos)
        print(f"Geração {gen+1} | Melhor: {melhor_pinos} pinos")
        if melhor_pinos == 1:
            print("Solução ótima encontrada!")
            break

    # Resultado final
    print("Melhor sequência encontrada:", populacao[0])
    print("Pinos restantes:", avaliar_individuo(tab, populacao[0]))
    return populacao[0]

# --- Visualização da solução genética ---

# Executa a sequência de movimentos encontrada pelo algoritmo genético, mostrando passo a passo no tabuleiro gráfico
# Exibe mensagem final com quantidade de pinos restantes
def mostrar_solucao(tab, movimentos):
    t = copy.deepcopy(tab)
    desenhar_tabuleiro(t)
    pygame.time.wait(1000)
    for mov in movimentos:
        if mov in movimentos_possiveis(t):
            atualizar_tabuleiro(t, mov)
            desenhar_tabuleiro(t)
            pygame.time.wait(350)
        else:
            break
    # Mensagem final
    font = pygame.font.SysFont(None, 48)
    texto = font.render(f'Fim! Pinos restantes: {contar_pinos(t)}', True, (255,255,0))
    tela.blit(texto, (30, LARGURA//2-24))
    pygame.display.flip()
    pygame.event.pump()
    pygame.time.wait(5000)


# --- Função Principal e Execução ---

# Executa o algoritmo genético, inicializa o pygame, mostra a solução visualmente e finaliza o programa
def main():
    global tela, clock

    print("Executando algoritmo genético para buscar solução...")
    movimentos = algoritmo_genetico()

    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Resta 1 - Algoritmo Genético")
    clock = pygame.time.Clock()

    # Mostra a solução encontrada no tabuleiro
    tab = tabuleiro_inicial()
    mostrar_solucao(tab, movimentos)

    pygame.quit()

if __name__ == "__main__":
    main()
