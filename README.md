# Tech Challenge2 - 5IADT
Tech Challenge - Fase 2: Exemplo de uso de IA Genetica para solução do jogo de Resta 1
da Pos Tech em IA para Devs da FIAP, 2025, conduzido pelo professor Sergio Polimante

Flavio Luiz Vicco - RM 361664

https://youtu.be/Ti9cvsEYWw8

![resta1](https://github.com/user-attachments/assets/3ef28afd-e988-4259-843b-45460c62706a)

> Olá, pessoal! Eu sou o Flavio Vicco e hoje vou apresentar o Tech Challenge da Fase 2 da Pos Tech em IA para Devs da FIAP, 2025, conduzido pelo professor Sergio Polimante.
Vou mostrar como aplicar um algoritmo genético para resolver o clássico jogo Resta 1, utilizando Python. Vamos juntos entender, na prática, cada passo dessa solução?

## 1. Apresentação do Problema
> Antes de mais nada, para quem não conhece: o objetivo do jogo Resta 1 é terminar com apenas um pino no tabuleiro. Ele tem o formato de uma cruz, e a dinâmica consiste em remover peças pulando uma sobre a outra – sempre na horizontal ou vertical, nunca na diagonal. O centro começa vazio. Simples de jogar… mas desafiador de resolver!

## 2. Estrutura do Programa
> O programa foi desenvolvido em Python e está organizado em três partes principais: as regras do tabuleiro, a visualização gráfica do jogo e, no centro de tudo, o coração da solução — o algoritmo genético.

## 3. Explicando o Algoritmo Genético
> É uma técnica de inteligência artificial inspirada no processo de evolução natural. A ideia é simples: começamos com várias “soluções” geradas aleatoriamente ou não, avaliamos quais são as melhores, combinamos essas soluções (o chamado crossover), aplicamos pequenas alterações (mutações), e repetimos esse ciclo várias vezes — sempre buscando resultados cada vez melhores.

## 4. Como o Algoritmo Gera as Soluções
> No nosso código, cada solução representa uma sequência de movimentos válidos no tabuleiro.
O algoritmo foi ajustado para priorizar jogadas nas bordas e movimentos próximos ao último realizado — uma tentativa de imitar estratégias humanas.
Essa abordagem ajuda o algoritmo a explorar caminhos mais promissores e chegar mais rapidamente a boas soluções.

## 5. Avaliando as Soluções
> Depois que cada sequência de movimentos é criada, ela é avaliada.
O critério principal é simples: quanto menos pinos restarem no tabuleiro, melhor a solução!
O cenário ideal é terminar com apenas um pino — de preferência no centro.
Importante: apenas as jogadas válidas são consideradas.

## 6. Evolução das Gerações
> Esse processo se repete ao longo de várias gerações.
A cada rodada, as melhores soluções são preservadas, e novas são geradas através de cruzamento (crossover) e mutação das anteriores.

## Dica Extra (Opcional)
> Dica importante:
Se quiser que o programa encontre soluções melhores e mais rápido, experimente ajustar os parâmetros de população, número de gerações e taxa de mutação.
Quanto maior a população e o número de gerações, maior a chance de o algoritmo encontrar a solução perfeita — embora o tempo de processamento também aumente.
Vale testar e encontrar o equilíbrio ideal para o seu desafio!

## 7. Visualizando a Solução
> Quando o algoritmo encontra uma solução ideal, entra em cena o Pygame.
Ele exibe o tabuleiro e anima cada movimento passo a passo, mostrando exatamente como a sequência de jogadas levou à solução final.
Dessa forma, você vê na prática como o computador resolveu o desafio — de forma visual, clara e dinâmica.

## 8. Encerramento
> E é assim que o algoritmo genético resolve o Resta 1. Até a próxima!
