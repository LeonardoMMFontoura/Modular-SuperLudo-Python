import tkinter
from tkinter import ttk
from view import des_canvas
from model import ludo
from controller import handler

def getValor():
	v = int(escolhevalor.get())
	escolhevalor.set("")
	handler.escolheuDado(v)

raiz = tkinter.Tk()
raiz.title("Super Ludo")
raiz.geometry('850x600')

def lanca():
    ludo.lancou = True
    lancar['state'] = tkinter.DISABLED
    salvar['state'] = tkinter.DISABLED
    handler.lanca()

	
#criação do canvas tabuleiro na janela principal
tab = tkinter.Frame(raiz, width=600, height=600)
tab.pack(side="left", fill='y')
cnv = tkinter.Canvas(tab, height=600, width=600)
cnv.bind("<Button-1>", handler.mouseClica)

#criação dos botões das opções na janela
botoes = tkinter.Frame(raiz)
botoes.pack(side="top", fill='y')

njogo = tkinter.Button(botoes, text="Novo Jogo", command=handler.novoJ)
njogo.pack(pady=10)

carregar = tkinter.Button(botoes, text="Carregar Jogo", command=handler.carregarJogo)
carregar.pack(pady=10)

salvar = tkinter.Button(botoes, text="Salvar", command=handler.salvarJogo)
#salvar.config(state="disabled")
salvar.pack(pady=10)

texto = tkinter.Label(botoes, text="A JOGAR:")
texto.config(font="Arial 16 bold", bd=2, height=1, width=18)
texto.pack(pady=10)

cnvdado = tkinter.Canvas(botoes, height=50, width=50)
cnvdado.pack(pady=10)

texto2 = tkinter.Label(botoes, text="Escolha o valor do dado:")
texto2.config(font="Arial 12 bold", bd=2, height=1, width=30)
texto2.pack(pady=5)

escolhevalor = ttk.Combobox(botoes, values=list(range(1,7)))
escolhevalor.pack(pady=5)

enviavalor = tkinter.Button(botoes, text="Enviar", command=getValor)
enviavalor.config(font="Arial 9 bold", bg="white", bd=2, height=1, width=7)
enviavalor.pack(pady=3)

lancar = tkinter.Button(botoes, text="Lançar Dado", command=lanca)
lancar.pack(pady=30)

for i in (njogo, carregar, salvar, lancar):
	i.config(font="Arial 12 bold", bg="white", bd=2, height=1, width=18)

des_canvas.inicializar(cnv, cnvdado)

cnv.pack()
raiz.mainloop()
