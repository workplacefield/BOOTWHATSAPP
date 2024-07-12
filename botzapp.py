from tkinter import messagebox as mb
from tkinter import ttk
from modulos import *
from PIL import ImageTk, Image
import webbrowser
import sys

matriz = []
mensagens = []

url_exe = 'https://github.com/resen-dev/bot_version/raw/main/'
url_src = 'https://raw.githubusercontent.com/resen-dev/bot_version/main/src/'

verificarSrc(url_src)

if verifificarAtualizações() is False:

    if mb.askquestion('Atualize', 'Atualizações foram encontradas, deseja atualizar?') == 'yes':
        try:
            baixarArquivos(url_exe, "updater.exe")
            os.startfile("updater.exe")
        except:
            mb.showerror("Erro", "Não foi possível atualizar.")

    sys.exit()

# FUNÇÃO PARA O USUARIO APAGAR UMA MENSAGEM / SALVAR NOS ARQUIVOS
def apagar_mensagem():
    list = get_file_names()
    nome = list[combobox.current()]
    delete_file(nome)
    tela_inicial()


# FUNÇÃO PARA O USUARIO CRIAR UMA NOVA MENSAGEM / SALVAR NOS ARQUIVOS
def criar_mensagem():
    if btnCriar['text'] == "CRIAR":  # trocar estado da tela para modo criação de mensagem
        tela_criar()
    else:

        nome = (txtNome.get()).upper()

        if nome.isspace() or nome == "":  # checando se o nome do arquivo é em branco
            lblCombo['text'] = "NOME EM BRANCO! "
            lblCombo['fg'] = "red"

        elif nome + '.txt' in get_file_names():  # checando se o nome do arquivo já existe
            lblCombo['text'] = "NOME JÁ EXISTE! "
            lblCombo['fg'] = "red"

        else:
            create_new_file(nome, txtMensagem.get("1.0", END))  # receber o nome para o novo arquivo
            tela_inicial()  # trocar estado da tela para modo inicial


# ESCREVE O ARQUIVO NO CAMPO DE TEXTO / EVENTO DA COMBOBOX
def colar_mensagem(event):
    file = event.widget.get()
    txtMensagem.delete("1.0", "end")
    txtMensagem.insert("1.0", get_file_text(file))
    btnEditar['state'] = "normal"
    btnApagar['state'] = "normal"


# TELAS DA GUI
def tela_editar():
    if btnEditar['text'] == "EDITAR":
        btnCriar['state'] = "disabled"
        btnApagar['state'] = "disabled"
        btnCancelar['state'] = "normal"
        combobox['state'] = 'disabled'
        btnEditar['text'] = "SALVAR"
        btnColar['state'] = 'disabled'
        btnDisparar['state'] = 'disabled'
    else:
        nome = get_file_names()
        create_new_file(nome[combobox.current()].replace(".txt", ""), txtMensagem.get("1.0", END))
        btnEditar['text'] = "EDITAR"
        tela_inicial()


def tela_criar():
    combobox.grid_remove()
    txtNome.grid()
    txtNome.delete(0, END)
    txtMensagem.delete("1.0", "end")
    lblCombo["text"] = "NOME DA MENSAGEM: "
    btnCancelar['state'] = 'normal'
    btnEditar['state'] = 'disabled'
    btnApagar['state'] = 'disabled'
    btnColar['state'] = "disabled"
    btnDisparar['state'] = "disabled"
    btnCriar['text'] = "SALVAR"


def tela_inicial():
    lblCombo['text'] = "SELECIONE A MENSAGEM:"
    txtNome.grid_remove()
    combobox.grid_remove()
    combobox.grid()
    combobox['values'] = get_file_names()
    combobox['state'] = 'readonly'
    combobox.set('')
    txtMensagem.delete("1.0", "end")
    txtMensagem.focus()
    btnCriar['text'] = 'CRIAR'
    btnCriar['state'] = 'normal'
    btnEditar['state'] = "disabled"
    btnApagar['state'] = "disabled"
    btnCancelar['state'] = "disabled"
    btnColar['state'] = 'normal'
    btnDisparar['state'] = 'normal'
    lblCombo['fg'] = 'black'
    btnEditar['text'] = "EDITAR"


