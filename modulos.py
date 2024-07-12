import os
import shutil
import sys
import time
import traceback

import pyperclip
import requests

from selenium import webdriver
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
from tkinter import *
from parse import quote

version = '0.20'


def exec_driver():
    s = ChromeService()
    s.creationflags = CREATE_NO_WINDOW
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir={}".format(profile))
    driver = webdriver.Chrome(service=s, options=options)
    return driver


qrCode = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/canvas'
xpathBotaoEnviar = "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"


def get_file_names():
    existe = os.path.exists('./mensagens')
    if existe == False:
        os.makedirs("./mensagens")

    for _, _, arquivos in os.walk('./mensagens'):
        return arquivos


def get_file_text(nome):
    with open("./mensagens/" + nome) as arquivo:
        return arquivo.read()


def create_new_file(nome, conteudo):
    with open(f'./mensagens/{nome}.txt', 'w') as arquivo:
        arquivo.write(conteudo)


def delete_file(nome):
    os.remove("./mensagens/" + nome)


# FUNÇÃO PARA RECEBER OS DADOS DO EXCEL E TRANSFORMA-LOS EM UMA MATRIZ
def obter_dados():
    matriz = []
    dados = (pyperclip.paste()).split("\r\n")  # SEPARA AS COLUNAS DAS LINHAS
    for linha in dados:
        matriz.append(linha.split("\t"))  # SEPARA AS LINHAS DA MATRIZ

    ultima_linha = matriz[-1]

    if len(ultima_linha) == 1:
        if ultima_linha[0] == '':
            matriz.pop()  # REMOVE A LISTA VAZIA QUE É CRIADA NO FIM DA MATRIZ

    return matriz


# RETIRA CARACTERES ESPECIAIS DOS NÚMEROS
def formatar_numeros(numeros):
    for x in range(len(numeros)):
        numeros[x] = ''.join(filter(str.isalnum, numeros[x]))

    return numeros


# FAZER UMA LISTA NA ORDEM DOS NÚMEROS DE TELEFONE
def obter_numeros(linhas):
    numeros = []
    for linha in linhas:
        numeros.append(linha[-1])

    return numeros


# FUNÇÃO PARA RECEBER O TEXTO DO USUÁRIO E INSERIR OS DADOS
def formatar_texto(texto, linhas):
    mensagens = []
    for linha in linhas:
        textoNovo = texto
        for dado in linha:
            textoNovo = textoNovo.replace("/dado/", dado, 1)
        mensagens.append(textoNovo)

    return mensagens


# FUNÇÃO PARA TRANSFORMAR A LISTA DE DADOS EM UMA STRING E ENVIAR PARA O POP UP DE LOG
def preparar_log(log):
    txt = ""
    for linha in log:
        for palavra in linha:
            txt += palavra
            txt += " "
        txt += "\n"

    return txt


# FUNÇÃO PARA CRIAR UM POP UP E MOSTRAR UM TEXTO
def openPopup(log, janela):
    top = Toplevel(janela)
    top.title("VERIFIQUE AS LINHAS DA PLANILHA")
    top.resizable(False, False)
    mylabel = Label(top)
    mylabel.grid()
    text = Text(mylabel, state=NORMAL)
    text.grid(row=0, column=1)
    scrollbar = Scrollbar(mylabel, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, sticky=NSEW)
    text.insert(END, preparar_log(log))
    text.bind("<1>", lambda event: text.focus_set())
    text['state'] = DISABLED


# FUNÇÃO PARA ENVIAR OS NÚMEROS E MENSAGENS COMO PARAMÊTRO PARA ABRIR O WHATSAPP WEB
def enviar_mensagens(texto, linhas, janela):
    try:
        log.clear()
    except:
        pass

    logFinal = []
    check = 2
    if texto.isspace():  # VERIFICA SE A MENSAGEM A SER ENVIADA ESTÁ EM BRANCO
        messagebox.showerror("Nenhuma mensagem", "Preencha o champo de mensagem.")

    else:

        numeros = formatar_numeros(obter_numeros(linhas))
        mensagens = formatar_texto(texto, linhas)

        for numero in numeros:  # VERIFICANDO SE A ÚLTIMA COLUNA POSSÍ APENSAS NÚMEROS DE TELEFONE
            if numero.isnumeric():
                check = 1
            else:
                check = 0
                break

        if check == 1:  # VALIDANDO SE A ÚLTIMA COLUNA POSSÍ APENAS NÚMEROS DE TELEFONE
            for index, numero in enumerate(numeros):
                open_page(numero, mensagens[index])
                print(index)

            for index in range(len(numeros)):
                containerLog = [numero, log[index]]
                logFinal.append(containerLog)
            openPopup(logFinal, janela)

        else:
            messagebox.showerror("Número de telefone inválido",
                                 "Verifique se a última coluna copiada possuí apenas números de telefone.")


log = []


def open_page(numero, mensagem):
    driver = exec_driver()

    time.sleep(1)

    try:
        driver.get(f"https://web.whatsapp.com/send?phone=+55{numero}&text={quote(mensagem)}")
    except Exception as e:
        with open('error.txt', 'w') as error_file:
            error_file.write(f"Ocorreu um erro: {e}\n")
            traceback.print_exc(file=error_file)

    i = 0
    j = 0

    print("carregando tela")
    while i == 0:

        try:
            driver.find_element(by=By.CLASS_NAME, value="xixxii4")
            i = 1
            print("carregou tela")
        except:
            pass

    time.sleep(1)
    print("carregando chat...")
    while j == 0:

        try:
            driver.find_element(by=By.CLASS_NAME, value="x132q4wb")
        except:
            j = 1
            print("carregou chat")

    try:

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpathBotaoEnviar))).click()

        time.sleep(1)

        element = driver.find_elements(By.XPATH, "//div[@class='x1pn4fmt x1rg5ohu x1w4ip6v']//span")[-1]

        element_html = element.get_attribute("outerHTML")

        start_index = element_html.find("<title>") + len("<title>")

        end_index = element_html.find("</title>")

        title_text = element_html[start_index:end_index]

        print("Aguardando envio")

        while title_text == "msg-time":
            element = driver.find_elements(By.XPATH, "//div[@class='x1pn4fmt x1rg5ohu x1w4ip6v']//span")[-1]
            element_html = element.get_attribute("outerHTML")

            start_index = element_html.find("<title>") + len("<title>")

            end_index = element_html.find("</title>")

            title_text = element_html[start_index:end_index]

        print("enviado")
        log.append("VALIDO")

    except Exception as e:
        print("ocorreu um erro ao enviar a mensagem")
        print(e)
        log.append("INVALIDO")


def verificarSrc(url):
    print("verificando src...")

    assets = ['task.ico', 'linkedln.png', 'github.png']

    if not os.path.exists('./src'):
        os.makedirs("./src")

    arquivos = [arquivos for _, _, arquivos in os.walk('./src')]

    for asset in assets:
        if asset not in arquivos[0]:
            baixarSrc(url + asset, "./src/" + asset)


def verifificarAtualizações():
    print("Checando versão...")
    r = requests.get('https://raw.githubusercontent.com/resen-dev/bot_version/main/version.txt')

    if r.status_code != 200:
        messagebox.showerror("Não foi possível conectar no servidor.",
                             "Verifique sua internet ou contate o administrador.")
        sys.exit()

    print("Versão: ", r.text)

    return r.text == version


def baixarArquivos(url, local_filename):
    with requests.get(url + local_filename, stream=True) as t:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(t.raw, f)


def baixarSrc(url, local_filename):
    with requests.get(url, stream=True) as t:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(t.raw, f)
