import tkinter
import random
from controller import handler
from view import des_canvas, des_tela

capt = 0

def proximo(jogo):
		handler.lancou = False
		des_tela.salvar['state'] = tkinter.NORMAL
		des_tela.lancar['state'] = tkinter.NORMAL
		jogo['jogadorVez'] += 1
		jogo['jogadorVez'] %= 4

def casa2Pecas(tabuleiro, casaTabuleiro):
    if casaTabuleiro > ultimaCasaBranca(0) + 1:
        return False
    pecas = []
    for j in tabuleiro:
        pecas += j
    return pecas.count(casaTabuleiro) == 2

def barreiras(tabuleiro, jogador):
    return [c for c in set(tabuleiro[jogador]) if (tabuleiro[jogador].count(c) > 1) and (c not in [0, 58])]
    
def barreirasOponentes(tabuleiro, jogador):
    bs = []
    for oponente in oponentes(jogador):
        bs += barreiras(tabuleiro, oponente)
    return bs

def barreirasOponentesTrajeto(tabuleiro, jogador, peca, valorDado):
    return [b for b in barreirasOponentes(tabuleiro, jogador) if 0 < casaJogador(b, jogador) - casaJogador(tabuleiro[jogador][peca], jogador) <= valorDado]

def casaInicialVazia(tabuleiro, jogador):
    return not casaInicial in tabuleiro[jogador]

def casaInicialCheia(tabuleiro, jogador):
		c=0
		for i in range(4):
			if tabuleiro[jogador][i] == 0:
				c+=1
		if c == 4:
				return True
		else:
				return False

def casaJogador(casaTabuleiro, jogador): 
	# cada jogador seria o quanto ele se movimentou em relação a si msm. Casa relativa ao jogador.
	# CasaJogador é a casa que está posicionado a partir da sua casa inicial
	# Se tabuleiro = 30
	# CasaJogador = (30 -2*13)%(52)
    if 1 <= casaTabuleiro <= 4 * casasBrancas:
        return (casaTabuleiro - jogador * casasBrancas)%((4 * casasBrancas))
    else:
        return casaTabuleiro

def casaTabuleiro(casaJogador, jogador): # numero de casas que o jogador já andou no tabuleiro. CasaTabuleiro é a casa do jogador em relação ao tabuleiro
		if 1 <= casaJogador <= 4 * casasBrancas:
				c = casaJogador + jogador * casasBrancas
				if c == 52:
						return c
				else:
						return c%((4 * casasBrancas))
		else:
				return casaJogador

def casaSaida(jogador): #casa de saída é a primeira casa do jogador depois de ele sair da sua respectiva casa inicial.
    return casaTabuleiro(1, jogador)

def casaSaidaVazia(tabuleiro, jogador):
    return not casaSaida(jogador) in tabuleiro[jogador]

def jogarDado():
    return int(6*random.random())+1

def oponentes(jogador):
    return [j for j in range(4) if j != jogador]

def ultimaCasaBranca(jogador):
    return casaTabuleiro(4 * casasBrancas-1, jogador)

abrigos = [10 + 13*i for i in range(4)]
casaInicial = 0
casasBrancas = 13
casaFinal = 58

def novoJogo():
		return {
        'jogadorVez': 0,
        'qtdDado6': 0,
        'pecaAnterior6': 0,
        'tabuleiro': [
            [casaSaida(0), 0, 0, 0],
            [casaSaida(1), 0, 0, 0],
            [casaSaida(2), 0, 0, 0],
            [casaSaida(3), 0, 0, 0]
        ]
    }


def podeMoverPeca(tabuleiro, jogador, peca, valorDado):
		print(tabuleiro)
		print("jogador",jogador)
		print("Peça",peca)
		print("Valor do Dado",valorDado)
		if handler.lancou == False:
			return False
		casaDestino = casaTabuleiro(casaJogador(tabuleiro[jogador][peca], jogador) + valorDado, jogador)
		print("Função casa tabuleiro me dá o valor da casa de destino:",casaDestino)
		if casaJogador(tabuleiro[jogador][peca], jogador) <= ultimaCasaBranca(0) and ultimaCasaBranca(0)<(casaJogador(tabuleiro[jogador][peca], jogador) + valorDado)< casaFinal:
			casaDestino = casaTabuleiro(casaJogador(tabuleiro[jogador][peca], jogador) + valorDado + 1, jogador)
		if 53 <= casaDestino < casaFinal and tabuleiro[jogador].count(casaDestino) > 0:
			return False
		if valorDado == 5:
				if tabuleiro[jogador][peca] == casaInicial:
						if not casaSaidaVazia(tabuleiro, jogador):
								return False
				elif not casaInicialVazia(tabuleiro, jogador) and casaSaidaVazia(tabuleiro, jogador):
						return False
		elif tabuleiro[jogador][peca] == casaInicial:
				return False
		if casaDestino in abrigos:
				if casa2Pecas(tabuleiro, casaDestino) or (casaDestino) in tabuleiro[jogador]:
						return False
		if casaDestino in [casaSaida(i) for i in range(4) if casa2Pecas(tabuleiro, casaSaida(i))]:
				return False
		if casaDestino in [casaSaida(i) for i in range(4) if casaSaida(i) in tabuleiro[jogador]]:
				return False
		if tabuleiro[jogador][peca] == casaFinal:
				return False
		if ultimaCasaBranca(0)+1 < tabuleiro[jogador][peca] < casaFinal and casaDestino != casaFinal:
				return False
		if barreirasOponentesTrajeto(tabuleiro, jogador, peca, valorDado):
				return False
		bs = barreiras(tabuleiro, jogador)	
		if tabuleiro[jogador][peca] in bs:
				if valorDado == 6:
						if casaDestino in abrigos:
								if casa2Pecas(tabuleiro, casaDestino) or (casaDestino) in tabuleiro[jogador]:
										return False
						if casaDestino in [casaSaida(i) for i in range(4) if casa2Pecas(tabuleiro, casaSaida(i))]:
								return False
						if barreirasOponentesTrajeto(tabuleiro, jogador, peca, valorDado):
								return False
						bs.remove(tabuleiro[jogador][peca])
						for b in bs:
								if 0 < casaJogador(b, jogador) - casaJogador(tabuleiro[jogador][peca], jogador) <= valorDado:
										return False
				else:
						return False
		for b in bs:
				if 0 < casaJogador(b, jogador) - casaJogador(tabuleiro[jogador][peca], jogador) <= valorDado:
						return False
		return True


