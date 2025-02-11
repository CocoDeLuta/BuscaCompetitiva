import heapq
from typing import List, Tuple, Optional, Dict

class Estado:
    def __init__(self, estado_jogo: Dict[int, Optional[str]], jogador_atual: str, trincas_formadas: Dict[str, set], conexoes: List[Tuple[int, int]]):
        self.estado_jogo = estado_jogo
        self.jogador_atual = jogador_atual
        self.trincas_formadas = trincas_formadas
        self.conexoes = conexoes

    def movimentos_possiveis(self, casa: int) -> List[int]:
        """
        Retorna os movimentos possíveis de uma peça específica do jogador atual.
        """
        movimentos = []
        for a, b in self.conexoes:
            if casa == a and self.estado_jogo[b] is None:
                movimentos.append(b)
            elif casa == b and self.estado_jogo[a] is None:
                movimentos.append(a)
        return movimentos

    def a_star_search(self) -> Optional[Tuple[int, int]]:
        """
        Executa o algoritmo A* para encontrar o melhor movimento visando formar uma trinca.
        Retorna a melhor jogada (casa_atual, casa_destino).
        """
        melhor_movimento = None
        menor_caminho = float('inf')

        trincas_faltantes = self.verificar_trincas_faltantes()
        
        for trinca in trincas_faltantes:
            casas_vazias = [casa for casa in trinca if self.estado_jogo[casa] is None]
            if len(casas_vazias) == 1:  # Priorizar completar trincas
                casa_destino = casas_vazias[0]
                caminho = self.a_star_search_casa(casa_destino)
                if caminho and len(caminho) < menor_caminho:
                    menor_caminho = len(caminho)
                    melhor_movimento = caminho[0]  # Primeiro movimento
        
        return melhor_movimento

    def a_star_search_casa(self, casa_final: int) -> Optional[List[Tuple[int, int]]]:
        """
        Calcula o caminho mais curto até uma casa específica usando A*.
        Retorna uma lista de movimentos [(origem, destino), ...].
        """
        fila = []
        heapq.heappush(fila, (0, casa_final, []))
        visitados = {casa_final: 0}

        while fila:
            custo, casa_atual, caminho = heapq.heappop(fila)
            if self.estado_jogo[casa_atual] == self.jogador_atual:
                return caminho
            for movimento in self.movimentos_possiveis(casa_atual):
                novo_custo = custo + 1
                if movimento not in visitados or novo_custo < visitados[movimento]:
                    heapq.heappush(fila, (novo_custo, movimento, caminho + [(casa_atual, movimento)]))
                    visitados[movimento] = novo_custo
        return None

    def verificar_trincas_faltantes(self) -> List[Tuple[int, int, int]]:
        """
        Retorna uma lista de trincas que ainda não foram completadas pelo jogador atual.
        """
        trincas = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15),
            (16, 17, 18), (19, 20, 21), (22, 23, 24),
            (1, 10, 22), (4, 11, 19), (7, 12, 16), (2, 5, 8),
            (17, 20, 23), (9, 13, 18), (6, 14, 21), (3, 15, 24)
        ]
        return [trinca for trinca in trincas if trinca not in self.trincas_formadas[self.jogador_atual]]
