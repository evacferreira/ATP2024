
import json 
import os
import unicodedata
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import FreeSimpleGUI as sg
from PIL import Image
import io
import calendar


#----------------------------------------------------------------Funções-------------------------------------------------------------------
#FUNÇÕES AUXILIARES    
def confirmarDOI(fnome,d): #confirma que o doi introduzido existe na base de dados
    publicacoes = lerBD(fnome)
    for publicacao in publicacoes:
        if isinstance(publicacao, dict): # Verifique se publicacao é um dicionário antes de usar o 'get'
            if publicacao.get('doi') == d:
                return True
    return False

def DOIexistentes(fnome):
    listadois=[]
    publicacoes=lerBD(fnome)
    for publicacao in publicacoes:
        if publicacao['doi'][29:] not in listadois:
            listadois.append(publicacao['doi'][29:])
        else:
            print('erro')
    return listadois

listaeliminados= []

def DOIeliminados(d):
  
    if d and d not in listaeliminados:  # Verifica se o DOI não é vazio e não está na lista
        listaeliminados.append(d)
    
    return listaeliminados

def criarDOI(fnome):
    lista=[]
    res=''
    existentes=DOIexistentes(fnome)
    for e in existentes:
        if e.isdigit():
          lista.append(int(e))
    eliminados=DOIeliminados(fnome)
    for el in eliminados:
        if el.isdigit():
          lista.append(int(el))
    
    ordenada=sorted(lista, reverse=True)
    num=ordenada[0]+1
    res='https://doi.org/10.20344/amp.'+str(num)
    return res

def gerarurl(fnome,doi):
    doi=criarDOI(fnome)
    res='https://www.actamedicaportuguesa.com/revista/index.php/amp/article/view/'+ doi[29:]
    return res

def gerarpdf(fnome, doi):
    doi=criarDOI(fnome)
    res='https://www.actamedicaportuguesa.com/revista/index.php/amp/article/view/'+ doi[29:]+'/'+doi[29:]
    return res

def obter_publicacao_por_doi(fnome, d): #recebe o doi de uma publicação e devolve a publicação por completo
    publicacoes = lerBD(fnome)
    for publicacao in publicacoes:
        if publicacao["doi"] == d:
            return publicacao
    return None

def obter_publicacao_por_titulo(fnome, titulo): #recebe o doi de uma publicação e devolve a publicação por completo
    publicacoes = lerBD(fnome)
    for publicacao in publicacoes:
        if publicacao["title"] == titulo:
            return publicacao
    return None

def listarAnos(fnome):
    dados_por_ano = conta_ano(fnome)
    anos = list(dados_por_ano.keys())

    return anos

def listar_autor(fnome):
    artigos = lerBD(fnome)
    lista = []
    
    for artigo in artigos:
        data_publicacao = artigo.get('publish_date')
        if data_publicacao:  # Só continua se o artigo tiver uma data
            autores = artigo.get("authors", [])
            for autor in autores:
                # Garante que autor tenha a chave 'name'
                if 'name' in autor and autor['name'] not in lista:
                    lista.append(autor['name'])
    
    ordenada = sorted(lista)
    return ordenada

#FUNÇÕES GERAIS
def lerBD(fnome):
    # Verifique se o arquivo existe e se não está vazio
    if not os.path.exists(fnome):
        
        return []
    
    # Verifique se o arquivo não está vazio
    if os.stat(fnome).st_size == 0:
        
        return []

    try:
        with open(fnome, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        
        return []
    
def importar_novos_registos(bd_atual, novo_ficheiro):

    with open(novo_ficheiro, 'r', encoding='utf-8') as f:
        novos_registos = json.load(f)

    # Criar um conjunto de DOIs existentes
    dois_existentes = {pub.get('doi') for pub in bd_atual if 'doi' in pub}

    # Adicionar apenas os registos novos
    novos_adicionados = 0
    for novo_registo in novos_registos:
        if novo_registo.get('doi') not in dois_existentes:
            bd_atual.append(novo_registo)
            novos_adicionados += 1

    return bd_atual, novos_adicionados

def exportarBd(fnome, fexportado):
    publicacoes_atualizadas = lerBD(fnome)
    with open(fexportado, "w", encoding="utf-8") as f_export:
        json.dump(publicacoes_atualizadas, f_export, indent=2, ensure_ascii=False)

    return fexportado

def criar2(fnome, abstract, palavras_chave, autores, doi, pdf, data_publicacao, titulo, url):
    publicacoes = lerBD(fnome)
    
    if confirmarDOI(fnome, doi):
        print("Publicação com esse DOI já existe.")
        return None
    else:
        # Cria o dicionário da nova publicação
        novapublicacao = {}

        # Adiciona os campos apenas se tiverem valor
        if abstract: novapublicacao["abstract"] = abstract
        if palavras_chave and any(palavras_chave):  
            novapublicacao["keywords"] = palavras_chave
        
        autores_filtrados = []
        for autor in autores:
            autor_filtrado = {key: value for key, value in autor.items() if value}  # Remove chaves com valores None ou vazios
            if autor_filtrado:  # Adiciona autor apenas se houver pelo menos um campo preenchido
                autores_filtrados.append(autor_filtrado)
        
        if autores_filtrados:
            novapublicacao["authors"] = autores_filtrados

        if doi:
            novapublicacao["doi"] = doi
        
        if pdf:
            novapublicacao["pdf"] = pdf

        if data_publicacao:
            novapublicacao["publish_date"] = data_publicacao
        
        if titulo:
            novapublicacao["title"] = titulo
        
        if url:
            novapublicacao["url"] = url

        # Adiciona a nova publicação ao arquivo JSON
        publicacoes.append(novapublicacao) 
        
        with open(fnome, "w", encoding='utf-8') as f:
            json.dump(publicacoes, f, indent=2, ensure_ascii=False)
        
        return novapublicacao

def eliminar(fnome,d): #coloca todas as tarefas que não vão ser eliminadas, e retorna-as ao json, não voltando apenas a que queremos eliminar
    publicacoes = lerBD(fnome)
    f=open(fnome,"w", encoding='utf-8')
    for publicacao in publicacoes:
        if publicacao["doi"] == d:
            publicacoes.remove(publicacao)
    
    DOIeliminados(d)

    json.dump(publicacoes,f, indent=2, ensure_ascii=False)
    return publicacoes


def atualizar2(fnome, **nova_publicacao):
    publicacoes = lerBD(fnome)

    listapublicacoes = []
    
    for publicacao in publicacoes:
        if publicacao["doi"] == nova_publicacao.get("doi"):
            
            # Verifica se o título e o abstract não estão vazios
            if not nova_publicacao.get("title") or not nova_publicacao.get("abstract"):
                continue  # Se faltar título ou abstract, não atualiza

            # Verifica se há pelo menos um autor com nome preenchido
            autores_atualizados = nova_publicacao.get("authors", [])
            autores_validos = [autor for autor in autores_atualizados if autor.get('name')]  # Filtra apenas os autores com nome válido
            if not autores_validos:
                continue  # Se não houver autores com nome, não atualiza

            # Atualiza os campos da publicação com os novos valores
            for key, value in nova_publicacao.items():
                # Se o valor for válido (não None ou vazio), atualiza o campo
                if value or value == 0:  # Aceita 0 como valor válido
                    publicacao[key] = value
                else:
                    # Se o valor for vazio, remove o campo (apaga completamente)
                    if key in publicacao:
                        del publicacao[key]
            if not nova_publicacao.get("keywords"):
                if "keywords" in publicacao:
                    del publicacao["keywords"]
        listapublicacoes.append(publicacao)

    with open(fnome, "w", encoding="utf-8") as f:
        json.dump(listapublicacoes, f, indent=2, ensure_ascii=False)


def ordena_por_titulo(fnome):
    def normaliza(texto):
        return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')
    
    publicacoes = lerBD(fnome)
    publicacoes.sort(key=lambda publicacao: normaliza(publicacao['title']).lower())
    
    return publicacoes


def ordena_por_data(fnome):
    publicacoes=lerBD(fnome)
    publicacoes_com_data = [pub for pub in publicacoes if pub.get('publish_date')]

    publicacoes_com_data.sort(key=lambda pub: datetime.strptime(pub['publish_date'].split(' — ')[0], '%Y-%m-%d'), reverse=True)

    return publicacoes_com_data


def consultar_todaspublicacoes(fnome):
    publicacoes=lerBD(fnome)
    return publicacoes

def consultaPublicacaoTitulo(fnome, titulo):
    publicacoes=lerBD(fnome)
    lista=[]
    for publicacao in publicacoes:
        if publicacao.get('title')==titulo and titulo!='':
            lista.append(publicacao)
    return lista

def consultaPublicacao_keywords(fnome, palavraschave):
    publicacoes=lerBD(fnome)
    lista=[]
    for publicacao in publicacoes:
        keywords = publicacao.get('keywords', '')
        if palavraschave in keywords and palavraschave!='':
            lista.append(publicacao)
    return lista

def consultaPublicacao_autor(fnome, autor):
    publicacoes=lerBD(fnome)
    lista=[]
    for publicacao in publicacoes:
        autores = publicacao.get('authors')
        if autores:
         for a in autores:
           if autor==a['name']:
             lista.append(publicacao)
    return lista

def consultaPublicacao_afiliacao(fnome, afiliacao):
    publicacoes = lerBD(fnome)
    lista = []  
    for publicacao in publicacoes:
        autores = publicacao.get('authors')  
        if isinstance(autores, list):  
            for a in autores:  
                if afiliacao in a.get('affiliation', '') and afiliacao != '':
                    lista.append(publicacao)  
                    break  
    return lista  

def consultaPublicacao_data(fnome, data):
    publicacoes = lerBD(fnome)  # Lê a base de dados
    lista = []  # Inicializa uma lista para armazenar resultados
    
    # Tenta formatar a data fornecida
    try:
        data_formatada = datetime.strptime(data, '%Y-%m-%d').date()  # Formata a data de entrada
    except ValueError:
        print("Erro: O formato da data deve ser YYYY-MM-DD.")
        return lista  # Retorna lista vazia se o formato estiver errado

    for publicacao in publicacoes:
        # Tente obter a data de publicação, convertendo-a se necessário
        pub_date = publicacao.get('publish_date')
        if isinstance(pub_date, str):
            try:
                pub_date = datetime.strptime(pub_date, '%Y-%m-%d').date()  # Converte string para data
            except ValueError:
                continue  # Se não puder converter, pule essa publicação

        if pub_date == data_formatada:  # Compara a data de publicação com a data formatada
            lista.append(publicacao)  # Adiciona a publicação à lista se as datas coincidirem
        
    return lista  # Retorna a lista de publicações


def opçoes_autores(fnome):
    publicacoes=lerBD(fnome)
    listaautores=[]
    for publicacao in publicacoes:
        autores = publicacao.get('authors',[])
        for a in autores:
           if a['name'] not in listaautores:
              listaautores.append(a['name'])
    return listaautores


def listar_aut_artigo(fnome): #lista os autores por ordem de frequência de artigos publicados
    artigos = lerBD(fnome)
    dicaut = {} #fazemos um novo dicionário
    for artigo in artigos:
        for autor in artigo["authors"]:
            nome = autor["name"]
            if nome not in dicaut: #se o autor não estiver no dicionário
                dicaut[nome] = 1 # n_artigos = 1
            else: #se já estiver
                dicaut[nome] += 1 # n_artigos aumenta
    listaut_art = sorted(dicaut.items(), key=lambda item: item[1], reverse=True) #retorna a lista dos tuplos (autor , n_artigos), ordenada do maior para o menor consoante n_artigos publicados pelos autores
    return listaut_art


def listar_aut_alfabetico(fnome): #lista com todos os autores por ordem alfabética
    listaut_alf = []
    artigos = lerBD(fnome)
    for artigo in artigos:
        for autor in artigo["authors"]:
            nome = autor["name"]
            if nome not in listaut_alf: #para listas grandes pode se tornar lento
                listaut_alf.append(nome)
    return sorted(listaut_alf)

def artigos_aut_artigo(fnome, autor_proc): #lista todos os artigos dos autores, organizando-os por frequência de artigos publicados
    lista = listar_aut_artigo(fnome)
    artigos = lerBD(fnome)
    dici = {}
    for autor, freq in lista:
        dici[autor] = []
        for artigo in artigos:
            for autor_art in artigo["authors"]:
                if autor_art["name"] == autor:
                    dici[autor].append(artigo)
                    break
    return dici.get(autor_proc, [])

def artigos_aut_alfabético(fnome, autor_art): #lista todos os artigos dos autores, organizando-os por ordem alfabética
    lista = listar_aut_alfabetico(fnome)
    artigos = lerBD(fnome)
    dic = {}
    for autor in lista:
        dic[autor] = []
        for artigo in artigos:
            for autor_alf in artigo["authors"]:
                if autor_alf["name"] == autor:
                    dic[autor].append(artigo)
                    break
    return dic.get(autor_art, [])


def listar_palavras(fnome): #lista as palavras por ordem de frequência em artigos publicados
    artigos = lerBD(fnome)
    dicpal = {}
    for artigo in artigos:
        palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
        if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
            palavras_chave = palavras_chave.lower().split(", ")
        elif isinstance(palavras_chave, list):  # Se for uma lista
            palavras_chave = [palavra.lower() for palavra in palavras_chave]
        else:
            continue
        for pal in palavras_chave:
            if pal not in dicpal:
                dicpal[pal] = 1
            else:
                dicpal[pal] += 1
    listapal_art = sorted(dicpal.items(), key = lambda item: item[1], reverse = True) #retorna a lista dos tuplos (pal , freq), ordenada do maior para o menor consoante freq em artigos
    return listapal_art


def listar_palavras_alfabetico(fnome):
    listapal_alf = []
    artigos = lerBD(fnome)
    for artigo in artigos:
        palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
        if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
            palavras_chave = palavras_chave.lower().split(", ")
        elif isinstance(palavras_chave, list):  # Se for uma lista
            palavras_chave = [palavra.lower() for palavra in palavras_chave]
        else:
            continue
        for pal in palavras_chave:
            if pal not in listapal_alf:
                listapal_alf.append(pal)
    return sorted(listapal_alf)


def artigo_palavra(fnome, palavra_art):
    lista = listar_palavras(fnome)
    artigos = lerBD(fnome)
    dic = {}
    for pal, freq in lista:
        dic[pal] = []
        for artigo in artigos:
            palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
            if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
                palavras_chave = palavras_chave.lower().split(", ")
            elif isinstance(palavras_chave, list):  # Se for uma lista
                palavras_chave = [palavra.lower() for palavra in palavras_chave]
            else:
                continue
            for pala in palavras_chave:
                if pala == pal:
                    dic[pal]. append(artigo)
                    break
    return dic.get(palavra_art, [])


def artigo_palavra_alfabetico(fnome, pal_proc):
    lista = listar_palavras_alfabetico(fnome)
    artigos = lerBD(fnome)
    dici = {}
    for pal in lista:
        dici[pal] = []
        for artigo in artigos:
            palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
            if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
                palavras_chave = palavras_chave.lower().split(", ")
            elif isinstance(palavras_chave, list):  # Se for uma lista
                palavras_chave = [palavra.lower() for palavra in palavras_chave]
            else:
                continue
            for pala in palavras_chave:
                if pala == pal:
                    dici[pal].append(artigo)
    return dici.get(pal_proc, [])


def consultaPublicacao_data1(fnome, data):
    publicacoes = lerBD(fnome)
    lista = []

    for publicacao in publicacoes:
        # Formata a data da publicação para string
        data_publicacao = publicacao.get('publish_date')
        
        if data_publicacao == data:  # Comparação string com string
            lista.append(publicacao)
    return lista


def conta_ano(fnome): #numero de publicação por ano
    artigos = lerBD(fnome)  
    publicacoes_por_ano = {}  # Dicionário para armazenar contagem por ano
    for artigo in artigos:
        data_publicacao = artigo.get("publish_date")  # Supondo que seja no formato 'YYYY-MM-DD'
        if isinstance(data_publicacao, str):  # Se for uma string, separa-a por -, tornando todas as letras minusculas
            partes_data = data_publicacao.split("-")
        else:
            continue
        ano = partes_data[0]  # obtem apenas o que representa o ano
        if ano in publicacoes_por_ano:
            publicacoes_por_ano[ano] += 1
        else:
            publicacoes_por_ano[ano] = 1
    return publicacoes_por_ano


def conta_ano_GrafBarras(fnome):
    plt.clf()
    dados_por_ano = conta_ano(fnome)
    anos = list(dados_por_ano.keys())  # Eixo X: anos
    num_publicacoes = list(dados_por_ano.values())  # Eixo Y: número de publicações

    plt.bar(anos, num_publicacoes, color="mediumvioletred")
    plt.xlabel("Ano")  # Rótulo do eixo X
    plt.ylabel("Número de Publicações")  # Rótulo do eixo Y
    plt.title("Número de Publicações por Ano")  # Título do gráfico
    plt.xticks(rotation=45)  # Rodar os anos no eixo X para melhor visualização
    plt.tight_layout()  # Ajustar margens para evitar cortes no gráfico

    # Adicionando o número de publicações acima de cada barra
    for i, valor in enumerate(num_publicacoes):
        plt.text(anos[i], valor + 0.1, str(valor), ha='center', va='bottom', fontsize=10)

    plt.savefig("grafico_conta_ano.png", dpi=180, bbox_inches="tight")

    return


def conta_mes(fnome, ano_art):  #número de publicações por mês de um determinado ano
    artigos = lerBD(fnome)
    publicacoes_mes = {f"{i:02}": 0 for i in range(1, 13)}  #para transformar no formato MM (01, 02, ..., 12)
    artigos_verificados = 0
    artigos_excluidos = 0

    for artigo in artigos:
        artigos_verificados += 1  # Contar cada artigo processado
        data_publicacao = artigo.get("publish_date")  # Supondo que seja no formato 'YYYY-MM-DD'
        
        # Verificar formato de data
        if isinstance(data_publicacao, str):
            partes_data = data_publicacao.split("-")
            if len(partes_data) >= 2:  # Certificar que há pelo menos ano e mês
                ano = partes_data[0]
                mes = partes_data[1]
                if ano_art == ano and mes in publicacoes_mes:
                    publicacoes_mes[mes] += 1
            else:
                artigos_excluidos += 1  # Registro para depuração
        else:
            artigos_excluidos += 1  # Registro para depuração
    
    return publicacoes_mes


def conta_Mes_de_AnoGraf(fnome, ano_selecionado):
    plt.clf()
    dados_por_mes = conta_mes(fnome, ano_selecionado)

    meses = list(dados_por_mes.keys())
    num_publicacoes = list(dados_por_mes.values())  # Eixo Y: número de publicações

    plt.bar(meses, num_publicacoes, color="darkmagenta")
    plt.xlabel("Mês")  # Rótulo do eixo X
    plt.ylabel("Número de Publicações")  # Rótulo do eixo Y
    plt.title("Número de Publicações por Mês em " + ano_selecionado )  # Título do gráfico
    plt.xticks(rotation=45)  # Rodar os anos no eixo X para melhor visualização
    plt.tight_layout()  # Ajustar margens para evitar cortes no gráfico
    plt.savefig(f"grafico_conta_mes_{ano_selecionado}.png",dpi=180,bbox_inches="tight")
    plt.show()
    return 


def conta_autor(fnome): #numero de publicações por autores (top 20)
    artigos = lerBD(fnome)
    diconta = {}  # Dicionário para armazenar a contagem de artigos por autor
    for artigo in artigos:
        for autor in artigo["authors"]:
            nome = autor["name"]
            if nome not in diconta:  # Se o autor não estiver no dicionário
                diconta[nome] = 1  # Inicializa a contagem
            else:
                diconta[nome] += 1  # Incrementa a contagem
    diconta_ordenado = dict(sorted(diconta.items(), key=lambda item: item[1], reverse=True)) # Ordena o dicionário do maior para o menor número de artigos publicados
    ditop = dict(list(diconta_ordenado.items())[:20]) #otem os top 20 autores
    return ditop


def conta_autor_Grafico(fnome):
    plt.clf()
    autores_top20 = conta_autor(fnome)  

  
    autores = list(autores_top20.keys())
    publicacoes = list(autores_top20.values())

   
    plt.figure(figsize=(12, 8))
    bars = plt.bar(autores, publicacoes, color='orchid')

    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=10)

    
    plt.xticks(rotation=45, ha='right', fontsize=10)  
    plt.xlabel('Autores', fontsize=12)
    plt.ylabel('Número de Publicações', fontsize=12)
    plt.title('Top 20 Autores com Mais Publicações', fontsize=14)
    plt.tight_layout()  
    plt.savefig("grafico_conta_autor.png",dpi=180,bbox_inches="tight")
    plt.show()
    return