def moverPeca(jogo, peca, valorDado, ehValorDado):
		global capt
		ehValorDado = True
		if not podeMoverPeca(jogo['tabuleiro'], jogo['jogadorVez'], peca, valorDado):
				return    
		if valorDado == 5:
				if jogo['tabuleiro'][jogo['jogadorVez']][peca] == 0:
						jogo['tabuleiro'][jogo['jogadorVez']][peca] = casaSaida(jogo['jogadorVez'])
						for oponente in oponentes(jogo['jogadorVez']):
								cap = 10
								if casaSaida(jogo['jogadorVez']) in jogo['tabuleiro'][oponente]:				
										for i in range(4):
												if jogo['tabuleiro'][oponente][i] == casaSaida(jogo['jogadorVez']):
														cap = i
								if cap != 10:
										jogo['tabuleiro'][oponente][cap] = 0
						proximo(jogo)
						return
		elif valorDado == 6:
				if jogo['qtdDado6'] == 2:
						if jogo['tabuleiro'][jogo['jogadorVez']][jogo['pecaAnterior6']] <= ultimaCasaBranca(0):
								jogo['tabuleiro'][jogo['jogadorVez']][jogo['pecaAnterior6']] = 0
						jogo['qtdDado6'] = 0
						proximo(jogo)
						return True
		if casaJogador(jogo['tabuleiro'][jogo['jogadorVez']][peca], jogo['jogadorVez']) <= ultimaCasaBranca(0) and ultimaCasaBranca(0)<(casaJogador(jogo['tabuleiro'][jogo['jogadorVez']][peca], jogo['jogadorVez']) + valorDado)< casaFinal:
				jogo['tabuleiro'][jogo['jogadorVez']][peca] = casaTabuleiro(casaJogador(jogo['tabuleiro'][jogo['jogadorVez']][peca], jogo['jogadorVez']) + valorDado + 1, jogo['jogadorVez'])
		else:
				jogo['tabuleiro'][jogo['jogadorVez']][peca] = casaTabuleiro(casaJogador(jogo['tabuleiro'][jogo['jogadorVez']][peca], jogo['jogadorVez']) + valorDado, jogo['jogadorVez'])
		for oponente in oponentes(jogo['jogadorVez']):
				if jogo['tabuleiro'][jogo['jogadorVez']][peca] <= (ultimaCasaBranca(0) + 1) and jogo['tabuleiro'][jogo['jogadorVez']][peca] in jogo['tabuleiro'][oponente]:
						for i in range(4):
								if jogo['tabuleiro'][jogo['jogadorVez']][peca] == jogo['tabuleiro'][oponente][i]:
										cap = i
						if not jogo['tabuleiro'][oponente][cap] in abrigos and not jogo['tabuleiro'][oponente][cap] == casaSaida(oponente):
								jogo['tabuleiro'][oponente][cap] = 0
								jogo['qtdDado6'] = 0
								capt = 1
								des_tela.lancar['state'] = tkinter.DISABLED					
								ehValorDado = False
								return 6
		if capt == 1:
				jogo['qtdDado6'] = 0
				des_tela.lancar['state'] = tkinter.DISABLED
				capt = 0
				#proximo(jogo)
				ehValorDado = False
				des_canvas.aposclique()
		if jogo['tabuleiro'][jogo['jogadorVez']][peca] == casaFinal:
				capt = 1
				jogo['qtdDado6'] = 0
				des_tela.lancar['state'] = tkinter.DISABLED
				ehValorDado = False
				return 6
		if valorDado == 6 and ehValorDado:
				jogo['pecaAnterior6'] = peca
				jogo['qtdDado6'] += 1
				jogo['jogadorVez'] -= 1
		if valorDado != 6:
				jogo['qtdDado6'] = 0
		proximo(jogo)
		return 1
