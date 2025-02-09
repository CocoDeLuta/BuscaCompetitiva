import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1400, 1000
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
    global remocao_pendente, jogador_atual
    if estado_jogo[casa] and estado_jogo[casa] != jogador_atual:
        estado_jogo[casa] = None
        pecas_restantes["Vermelho" if jogador_atual == "Azul" else "Azul"] -= 1
        remocao_pendente = False
        jogador_atual = "Vermelho" if jogador_atual == "Azul" else "Azul"

def verificar_derrota(jogador):
    pecas_no_tabuleiro = sum(1 for casa in estado_jogo.values() if casa == jogador)
    return pecas_no_tabuleiro < 3 and pecas_restantes[jogador] == 0

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

def algoritmo_a_estrela():
    # Exemplo de lógica para mover peças
    for origem, destino in conexoes:
        if estado_jogo[origem] == "Azul" and estado_jogo[destino] is None:
            return (origem, destino)
    return (None, None)

def algoritmo_minimax():
    # Exemplo de lógica para mover peças
    for origem, destino in conexoes:
        if estado_jogo[origem] == "Azul" and estado_jogo[destino] is None:
            return (origem, destino)
    return (None, None)

def menu_principal():
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Jogo de Trilha", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        font = pygame.font.Font(None, 36)
        modos = ["Humano vs Humano", "Humano vs A*", "Humano vs Minimax", "A* vs Minimax"]
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
        text = font.render(f"{vencedor} venceu!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

        font = pygame.font.Font(None, 36)
        text = font.render("Voltar ao Menu", True, (255, 255, 255))
        button_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return

def jogo(modo_jogo):
    global jogador_atual, peca_selecionada, remocao_pendente, vencedor
    rodando = True
    casa_origem, casa_destino = None, None
    
    while rodando:
        screen.fill((30, 30, 30))

        for c1, c2 in conexoes:
            pygame.draw.line(screen, (255, 255, 255), casas[c1], casas[c2], 3)

        for casa, pos in casas.items():
            cor = (0, 255, 0) if estado_jogo[casa] is None else (255, 0, 0) if estado_jogo[casa] == "Vermelho" else (0, 0, 255)
            pygame.draw.circle(screen, cor, pos, 20)
            font = pygame.font.Font(None, 24)
            text = font.render(str(casa), True, (0, 0, 0))
            screen.blit(text, (pos[0] - 8, pos[1] - 8))

        font = pygame.font.Font(None, 36)
        text_vermelho = font.render(f"Vermelho - Restantes: {pecas_restantes['Vermelho']} Colocadas: {pecas_colocadas['Vermelho']}", True, (255, 0, 0))
        text_azul = font.render(f"Azul - Restantes: {pecas_restantes['Azul']} Colocadas: {pecas_colocadas['Azul']}", True, (0, 0, 255))
        screen.blit(text_vermelho, (50, HEIGHT - 150))
        screen.blit(text_azul, (50, HEIGHT - 100))

        if remocao_pendente:
            font = pygame.font.Font(None, 36)
            text = font.render("Remova uma peça do oponente!", True, (255, 255, 0))
            screen.blit(text, (50, HEIGHT - 50))

        cor_turno = (255, 0, 0) if jogador_atual == "Vermelho" else (0, 0, 255)
        text_turno = font.render(f"Vez de: {jogador_atual}", True, cor_turno)
        screen.blit(text_turno, (WIDTH // 2 - text_turno.get_width() // 2, 20))

        if peca_selecionada is not None:
            desenhar_setas(peca_selecionada)

        if casa_origem is not None and casa_destino is not None:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Movimento: ({casa_origem} -> {casa_destino})", True, (255, 255, 0))
            screen.blit(text, (50, HEIGHT // 2))  # Mensagem movida para o lado esquerdo
            button_text = font.render("Continuar", True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
            pygame.draw.rect(screen, (100, 100, 100), button_rect.inflate(20, 10))
            screen.blit(button_text, button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and vencedor is None:
                mx, my = event.pos
                if casa_origem is not None and casa_destino is not None and button_rect.collidepoint((mx, my)):
                    casa_origem, casa_destino = None, None
                    continue
                for casa, pos in casas.items():
                    if (pos[0] - 20 <= mx <= pos[0] + 20) and (pos[1] - 20 <= my <= pos[1] + 20):
                        if remocao_pendente:
                            remover_peca(casa)
                        elif estado_jogo[casa] == jogador_atual and pecas_colocadas[jogador_atual] == 9:
                            peca_selecionada = casa
                        elif estado_jogo[casa] is None and peca_selecionada is not None:
                            if (peca_selecionada, casa) in conexoes or (casa, peca_selecionada) in conexoes:
                                estado_jogo[casa] = jogador_atual
                                estado_jogo[peca_selecionada] = None
                                peca_selecionada = None
                                if verificar_linha(jogador_atual):
                                    remocao_pendente = True
                                if verificar_derrota("Vermelho" if jogador_atual == "Azul" else "Azul"):
                                    vencedor = jogador_atual
                                    rodando = False
                                if not remocao_pendente:
                                    jogador_atual = "Vermelho" if jogador_atual == "Azul" else "Azul"
                        elif estado_jogo[casa] is None and pecas_colocadas[jogador_atual] < 9:
                            estado_jogo[casa] = jogador_atual
                            pecas_colocadas[jogador_atual] += 1
                            pecas_restantes[jogador_atual] -= 1
                            if verificar_linha(jogador_atual):
                                remocao_pendente = True
                            if verificar_derrota("Vermelho" if jogador_atual == "Azul" else "Azul"):
                                vencedor = jogador_atual
                                rodando = False
                            if not remocao_pendente:
                                jogador_atual = "Vermelho" if jogador_atual == "Azul" else "Azul"

        if modo_jogo == "Humano vs A*" and jogador_atual == "Azul" and vencedor is None:
            if pecas_restantes["Azul"] > 0:
                for casa, ocupado in estado_jogo.items():
                    if ocupado is None:
                        estado_jogo[casa] = "Azul"
                        pecas_colocadas["Azul"] += 1
                        pecas_restantes["Azul"] -= 1
                        if verificar_linha("Azul"):
                            remocao_pendente = True
                        if verificar_derrota("Vermelho"):
                            vencedor = "Azul"
                            rodando = False
                        if not remocao_pendente:
                            jogador_atual = "Vermelho"
                        break
            else:
                casa_origem, casa_destino = algoritmo_a_estrela()
                if casa_origem is not None and casa_destino is not None:
                    estado_jogo[casa_destino] = "Azul"
                    estado_jogo[casa_origem] = None
                    if verificar_linha("Azul"):
                        remocao_pendente = True
                    if verificar_derrota("Vermelho"):
                        vencedor = "Azul"
                        rodando = False
                    if not remocao_pendente:
                        jogador_atual = "Vermelho"
        elif modo_jogo == "Humano vs Minimax" and jogador_atual == "Azul" and vencedor is None:
            if pecas_restantes["Azul"] > 0:
                for casa, ocupado in estado_jogo.items():
                    if ocupado is None:
                        estado_jogo[casa] = "Azul"
                        pecas_colocadas["Azul"] += 1
                        pecas_restantes["Azul"] -= 1
                        if verificar_linha("Azul"):
                            remocao_pendente = True
                        if verificar_derrota("Vermelho"):
                            vencedor = "Azul"
                            rodando = False
                        if not remocao_pendente:
                            jogador_atual = "Vermelho"
                        break
            else:
                casa_origem, casa_destino = algoritmo_minimax()
                if casa_origem is not None and casa_destino is not None:
                    estado_jogo[casa_destino] = "Azul"
                    estado_jogo[casa_origem] = None
                    if verificar_linha("Azul"):
                        remocao_pendente = True
                    if verificar_derrota("Vermelho"):
                        vencedor = "Azul"
                        rodando = False
                    if not remocao_pendente:
                        jogador_atual = "Vermelho"
        elif modo_jogo == "A* vs Minimax" and vencedor is None:
            if jogador_atual == "Vermelho":
                if pecas_restantes["Vermelho"] > 0:
                    for casa, ocupado in estado_jogo.items():
                        if ocupado is None:
                            estado_jogo[casa] = "Vermelho"
                            pecas_colocadas["Vermelho"] += 1
                            pecas_restantes["Vermelho"] -= 1
                            if verificar_linha("Vermelho"):
                                remocao_pendente = True
                            if verificar_derrota("Azul"):
                                vencedor = "Vermelho"
                                rodando = False
                            if not remocao_pendente:
                                jogador_atual = "Azul"
                            break
                else:
                    casa_origem, casa_destino = algoritmo_a_estrela()
                    if casa_origem is not None and casa_destino is not None:
                        estado_jogo[casa_destino] = "Vermelho"
                        estado_jogo[casa_origem] = None
                        if verificar_linha("Vermelho"):
                            remocao_pendente = True
                        if verificar_derrota("Azul"):
                            vencedor = "Vermelho"
                            rodando = False
                        if not remocao_pendente:
                            jogador_atual = "Azul"
            else:
                if pecas_restantes["Azul"] > 0:
                    for casa, ocupado in estado_jogo.items():
                        if ocupado is None:
                            estado_jogo[casa] = "Azul"
                            pecas_colocadas["Azul"] += 1
                            pecas_restantes["Azul"] -= 1
                            if verificar_linha("Azul"):
                                remocao_pendente = True
                            if verificar_derrota("Vermelho"):
                                vencedor = "Azul"
                                rodando = False
                            if not remocao_pendente:
                                jogador_atual = "Vermelho"
                            break
                else:
                    casa_origem, casa_destino = algoritmo_minimax()
                    if casa_origem is not None and casa_destino is not None:
                        estado_jogo[casa_destino] = "Azul"
                        estado_jogo[casa_origem] = None
                        if verificar_linha("Azul"):
                            remocao_pendente = True
                        if verificar_derrota("Vermelho"):
                            vencedor = "Azul"
                            rodando = False
                        if not remocao_pendente:
                            jogador_atual = "Vermelho"

    if vencedor:
        tela_vitoria(vencedor)

while True:
    modo_jogo = menu_principal()
    jogo(modo_jogo)