def conta_autor_anos(fnome, autor_selecionado):
    artigos = lerBD(fnome)  
    publicacoes_ano = {}  
    autor_selecionado = autor_selecionado.strip().lower().replace("  ", " ")  
    
    for artigo in artigos:
        data_publicacao = artigo.get("publish_date")
        if not isinstance(data_publicacao, str):
            continue 
        
        partes_data = data_publicacao.split("-")
        ano = partes_data[0] 
        
        # Exibir os autores para depuração
        autores_artigo = artigo.get("authors", [])

        
        for autor in autores_artigo:
            if isinstance(autor, dict):
                autor_nome = autor.get("name", "").strip().lower().replace("  ", " ")
            elif isinstance(autor, str):  # Caso o autor seja uma string simples
                autor_nome = autor.strip().lower().replace("  ", " ")
            else:
                continue  # Pula se o formato for inesperado
            if autor_selecionado == autor_nome:
                publicacoes_ano[ano] = publicacoes_ano.get(ano, 0) + 1
    
    publicacoes_ano_ordenado = dict(sorted(publicacoes_ano.items()))
    
    if not publicacoes_ano_ordenado:
        print("\nNenhuma publicação encontrada para esse autor.")
        
    return publicacoes_ano_ordenado


def conta_autor_anos_Grafico(fnome, autor_selecionado):
    plt.clf()
    dadosAutor_por_ano = conta_autor_anos(fnome, autor_selecionado)
    anos = list(dadosAutor_por_ano.keys())
    num_publicacoes = list(dadosAutor_por_ano.values())

    plt.bar(anos, num_publicacoes, color="lightpink")
    plt.xlabel("Ano")  # Eixo X
    plt.ylabel("Número de Publicações")  # Rótulo do eixo Y
    plt.title("Nº de Publicações de " + autor_selecionado + " por Ano")  # Título do gráfico
    plt.xticks(rotation=45)  # Rodar os anos no eixo X para melhor visualização

    # Configurar a escala do eixo Y para números de 1 em 1
    max_publicacoes = max(num_publicacoes)  # Encontrar o valor máximo de publicações
    plt.yticks(np.arange(0, max_publicacoes + 1, 1))  # Escala variando de 1 em 1

    plt.tight_layout()  # Ajustar margens para evitar cortes no gráfico
    plt.savefig(f"grafico_autor_anos_{autor_selecionado}.png", dpi=180, bbox_inches="tight")  # Salvar a imagem
    plt.show()
    return


def conta_palavras_chave(fnome): #palavras chave pela frequencia (top 20)
    artigos = lerBD(fnome)
    diconta = {}
    for artigo in artigos:
        palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
        if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
            palavras_chave = palavras_chave.lower().split(", ")
        elif isinstance(palavras_chave, list):  # Se for uma lista
            palavras_chave = [palavra.lower() for palavra in palavras_chave]
        else:
            continue
        for palavra in palavras_chave:
            if palavra not in diconta:
                diconta[palavra] = 1
            else:
                diconta[palavra] += 1
    diconta_ordenado = dict(sorted(diconta.items(), key=lambda item: item[1], reverse=True)) # Ordena o dicionário do maior para o menor número de ocorrências
    ditop = dict(list(diconta_ordenado.items())[:20]) #otem os top 20 palavras 
    return ditop 


