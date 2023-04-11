#!/usr/bin/env python3
'''Tokenizer'''

import sys 
import re
import fileinput

__version__ = '0.3.0'

def main():
    f = open("output.txt", "w")
    
    text = ""
    
    for line in fileinput.input():
        text += line
        
    # 1 . Separar pontuação das palavras
    regex_cap = r"([a-zA-ZêÉ])([?.!-,;])"
    text = re.sub(regex_cap, r"\1 \2", text, flags= re.UNICODE)
    
    # Separa o Sr. e o Sra.
    regex_cap = r"([sS][rR][aA]?) .\n? ?([a-zA-Z]*)"
    text = re.sub(regex_cap, r"\1. \2", text, flags= re.UNICODE)
    
    
    # 2 . Marcar Capitulos
    regex_cap = r".*(CAP[IÍ]TULO \w+).*" # Marca os CAPITULOS
    text = re.sub(regex_cap, r"\n# \1", text)
    
    # Tira os \n a mais
    regex_cap = r"\n+"
    text = re.sub(regex_cap, r"\n\n", text, flags = re.UNICODE)
    
    
    # 3 . # 4 . Juntar Linhas da mesma frase
    regex_cap = r"([a-z0-9;-ãê!?,\.])\n+([a-z0-9E\"])" # Tira os paragrafes dentro da mesma frase
    text = re.sub(regex_cap, r"\1 \2", text, flags = re.UNICODE)
    
    # 5 . Uma frase por linha
    regex_cap = r"(?<= \.)\s(.+?) \."
    text = re.sub(regex_cap, r" \n\t\t\1 .", text, flags = re.UNICODE)
    
    #regex_cap = r"\n(.*?) .\n"
    #text = re.sub(regex_cap, r"<paragrafo>\1<paragrafo", text, flags = re.UNICODE)
    
    
    arr_poemas = []
    
    def guardar_poema(poema):
        dic_poemas.append(poema[1])
        return f">>{len(dic_poemas)}<<"
    
    regex_poema = r"<poema>(.*?)</poema>"
    text = re.sub(regex_poema, guardar_poema, text, flags = re.S)

    f.write(text)