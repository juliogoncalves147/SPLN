# Tratar Títulos sem Numeração ###T
# Tratar Títulos com Numeração ###TN
# Cada Título Numerado tem a área associada ###AREA
# Cada Titulo Numerado pode ter ou não sinónimos ###SIN
# Cada Titulo Numerado tem uma ou mais linguas associadas ###LINGUA
# Variante = ###VAR

import re
import json

texto = open('medicina.xml', 'r').read()


def remove_cabecalho(texto):
    texto = re.sub(r'<text.* font="1">ocabulario.*</text>', r'###', texto)
    texto = re.sub(r'.*\n###\n.*\n', r'', texto)
    texto = re.sub(r'<page.*\n|</page>\n', r'', texto)

    return texto


texto = remove_cabecalho(texto)

def remove_empty_linhas(texto):
    texto = re.sub(r'<text.* font="0">\s</text>', r'', texto)
    texto = re.sub(r'<text.* font="\d+"><b>\s*</b></text>', r'', texto)
    texto = re.sub(r'<text.* font="\d+"><i>\s*</i></text>', r'', texto)
    texto = re.sub(r'<text.* font="\d+">\s*</text>', r'', texto)
    return texto

texto = remove_empty_linhas(texto)


def trata_titulos(texto):
    texto = re.sub(r'<text.* height="18" font="3">\s*<b>\s*(\S.*)</b></text>', r'###T \1', texto)
    return texto

texto = trata_titulos(texto)


def trata_titulos_numerados(texto):
    texto = re.sub(r'###T (\d+.*)', r'###TN \1', texto)
    return texto

texto = trata_titulos_numerados(texto)


def trata_descricao_titulos(texto):
    texto = re.sub(r'<text.*?>\s*(Vid\.-.*)\s*</text>', r'DESC \1', texto)
    texto = re.sub(r'<text.*?>\s*(Vid\..*)\s*</text>', r'DESC \1', texto)
    return texto

texto = trata_descricao_titulos(texto)

def trata_area(texto):
    texto = re.sub(r'<text.* font="6"><i>\s*(.*)\s*</i></text>', r'AREA \1', texto)
    return texto

texto = trata_area(texto)


def trata_lingua(texto):
    texto = re.sub(r'<text.* font="0">\s*(\w+)\s*</text>', r'LINGUA \1', texto)
    return texto

texto = trata_lingua(texto)

def trata_sinonimos(texto):
    texto = re.sub(r'<text.* font="5">\s*(SIN\.-)(.*)</text>', r'SIN \2', texto)
    texto = re.sub(r'<text.* font="0">\s*(SIN\.-)(.*)</text>', r'SIN \2', texto)
    return texto

texto = trata_sinonimos(texto)

def trata_variante(texto):
    texto = re.sub(r'<text.* font="5">\s*(VAR.*)</text>', r'VAR \1', texto)
    texto = re.sub(r'<text.* font="0">\s*(VAR.*)</text>', r'VAR \1', texto)
    return texto

texto = trata_variante(texto)

def trata_fontspec(texto):
    texto = re.sub(r'<fontspec.*', r'', texto)
    return texto

texto = trata_fontspec(texto)

def trata_texto(texto):
    texto = re.sub(r'<text.* font="7"><i>(.*?)<\/i><\/text>', r'@\1', texto)
    texto = re.sub(r'<text.* font="0">;\s*</text>', r';', texto)
    return texto

texto = trata_texto(texto)

def trata_sinonimos_continuacao(texto):
    texto = re.sub(r'<text.* font="5">\s*(\S.*)</text>', r'\1', texto)
    return texto

texto = trata_sinonimos_continuacao(texto)


def trata_nota(texto):
    texto = re.sub(r'<text.* font="9">\s*(Nota.*)</text>', r'\1', texto)
    texto = re.sub(r'<text.* font="9">\s*(\S*)</text>', r'\1', texto)
    return texto

texto = trata_nota(texto)

def trata_titulos_numerados_continuacao(texto):
    texto = re.sub(r'<text.* font="10"><i><b>\s*(\S.*)</b></i></text>', r'\1', texto)
    return texto

texto = trata_titulos_numerados_continuacao(texto)

def trata_texto_continuacao(texto):
    texto = re.sub(r'<text.* font="11"><b>\s*(\S.*)</b></text>', r'\1', texto)
    return texto

texto = trata_texto_continuacao(texto)

def trata_nota_continuacao(texto):
    texto = re.sub(r'<text.* font="9">\s*(\S.*)</text>', r'\1', texto)
    return texto

texto = trata_nota_continuacao(texto)

def trata_tags_inuteis(texto):
    texto = re.sub(r'<\?xml.*>', r'', texto)
    texto = re.sub(r'<pdf2xml.*>', r'', texto)
    texto = re.sub(r'<!DOCTYPE.*>', r'', texto)
    texto = re.sub(r'</pdf2xml>', r'', texto)
    return texto


texto = trata_tags_inuteis(texto)

# dicionario
dic = {"T": {}, "C": {}}
entrada_atual = ""

file = open('medicina.txt', 'w')
file.write(texto)
file.close()

lista = texto.split("###")

dicionario = {"T" : {}, "TN" : {}}

for elemento in lista:
    if elemento[0] == 'T':
        elemento = elemento.split('\n')
        #remove all empty strings
        elemento = list(filter(None, elemento))
        elemento[0] = elemento[0].split(' ')[1]
        #adiciona elemento ao dicionario
        dicionario["T"][elemento[0]] = elemento[1:]

    elif elemento[0] == 'TN':
        elemento = elemento[1:]
        linguas = elemento.split('LINGUA')
        areas = linguas[0].split('AREA')[1:]
        areas = limpaListaElementos(areas)
        titulo = linguas[0].split('AREA')[0]
        linguas = linguas[1:]
        linguas = subByArrow(linguas)
        linguas = limpaListaElementos(linguas)
        numero = titulo.split(' ')[1]
        nome = titulo.split(' ')[2:-1]
        nome = list(filter(None, nome))
        genero = titulo.split(' ')[-1]
        genero = limpaElemento(genero)
        dicionario['TN'][numero] = {'nome': nome,'genero' : genero,'areas': areas, 'linguas': linguas}
    
file = open("dicionario.json", "w")
file.write(json.dumps(dicionario, indent=4, sort_keys=True))
file.close()

file = open("dicionario.txt", "w")
file.write(str(dicionario))
file.close()