# GUI
backgroundColor = "#69f0ae"
buttonColor = "#2bbd7e"
buttonSize = 13
margem = 5

janela = Tk()
janela.title("BOTZAPP " + version)
janela.resizable(False, False)
janela.config(background=backgroundColor, padx=margem, pady=margem)

## CRIANDO OS WIDGETS

# HEADER
header = Frame(bg=backgroundColor)
lblCombo = Label(header, text="SELECIONE A MENSAGEM:", bg=backgroundColor)
txtNome = Entry(header, width=29)
combobox = ttk.Combobox(header, state="readonly", values=get_file_names(), width=24)

# CONTENT
txtMensagem = Text(janela, width=40, height=25)
aside = Frame(bg=backgroundColor)
btnCriar = Button(aside, text="CRIAR", bg=buttonColor, width=buttonSize, command=criar_mensagem)
btnEditar = Button(aside, text="EDITAR", bg=buttonColor, width=buttonSize, state="disabled", command=tela_editar)
btnApagar = Button(aside, text="APAGAR", bg=buttonColor, width=buttonSize, state="disabled", command=apagar_mensagem)
btnCancelar = Button(aside, text="CANCELAR", bg=buttonColor, width=buttonSize, state="disabled", command=tela_inicial)
containerImagens = Frame(janela, bg=backgroundColor)

# FOOTER
footer = Frame(bg=backgroundColor)


def colar_dados():  # DEIXA OS DADOS SALVOS EM CACHE
    global matriz
    matriz = obter_dados()
    openPopup(matriz, janela)


btnColar = Button(footer, text="COLAR CÉLULAS", bg=buttonColor, command=colar_dados)
btnDisparar = Button(footer, text="ENVIAR MENSAGENS", bg=buttonColor, command= lambda: enviar_mensagens(txtMensagem.get("1.0", "end"), matriz, janela))

# IMAGENS
github = Image.open("./src/github.png")
github = github.resize((48, 48), Image.Resampling.LANCZOS)
imgGithub = ImageTk.PhotoImage(github)
lblGithub = Label(containerImagens, image=imgGithub, bg=backgroundColor)
lblGithub.image = ImageTk.PhotoImage(github)

linkedln = Image.open("./src/linkedln.png")
linkedln = linkedln.resize((48, 48), Image.Resampling.LANCZOS)
imgLinkedln = ImageTk.PhotoImage(linkedln)
lblLinkedln = Label(containerImagens, image=imgLinkedln, bg=backgroundColor)
lblLinkedln.image = imgLinkedln

## POSICIONANDO ELEMENTOS

# HEADER
header.grid(row=0, column=0)
lblCombo.grid(row=0, column=0, pady=margem, padx=margem)
txtNome.grid(row=0, column=1, pady=margem, padx=margem)
txtNome.grid_remove()
combobox.grid(row=0, column=1, pady=margem, padx=margem)

# CONTENT
txtMensagem.grid(row=1, column=0, pady=margem, padx=margem)
aside.grid(row=1, column=1)
btnCriar.grid(row=1, column=0, pady=margem, padx=margem)
btnEditar.grid(row=2, column=0, pady=margem, padx=margem)
btnApagar.grid(row=3, column=0, pady=margem, padx=margem)
btnCancelar.grid(row=4, column=0, pady=margem, padx=margem)
containerImagens.grid(row=2, column=1)
lblLinkedln.grid(row=0, column=1)

# FOOTER
footer.grid(row=2, column=0)
btnColar.grid(row=0, column=0, pady=margem, padx=margem)
btnDisparar.grid(row=0, column=1, pady=margem, padx=margem)

combobox.bind("<<ComboboxSelected>>", colar_mensagem)  # EVENTO DA COMBOBOX APÓS ALTERAR O VALOR
lblLinkedln.bind("<Button-1>", lambda event: webbrowser.open('https://www.linkedin.com/in/raulresendedev/'))

janela.mainloop()
