import pygame
import sys
import estado

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Trilha")

offset_x, offset_y = WIDTH // 4, HEIGHT // 12
casas = {
    1:  (100 + offset_x, 100 + offset_y),  2:  (400 + offset_x, 100 + offset_y),  3:  (700 + offset_x, 100 + offset_y),
    4:  (200 + offset_x, 200 + offset_y),  5:  (400 + offset_x, 200 + offset_y),  6:  (600 + offset_x, 200 + offset_y),
    7:  (300 + offset_x, 300 + offset_y),  8:  (400 + offset_x, 300 + offset_y),  9:  (500 + offset_x, 300 + offset_y),
    10: (100 + offset_x, 400 + offset_y), 11: (200 + offset_x, 400 + offset_y), 12: (300 + offset_x, 400 + offset_y), 
    13: (500 + offset_x, 400 + offset_y), 14: (600 + offset_x, 400 + offset_y), 15: (700 + offset_x, 400 + offset_y),
    16: (300 + offset_x, 500 + offset_y), 17: (400 + offset_x, 500 + offset_y), 18: (500 + offset_x, 500 + offset_y),
    19: (200 + offset_x, 600 + offset_y), 20: (400 + offset_x, 600 + offset_y), 21: (600 + offset_x, 600 + offset_y),
    22: (100 + offset_x, 700 + offset_y), 23: (400 + offset_x, 700 + offset_y), 24: (700 + offset_x, 700 + offset_y)
}

conexoes = [
    (1, 2), (2, 3), (1, 10), (3, 15), (10, 22), (15, 24), (22, 23), (23, 24),
    (4, 5), (5, 6), (4, 11), (6, 14), (11, 19), (14, 21), (19, 20), (20, 21),
    (7, 8), (8, 9), (7, 12), (9, 13), (12, 16), (13, 18), (16, 17), (17, 18),
    (2, 5), (5, 8), (10, 11), (11, 12), (13, 14), (14, 15), (17, 20), (20, 23)
]

estado_jogo = {i: None for i in casas.keys()}

jogador_atual = "Vermelho"
pecas_colocadas = {"Vermelho": 0, "Azul": 0}
pecas_restantes = {"Vermelho": 9, "Azul": 9}
pecas_tabuleiro = {"Vermelho": 0, "Azul": 0}
remocao_pendente = False
trincas_formadas = {"Vermelho": set(), "Azul": set()}
peca_selecionada = None
vencedor = None


def verificar_linha(jogador):
    trincas = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15), (16, 17, 18), (19, 20, 21), (22, 23, 24),
        (1, 10, 22), (4, 11, 19), (7, 12, 16), (2, 5, 8), (17, 20, 23), (9, 13, 18), (6, 14, 21), (3, 15, 24)
    ]
    for c1, c2, c3 in trincas:
        if estado_jogo[c1] == estado_jogo[c2] == estado_jogo[c3] == jogador:
            if (c1, c2, c3) not in trincas_formadas[jogador]:
                trincas_formadas[jogador].add((c1, c2, c3))
                return True
    return False

def remover_peca(casa):
    global remocao_pendente, jogador_atual, pecas_tabuleiro
    if estado_jogo[casa] and estado_jogo[casa] != jogador_atual:
        estado_jogo[casa] = None
        pecas_tabuleiro["Vermelho" if jogador_atual == "Azul" else "Azul"] -= 1
        remocao_pendente = False
        jogador_atual = "Vermelho" if jogador_atual == "Azul" else "Azul"

def verificar_derrota(jogador):
    if pecas_restantes[jogador] > 0: # jogador ainda nao colocou todas as pecas
        return False
    
    if pecas_tabuleiro[jogador] < 3: # jogador tem menos de 3 pecas
        return True
    

