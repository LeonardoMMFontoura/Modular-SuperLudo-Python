import tkinter
from model import ludo
from controller import handler

#lado casa inicial -> 240
#lado casa branca -> 40
#raio da peça -> 40
#base do triângulo da casa final -> 120
#altura do triângulo da casa final -> 60
#altura do triângulo branco -> 30
#base do triângulo branco -> 30

ladoCasa = 40
cnv = {}
jogo = {}
valorDado = 0
cnvdado = {}
dadoimg = []
cores = ["red", "green", "yellow", "blue"]

def jogou(dado):
	global valorDado
	valorDado = dado
	desenhaDadoJogador(cnvdado, valorDado, jogo['jogadorVez'])

def novo():
	global jogo, valorDado, dadoimg, cnvdado
	jogo = handler.getJogo()
	desenhaCasas(cnv)
	desenhaPecas(cnv, jogo['tabuleiro'])
	cnvdado.create_rectangle(0, 0, 40, 40, fill=cores[0])

def desenhaDadoJogador(cnvdado, n, j):
	global dadoimg
	cnvdado.create_rectangle(0, 0, 40, 40, fill=cores[j])
	cnvdado.create_image(5, 5, image=dadoimg[n-1], anchor='nw')

def aposclique():
	global jogo
	desenhaCasas(cnv)
	desenhaPecas(cnv, jogo['tabuleiro'])
	cnvdado.create_rectangle(0, 0, 40, 40, fill=cores[jogo['jogadorVez']])

def inicializar(canvtab, canvdado):
	global cnv, cnvdado, dadoimg
	for n in range(6):
		dadoimg.append(tkinter.PhotoImage(file="dado_"+str(n + 1)+".png"))
	cnv = canvtab
	cnvdado = canvdado
	desenhaCasas(cnv)

def desenhaCasasBrancas(cnv):
	for x1 in [ladoCasa * i for i in range(15)]: # 15 vezes
		#print(x1) # 0 40 80 120 160
		for y1 in [ladoCasa * j for j in range(15)]: # 15 vezes
			#print(y1) #  0 40 80 120 160
			cnv.create_rectangle(x1, y1, x1+ladoCasa, y1+ladoCasa, fill="white")
			
def coordCasasIniciais(j):
	v = [ladoCasa, 4*ladoCasa] # 40 e 160
	#print(v) 
	coords = []
	#print(type(j)) # inteiros 0 1 2 3 4
	for x0 in v:
		for y0 in v:
			coords.append(rotacionase([x0, y0], j))
	"""
	[[40, 40], [40, 160], [160, 40], [160, 160]]
    [[520, 40], [400, 40], [520, 160], [400, 160]]
    [[520, 520], [520, 400], [400, 520], [400, 400]]
    [[40, 520], [160, 520], [40, 400], [160, 400]]
	"""
	return coords

def coordCasaRetaFinal(j): # rotacionase
	return [rotacionase([(i+1)*ladoCasa, 7*ladoCasa], j) for i in range(6)]

def desenhaCasasIniciais(cnv, j):
	#print(type(cnv)) #<class 'tkinter.Canvas'>
	#print(type(j)) #int
	#print(cnv) #.!frame.!canvas
	#print(j) #0 1 2 3 4
	x1, y1 = rotaciona([0, 0], j) # x1 e y1 tipo inteiro
	#print(type(x1)) 
	#print(y1)
	x2, y2 = rotaciona([6*ladoCasa, 6*ladoCasa], j)
	cnv.create_rectangle(x1, y1, x2, y2, fill=cores[j]) # coordenadas de criação das casas iniciais. Aqui que desenha!!!
	for x, y in coordCasasIniciais(j):
		cnv.create_oval(x, y, x+ladoCasa, y+ladoCasa, fill="white", width=3) # esse loop faz o desenho oval das casinhas da casa inicial 

def desenhaCasaSaida(cnv, j):
	x, y = coordCasaComum(ludo.casaSaida(0)) # faz a orientação do desenho na casa de saida
	cnv.create_rectangle(rotaciona([x, y], j) + rotaciona([x + ladoCasa, y + ladoCasa], j), fill=cores[j]) # essa linha desenha o retangulo da casa de saida
	cnv.create_polygon(rotaciona([x+5, y+35], j) + rotaciona([x+5, y+5], j) + rotaciona([x+35, y+20], j), fill="white") # essa linha desenha o triangulo da casa de saida

