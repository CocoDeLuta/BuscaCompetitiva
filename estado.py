import heapq
import copy
from typing import List, Callable, Optional

class Estado:
    def __init__(self, estado_jogo: dict, jogador_atual: str):
        self.estado_jogo = estado_jogo
        self.jogador_atual = jogador_atual

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.estado_jogo.items())))

    def __eq__(self, other) -> bool:
        return self.estado_jogo == other.estado_jogo

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)

    def __gt__(self, other) -> bool:
        return hash(self) > hash(other)

    def movimentos_possiveis(self, conexoes: List[tuple], jogador: str) -> List[tuple]:
        movimentos = []
        for casa_origem, casa_destino in conexoes:
            if self.estado_jogo[casa_origem] == jogador and self.estado_jogo[casa_destino] is None:
                movimentos.append((casa_origem, casa_destino))
        return movimentos

    def aplicar_movimento(self, movimento: tuple, jogador: str) -> 'Estado':
        nova_estado = copy.deepcopy(self.estado_jogo)
        casa_origem, casa_destino = movimento
        nova_estado[casa_origem] = None
        nova_estado[casa_destino] = jogador
        return Estado(nova_estado, "Vermelho" if jogador == "Azul" else "Azul")
    
    def a_star_search(self, conexoes: List[tuple], jogador: str, objetivo_funcao: Callable[['Estado'], bool]) -> Optional[List['Estado']]:
        fronteira = []
        heapq.heappush(fronteira, (0, self))
        custos = {self: 0}
        came_from = {self: None}

        while fronteira:
            _, estado_atual = heapq.heappop(fronteira)

            if objetivo_funcao(estado_atual):
                # Reconstruir o caminho
                caminho = []
                while came_from[estado_atual]:
                    caminho.append(estado_atual)
                    estado_atual = came_from[estado_atual]
                caminho.reverse()
                return caminho

            for movimento in estado_atual.movimentos_possiveis(conexoes, jogador):
                prox_estado = estado_atual.aplicar_movimento(movimento, jogador)
                novo_custo = custos[estado_atual] + 1
                if prox_estado not in custos or novo_custo < custos[prox_estado]:
                    custos[prox_estado] = novo_custo
                    prioridade = novo_custo + self.heuristica(prox_estado, jogador, objetivo_funcao)
                    heapq.heappush(fronteira, (prioridade, prox_estado))
                    came_from[prox_estado] = estado_atual

        return None  # Sem caminho encontrado
    
    def heuristica(self, estado: 'Estado', jogador: str, objetivo_funcao: Callable[['Estado'], bool]) -> int:
        # Esta é uma heurística simplificada. Pode ser refinada conforme necessário.
        if objetivo_funcao.__name__ == "objetivo_bloquear":
            # Número de peças inimigas restantes que precisam ser removidas
            pecas_inimigas = sum(1 for p in estado.estado_jogo.values() if p == ("Vermelho" if jogador == "Azul" else "Azul"))
            return max(0, pecas_inimigas - 2)  # Queremos menos que 3
        elif objetivo_funcao.__name__ == "objetivo_trinca":
            # Número de trincas faltantes
            trincas_faltantes = self.contar_trincas_faltantes(estado.estado_jogo, jogador)
            return trincas_faltantes
        return 0

    def contar_trincas_faltantes(self, estado_jogo: dict, jogador: str) -> int:
        trincas = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15),
            (16, 17, 18), (19, 20, 21), (22, 23, 24),
            (1, 10, 22), (4, 11, 19), (7, 12, 16), (2, 5, 8),
            (17, 20, 23), (9, 13, 18), (6, 14, 21), (3, 15, 24)
        ]
        faltantes = 0
        for trinca in trincas:
            if not all(estado_jogo[casa] == jogador for casa in trinca):
                faltantes += 1
        return faltantes

    def objetivo_bloquear(self, estado: 'Estado') -> bool:
        # Verifica se o oponente tem menos de 3 peças
        jogador_oponente = "Vermelho" if estado.jogador_atual == "Azul" else "Azul"
        pecas_oponente = sum(1 for p in estado.estado_jogo.values() if p == jogador_oponente)
        return pecas_oponente < 3

    def objetivo_trinca(self, estado: 'Estado') -> bool:
        # Verifica se o jogador conseguiu uma trinca
        jogador = "Azul" if estado.jogador_atual == "Vermelho" else "Vermelho"
        trincas = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15),
            (16, 17, 18), (19, 20, 21), (22, 23, 24),
            (1, 10, 22), (4, 11, 19), (7, 12, 16), (2, 5, 8),
            (17, 20, 23), (9, 13, 18), (6, 14, 21), (3, 15, 24)
        ]
        for trinca in trincas:
            if all(estado.estado_jogo[casa] == jogador for casa in trinca):
                return True
        return False

# Exemplo de uso
estado_inicial = Estado(
    estado_jogo={
        1: "Azul", 2: "Azul", 3: None, 4: "Vermelho", 5: None, 6: "Vermelho",
        7: None, 8: "Azul", 9: "Vermelho", 10: None, 11: "Azul", 12: None,
        13: "Vermelho", 14: None, 15: "Azul", 16: "Vermelho", 17: None, 18: "Azul",
        19: "Vermelho", 20: None, 21: "Azul", 22: "Vermelho", 23: None, 24: "Azul"
    },
    jogador_atual="Azul"
)

conexoes = [
    (1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9), (10, 11), (11, 12),
    (13, 14), (14, 15), (16, 17), (17, 18), (19, 20), (20, 21), (22, 23), (23, 24),
    (1, 10), (10, 22), (4, 11), (11, 19), (7, 12), (12, 16), (2, 5), (5, 8),
    (17, 20), (20, 23), (9, 13), (13, 18), (6, 14), (14, 21), (3, 15), (15, 24)
]

caminho_bloquear = estado_inicial.a_star_search(
    conexoes=conexoes,
    jogador="Azul",
    objetivo_funcao= estado_inicial.objetivo_bloquear
)
print("Caminho Bloquear:", caminho_bloquear)