def desenhar_setas(casa):
    cor_seta = (255, 0, 0) if jogador_atual == "Vermelho" else (0, 0, 255)
    for c1, c2 in conexoes:
        if c1 == casa and estado_jogo[c2] is None:
            pos2 = casas[c2]
            pygame.draw.polygon(screen, cor_seta, [
                (pos2[0] - 10, pos2[1] - 10), 
                (pos2[0] + 10, pos2[1] - 10), 
                (pos2[0], pos2[1] + 10)
            ])
        elif c2 == casa and estado_jogo[c1] is None:
            pos2 = casas[c1]
            pygame.draw.polygon(screen, cor_seta, [
                (pos2[0] - 10, pos2[1] - 10), 
                (pos2[0] + 10, pos2[1] - 10), 
                (pos2[0], pos2[1] + 10)
            ])
            
def verificar(): # Verifica se o jogador atual formou uma trinca ou se o oponente perdeu
    global remocao_pendente, vencedor, jogador_atual
    if verificar_linha(jogador_atual):
        remocao_pendente = True
    if verificar_derrota("Vermelho" if jogador_atual == "Azul" else "Azul"):
        vencedor = jogador_atual
        rodando = False
        tela_vitoria(vencedor)
    if not remocao_pendente:
        jogador_atual = "Vermelho" if jogador_atual == "Azul" else "Azul"

def algoritmo_a_estrela():
    estado_atual = estado.Estado(estado_jogo, "Azul")  # Corrigido para chamar a classe Estado

    # Primeiro, tentar bloquear
    caminho_bloquear = estado_atual.a_star_search(
        conexoes=conexoes,
        jogador="Azul",
        objetivo_funcao= estado_atual.objetivo_bloquear
    )
    movimentos_bloquear = len(caminho_bloquear) if caminho_bloquear else float('inf')

    # Segundo, tentar criar trinca
    caminho_trinca = estado_atual.a_star_search(
        conexoes=conexoes,
        jogador="Azul",
        objetivo_funcao=estado_atual.objetivo_trinca
    )
    movimentos_trinca = len(caminho_trinca) if caminho_trinca else float('inf')

    # Decidir qual ação tomar
    if movimentos_bloquear < movimentos_trinca:
        # Executar a primeira ação do caminho_bloquear
        primeiro_movimento = caminho_bloquear[0]  # Ajustado para pegar o movimento
        # Precisamos determinar qual movimento levar do estado atual para o próximo estado
        for movimento in estado_atual.movimentos_possiveis(conexoes, "Azul"):
            estado_proximo = estado_atual.aplicar_movimento(movimento, "Azul")
            if estado_proximo == caminho_bloquear[1]:
                return movimento
    elif movimentos_trinca < movimentos_bloquear:
        # Executar a primeira ação do caminho_trinca
        primeiro_movimento = caminho_trinca[0]  # Ajustado para pegar o movimento
        for movimento in estado_atual.movimentos_possiveis(conexoes, "Azul"):
            estado_proximo = estado_atual.aplicar_movimento(movimento, "Azul")
            if estado_proximo == caminho_trinca[1]:
                return movimento
    else:
        # Se ambos são igualmente viáveis ou nenhum encontrado, fazer um movimento aleatório
        for movimento in estado_atual.movimentos_possiveis(conexoes, "Azul"):
            return movimento