def desenhaCasasRetaFinal(cnv, j):
	for c in coordCasaRetaFinal(j): 
		x, y = c
		#print(c) # c é uma lista de coordenadas para a casa final
		cnv.create_rectangle(x, y, x+ladoCasa, y+ladoCasa, fill=cores[j])

def desenhaCasaFinal(cnv, j): #j são inteiros que correspondem aos jogadores
	p = rotaciona([ladoCasa * 6, ladoCasa * 6], j) + rotaciona([ladoCasa * 6, ladoCasa * 9], j) + rotaciona([ladoCasa * 7.5, ladoCasa * 7.5], j)
	#print(type(p)) # p é uma lista de coordenadas que definem a casa final
	#print(p)
	""" [240, 240, 240, 360, 300.0, 300.0]
	[360, 240, 240, 240, 300.0, 300.0]
	[360, 360, 360, 240, 300.0, 300.0]
	[240, 360, 360, 360, 300.0, 300.0]"""
	cnv.create_polygon(p, outline="black", fill=cores[j]) # essa linha desenha a casa final 

def desenhaCasasAbrigos(cnv): # olhar ludo.abrigos e coordCasaComum
	for x, y in [coordCasaComum(a) for a in ludo.abrigos]:
		cnv.create_rectangle(x, y, x + ladoCasa, y + ladoCasa, fill="black")

def coordCasaBrancaJ0(c): #c é uma casa no tabuleiro
	i = c + 1
	if 1 <= i <= 5:
		return [ladoCasa * i, ladoCasa * 6]
	elif 6 <= i <= 10:
		return [ladoCasa * 6, ladoCasa * (11-i)]
	elif 11 <= i <= 13:
		return [ladoCasa * (i - 5), 0]


def rotaciona(p, j): # devolve uma lista com as coordenadas
 	return [lambda c: c, lambda c: [15*ladoCasa - c[1], c[0]], lambda c: [15*ladoCasa - c[0], 15*ladoCasa - c[1]], lambda c: [c[1], 15*ladoCasa - c[0]]][j](p)

