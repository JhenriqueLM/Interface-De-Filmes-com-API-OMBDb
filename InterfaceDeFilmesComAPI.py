from customtkinter import *
import requests
from PIL import Image
from io import BytesIO
import re

# Recebendo a url da API
def Films( name_film):
    global pagina
    print(pagina)
    response = requests.get(f"https://www.omdbapi.com/?apikey=241e144&s={name_film}&page={pagina}&plot=full")
    response = response.json()
    return response

# recenbendo a image do poster do filme para exibicao   
def imagemDoPoster (url):
    imagemResponse = requests.get(url).content
    imgem = Image.open(BytesIO(imagemResponse))
    imagemASerExibida = CTkImage(light_image= imgem,size=(180, 252))
    return imagemASerExibida

# Exxibindo as informacoes do filme( titulo, ano , poster)
def perfilFilmes(nameFilm):

    global distanciamentoNoComprimento
    global distanciamentoNaLargura
    global leitoDeFilm
    global pagina
   
    nameFilm =re.sub(r'"','', nameFilm)
    filme = Films(nameFilm)
    lacalizado = filme['Search'][leitoDeFilm]['Title']
    font = ('Arial', 18)
    labelTitle = CTkLabel(janela, text= f"{lacalizado}", font= font)
    labelTitle.place(x= 105 + distanciamentoNoComprimento ,y = 120 + distanciamentoNaLargura)


    font = ('Arial',12)
    labelYear = CTkLabel(janela, text= f"Ano De Lancamento: {filme['Search'][leitoDeFilm]['Year']}",font= font)
    labelYear.place( x=105 + distanciamentoNoComprimento , y= 407 + distanciamentoNaLargura)

    labelPoster = CTkLabel(janela, image = imagemDoPoster(filme['Search'][leitoDeFilm]['Poster']),text="")
    labelPoster.place( x=105 + distanciamentoNoComprimento, y= 160 + distanciamentoNaLargura)
    distanciamentoNoComprimento = distanciamentoNoComprimento + 280

    leitoDeFilm = leitoDeFilm +1

# Exibindos as informacao do filme e enquadrando na tela
def atualizandoQuantidadeDePoster(enredo):
    global distanciamentoNoComprimento
    global distanciamentoNaLargura
    global leitoDeFilm
    global numeroDePoster
    x = 11
    for x in range(x):
        global leitoDeFilm
        perfilFilmes(enredo )
        numeroDePoster = numeroDePoster + 1
        if numeroDePoster == 5:
            distanciamentoNoComprimento = 0
            distanciamentoNaLargura = 330
        if numeroDePoster == 10 :
            leitoDeFilm = 0 
            distanciamentoNoComprimento = 0
            distanciamentoNaLargura = 0
        mudadorDePagina("Direito")
        mudadorDePagina("Esqueda")
        
    
# E a funcao que executa atualizandoQuantidadeDePoster e moster os butoes na tela 
def PlayList ():
    global distanciamentoNoComprimento
    global distanciamentoNaLargura
    global leitoDeFilm
    global enredo 
    global pagina
    distanciamentoNoComprimento = 0
    distanciamentoNaLargura  = 0
    leitoDeFilm = 0
    respose = enredo.get()
    atualizandoQuantidadeDePoster(respose)
    #print(pagina)


    #print("Butao esta sendo pressionado ")

# Passa a pagina de filmes atualizando na tela
def passaPagina():
    global pagina
    limpar_janela()
    pagina = pagina +1
    # print(pagina)
    # print(pag)
    PlayList()
    #print("Butao esta sendo pressionado ") 

# volt a pagina de filmes atualizando para a tela anterior
def voltaPagina():
    global pagina
    limpar_janela()
    pagina = pagina -1
    print(pagina)
    # print(pag)
    PlayList()

# limpa a tela para receber uma nova pagina de filmes 
def limpar_janela():
    global numeroDePoster
    for widget in janela.winfo_children():
        if isinstance (widget,CTkLabel ):
            widget.destroy()
    font = ('Arial', 50)
    titleDaPagina = CTkLabel(janela, text="Filmes" , font = font)
    titleDaPagina.place(x = 730, y = 40)
    numeroDePoster = 1


# Exibindo os botoes de passa ou volta a pagina 
def mudadorDePagina(ladoDaSeta):
    global pagina

    if ladoDaSeta == "Direito":
        
        seta =  "primeiroFrontEnd\ImagemDaSeta.png"
        imageDaSeta = Image.open(seta)
        imageDaSetaDireita =imageDaSeta.rotate(180)

        imageCeta= CTkImage(light_image= imageDaSetaDireita, size=(15,60))
        button = CTkButton(janela, text="", image =imageCeta, width= 50, height= 10, command= passaPagina)
        button.place(x = 1440 , y =400)
    else :
        print(pagina)
        if pagina > 1 :
            seta =  "primeiroFrontEnd\ImagemDaSeta.png"
            imageDaSeta = Image.open(seta)

            imageCeta= CTkImage(light_image= imageDaSeta, size=(15,60))
            button = CTkButton(janela, text="", image =imageCeta, width= 50, height= 10 ,command= voltaPagina)
            button.place(x = 40 , y =400)

# Criando a tela 
set_appearance_mode( "dack")

janela = CTk()
janela.title("Filme")
janela.geometry("1920x1080")
distanciamentoNoComprimento = 0
distanciamentoNaLargura = 0
numeroDePoster = 0
leitoDeFilm =0
pagina =1

font = ('Arial', 50)
titleDaPagina = CTkLabel(janela, text="Filmes" , font = font)
titleDaPagina.place(x = 730, y = 40)

enredo = CTkEntry(janela, placeholder_text="Digite o nome do filme" , width= 230)
enredo.place(x= 1190, y = 45)

button = CTkButton(janela, text="Pesquisa", width= 70, height= 27, command=PlayList)
button.place(x = 1360 , y =45)
button = CTkButton(janela, text="Limpa", width= 70, height= 27, command= limpar_janela)
button.place(x = 1360 , y =80)

janela.mainloop()
    