def menu_principal():
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Jogo de Trilha", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        font = pygame.font.Font(None, 36)
        modos = ["Humano vs Humano", "Humano vs A*"]
        for i, modo in enumerate(modos):
            text = font.render(modo, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, modo in enumerate(modos):
                    text = font.render(modo, True, (255, 255, 255))
                    if (WIDTH // 2 - text.get_width() // 2 <= mx <= WIDTH // 2 + text.get_width() // 2) and (HEIGHT // 2 + i * 50 <= my <= HEIGHT // 2 + i * 50 + text.get_height()):
                        return modo

def tela_vitoria(vencedor):
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        texto_vencedor = font.render(f"{vencedor} venceu!", True, (255, 255, 255))
        screen.blit(texto_vencedor, (WIDTH // 2 - texto_vencedor.get_width() // 2, HEIGHT // 3))

        font = pygame.font.Font(None, 36)
        texto_voltar = font.render("Voltar ao Menu", True, (255, 255, 255))
        button_rect = pygame.Rect(0, 0, texto_voltar.get_width() + 20, texto_voltar.get_height() + 10)
        button_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        pygame.draw.rect(screen, (100, 100, 100), button_rect)
        screen.blit(texto_voltar, texto_voltar.get_rect(center=button_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return

def jogo(modo_jogo):
    global jogador_atual, peca_selecionada, remocao_pendente, vencedor, rodadas
    rodando = True
    casa_origem, casa_destino = None, None
    
    while rodando:
        screen.fill((30, 30, 30))

        # Desenhar conexões entre as casas
        for c1, c2 in conexoes:
            pygame.draw.line(screen, (255, 255, 255), casas[c1], casas[c2], 3)

        # Desenhar as casas e as peças
        for casa, pos in casas.items():
            cor = (0, 255, 0) if estado_jogo[casa] is None else (255, 0, 0) if estado_jogo[casa] == "Vermelho" else (0, 0, 255)
            pygame.draw.circle(screen, cor, pos, 20)
            font = pygame.font.Font(None, 24)
            text = font.render(str(casa), True, (0, 0, 0))
            screen.blit(text, (pos[0] - 8, pos[1] - 8))

        # Desenhar informações dos jogadores
        font = pygame.font.Font(None, 36)
        text_vermelho = font.render(f"Vermelho - Restantes: {pecas_restantes['Vermelho']} Colocadas: {pecas_colocadas['Vermelho']} Tabuleiro: {pecas_tabuleiro['Vermelho']}", True, (255, 0, 0))
        text_azul = font.render(f"Azul - Restantes: {pecas_restantes['Azul']} Colocadas: {pecas_colocadas['Azul']} Tabuleiro: {pecas_tabuleiro['Azul']}", True, (0, 0, 255))
        screen.blit(text_vermelho, (50, HEIGHT - 150))
        screen.blit(text_azul, (50, HEIGHT - 100))

        # Mensagem de remoção pendente
        if remocao_pendente:
            text = font.render("Remova uma peça do oponente!", True, (255, 255, 0))
            screen.blit(text, (50, HEIGHT - 50))

        # Mensagem de turno
        cor_turno = (255, 0, 0) if jogador_atual == "Vermelho" else (0, 0, 255)
        text_turno = font.render(f"Vez de: {jogador_atual}", True, cor_turno)
        screen.blit(text_turno, (WIDTH // 2 - text_turno.get_width() // 2, 20))

        # Desenhar setas para a peça selecionada
        if peca_selecionada is not None:
            desenhar_setas(peca_selecionada)

        # Mensagem de movimento
        if casa_origem is not None and casa_destino is not None:
            text = font.render(f"Movimento: ({casa_origem} -> {casa_destino})", True, (255, 255, 0))
            screen.blit(text, (50, HEIGHT // 2))
            button_text = font.render("Continuar", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
            pygame.draw.rect(screen, (100, 100, 100), button_rect.inflate(20, 10))
            screen.blit(button_text, button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Fechar o jogo
                rodando = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and vencedor is None:
                mx, my = event.pos # Pega a posição do mouse
                
                if casa_origem is not None and casa_destino is not None and button_rect.collidepoint((mx, my)):
                    casa_origem, casa_destino = None, None # Limpa a seleção de casas
                    continue
                
                for casa, pos in casas.items(): # Verifica se o mouse está em cima de uma casa
                    if (pos[0] - 20 <= mx <= pos[0] + 20) and (pos[1] - 20 <= my <= pos[1] + 20):
                        if remocao_pendente:
                            remover_peca(casa) # Remove a peça do oponente
                            
                        elif estado_jogo[casa] == jogador_atual and pecas_colocadas[jogador_atual] == 9:
                            peca_selecionada = casa # Seleciona a peça
                            
                        elif estado_jogo[casa] is None and peca_selecionada is not None:
                            if (peca_selecionada, casa) in conexoes or (casa, peca_selecionada) in conexoes:
                                estado_jogo[casa] = jogador_atual
                                estado_jogo[peca_selecionada] = None
                                peca_selecionada = None
                                pecas_tabuleiro[jogador_atual] += 1
                                verificar() # Verifica se o jogador formou uma trinca ou se o oponente perdeu
                                
                                    
                        elif estado_jogo[casa] is None and pecas_colocadas[jogador_atual] < 9:
                            estado_jogo[casa] = jogador_atual
                            pecas_colocadas[jogador_atual] += 1
                            pecas_restantes[jogador_atual] -= 1
                            pecas_tabuleiro[jogador_atual] += 1
                            
                            verificar() # Verifica se o jogador formou uma trinca ou se o oponente perdeu

        # Lógica para o modo "Humano vs A*"
        if modo_jogo == "Humano vs A*" and jogador_atual == "Azul" and vencedor is None:
            if pecas_restantes["Azul"] > 0: # Se o jogador ainda não colocou todas as peças
                for casa, ocupado in estado_jogo.items():
                    if ocupado is None: # Coloca a peça em uma casa vazia
                        estado_jogo[casa] = jogador_atual
                        pecas_colocadas[jogador_atual] += 1
                        pecas_restantes[jogador_atual] -= 1
                        pecas_tabuleiro[jogador_atual] += 1
                        verificar() # Verifica se o jogador formou uma trinca ou se o oponente perdeu
                        break
            else:
                # Executa o algoritmo A*
                movimento = algoritmo_a_estrela()
                print("Movimento:", movimento)
                if movimento != (None, None):
                    casa_origem, casa_destino = movimento
                    estado_jogo[casa_destino] = "Azul"
                    estado_jogo[casa_origem] = None
                    pecas_colocadas["Azul"] += 1  # Atualize conforme a lógica do movimento
                    # Verificar trinca e derrota
                    verificar()
                        
        # Lógica para o modo "Humano vs Minimax"
        elif modo_jogo == "Humano vs Minimax" and jogador_atual == "Azul" and vencedor is None:
            if pecas_restantes["Azul"] > 0:
                for casa, ocupado in estado_jogo.items():
                    if ocupado is None:
                        estado_jogo[casa] = "Azul"
                        pecas_colocadas["Azul"] += 1
                        pecas_restantes["Azul"] -= 1
                        verificar()
                        break
            else:
                casa_origem, casa_destino = algoritmo_minimax()
                if casa_origem is not None and casa_destino is not None:
                    estado_jogo[casa_destino] = "Azul"
                    estado_jogo[casa_origem] = None
                    verificar()
        # Lógica para o modo "A* vs Minimax"
        elif modo_jogo == "A* vs Minimax" and vencedor is None:
            if jogador_atual == "Vermelho":
                if pecas_restantes["Vermelho"] > 0:
                    for casa, ocupado in estado_jogo.items():
                        if ocupado is None:
                            estado_jogo[casa] = "Vermelho"
                            pecas_colocadas["Vermelho"] += 1
                            pecas_restantes["Vermelho"] -= 1
                            verificar()
                            break
                else:
                    casa_origem, casa_destino = algoritmo_a_estrela()
                    if casa_origem is not None and casa_destino is not None:
                        estado_jogo[casa_destino] = "Vermelho"
                        estado_jogo[casa_origem] = None
                        verificar()
            else:
                if pecas_restantes["Azul"] > 0:
                    for casa, ocupado in estado_jogo.items():
                        if ocupado is None:
                            estado_jogo[casa] = "Azul"
                            pecas_colocadas["Azul"] += 1
                            pecas_restantes["Azul"] -= 1
                            verificar()
                            break
                else:
                    casa_origem, casa_destino = algoritmo_minimax()
                    if casa_origem is not None and casa_destino is not None:
                        estado_jogo[casa_destino] = "Azul"
                        estado_jogo[casa_origem] = None
                        verificar()

    if vencedor:
        tela_vitoria(vencedor)

while True:
    modo_jogo = menu_principal()
    jogo(modo_jogo)