def rotacionase(p, j): # devolve uma lista com as coordendas
	return [x - ladoCasa//2 for x in rotaciona([x + ladoCasa//2 for x in p], j)]

def coordCasaComum(c):
	i = c - 1
	return rotacionase(coordCasaBrancaJ0(i % 13), i // 13)
# print(coordCasaComum(0))
# print(coordCasaComum(1))
# print(coordCasaComum(2))
# print(coordCasaComum(3))
"""
[0, 240]
[40, 240] 
[80, 240] 
[120, 240]
"""

def coordCasaRetaFinal(j):
	return [rotacionase([(i+1)*ladoCasa, 7*ladoCasa], j) for i in range(6)]
# print(coordCasaRetaFinal(0)) 
# print(coordCasaRetaFinal(1))
# print(coordCasaRetaFinal(2))
# print(coordCasaRetaFinal(3))
"""
[[40, 280], [80, 280], [120, 280], [160, 280], [200, 280], [240, 280]]
[[280, 40], [280, 80], [280, 120], [280, 160], [280, 200], [280, 240]]  
[[520, 280], [480, 280], [440, 280], [400, 280], [360, 280], [320, 280]]
[[280, 520], [280, 480], [280, 440], [280, 400], [280, 360], [280, 320]]
"""

def desenhaCasas(cnv):
	desenhaCasasBrancas(cnv)
	desenhaCasasAbrigos(cnv)
	for j in range(4):
		desenhaCasasIniciais(cnv, j)
		desenhaCasaSaida(cnv, j)
		desenhaCasasRetaFinal(cnv, j)
		desenhaCasaFinal(cnv, j)
	
def desenhaPecasBarreiras(cnv, tabuleiro, j):  
	for x, y in [coordCasaComum(b) for b in ludo.barreiras(tabuleiro, j)]:
		cnv.create_oval(x + 2, y + 2, x+38, y+38, fill=cores[j])
		cnv.create_oval(x + 5, y + 5, x+35, y+35, fill="black")
		desenhaPeca(cnv, x, y, cores[j])

def desenhaPeca(cnv, x, y, color):
	cnv.create_oval(x + 8, y + 8, x+32, y+32, fill=color)

def desenhaPecasIniciais(cnv, tabuleiro, j):
	qtdPecasIniciais = tabuleiro[j].count(0)
	for x, y in coordCasasIniciais(j)[:qtdPecasIniciais]:
		desenhaPeca(cnv, x, y, cores[j])

def desenhaPecasComunsERetaFinal(cnv, tabuleiro, j):
	for p in range(4):
		c = tabuleiro[j][p]
		if ludo.casa2Pecas(tabuleiro, c):
			continue
		if 1 <= c <= ludo.ultimaCasaBranca(0)+1:
			x, y = coordCasaComum(tabuleiro[j][p])
			desenhaPeca(cnv, x, y, cores[j])
		elif (ludo.ultimaCasaBranca(0)+1) < c < ludo.casaFinal:
			x, y = coordCasaRetaFinal(j)[c - ludo.ultimaCasaBranca(0)-2]
			desenhaPeca(cnv, x, y, cores[j])

def desenhaPecasAbrigos(cnv, tabuleiro):
	for abrigo in ludo.abrigos + [ludo.casaSaida(i) for i in range(4)]:
		if ludo.casa2Pecas(tabuleiro, abrigo):
			coresPecas = [cor for i, cor in enumerate(cores) if abrigo in tabuleiro[i]]
			x, y = coordCasaComum(abrigo)
			cnv.create_oval(x + 2, y + 2, x+38, y+38, fill=coresPecas[1])
			cnv.create_oval(x + 5, y + 5, x+35, y+35, fill="white")
			desenhaPeca(cnv, x, y, coresPecas[0])

def desenhaPecas(cnv, tabuleiro):
	desenhaPecasAbrigos(cnv, tabuleiro)
	for j in range(4):
		desenhaPecasIniciais(cnv, tabuleiro, j)
		desenhaPecasComunsERetaFinal(cnv, tabuleiro, j)
		desenhaPecasCasaFinal(cnv, tabuleiro, j)
		desenhaPecasBarreiras(cnv, tabuleiro, j)

def desenhaPecasCasaFinal(cnv, tabuleiro, j):
	x, y = coordCasaRetaFinal(0)[5]
	for i in range(tabuleiro[j].count(ludo.casaFinal)):
		dx, dy = rotacionase([3 * i + x, 3 * i + y], j)
		desenhaPeca(cnv, dx, dy, cores[j])



# Somente para fins de testes
def callback(event):
	pass
def constroiJanela():
	global cnv, cnvdado
	#criação da janela principal
	raiz = tkinter.Tk()
	for n in range(6):
		dadoimg.append(tkinter.PhotoImage(file="dado_"+str(n + 1)+".png"))

	raiz.title("Super Ludo")
	raiz.geometry('850x600')
	#alterna.inicializa()
	#criação do canvas tabuleiro na janela principal
	tab = tkinter.Frame(raiz, width=600, height=600)
	tab.pack(side="left", fill='y')
	cnv = tkinter.Canvas(tab, height=600, width=600)
	cnv.bind("<Button-1>", callback)

	#criação dos botões das opções na janela
	botoes = tkinter.Frame(raiz)
	botoes.pack(side="top", fill='y')
	njogo = tkinter.Button(botoes, text="Novo Jogo", command=novo)
	carregar = tkinter.Button(botoes, text="Carregar Jogo")
	salvar = tkinter.Button(botoes, text="Salvar")
	cnvdado = tkinter.Canvas(botoes, height=50, width=50)

	for i in (njogo, carregar, salvar):
		i.config(font="Arial 12 bold", bg="white", bd=2, height=1, width=18)
	#desenha o tabuleiro e as opções
	
	return [njogo, carregar, salvar, cnv, cnvdado, raiz]
	
	
def desenhaJanela(lista):
	lista[0].pack()
	lista[1].pack()
	lista[2].pack()
	lista[3].pack()
	lista[4].pack()
	lista[5].mainloop()