def conta_palavras_chaveGrafico(fnome):
    plt.clf()
    palavras_frequentes = conta_palavras_chave(fnome)  # Obtém as 20 palavras mais frequentes

   
    palavras = list(palavras_frequentes.keys())
    frequencias = list(palavras_frequentes.values())

  
    plt.figure(figsize=(12, 8))
    bars = plt.bar(palavras, frequencias, color='indigo')

  
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=10)

   
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotaciona os rótulos das palavras para melhor legibilidade
    plt.xlabel('Palavras-Chave', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.title('Top 20 Palavras-Chave Mais Frequentes', fontsize=14)
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    plt.savefig("conta_palavras_chaveGrafico.png",dpi=180,bbox_inches="tight")
    plt.show()


def palavra_mais_frequente(fnome): #palavra chave mais frequente por ano
    artigos = lerBD(fnome)
    palavras_ano = {}
    for artigo in artigos:
        data_publicacao = artigo.get("publish_date", "").split(" —")[0].strip()
        try:
            ano = data_publicacao.split("-")[0]
        except IndexError:
            continue  # Ignorar casos onde a data não está no formato esperado
        palavras_chave = artigo.get("keywords", [])  # Obtém as palavras-chave (ou uma lista vazia, se não existir)
        if isinstance(palavras_chave, str):  # Se for uma string, separa-a por vírgulas, tornando todas as letras minusculas
            palavras_chave = palavras_chave.lower().split(", ")
        elif isinstance(palavras_chave, list):  # Se for uma lista
            palavras_chave = [palavra.lower() for palavra in palavras_chave]
        else:
            continue


        if ano not in palavras_ano:
            palavras_ano[ano] = {} #para ser mais fácil fazer a contagem, temos um dicionário em que as chaves são os anos e os valores são dicionários em que aa chaves são as palavras e os valores a frequência da respetivas palavras
        for palavra in palavras_chave:
            palavras_ano[ano][palavra] = palavras_ano[ano].get(palavra, 0) + 1
    mais_frequentes_por_ano = {}
    for ano, palavras in palavras_ano.items():
        if palavras: #ter a certeza de que não há um ano com 0 palavras associada a influenciar o max
            palavra_frequente = max(palavras.items(), key=lambda item: item[1])  #encontra a palavra mais frequente (máximo na contagem)
            mais_frequentes_por_ano[ano] = palavra_frequente  #associa respetiva palavra ao ano no novo dicionário
    return mais_frequentes_por_ano


def palavra_mais_frequente_Ano_Grafico(fnome):
    plt.clf()
    # Obter as palavras mais frequentes por ano e suas frequências
    mais_frequentes_por_ano = palavra_mais_frequente(fnome)
    
    # Extrair anos e frequências
    anos = list(mais_frequentes_por_ano.keys())
    frequencias = [freq[1] for freq in mais_frequentes_por_ano.values()]
    palavras = [freq[0] for freq in mais_frequentes_por_ano.values()]  # Palavras mais frequentes
    
    # Determinar a palavra mais frequente no geral
    palavra_mais_frequente_global = max(
        mais_frequentes_por_ano.values(), key=lambda item: item[1]
    )[0]
    
    # Criar gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(anos, frequencias, color="plum")
    
    # Adicionar rótulos
    plt.xlabel("Ano")
    plt.ylabel("Número de Ocorrências")
    plt.title(f"Frequência da Palavra '{palavra_mais_frequente_global}' por Ano")
    plt.xticks(rotation=45)
    
    # Adicionar números de publicações acima de cada barra
    for i, valor in enumerate(frequencias):
        plt.text(i, valor + 0.5, str(valor), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig("grafico_palavra_mais_frequente_Ano.png", dpi=180, bbox_inches="tight")  # Salvar a imagem
    plt.show()

    return

#--------------------------------------------------------------INTERFACE GUI-------------------------------------------------------------------
sg.theme("dark purple")

def janelaErro(mensagem):
    interface=[[sg.Text(mensagem)], [sg.Button("Sair")]]
    janela= sg.Window(title="Mensagem de erro", default_element_size=(10,1)).Layout(interface)

    stop=False  
    while not stop:
        event, values = janela.read()
        if event == "Sair" or event == sg.WIN_CLOSED:
            stop = True
    janela.close()

Texto = []

imagem_path = 'imagem.png'
tamanho_imagem = (130,130)
imagem = Image.open(imagem_path)
imagem_redimensionada = imagem.resize(tamanho_imagem)
imagem_bytes = io.BytesIO()
imagem_redimensionada.save(imagem_bytes,format='PNG')

botoesinterface = [ 
    [sg.Button("Carregar BD",size=(20,2), key='-CARREGARBD-')],
    [sg.Button("Nova Publicação",size=(20,2), key='-NOVAPUBLICACAO-',disabled=True)],
    [sg.Button("Eliminar Publicação",size=(20,2),key='-ELIMINARPUBLICACAO-',disabled=True)],
    [sg.Button("Atualizar Publicação",size=(20,2),key='-ATUALIZARPUBLICACAO-',disabled=True)],
    [sg.Button("Consultar Publicação",size=(20,2),key='-CONSULTARPUBLICACAO-',disabled=True)],
    [sg.Button("Organizar Publicações",size=(20,2),key='-ORGANIZARPUBLICACOES-',disabled=True)],
    [sg.Button("Análise de Publicações",size=(20,2),key='-ANALISEDEPUBLICACOES-',disabled=True)],
    [sg.Button("Estatísticas",size=(20,2),key='-ESTATISTICAS-',disabled=True)],
    [sg.Button("Importar BD",size=(20,2), key='-IMPORTARBD-',disabled=True)],
    [sg.Button("Exportar BD",size=(20,2), key='-EXPORTARBD-',disabled=True)],
    [sg.Button("Sair",size=(20,2))]
]

barra = [
    [sg.Text(
        'Artigos',  
        justification='center', 
        size=(80, 1),  # Tamanho ajustado para centralização
        background_color='white',  # Fundo branco
        text_color='#4b0082',  # Texto roxo
        pad=(0, 0)
    )]
]

caixatexto = [
    *barra,
    [sg.Listbox(values=Texto, size=(85, 30), key="_Texto", pad=(0, 0))]
]

imageminterface = [
    [sg.Image(data=imagem_bytes.getvalue(), size=tamanho_imagem, pad=(20, 5))]
]

interfaceprincipal = [
    [sg.Menu([['Ajuda', ['Carregar BD', 'Nova Publicação', 'Eliminar Publicação', 'Atualizar Publicação',
                          'Consultar Publicação', 'Organizar Publicações', 'Análise de Publicações', 
                          'Estatísticas', 'Importar BD', 'Exportar BD']]])],
    [sg.Column(imageminterface),
     sg.Text('Biblioteca de Artigos ', font=("Times_New_Roman", 29), pad=((80, 0), 10))],
    [sg.Column(botoesinterface),
     sg.VSep(), 
     sg.Column(caixatexto)]
]

janelaprincipal = sg.Window("Gestor de Publicações", margins=(100, 50), default_element_size=(20, 10), size=(1000, 800)).Layout(interfaceprincipal)

stop = False
bd_carregada=False
while not stop:
    evento, valor = janelaprincipal.read()
    if evento == "Sair" or evento == sg.WIN_CLOSED:
        layoutsair = [
            [sg.Text("Tem a certeza que quer sair do programa?")],
            [sg.Button('Voltar ao Programa'), sg.Button('Sair')]
        ]

        janelasair = sg.Window("Sair", layoutsair)
        eventosair, valorsair = janelasair.read()

        if eventosair == "Voltar ao Programa" or evento == sg.WIN_CLOSED:
            janelasair.close()
            stop = False
        elif eventosair == "Sair":
            janelasair.close()
            stop = True
            janelaprincipal.close()

    elif evento == "Carregar BD":
        layoutajudacarregarbd=[
            [sg.Text(' 1º Para conseguir trabalhar na aplicação o primeiro passo deve ser carregar uma base de dados, clicando no botão "Carregar BD"; \n 2º Clicar em browser e escolher um ficheiro válido; \n 3º Clicar em “Carregar”.')],
            [sg.Image(filename='ajudacarregarbd.png', key='imagem1', size=(800, 300))],
            [sg.Button('Fechar')]
        ]
        janelaajudacarregarbd = sg.Window("Ajuda Nova Tarefa", layoutajudacarregarbd)
        
        stop01 = False
        while not stop01:
            evento01,valor01 = janelaajudacarregarbd.read()
            if evento01 == 'Fechar' or evento01 == sg.WIN_CLOSED:
                stop01 = True
                janelaajudacarregarbd.close()
    
    elif evento == "Nova Publicação":
        layoutajudanovapublicacao = [[sg.Text(' 1º Clicar no botão "Nova Publicação"; \n 2º Preencher devidamente todos os parâmetros obrigatórios sobre a nova publicação a criar; \n Os campos obrigatórios são o Título, o Abstract, e deve ter pelo menos 1 Nome de Autor preenchido; \n Caso tenha preenchido a Afiliação ou o Orcid mas não o Nome, o programa não vai assumir esse autor. \n 3º Clicar em “Adicionar Autor” para adicionar a informação do(s) autor(es).')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudanovapublicacao.png', key='imagem2', size=(400, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudanovapublicacao = sg.Window("Ajuda Nova Publicação", layoutajudanovapublicacao)
        
        stop02 = False
        while not stop02:
            evento02,valor02 = janelaajudanovapublicacao.read()
            if evento02 == 'Fechar' or evento02 == sg.WIN_CLOSED:
                stop02 = True
                janelaajudanovapublicacao.close()

    elif evento == "Eliminar Publicação":
        layoutajudaeliminarpublicacao = [[sg.Text(' 1º Clicar no botão "Eliminar Publicação"; \n 2º Preencher devidamente com um DOI válido; \n 3º Clicar em "Submeter".')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaeliminarpublicacao.png', key='imagem3', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaeliminarpublicacao = sg.Window("Ajuda Eliminar Publicação", layoutajudaeliminarpublicacao)
        
        stop03 = False
        while not stop03:
            evento03,valor03 = janelaajudaeliminarpublicacao.read()
            if evento03 == 'Fechar' or evento03 == sg.WIN_CLOSED:
                stop03 = True
                janelaajudaeliminarpublicacao.close()

    elif evento == "Atualizar Publicação":
        layoutajudaatualizarpublicacao = [[sg.Text(' 1º Clicar no botão "Atualizar Publicação"; \n 2º Preencher devidamente com um DOI válido; \n 3º Clicar em "Submeter"; \n 4º Preencher na nova janela a informação nova, se não alterar um certo parâmetro, o programa vai assumir a informação anterior.')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaatualizarpublicacao.png', key='imagem4', size=(500, 400))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaatualizarpublicacao = sg.Window("Ajuda Atualizar Publicação", layoutajudaatualizarpublicacao)
        
        stop04 = False
        while not stop04:
            evento04,valor04 = janelaajudaatualizarpublicacao.read()
            if evento04 == 'Fechar' or evento04 == sg.WIN_CLOSED:
                stop04 = True
                janelaajudaatualizarpublicacao.close()

    elif evento == "Consultar Publicação":
        layoutajudaconsultarpublicacao = [[sg.Text(' 1º Clicar no botão "Consultar Publicação"; \n 2º Escolher o tipo de consulta que pretende; \n 3º Clicar em "Submeter"; \n 4º A informação é exposta na janela principal.')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaconsultar.png', key='imagem5', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaconsultarpublicacao = sg.Window("Ajuda Consultar Publicação", layoutajudaconsultarpublicacao)
        
        stop05 = False
        while not stop05:
            evento05,valor05 = janelaajudaconsultarpublicacao.read()
            if evento05 == 'Fechar' or evento05 == sg.WIN_CLOSED:
                stop05 = True
                janelaajudaconsultarpublicacao.close()

    elif evento == "Organizar Publicações":
        layoutajudaorganizarpublicacao = [[sg.Text(' 1º Clicar no botão "Organizar Publicações"; \n 2º Escolher o tipo de organização que pretende; \n 3º Clicar em "Submeter"; \n 4º A informação é exposta na janela principal.')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudarorganizar.png', key='imagem6', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaorganizarpublicacao = sg.Window("Ajuda Organizar Publicações", layoutajudaorganizarpublicacao)
        
        stop06 = False
        while not stop06:
            evento06,valor06 = janelaajudaorganizarpublicacao.read()
            if evento06 == 'Fechar' or evento06 == sg.WIN_CLOSED:
                stop06 = True
                janelaajudaorganizarpublicacao.close()

    elif evento == "Análise de Publicações":
        layoutajudaanalise = [[sg.Text(' 1º Clicar no botão "Análise de Publicações"; \n 2º Escolher o tipo de análise que pretende; \n 3º Clicar em "Submeter"; \n 4º A informação é exposta na janela principal.')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaanalise.png', key='imagem7', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaanalise = sg.Window("Ajuda Análise de Publicações", layoutajudaanalise)
        
        stop07 = False
        while not stop07:
            evento07,valor07 = janelaajudaanalise.read()
            if evento07 == 'Fechar' or evento07 == sg.WIN_CLOSED:
                stop07 = True
                janelaajudaanalise.close()

    elif evento == "Estatísticas":
        layoutajudaestatisticas = [[sg.Text(' 1º Clicar no botão "Estatísticas"; \n 2º Escolher a estatística que pretende; \n 3º Clicar em "Submeter"; \n 4º A informação é exposta na janela principal.')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaestatisticas.png', key='imagem8', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaestatisticas = sg.Window("Ajuda Estatísticas", layoutajudaestatisticas)
        
        stop08 = False
        while not stop08:
            evento08,valor08 = janelaajudaestatisticas.read()
            if evento08 == 'Fechar' or evento08 == sg.WIN_CLOSED:
                stop08 = True
                janelaajudaestatisticas.close()

    elif evento == "Importar BD":
        layoutajudaimportar = [[sg.Text(' 1º Clicar no botão "Importar BD"; \n 2º Escolher o ficheiro válido que pretende importar; \n 3º Clicar em "OK".')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaimportar.png', key='imagem9', size=(500, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaimportar = sg.Window("Ajuda Importar BD", layoutajudaimportar)
        
        stop09 = False
        while not stop09:
            evento09,valor09 = janelaajudaimportar.read()
            if evento09 == 'Fechar' or evento09 == sg.WIN_CLOSED:
                stop09 = True
                janelaajudaimportar.close()

    elif evento == "Exportar BD":
        layoutajudaexportar = [[sg.Text(' 1º Clicar no botão "Exportar BD"; \n 2º Escolher o ficheiro válido que pretende; \n 3º Clicar em "Exportar".')],
            [sg.Column(
                [
                    [sg.Image(filename='ajudaexportar.png', key='imagem10', size=(600, 300))],
                    [sg.Button('Fechar')]
                ],
                justification='center'
            )]]
        janelaajudaexportar = sg.Window("Ajuda Exportar BD", layoutajudaexportar)
        
        stop010 = False
        while not stop010:
            evento010,valor010 = janelaajudaexportar.read()
            if evento010== 'Fechar' or evento010 == sg.WIN_CLOSED:
                stop010 = True
                janelaajudaexportar.close()


    elif evento=='-CARREGARBD-':
      
        tiposfile = (("JSON Files", "*.json"), ("All Files", "*.*"))
        layoutcarregarbd = [
            [
                sg.Text("Base de dados:"), 
                sg.Input(key="-FICHEIRO-", readonly=True, enable_events=True),
                sg.FileBrowse(file_types = tiposfile, size=(8,1)),
                sg.Button(key="-CARREGAR-", button_text="Carregar", size=(12,1), disabled=True)
            ]
        ]
        janelacarregarbd = sg.Window("Carregamento da base de dados",layoutcarregarbd, size=(650,100))
        stop1=False
        while not stop1:

            evento1, valor1= janelacarregarbd.read()

            if evento1 == sg.WIN_CLOSED:
                janelaprincipal["_Texto"].update("")
                stop1=True

            elif evento1 =="-FICHEIRO-":
                janelacarregarbd["-CARREGAR-"].update(disabled=False)

            elif evento1 == "-CARREGAR-":
                if valor1["-FICHEIRO-"]:
                    BDArtigos= lerBD(valor1["-FICHEIRO-"])
                    stop1=True
                    Texto=['Base de Dados carregada com sucesso!']
                    janelaprincipal["_Texto"].update(Texto)
                    bd_carregada = True  # Marca a BD como carregada
                    
                    # Habilita os outros botões
                    for btn in ['-NOVAPUBLICACAO-', '-ELIMINARPUBLICACAO-', '-ATUALIZARPUBLICACAO-', '-CONSULTARPUBLICACAO-', '-ORGANIZARPUBLICACOES-', 
                                '-ANALISEDEPUBLICACOES-', '-ESTATISTICAS-', '-IMPORTARBD-', '-EXPORTARBD-']:
                        janelaprincipal[btn].update(disabled=False)
                janelacarregarbd.close()




    elif evento == "-NOVAPUBLICACAO-" and bd_carregada:

        def adicionar_autor( contador_autores):
            return [
           [sg.Text(f'Autor {contador_autores + 1} - Nome:', size=(15, 1)), sg.InputText(key=f'_AutorNome_{contador_autores}')],
           [sg.Text(f'Autor {contador_autores + 1} - Afiliação:', size=(15, 1)), sg.InputText(key=f'_AutorAfiliacao_{contador_autores}')],
           [sg.Text(f'Autor {contador_autores + 1} - Orcid:', size=(15, 1)), sg.InputText(key=f'_AutorOrcid_{contador_autores}')]
           ]
        

        contador_autores=0

        layoutnovapublicacao = [
         [sg.Text('Preencha os seguintes parâmetros:')],
         [sg.Text('Abstract:', size=(15, 1)), sg.InputText(key='_Abstract')],  # Adiciona chave '_Abstract'
         [sg.Text('Keywords:', size=(15, 1)), sg.InputText(key='_Keywords')],  # Adiciona chave '_Keywords'
         [sg.Text('Autores:', size=(15, 1))],
         [sg.Column([], key='-AUTORES-', scrollable=True, vertical_scroll_only=True, size=(400, 200))],  # Adicionando a rolagem
         [sg.Button('+ Adicionar Autor', key='-ADICIONAR_AUTOR-')],
         [sg.Text('Data de Publicação:', size=(15, 1)), sg.Input(key='_Data', readonly=True), sg.CalendarButton('Escolher Data', target='_Data')],
         [sg.Text('Título:', size=(15, 1)), sg.InputText(key='_Titulo')],  # Adiciona chave '_Titulo'
         [sg.Button("Submeter"), sg.Button("Sair", size=(20, 1))]
        ]


        janelanovapublicacao = sg.Window("Nova Publicação", layoutnovapublicacao)
        stop2 = False
        while not stop2:
            evento2, valor2 = janelanovapublicacao.read()
            if evento2 == "Sair" or evento2 == sg.WIN_CLOSED:
                stop2 = True

            elif evento2 == "-ADICIONAR_AUTOR-":
                # Adiciona novos campos de autor
                novo_autor_layout = adicionar_autor(contador_autores)
                # Corrige para adicionar diretamente dentro da coluna '-AUTORES-'
                janelanovapublicacao.extend_layout(janelanovapublicacao['-AUTORES-'], novo_autor_layout)
                contador_autores += 1


            elif evento2 == "Submeter":
                autores = []

                for i in range(contador_autores):
                    nome_autor = valor2.get(f'_AutorNome_{i}', '')
                    afiliacao_autor = valor2.get(f'_AutorAfiliacao_{i}', '')  # Afiliação é opcional
                    orcid_autor = valor2.get(f'_AutorOrcid_{i}', '')  # ORCID é opcional
                        
                    if nome_autor:
                        autores.append({
                          "name": nome_autor,
                          "affiliation": afiliacao_autor if afiliacao_autor else None,
                          "orcid": orcid_autor if orcid_autor else None
                             })
                        
                palavras_chave = valor2.get('_Keywords', '').split(',')
                palavras_chave = [palavra.strip() for palavra in palavras_chave]
  
                if not autores or not valor2['_Titulo'] or not valor2['_Abstract']:
                     janelaErro("Erro! É obrigatório preencher os parâmetros: Título, Abstract e Nome de Autor!")
                     stop2 = False
               
        
                else:
                    data_formatada_str = valor2['_Data'] if valor2['_Data'] else ""
                    if data_formatada_str:   
                       data_formatada_str = data_formatada_str[:10]  
                    doi = criarDOI(valor1['-FICHEIRO-'])
                    url = gerarurl(valor1['-FICHEIRO-'], doi)
                    pdf = gerarpdf(valor1['-FICHEIRO-'], doi)

                    nova_publicacao = criar2(valor1['-FICHEIRO-'],valor2['_Abstract'], palavras_chave,   autores, doi, pdf, data_formatada_str, valor2['_Titulo'],url )
                    stop2 = True

        janelanovapublicacao.close()

      
    elif evento == '-ELIMINARPUBLICACAO-' and bd_carregada:
        layouteliminarpublicacao = [
            [sg.Text("Introduza o DOI da publicação que pretende eliminar:")],
            [sg.InputText(key='_doi')],
            [sg.Button('Submeter'), sg.Button('Sair')]
        ]

        janelaeliminarpublicacao = sg.Window("Eliminar Publicação", layouteliminarpublicacao)

        stop3 = False
        while not stop3:
            evento3, valor3 = janelaeliminarpublicacao.read()
            if evento3 == "Sair" or evento3 == sg.WIN_CLOSED:
                stop3 = True  
                janelaeliminarpublicacao.close() 
            elif evento3 == "Submeter":
                if valor3['_doi'] == "": 
                    janelaErro("Erro! Tem de preencher o parâmetro!")
                else:
                    resultado3 = confirmarDOI(valor1['-FICHEIRO-'], valor3['_doi'])
                    if not resultado3:
                        janelaErro("Erro! Não existe nenhuma publicação com esse DOI!")
                    else:
                        listpub = obter_publicacao_por_doi(valor1['-FICHEIRO-'], valor3['_doi'])

                        # Verificar se as chaves "authors" e "keywords" existem e formatá-las adequadamente
                        autores = ', '.join([autor["name"] for autor in listpub.get("authors", [])])
                        keywords = ', '.join(listpub.get("keywords", []))  # Caso keywords exista, junta em uma string

                        # Montar o conteúdo da publicação
                        infpub = []
                        for chave, valor in listpub.items():
                            # Se a chave for "authors" ou "keywords", já tratamos a formatação antes
                            if chave == "authors":
                                infpub.append(f"Autores: {autores}")
                            elif chave == "keywords":
                                infpub.append(f"Palavras-chave: {keywords}")
                            else:
                                # Para os outros campos, apenas adicionamos normalmente
                                infpub.append(f"{chave}: {valor}")

                        # Exibir o texto formatado na Multiline
                        infpub_texto = "\n".join(infpub)

                        layouteliminarpubcerta = [
                            [sg.Text("É esta a publicação que pretende eliminar?")], 
                            [sg.Multiline(default_text=infpub_texto, size=(35, 8), key='-TEXTBOX-', disabled=True)],
                            [sg.Button('Eliminar esta publicação'), sg.Button('Cancelar')]
                        ]

                        janelaeliminarpubcerta = sg.Window("Eliminar", layouteliminarpubcerta)
                        evento31, valor31 = janelaeliminarpubcerta.read()

                        if evento31 == "Cancelar":
                            janelaeliminarpubcerta.close()

                        elif evento31 == "Eliminar esta publicação":
                            listaEliminar = eliminar(valor1['-FICHEIRO-'], valor3['_doi'])
                            listaeliminados.append(valor3['_doi'][29:])
                            janelaeliminarpubcerta.close()
                            stop3 = True
        janelaeliminarpublicacao.close()
   

    elif evento == "-ATUALIZARPUBLICACAO-" and bd_carregada:

        def adicionar_autor(contador_autores):
            return [
           [sg.Text(f'Autor {contador_autores + 1} - Nome:', size=(15, 1)), sg.InputText(key=f'_AutorNome_{contador_autores}')],
           [sg.Text(f'Autor {contador_autores + 1} - Afiliação:', size=(15, 1)), sg.InputText(key=f'_AutorAfiliacao_{contador_autores}')],
           [sg.Text(f'Autor {contador_autores + 1} - Orcid:', size=(15, 1)), sg.InputText(key=f'_AutorOrcid_{contador_autores}')]
           ]
        

        contador_autores=0
          
        layoutatualizarpub = [
        [sg.Text("Introduza o DOI da publicação que deseja atualizar:")],
        [sg.InputText(key='_doi_atualizar')],
        [sg.Button('Submeter'), sg.Button('Sair')]
        ]


        janelaatualizarpub = sg.Window("Atualizar Tarefa", layoutatualizarpub)

        stop4 = False
        while not stop4:
            evento4,valor4 = janelaatualizarpub.read()
            if evento4 == "Sair" or evento4 == sg.WIN_CLOSED:
                stop4 = True
                janelaatualizarpub.close()
            elif evento4 == "Submeter": 
                if valor4['_doi_atualizar'] == "":
                    janelaErro("Erro! Tem de introduzir um DOI!")
                    
                else:
                    resultado4 = confirmarDOI (valor1['-FICHEIRO-'],valor4['_doi_atualizar'])
                    if resultado4 == False:
                        janelaErro("Erro! o DOI introduzido não é válido")
                        stop4 = False
                    else:
                        stop4= True
                        publicacao = obter_publicacao_por_doi(valor1['-FICHEIRO-'],valor4['_doi_atualizar'])
                        autores = publicacao.get("authors", [])
                        autores_layout = []
                        contador_autores = len(autores)
                        for i, autor in enumerate(autores):
                            autores_layout.append([sg.Text(f'Autor {i+1} - Nome:', size=(15, 1)),sg.InputText(default_text=autor.get('name', ''), key=f'_AutorNome_{i}')])
                            autores_layout.append([sg.Text(f'Autor {i+1} - Afiliação:', size=(15, 1)),sg.InputText(default_text=autor.get('affiliation', ''), key=f'_AutorAfiliacao_{i}')])
                            autores_layout.append([sg.Text(f'Autor {i+1} - Orcid:', size=(15, 1)),sg.InputText(default_text=autor.get('orcid', ''), key=f'_AutorOrcid_{i}')])
                        

                        layoutatualizarpublicacao = [
                        [sg.Text('Atualize os parâmetros da publicação:')],
                        [sg.Text('Abstract:', size=(15, 1)), sg.InputText(default_text=publicacao.get('abstract', ''), key='_Abstract')],
                        [sg.Text('Keywords:', size=(15, 1)), sg.InputText(default_text=publicacao.get('keywords', []), key='_Keywords')],
                        [sg.Text('Autores:', size=(15, 1))],
                        [sg.Column(autores_layout, key='-AUTORES-', scrollable=True, vertical_scroll_only=True, size=(400, 200))],
                        [sg.Button('+ Adicionar Autor', key='-ADICIONAR_AUTOR-')],
                        [sg.Text('Data de Publicação:', size=(15, 1)),sg.Input(key='_Data', readonly=True), sg.CalendarButton('Escolher Data', target='_Data')],
                        [sg.Text('Título:', size=(15, 1)), sg.InputText(default_text=publicacao.get('title', ''), key='_Titulo')],
                        [sg.Button("Submeter Atualização"), sg.Button("Cancelar")]
                        ]


                        janelaatualizarpub.close()
                        janelaatualizarpub = sg.Window("Atualizar Publicação", layoutatualizarpublicacao)
                       
                        stop41 = False
                        while not stop41:
                            evento41, valor41 = janelaatualizarpub.read()
                        
                            if evento41 == "Cancelar" or evento41 == sg.WIN_CLOSED:
                               janelaatualizarpub.close()
                               stop41 = True
                            
                            elif evento41 == "-ADICIONAR_AUTOR-":
                               novo_autor_layout = adicionar_autor(contador_autores)
                               janelaatualizarpub.extend_layout(janelaatualizarpub['-AUTORES-'], novo_autor_layout)
                               contador_autores += 1
                            
                            elif evento41 == "Submeter Atualização":
                                autores_atualizados = []
                                for i in range(contador_autores):
                                   nome_autor = valor41.get(f'_AutorNome_{i}', '')
                                   afiliacao_autor = valor41.get(f'_AutorAfiliacao_{i}', '')
                                   orcid_autor = valor41.get(f'_AutorOrcid_{i}', '')
                                
                                   
                                   autor = {"name": nome_autor}
                                   if orcid_autor:  # Só adiciona se o campo for preenchido
                                       autor["orcid"] = orcid_autor
                                   if afiliacao_autor:
                                       autor['affiliation']=afiliacao_autor

                                   if nome_autor:
                                    autores_atualizados.append(autor)
                                
                                palavras_chave_atualizadas = valor41.get('_Keywords', '').strip().split(',')
                                palavras_chave_atualizadas = [palavra.strip() for palavra in palavras_chave_atualizadas if palavra.strip()]

                            
                                if not autores_atualizados or not valor41['_Titulo'] or not valor41['_Abstract']:
                                    janelaErro("Erro! Todos os campos obrigatórios devem ser preenchidos!")
                                      
                                else:
                            
                                    data_formatada_str = valor41['_Data'].strip() if valor41['_Data'].strip() else ""
                                    if data_formatada_str:
                                        data_formatada_str = data_formatada_str[:10]

                                    pdf = publicacao.get('pdf', '')
                                    url = publicacao.get('url', '') 
                                  
                                    nova_publicacao = {"abstract": valor41['_Abstract'].strip(),"authors": autores_atualizados,"doi": valor4['_doi_atualizar'],"pdf": publicacao.get('pdf', ''),"title": valor41['_Titulo'].strip(),"url": publicacao.get('url', '')}

                                    # Adicionando keywords e publish_date apenas se houverem valores
                                    if palavras_chave_atualizadas:
                                        nova_publicacao["keywords"] = palavras_chave_atualizadas

                                    if data_formatada_str:
                                        nova_publicacao["publish_date"] = data_formatada_str


                                    atualizar2(valor1['-FICHEIRO-'],**nova_publicacao)
                                    janelaErro("Publicação atualizada com sucesso!")
                                    janelaatualizarpub.close()
                                    stop41 = True


    elif evento == "-CONSULTARPUBLICACAO-" and bd_carregada:
        opcoes_consultar = [
            "Consultar todas as Publicações",
            "Consultar Publicação Completa",
            "Consultar Publicações por título",
            "Consultar Publicações por autor",
            "Consultar Publicações por afiliação",
            "Consultar Publicações por data",
            "Consultar Publicações por palavra-chave"
        ]
        Texto.clear()
        layoutConsultar = [
            [sg.Text("Que tipo de consulta pretende fazer?")],
            [sg.Combo(opcoes_consultar, enable_events=False, default_value=None, key='_Consultar_')],
            [sg.Button('Submeter'), sg.Button('Sair')]
        ]

        janelaconsultar = sg.Window("Consultar Publicação", layoutConsultar)

        stop5 = False
        while not stop5:
            evento5, valor5 = janelaconsultar.read()

            if evento5 == "Sair" or evento5 == sg.WIN_CLOSED:
                stop5 = True
                janelaconsultar.close()

            elif evento5 == "Submeter":
                if valor5["_Consultar_"] is None:
                    janelaErro("Erro! Tem de escolher uma opção!") 
                elif valor5["_Consultar_"] not in opcoes_consultar:
                    janelaErro("Erro! Escolha uma opção válida!")  
                else:
                    opcao = valor5["_Consultar_"]
                    stop5 = True  # Fechar a janela de opções após selecionar

                    if opcao == "Consultar todas as Publicações":
                        Texto.clear()
                        publicacoes = consultar_todaspublicacoes(valor1['-FICHEIRO-'])

                        if not publicacoes:
                            Texto.append("Não existem publicações disponíveis.")
                        else:
                            titulos_disponiveis = [pub['title'] for pub in publicacoes]

                            # Criar uma nova janela para exibir os títulos
                            layout_titulos = [
                                [sg.Listbox(values=titulos_disponiveis, size=(100, 20), key='_TITULOS_')],
                                [sg.Button("Detalhes"), sg.Button("Fechar")]
                            ]
                            
                            janela_titulos = sg.Window("Títulos Disponíveis", layout_titulos)

                            while True:
                                evento_titulos, valor_titulos = janela_titulos.read()
                                if evento_titulos in (sg.WIN_CLOSED, "Fechar"):
                                    janela_titulos.close()
                                    janelaconsultar.close()
                                    break
                                
                                elif evento_titulos == "Detalhes":
                                    janela_titulos.close()
                                    janelaconsultar.close()
                                    if not valor_titulos['_TITULOS_']:
                                        janelaErro("Erro! Selecione um título!")
                                    else:
                                        titulo_selecionado = valor_titulos['_TITULOS_'][0]
                                        pub_selecionada = next(pub for pub in publicacoes if pub['title'] == titulo_selecionado)

                                        detalhes_pub = [
                                            f"Título: {pub_selecionada['title']}",
                                            f"Autores: {', '.join([autor['name'] for autor in pub_selecionada['authors']])}",
                                            f"Data: {pub_selecionada.get('publish_date', 'Sem data')}",
                                            f"DOI: {pub_selecionada.get('doi', 'Sem DOI')}",
                                            f"Resumo: {pub_selecionada.get('abstract', 'Sem resumo')}"
                                        ]
                                        
                                        # Atualiza a janela principal com os detalhes da publicação
                                        janelaprincipal['_Texto'].update(values = detalhes_pub)
                            
                            # Fechar a janela de títulos após terminar a leitura
                            janela_titulos.close() 

                    elif opcao == "Consultar Publicação Completa":
                        Texto.clear()
                        layoutpublicacaocompleta = [
                            [sg.Text("Introduza o DOI da publicação que pretende consultar:")],
                            [sg.InputText(key='_publicacaocompleta')],
                            [sg.Button('Submeter'), sg.Button('Sair')]
                        ]

                        janelapublicacaocompleta = sg.Window("Consultar Publicação Completa", layoutpublicacaocompleta)

                        stop52 = False
                        while not stop52:
                            evento52, valor52 = janelapublicacaocompleta.read()
                            if evento52 == "Sair" or evento52 == sg.WIN_CLOSED:
                                stop52 = True  
                                janelaconsultar.close() 
                                janelapublicacaocompleta.close()
                            elif evento52 == "Submeter":
                                if valor52['_publicacaocompleta'] == "":
                                    janelaErro("Erro! Tem de preencher o parâmetro!")
                                    stop52 = False
                                else: 
                                    resultado52 = confirmarDOI(valor1['-FICHEIRO-'], valor52['_publicacaocompleta'])
                                    if resultado52 is False:
                                        janelaErro("Erro! O DOI introduzido não é válido")
                                        stop52 = False
                                    elif resultado52 is True:
                                        stop52 = True
                                        janelaconsultar.close()  # Fecha a janela de consulta
                                        listaConsultardoi = obter_publicacao_por_doi(valor1['-FICHEIRO-'], valor52['_publicacaocompleta'])                    
                                        if isinstance(listaConsultardoi, dict):
                                            for chave, valor in listaConsultardoi.items():
                                                Texto.append(f"{chave.capitalize()}:\n{valor}\n")  # Formata com título e conteúdo separado
                                            janelaprincipal['_Texto'].update(values=Texto) 
                                            janelapublicacaocompleta.close()
                                        else:
                                            janelaErro('Introduza uma das opções!')
                                            stop52 = False
                                            janelapublicacaocompleta.close()
                                            break

                    elif opcao in ["Consultar Publicações por título", 
                                    "Consultar Publicações por autor", 
                                    "Consultar Publicações por afiliação", 
                                    "Consultar Publicações por data", 
                                    "Consultar Publicações por palavra-chave"]:
    
                        layout_consulta = [
                            [sg.Text(f"Introduza o {opcao.split(' ')[-1]} que pretende consultar:")],
                            [sg.InputText(key='_CONSULTA_')],
                            [sg.Button('Submeter'), sg.Button('Sair')]
                        ]

                        janela_consulta = sg.Window(f"Consulta por {opcao.split(' ')[-1]}", layout_consulta)

                        stop53 = False
                        while not stop53:
                            evento53, valor53 = janela_consulta.read()

                            if evento53 in (sg.WIN_CLOSED, "Sair"):
                                stop53 = True
                                janelaconsultar.close()
                                janela_consulta.close()
                                break

                            elif evento53 == 'Submeter':
                                janelaconsultar.close()
                                consulta_entrada = valor53['_CONSULTA_']
                                if consulta_entrada == "":
                                    janelaErro("Erro! O campo não pode estar vazio!")
                                else:
                                    # Chama a função apropriada com base na opção escolhida
                                    if opcao == "Consultar Publicações por título":
                                        resultados = consultaPublicacaoTitulo(valor1['-FICHEIRO-'], consulta_entrada)
                                    elif opcao == "Consultar Publicações por autor":
                                        resultados = consultaPublicacao_autor(valor1['-FICHEIRO-'], consulta_entrada)
                                    elif opcao == "Consultar Publicações por afiliacao":
                                        resultados = consultaPublicacao_afiliacao(valor1['-FICHEIRO-'], consulta_entrada)
                                    elif opcao == "Consultar Publicações por data":
                                        resultados = consultaPublicacao_data(valor1['-FICHEIRO-'], consulta_entrada)
                                    elif opcao == "Consultar Publicações por palavra-chave":
                                        resultados = consultaPublicacao_keywords(valor1['-FICHEIRO-'], consulta_entrada)

                                    # Atualiza a interface principal com os resultados
                                    
                                    if not resultados:
                                        Texto.append("Nenhuma publicação encontrada.\n")
                                    else:
                                        for pub in resultados:
                                            Texto.append(f"Título: {pub['title']}\n")
                                            Texto.append(f"Autores: {', '.join([autor['name'] for autor in pub['authors']])}\n")
                                            Texto.append(f"Data: {pub.get('publish_date', 'Sem data')}\n")
                                            Texto.append(f"DOI: {pub.get('doi', 'Sem DOI')}\n")
                                            Texto.append(f"Resumo: {pub.get('abstract', 'Sem resumo')}\n")
                                            Texto.append("-" * 1000)  # Limita a separação entre artigos
                                            stop53 = True
                                        # Atualiza a janela principal com o texto
                                        
                                    janelaprincipal['_Texto'].update(values=Texto)
                                    Texto.clear()
                                        
                                    janela_consulta.close()  # Fecha a janela de consulta       
                                
                                                                            


    elif evento=='-ORGANIZARPUBLICACOES-' and bd_carregada:
        opçoes_ordenar=['Título', 'Data de Publicação']
        layoutorganizarpublicacoes = [
            [sg.Text("Pretende organizar as publicações por:")],
            [sg.Combo(opçoes_ordenar, enable_events=False, default_value= None,key='_Ordenar')],
            [sg.Button('Submeter'), sg.Button('Sair')]
        ]

       
        
        janelaorganizarpublicacoes = sg.Window("Organizar Publicações", layoutorganizarpublicacoes)

        stop6 = False
        while not stop6:
            evento6,valor6 = janelaorganizarpublicacoes.read()
            if evento6 == "Sair" or evento6 == sg.WIN_CLOSED:
                janelaorganizarpublicacoes.close()
                stop6 = True
                 
            elif evento6 == "Submeter":
                if valor6['_Ordenar']  == "": 
                    janelaErro("Erro! Escolha uma opção!")
                    stop6 = False
                else:
                    
                    if valor6['_Ordenar']=='Título':
                        Texto.clear()
                        listaordenartitulo=ordena_por_titulo(valor1['-FICHEIRO-'])
                        if listaordenartitulo == []:
                            Texto = ["Não existem publicações!"]
                            
                        else:                          
                            Texto = [f"{i+1} : {pub['title']}" for i,pub in enumerate(listaordenartitulo)]
                            janelaprincipal.find_element('_Texto').Update(values=Texto)
                            janelaorganizarpublicacoes.close()

                    elif valor6['_Ordenar']=='Data de Publicação':
                        Texto.clear()
                        listaordenardata=ordena_por_data(valor1['-FICHEIRO-'])
                        if listaordenardata == []:
                            Texto = ["Não existem publicações!"]
                            
                        else:                          
                            Texto = [f"{pub['publish_date']}: {pub['title']}" for pub in listaordenardata]
                            janelaprincipal.find_element('_Texto').Update(values=Texto)
                            janelaorganizarpublicacoes.close()
        

                                  
    elif evento == '-ANALISEDEPUBLICACOES-' and bd_carregada:
        opcoes_analisar = ['Autor por frequência de publicação', 'Autor por ordem alfabética', 'Keywords por frequência', 'Keywords por ordem alfabética']
        layoutanalisarpublicacoes = [
            [sg.Text("Pretende analisar as publicações por:")],
            [sg.Combo(opcoes_analisar, enable_events=False, default_value=None, key='_Analisar')],
            [sg.Button('Submeter'), sg.Button('Sair')]
        ]

        janelaanalisarpublicacoes = sg.Window("Analisar Publicações", layoutanalisarpublicacoes)

        stop7 = False
        while not stop7:
            evento7, valor7 = janelaanalisarpublicacoes.read()
            if evento7 == "Sair" or evento7 == sg.WIN_CLOSED:
                stop7 = True
            elif evento7 == "Submeter":
                if not valor7['_Analisar']:
                    janelaErro("Erro! Escolha uma opção!")
                    stop7 = False
                else:
                    Texto.clear()
                    autores = []
                    funcao_listagem_artigos = None
                    if valor7['_Analisar'] in ['Autor por frequência de publicação','Autor por ordem alfabética']:
                        if valor7['_Analisar'] == 'Autor por frequência de publicação':
                            lista_autores_freq = listar_aut_artigo(valor1['-FICHEIRO-'])
                            if not lista_autores_freq:
                                Texto = ["Não existem publicações!"]
                            else:
                                autores = [autor for autor, _ in lista_autores_freq]
                                funcao_listagem_artigos = artigos_aut_artigo

                        elif valor7['_Analisar'] == 'Autor por ordem alfabética':
                            autores = listar_aut_alfabetico(valor1['-FICHEIRO-'])
                            if not autores:
                                Texto = ["Não existem publicações!"]
                            else:
                                funcao_listagem_artigos = artigos_aut_alfabético

                        if autores:
                                layout_autores = [
                                    [sg.Text("Autores disponíveis:")],
                                    [sg.Listbox(values=autores, size=(30, 10), key='_Autores')],
                                    [sg.Button('Ver Artigos'), sg.Button('Voltar')]
                                ]

                                janela_autores = sg.Window("Lista de Autores", layout_autores)

                                stop_autores = False
                                while not stop_autores:
                                    evento_autores, valor_autores = janela_autores.read()
                                    if evento_autores == "Voltar" or evento_autores == sg.WIN_CLOSED:
                                        stop_autores = True
                                    elif evento_autores == "Ver Artigos":
                                        autor_selecionado = valor_autores['_Autores'][0] if valor_autores['_Autores'] else None
                                        if not autor_selecionado:
                                            janelaErro("Erro! Selecione um autor!")
                                        else:
                                            artigos = funcao_listagem_artigos(valor1['-FICHEIRO-'], autor_selecionado)
                                            janelaprincipal["_Texto"].update([artigo['title'] for artigo in artigos])
                                            break
                                janela_autores.close()

                    elif  valor7['_Analisar'] in ['Keywords por frequência', 'Keywords por ordem alfabética']:
                        if  valor7['_Analisar'] == 'Keywords por frequência':
                            lista_palavras_freq = listar_palavras(valor1['-FICHEIRO-'])
                            if not lista_palavras_freq:
                                Texto = ["Não existem publicações!"]
                            else:
                                palavras = [palavra for palavra, _ in lista_palavras_freq]
                                funcao_listagem_artigos = artigo_palavra

                        elif valor7['_Analisar'] == 'Keywords por ordem alfabética':
                            palavras = listar_palavras_alfabetico(valor1['-FICHEIRO-'])
                            if not palavras:
                                Texto = ["Não existem publicações!"]
                            else:
                                funcao_listagem_artigos = artigo_palavra_alfabetico

                        if palavras:
                                layout_palavras = [
                                    [sg.Text("Keywords disponíveis:")],
                                    [sg.Listbox(values=palavras, size=(30, 10), key='_Palavras')],
                                    [sg.Button('Ver Artigos'), sg.Button('Voltar')]
                                ]

                                janela_palavras = sg.Window("Lista de Palavras", layout_palavras)

                                stop_palavras = False
                                while not stop_palavras:
                                    evento_palavras, valor_palavras = janela_palavras.read()
                                    if evento_palavras == "Voltar" or evento_palavras == sg.WIN_CLOSED:
                                        stop_palavras = True
                                    elif evento_palavras == "Ver Artigos":
                                        palavra_selecionada = valor_palavras['_Palavras'][0] if valor_palavras['_Palavras'] else None
                                        if not palavra_selecionada:
                                            janelaErro("Erro! Selecione uma keyword!")
                                        else:
                                            artigos = funcao_listagem_artigos(valor1['-FICHEIRO-'], palavra_selecionada)
                                            janelaprincipal["_Texto"].update([artigo['title'] for artigo in artigos])
                                            break
                                janela_palavras.close()
            janelaanalisarpublicacoes.close()


    elif evento == '-ESTATISTICAS-':
        

        layoutestatistica = [
            [sg.Text("Qual o gráfico que pretende visualizar?")],
            [sg.Button("Publicações por Ano"),sg.Button("Publicações por Mês de um Ano")],
            [sg.Button("Top 20 autores"),sg.Button("Publicações por Ano de um Autor"),sg.Button("Top 20 Palavras-Chave"), sg.Button("Palavra-Chave Mais Frequente por Ano")],
            [sg.Button("Sair")]
        ]

        janelaestatistica = sg.Window("Dados Estatísticos",layoutestatistica)  #Dados Estatísticos é o título
        

        stop8 = False
        while not stop8:
            evento8, valor8 = janelaestatistica.read()   
            if evento8 == "Sair" or evento8 == sg.WIN_CLOSED:
                stop8 = True

            elif evento8 =="Publicações por Ano":
                Texto.clear()  #N E
                janelaestatistica.close()
                ima1= Image.open("grafico_conta_ano.png")
                tamanho_imagem1 = (500,400)
                imagem_redimensionada1 = ima1.resize(tamanho_imagem1)
                imagem_bytesprogresso = io.BytesIO()
                imagem_redimensionada1.save(imagem_bytesprogresso, format='PNG')
                layout_grafico_Publicações_por_Ano=[
                [sg.Text('Gráfico das Publicações por Ano')],
                [sg.Image(data=imagem_bytesprogresso.getvalue(),size = tamanho_imagem1, pad=(20, 10))],
                [sg.Button('Fechar')]
                ]
                janela_grafico_Publicações_por_Ano = sg.Window("Publicações por Ano", layout_grafico_Publicações_por_Ano) #Nova janela 
            
                stop81 = False
                while not stop81:
                    evento81,valor81 = janela_grafico_Publicações_por_Ano.read()
                    if evento81 == 'Fechar' or evento81 == sg.WIN_CLOSED:
                        stop81 = True
                        janela_grafico_Publicações_por_Ano.close()

            elif evento8 == "Publicações por Mês de um Ano": 
                Texto.clear()  # Limpar conteúdo
                janelaestatistica.close()

                anos = listarAnos(valor1['-FICHEIRO-'])

                if anos:
                    layout_opcoes_Publicações_por_Mes = [
                        [sg.Text("Qual o ano que pretende analisar?")],
                        [sg.Listbox(values=anos, size=(30, 10), key='_Anos')],
                        [sg.Button('Ver Gráfico'), sg.Button('Voltar')]
                    ]

                    janela_opcoes_Publicações_por_Mes = sg.Window("Publicações por Mês", layout_opcoes_Publicações_por_Mes)

                    stop82 = False
                    while not stop82:
                        evento82, valor82 = janela_opcoes_Publicações_por_Mes.read()

                        if evento82 == 'Voltar' or evento82 == sg.WIN_CLOSED:
                            stop82 = True
                            janela_opcoes_Publicações_por_Mes.close()
            

                        elif evento82 == 'Ver Gráfico':
                            if not valor82['_Anos']:  
                                sg.popup("Por favor, selecione um ano antes de continuar.", title="Erro")
                                continue

                            ano_selecionado = valor82['_Anos'][0]  

                            
                            conta_Mes_de_AnoGraf(valor1['-FICHEIRO-'], ano_selecionado)

                            try:
                                
                                imaM = Image.open(f"grafico_conta_mes_{ano_selecionado}.png")
                                print(imaM)
                                tamanho_imagemM = (500, 400)
                                imagem_redimensionadaM = imaM.resize(tamanho_imagemM)
                                imagem_bytesprogresso = io.BytesIO()
                                imagem_redimensionadaM.save(imagem_bytesprogresso, format='PNG')

                                layout_grafico_Publicações_por_Mes = [
                                    [sg.Text(f'Gráfico das Publicações por Mês - {ano_selecionado}')],
                                    [sg.Image(data=imagem_bytesprogresso.getvalue(), size=tamanho_imagemM, pad=(20, 10))],
                                    [sg.Button('Fechar')]
                                ]
                                janela_grafico_Publicações_por_Mes = sg.Window(f"Publicações por Mês - {ano_selecionado}", layout_grafico_Publicações_por_Mes)

                                stop83 = False
                                while not stop83:
                                    evento83, valor83 = janela_grafico_Publicações_por_Mes.read()
                                    if evento83 == 'Fechar' or evento83 == sg.WIN_CLOSED:
                                        stop83 = True
                                        janela_grafico_Publicações_por_Mes.close()

                            except FileNotFoundError:
                                sg.popup(f"Erro: O gráfico para o ano {ano_selecionado} não foi gerado corretamente.", title="Erro")


            elif evento8 == "Top 20 autores":
                Texto.clear()  #N E
                janelaestatistica.close()
                ima1= Image.open("grafico_conta_autor.png")
                tamanho_imagem1 = (500,400)
                imagem_redimensionada1 = ima1.resize(tamanho_imagem1)
                imagem_bytesprogresso = io.BytesIO()
                imagem_redimensionada1.save(imagem_bytesprogresso, format='PNG')
                layout_grafico_Top_20_Autores=[
                [sg.Text('Gráfico dos Top 20 Autores')],
                [sg.Image(data=imagem_bytesprogresso.getvalue(),size = tamanho_imagem1, pad=(20, 10))],
                [sg.Button('Fechar')]
                ]
                janela_grafico_Top_20_Autores = sg.Window("Top 20 Autores", layout_grafico_Top_20_Autores) #Nova janela 
                
                stop84 = False
                while not stop84:
                    evento84,valor84 = janela_grafico_Top_20_Autores.read()
                    if evento84 == 'Fechar' or evento84 == sg.WIN_CLOSED:
                        stop84 = True
                        janela_grafico_Top_20_Autores.close()


            elif evento8 == "Publicações por Ano de um Autor":
                Texto.clear()  # Limpar conteúdo
                janelaestatistica.close()

                autores = listar_autor(valor1['-FICHEIRO-'])

                if autores:
                    layout_opcoes_Publicações_por_Autor = [
                        [sg.Text("Qual o autor que pretende analisar?")],
                        [sg.Listbox(values=autores, size=(30, 10), key='_Autores')],
                        [sg.Button('Ver Gráfico'), sg.Button('Fechar')]
                    ]

                    janela_opcoes_Publicações_por_Autor = sg.Window("Publicações por Ano de um Autor", layout_opcoes_Publicações_por_Autor)

                    stop85 = False
                    while not stop85:
                        evento85, valor85 = janela_opcoes_Publicações_por_Autor.read()

                        if evento85 == 'Voltar' or evento85 == sg.WIN_CLOSED:
                            stop85 = True
                            janela_opcoes_Publicações_por_Autor.close()

                        elif evento85 == 'Ver Gráfico':
                            autor_selecionado = valor85['_Autores'][0]  # Captura o autor selecionado

                            # Gera o gráfico para o autor selecionado
                            conta_autor_anos_Grafico(valor1['-FICHEIRO-'], autor_selecionado)

                            # Carrega o gráfico gerado
                            ima85 = Image.open(f"grafico_autor_anos_{autor_selecionado}.png")  
                            print(ima85)
                            tamanho_imagem85 = (500, 400)
                            imagem_redimensionada85 = ima85.resize(tamanho_imagem85)
                            imagem_bytesprogresso = io.BytesIO()
                            imagem_redimensionada85.save(imagem_bytesprogresso, format='PNG')

                            layout_grafico_Publicações_por_Autor = [
                                [sg.Text(f'Gráfico das Publicações por Ano - {autor_selecionado}')],
                                [sg.Image(data=imagem_bytesprogresso.getvalue(), size=tamanho_imagem85, pad=(20, 10))],
                                [sg.Button('Fechar')]
                            ]
                            janela_grafico_Publicações_por_Autor = sg.Window(f"Publicações por Ano - {autor_selecionado}", layout_grafico_Publicações_por_Autor)
                            janela_opcoes_Publicações_por_Autor.close()
                            stop85 = False
                            while not stop85:
                                evento85, valor85 = janela_grafico_Publicações_por_Autor.read()
                                if evento85 == 'Fechar' or evento85 == sg.WIN_CLOSED:
                                    stop85 = True
                                    janela_grafico_Publicações_por_Autor.close()


            elif evento8 == "Top 20 Palavras-Chave":
                Texto.clear()  #N E
                janelaestatistica.close()
                ima1= Image.open("conta_palavras_chaveGrafico.png")
                tamanho_imagem1 = (500,400)
                imagem_redimensionada1 = ima1.resize(tamanho_imagem1)
                imagem_bytesprogresso = io.BytesIO()
                imagem_redimensionada1.save(imagem_bytesprogresso, format='PNG')
                layout_grafico_Top_20_PalavrasChave=[
                [sg.Text('Gráfico dos Top 20 Palavras-Chave')],
                [sg.Image(data=imagem_bytesprogresso.getvalue(),size = tamanho_imagem1, pad=(20, 10))],
                [sg.Button('Fechar')]
                ]
                janela_grafico_Top_20_PalavrasChave = sg.Window("Top 20 Autores", layout_grafico_Top_20_PalavrasChave) #Nova janela 
                
                stop86 = False
                while not stop86:
                    evento86,valor86 = janela_grafico_Top_20_PalavrasChave.read()
                    if evento86 == 'Fechar' or evento86 == sg.WIN_CLOSED:
                        stop86 = True
                        janela_grafico_Top_20_PalavrasChave.close()


            elif evento8 =="Palavra-Chave Mais Frequente por Ano":
                Texto.clear()  #N E
                janelaestatistica.close()
                ima1= Image.open("grafico_palavra_mais_frequente_Ano.png")
                tamanho_imagem1 = (500,400)
                imagem_redimensionada1 = ima1.resize(tamanho_imagem1)
                imagem_bytesprogresso = io.BytesIO()
                imagem_redimensionada1.save(imagem_bytesprogresso, format='PNG')
                layout_grafico_PalavrasChave_Mais_Frequente_Ano=[
                [sg.Text(f"Frequência da Palavra Mais Frequente por Ano")],
                [sg.Image(data=imagem_bytesprogresso.getvalue(),size = tamanho_imagem1, pad=(20, 10))],
                [sg.Button('Fechar')]
                ]
                janela_grafico_PalavrasChave_Mais_Frequente_Ano = sg.Window("Top 20 Autores", layout_grafico_PalavrasChave_Mais_Frequente_Ano) #Nova janela 
                
                stop87 = False
                while not stop87:
                    evento87,valor87 = janela_grafico_PalavrasChave_Mais_Frequente_Ano.read()
                    if evento87 == 'Fechar' or evento87 == sg.WIN_CLOSED:
                        stop87 = True
                        janela_grafico_PalavrasChave_Mais_Frequente_Ano.close()


    elif evento == "-IMPORTARBD-":
        
        
        caminho_ficheiro = sg.popup_get_file(
            "Selecione o ficheiro para importar registos",
            file_types=[("JSON Files", "*.json"), ("Todos os Ficheiros", "*.*")]
        )
        if caminho_ficheiro:
            # Verificar se o arquivo existe e não está vazio
            if not os.path.exists(caminho_ficheiro):
                janelaErro(f"Erro: O arquivo {caminho_ficheiro} não foi encontrado.")
                janelaprincipal["_Texto"].update(["Erro: O arquivo não foi encontrado."])
            elif os.stat(caminho_ficheiro).st_size == 0:
                janelaErro(f"Erro: O arquivo {caminho_ficheiro} está vazio.")
                janelaprincipal["_Texto"].update(["Erro: O arquivo está vazio."])
            else:
                bd_atual = lerBD(valor1['-FICHEIRO-'])
                # Tenta importar novos registos
                bd_atual, novos_adicionados = importar_novos_registos(bd_atual, caminho_ficheiro)

                if novos_adicionados > 0:
                    janelaprincipal["_Texto"].update([f"{novos_adicionados} novos registos adicionados com sucesso!"])
                else:
                    janelaprincipal["_Texto"].update(["Nenhum novo registo foi adicionado."])
        else:
            janelaprincipal["_Texto"].update(["Nenhum ficheiro foi selecionado."])


    elif evento == '-EXPORTARBD-' and bd_carregada: #ACABAR DE PASSAR PARA EVENTO E VALOR 10
        tiposfile = (("JSON Files", "*.json"), ("All Files", "*.*"))
        layoutexportarbd = [
            [
                sg.Text("Guardar base de dados como:"),
                sg.Input(key="-FICHEIROEXPORTAR-", size=(50, 1)),
                sg.FileSaveAs(button_text="Procurar", file_types=tiposfile, default_extension=".json", size=(8, 1))
            ],
            [sg.Button("Exportar", key="-GUARDAR-", size=(12, 1)), sg.Button("Cancelar", size=(12, 1))]
        ]

        # Janela de exportação
        janelaexportarbd = sg.Window("Exportar Ficheiro", layoutexportarbd, size=(650, 100))
        while True:
            evento10, valores10 = janelaexportarbd.read()

            if evento10 in (sg.WIN_CLOSED, "Cancelar"):
                janelaexportarbd.close()
                break

            elif evento10 == "-GUARDAR-":
                ficheiro_exportado = valores10["-FICHEIROEXPORTAR-"]
                if ficheiro_exportado:
                    try:
                        # Exporta a base de dados para o ficheiro especificado
                        exportarBd(valor1["-FICHEIRO-"], ficheiro_exportado)
                        janelaexportarbd.close()
                        sg.popup("Base de dados exportada com sucesso para:", ficheiro_exportado)
                        break
                    except Exception as e:
                        sg.popup_error(f"Erro ao exportar a base de dados: {e}")                              
    
janelaprincipal.close()

#------------------------------------------------------------LINHA DE COMANDO------------------------------------------------------------------

base = None  
n = -1

while n != 0:
    n = int(input("""Biblioteca de Artigos: 
        1 - Carregar Base de dados; 
        2 - Criar Publicação;
        3 - Eliminar Publicação;
        4 - Consultar Publicações;
        5 - Analisar Publicações;
        6 - Estatísticas;
        7 - Importar;
        8 - Exportar;
        9 - Ajuda;
        0 - Sair.\n"""))

    if n == 1:
        ficheiro = input("Qual o caminho para o ficheiro que pretende carregar?")
        if ficheiro == "":
            print("Caminho inválido!")
        else:
            base = lerBD(ficheiro)
            print("Base carregada com sucesso!")

    elif n in [2, 3, 4, 5, 6, 7, 8] and base is None:
        print("Erro: Tem de carregar a base de dados primeiro (opção 1).")


    elif n == 2:
        while True:
            abstract = input("Qual é o abstrato da publicação? ")
            if abstract.strip():
                break
            print("Erro: Tem de inserir um Abstract!")

        while True:
            title = input("Qual é o título da publicação? ")
            if title.strip():
                break
            print("Erro: Tem de inserir um título!")

        while True:
            try:
                n_authors = int(input("Qual o número de autores da publicação? "))
                if n_authors <= 0:
                    print("Erro: Tem de haver pelo menos um autor.")
                    continue
                break
            except ValueError:
                print("Erro: Introduza um número válido.")

        l_authors = []
        for i in range(n_authors):
            while True:
                author_name = input(f"Nome do autor {i + 1}: ")
                if author_name.strip():
                    author_affiliation = input(f"Afilição do autor {i + 1} (Deixe em branco se não aplicável): ").strip()
                    author_orcid = input(f"ORCID do autor {i + 1} (Deixe em branco se não aplicável): ").strip()

                    author_dict = {"name": author_name}

                    if author_affiliation:
                        author_dict["affiliation"] = author_affiliation
                    if author_orcid:
                        author_dict["orcid"] = author_orcid

                    l_authors.append(author_dict)
                    break
                else:
                    print("Erro: O nome do autor não pode estar vazio!")

        keywords = input("Quais são as palavras-chave da publicação? ")
        keywords = keywords.split(",") if keywords.strip() else []

        publish_date = input("Qual é a data de publicação (YYYY-MM-DD)? ").strip()
        publish_date = publish_date if publish_date else None

        doi = criarDOI(ficheiro)
        pdf = gerarpdf(ficheiro, doi)
        url = gerarurl(ficheiro, doi)

        publicacao = {
            "abstract": abstract,
            "title": title,
            "authors": l_authors,
            "doi": doi,
            "pdf": pdf,
            "url": url,
        }

        if keywords:
            publicacao["keywords"] = keywords
        if publish_date:
            publicacao["publish_date"] = publish_date

        criar2(ficheiro, abstract=abstract, palavras_chave=keywords, autores=l_authors, doi=doi, pdf=pdf, data_publicacao=publish_date, titulo=title, url=url)
        print("Publicação criada com sucesso!")

    elif n == 3:
        doi = input("Qual o DOI da publicação que pretende eliminar? ")
        if doi.strip():
            eliminar(ficheiro, doi)
        else:
            print("Erro: O campo DOI não pode estar vazio.")


    elif n == 4:
        m = int(input("""O que quer consultar?
        1 - Publicação completa;
        2 - Publicação por título;
        3 - Publicação por autor;
        4 - Publicação por afiliação;
        5 - Publicação por data;
        6 - Publicação por palavra-chave.\n"""))

        if m == 1:
            doi = input("Qual é o DOI da publicação? ")
            
            if doi.strip():
                    if confirmarDOI(ficheiro,doi):
                        publicacao = obter_publicacao_por_doi(ficheiro, doi)
                        if publicacao:
                            print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                            print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                            print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                            print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                            print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")


                            print("** AUTORES **")
                            for autor in publicacao.get('authors', []):
                                print(f"  - Nome: {autor['name']}")
                                if 'affiliation' in autor:
                                    print(f"    Afiliação: {autor['affiliation']}")
                                if 'orcid' in autor:
                                    print(f"    ORCID: {autor['orcid']}")
                                print()

                            if 'keywords' in publicacao:
                                print(f"** PALAVRAS-CHAVE **")
                                print(", ".join(publicacao['keywords']))
                            if 'publish_date' in publicacao:
                                print(f"** DATA DE PUBLICAÇÃO **")
                                print(publicacao['publish_date'])

                        else:
                          print("Erro: Publicação não encontrada!")
                    else:
                        print("Erro: DOI não encontrado na base de dados!")  
            else:
               print("Erro: DOI inválido!")


        elif m == 2:
            titulo = input("Qual é o título da publicação? ")
            if titulo.strip():
                publicacoes = consultaPublicacaoTitulo(ficheiro, titulo)
                if publicacoes:
                    for publicacao in publicacoes:
                        print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                        print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                        print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                        print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                        print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")


                        print("** AUTORES **")
                        for autor in publicacao.get('authors', []):
                            print(f"  - Nome: {autor['name']}")
                            if 'affiliation' in autor:
                                print(f"    Afiliação: {autor['affiliation']}")
                            if 'orcid' in autor:
                                print(f"    ORCID: {autor['orcid']}")
                            print()

                        if 'keywords' in publicacao:
                            print(f"** PALAVRAS-CHAVE **")
                            print(publicacao['keywords'])
                        if 'publish_date' in publicacao:
                            print(f"** DATA DE PUBLICAÇÃO **")
                            print(publicacao['publish_date'])
                else:
                    print("Erro: Publicação com esse título não encontrada!")
            else:
                print("Erro: Título inválido!")

        elif m == 3:
            autor = input("Qual é o autor da publicação? ")
            if autor.strip():
                publicacoes = consultaPublicacao_autor(ficheiro, autor)
                if publicacoes:
                    for publicacao in publicacoes:
                        print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                        print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                        print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                        print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                        print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")


                        print("** AUTORES **")
                        for autor_item in publicacao.get('authors', []):
                            print(f"  - Nome: {autor_item['name']}")
                            if 'affiliation' in autor_item:
                                print(f"    Afiliação: {autor_item['affiliation']}")
                            if 'orcid' in autor_item:
                                print(f"    ORCID: {autor_item['orcid']}")
                            print()

                    if 'keywords' in publicacao:
                        print(f"** PALAVRAS-CHAVE **")
                        print(publicacao['keywords'])
                    if 'publish_date' in publicacao:
                        print(f"** DATA DE PUBLICAÇÃO **")
                        print(publicacao['publish_date'])
                else:
                    print("Erro: Publicações de autor não encontradas!")
            else:
               print("Erro: Autor inválido!")

        elif m == 4:
            afiliacao = input("Qual é a afiliação do autor? ")
            if afiliacao.strip():
                publicacoes = consultaPublicacao_afiliacao(ficheiro, afiliacao)
                if publicacoes:
                    for publicacao in publicacoes:
                        print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                        print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                        print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                        print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                        print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")

                        print("** AUTORES **")
                        for autor in publicacao.get('authors', []):
                            print(f"  - Nome: {autor['name']}")
                            if 'affiliation' in autor:
                                print(f"    Afiliação: {autor['affiliation']}")
                            if 'orcid' in autor:
                                print(f"    ORCID: {autor['orcid']}")
                            print()

                        if 'keywords' in publicacao:
                            print(f"** PALAVRAS-CHAVE **")
                            print(publicacao['keywords'])
                        if 'publish_date' in publicacao:
                            print(f"** DATA DE PUBLICAÇÃO **")
                            print(publicacao['publish_date'])
                else:
                    print(f"Erro: Nenhuma publicação encontrada para a afiliação '{afiliacao}'!")
            else:
                print("Erro: Afiliação inválida!")

        elif m == 5:
            data = input("Qual é a data da publicação (YYYY-MM-DD)? ")
            if data.strip():
                try:
                    datetime.strptime(data, '%Y-%m-%d')
                    publicacoes = consultaPublicacao_data1(ficheiro, data)

                    if publicacoes:
                        for publicacao in publicacoes:
                            print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                            print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                            print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                            print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                            print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")

                            print("** AUTORES **")
                            for autor in publicacao.get('authors', []):
                                print(f"  - Nome: {autor['name']}")
                                if 'affiliation' in autor:
                                    print(f"    Afiliação: {autor['affiliation']}")
                                if 'orcid' in autor:
                                    print(f"    ORCID: {autor['orcid']}")
                                print()

                            if 'keywords' in publicacao:
                                print(f"** PALAVRAS-CHAVE **")
                                print(publicacao['keywords'])
                            if 'publish_date' in publicacao:
                                print(f"** DATA DE PUBLICAÇÃO **")
                                print(publicacao['publish_date'])
                    else:
                        print(f"Erro: Nenhuma publicação encontrada para a data '{data}'!")

                except ValueError:
                    print("Erro: Formato de data inválido! Use YYYY-MM-DD.")
            else:
                print("Erro: Data inválida!")

        elif m == 6:
            palavra_chave = input("Qual é a palavra-chave da publicação? ")
            if palavra_chave.strip():
                publicacoes = consultaPublicacao_keywords(ficheiro, palavra_chave)
                if publicacoes:
                    for publicacao in publicacoes:
                        print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                        print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                        print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                        print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                        print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")


                        print("** AUTORES **")
                        for autor in publicacao.get('authors', []):
                            print(f"  - Nome: {autor['name']}")
                            if 'affiliation' in autor:
                                print(f"    Afiliação: {autor['affiliation']}")
                            if 'orcid' in autor:
                                print(f"    ORCID: {autor['orcid']}")
                            print()

                        if 'keywords' in publicacao:
                            print(f"** PALAVRAS-CHAVE **")
                            print(publicacao['keywords'])
                        if 'publish_date' in publicacao:
                            print(f"** DATA DE PUBLICAÇÃO **")
                            print(publicacao['publish_date'])
                else:
                    print(f"Erro: Nenhuma publicação encontrada com a palavra-chave '{palavra_chave}'!")
            else:
                print("Erro: Palavra-chave inválida!")


    elif n == 5:
            x = int(input("""Como pretende listar os autores?
            1 - Por frequência de publicação;
            2 - Por ordem alfabética.\n"""))

            if x == 1:
                autores = listar_aut_artigo(ficheiro)
                if autores:
                    for autor, freq in autores:
                        print(f"{autor}: {freq} publicações")
                    author = input("Introduza o autor de quem quer ver as publicações: ")
                    if author:
                        publ = artigos_aut_artigo(ficheiro, author)
                        if publicacao:
                            print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                            print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                            print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                            print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                            print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")

                            print("** AUTORES **")
                            for autor in publicacao.get('authors', []):
                                print(f"  - Nome: {autor['name']}")
                                if 'affiliation' in autor:
                                    print(f"    Afiliação: {autor['affiliation']}")
                                if 'orcid' in autor:
                                    print(f"    ORCID: {autor['orcid']}")
                                print()

                            if 'keywords' in publicacao:
                                print(f"** PALAVRAS-CHAVE **")
                                print(publicacao['keywords'])
                            if 'publish_date' in publicacao:
                                print(f"** DATA DE PUBLICAÇÃO **")
                                print(publicacao['publish_date'])
                    else:
                        print("Erro: Nome do autor inválido.")
                else:
                    print("Erro: Não há autores na base de dados.")

            elif x == 2:
                autores = listar_aut_alfabetico(ficheiro)
                if autores:
                    print("Autores ordenados por ordem alfabética:")
                    for autor in autores:
                        print(autor)
                    author = input("Introduza o autor de quem quer ver as publicações: ")
                    if author in autores:
                        publ = artigos_aut_alfabético(ficheiro, author)
                        if publ:
                            print(f"\n** TÍTULO **\n{publicacao.get('title', 'Título não disponível')}\n")
                            print(f"** ABSTRACT **\n{publicacao.get('abstract', 'Resumo não disponível')}\n")
                            print(f"** DOI **\n{publicacao.get('doi', 'DOI não disponível')}\n")
                            print(f"** PDF **\n{publicacao.get('pdf', 'PDF não disponível')}\n")
                            print(f"** URL **\n{publicacao.get('url', 'URL não disponível')}\n")

                            # Exibe autores
                            print("** AUTORES **")
                            for autor in publicacao.get('authors', []):
                                print(f"  - Nome: {autor['name']}")
                                if 'affiliation' in autor:
                                    print(f"    Afiliação: {autor['affiliation']}")
                                if 'orcid' in autor:
                                    print(f"    ORCID: {autor['orcid']}")
                                print()

                            # Exibe palavras-chave e data de publicação
                            if 'keywords' in publicacao:
                                print(f"** PALAVRAS-CHAVE **")
                                print(publicacao['keywords'])
                            if 'publish_date' in publicacao:
                                print(f"** DATA DE PUBLICAÇÃO **")
                                print(publicacao['publish_date'])
                    else:
                        print("Erro: Nome do autor inválido.")
                else:
                    print("Erro: Não há autores na base de dados.")


    elif n == 6:
        #print("Estatísticas em desenvolvimento...")
        g = int(input("""Qual o gráfico que pretende visualizar?
        1 - Publicações por Ano;
        2 - Publicações por Mês de um Ano;
        3 - Top 20 autores;
        4 - Publicações por Ano de um Autor;
        5 - Top 20 Palavras-Chave;
        6 - A Palavra-Chave Mais Frequente por Ano.\n"""))

        if g==1:
            conta_ano_GrafBarras(ficheiro)

        elif g==2:
            anoSel=input("Qual o ano que pretende consultar?")
            conta_Mes_de_AnoGraf(ficheiro, anoSel)

        elif g==3:
            conta_autor_Grafico(ficheiro)

        elif g==4:
            autorSel=input("Qual o autor que pretende consultar?")
            conta_autor_anos_Grafico(ficheiro, autorSel)

        elif g==5:
            conta_palavras_chaveGrafico(ficheiro)

        elif g==6:
            palavra_mais_frequente_Ano_Grafico(ficheiro)



    elif n == 7:
        caminho = input("Caminho do ficheiro para importar: ")
        if caminho.strip():
            importar_novos_registos(ficheiro, caminho)
        else:
            print("Erro: Caminho inválido!")

    elif n == 8:
        expor = input("Qual o nome do ficheiro que pretende exportar?")
        if expor == "" :
            print("Nome inválido!")
        else:
            exportarBd(ficheiro,expor)

    elif n == 9:
        print("""
            - Ao selecionar a opção 1, selecionar do computador a base de dados pretendida, de forma a conseguir trabalhar nas restantes opções.
            - Ao selecionar a opção 2, preencher todos os campos pedidos e a função vai adicionar a nova publicação à base de dados.
            - Ao selecionar a opção 3, escolher uma publicação pelo seu doi e a publicação vai ser eliminada da base de dados.
            - Ao selecionar a opção 4, deve seguir os seguintes passos:
              - escolher de que forma pretende consultar as publicações:
              - se selecionar a opção "Consultar Publicação completa";
              -se selecionar a opção "Consultar Publicação por titulo";
              -se selecionar a opção "Consultar Publicação por autor";
              -se selecionar a opção "Consultar Publicação por afiliação";
              -se selecionar a opção "Consultar Publicação por data de publicação";
              -se selecionar a opção "Consultar Publicação por palavra-passe";
            - Ao selecionar a opção 5, deve seguir os seguintes passos: 
              - escolhar como pretende listar os autores das publições (por frequência de publicação ou por ordem alfabético);
              - escolher qual o autor que pretende visualisar as publicações.
            - Ao selecionar a opção 6, ao selecionar a opção é gerado um relatório de estatísticas do ficheiro até ao momento.
            - Ao selecionar a opção 7, selecionar do computador um ficheiro, sendo a informação nele contida agregada ao carregado previamente.
            - Ao selecionar a opção 8, escolher o nome para ficheiro e as alterações são exportadas para um novo ficheiro em json.""")
