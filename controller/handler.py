from model import ludo
from view  import des_canvas, des_tela
from tkinter import messagebox, filedialog
import json
import tkinter

ladoCasa = 40
lancou = False

def novoJ(): # cria um novo jogo
	global jogo 
	des_tela.salvar['state'] = tkinter.NORMAL
	des_tela.lancar['state'] = tkinter.NORMAL
	jogo = ludo.novoJogo()
	des_canvas.novo()

def getJogo():
	global jogo
	return jogo

def escolheuDado(valor):
	global lancou 
	lancou = True
	global jogo, valorDado
	valorDado = valor
	des_canvas.jogou(valorDado)
	if not [p for p in range(4) if ludo.podeMoverPeca(jogo['tabuleiro'], jogo['jogadorVez'], p, valorDado)]:
			ludo.proximo(jogo)
			des_canvas.aposclique()
			return
	if ludo.casaInicialCheia(jogo['tabuleiro'], jogo['jogadorVez']):
		if valorDado != 5:
			ludo.proximo(jogo)
			des_canvas.aposclique()
	if valorDado == 5:
		trata5()

def lanca():  # valor do dado
	global lancou 
	lancou = True
	global jogo, valorDado
	valorDado = ludo.jogarDado()
	des_canvas.jogou(valorDado)
	if not [p for p in range(4) if ludo.podeMoverPeca(jogo['tabuleiro'], jogo['jogadorVez'], p, valorDado)]:
			ludo.proximo(jogo)
			des_canvas.aposclique()
			return
	if ludo.casaInicialCheia(jogo['tabuleiro'], jogo['jogadorVez']):
		if valorDado != 5:
			ludo.proximo(jogo)
			des_canvas.aposclique()
	if valorDado == 5:
		trata5()

def trata5():
	global jogo
	if not ludo.casaInicialVazia(jogo['tabuleiro'], jogo['jogadorVez']):
		if ludo.casaSaidaVazia(jogo['tabuleiro'], jogo['jogadorVez']):
			pecaEscolhida = jogo['tabuleiro'][jogo['jogadorVez']].index(0)
			if ludo.podeMoverPeca(jogo['tabuleiro'], jogo['jogadorVez'], pecaEscolhida, 5):
				ludo.moverPeca(jogo, pecaEscolhida, 5, True)
				des_canvas.aposclique()


def clicouCasa(coordCasa, coordPonteiro):
	cx, cy = coordCasa
	px, py = coordPonteiro
	return cx <= px <= cx + ladoCasa and cy <= py <= cy + ladoCasa

def escolhePeca(tabuleiro, jogadorVez, coordPonteiro):
	for i, casaTabuleiro in enumerate(tabuleiro[jogadorVez]):
		if 1 <= casaTabuleiro <= ludo.ultimaCasaBranca(0)+1:
			if clicouCasa(des_canvas.coordCasaComum(casaTabuleiro), coordPonteiro):
				return i
		elif ludo.ultimaCasaBranca(0)+1 < casaTabuleiro < ludo.casaFinal:
			if clicouCasa(des_canvas.coordCasaRetaFinal(jogadorVez)[casaTabuleiro - ludo.ultimaCasaBranca(0) - 2], coordPonteiro):
				return i
	return -1

def mouseClica(event):
	global valorDado, jogo
	c = 0
	cores = ["red", "green", "yellow", "blue"]
	pecaEscolhida = escolhePeca(jogo['tabuleiro'], jogo['jogadorVez'], [event.x, event.y])
	if pecaEscolhida == -1:
		return
	if ludo.podeMoverPeca(jogo['tabuleiro'], jogo['jogadorVez'], pecaEscolhida, valorDado):
		jogadorVez = jogo['jogadorVez']
		c = ludo.moverPeca(jogo, pecaEscolhida, valorDado, True)
		des_canvas.aposclique()
		if jogo['tabuleiro'][jogadorVez].count(58) == 4:
			colocacao = list(range(4))
			colocacao.sort(key=lambda j: sum([ludo.casaJogador(p, j) for p in jogo['tabuleiro'][j]]), reverse=True)
			print(colocacao)
			mensagem = ""
			i = 0
			for j in colocacao:
				i += 1
				mensagem += "Colocação " + str(i) + ":  " + cores[j] + "\n" 
			messagebox.showinfo(message=mensagem)
			
	if c == 6:
		escolheuDado(6)
	return
	
def salvarJogo():
	global jogo
	data = [("text files","*.txt"),("all files","*.*")]
	f = filedialog.asksaveasfile(initialdir=".", title="Salvar Jogo - Super Ludo", mode='w', defaultextension=data, filetypes=data)
	if f is None:
		messagebox.showerror("Erro", "Erro ao salvar arquivo!")
		return
	text2save = str(jogo) # starts from `1.0`, not `0.0`
	f.write(text2save)
	f.close()

def carregarJogo():
	global jogo
	input = filedialog.askopenfile(initialdir=".", title="Carregar Jogo - Super Ludo", filetypes=(("text files","*.txt"),("all files","*.*")))
	if input == None:
		messagebox.showerror("Erro", "Erro ao carregar arquivo!")
		return
	des_tela.salvar['state'] = tkinter.NORMAL
	des_tela.lancar['state'] = tkinter.NORMAL
	jogo = json.loads(input.read().replace("'", "\"")) 
	input.close()
	des_canvas.novo()
