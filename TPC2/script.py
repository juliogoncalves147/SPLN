import os
import re
import json

# Load your PDF
#os.system("pdftohtml -f 20 -l 543 -xml medicina.pdf");
fi = open("medicina.xml", "r")
fo = open("output.xml", "w+")

completos=0
incompletos=0

idL=0
input = fi.read()

# linha de xml em que o grupo 4 é o texto
linha = r'<text((([^>])))*>(.*)<\/text>'

dicionario = {}

def removeNotText(text):
    txt=r'^(<text.*\n)'
    text = re.sub(txt, r'#\1', text, flags=re.MULTILINE)
    noTxt = r'^[^#].*\n'
    text = re.sub(noTxt, '', text, flags=re.MULTILINE)
    text = re.sub(r'^#', '', text, flags=re.MULTILINE)
    return text

def removeHeaderFooter(text):
    # remove header
        # font=1 cabecalho e linha anterior
    header = r'^.*\n.*font="1">ocabulario.*\n.*\n'
    text = re.sub(header, '', text, flags=re.MULTILINE)
    # remove footer
        # font=2 para o numero de pagina
    footer = r'<text.*font=\"1\".*'
    text = re.sub(footer, '', text, flags=re.MULTILINE)
    return text

def fontX(text):
    return re.sub(r'<text[^>]+(font=\"\d+\")>(.*)<\/text>', r'<text \1>\2</text>', text, flags=re.MULTILINE)

def removeEmpty(text):
    return re.sub(r'<text[^>]+>(\s*)<\/text>\n', r'', text, flags=re.MULTILINE)

def removeSpaces(text):
    return re.sub(r'(\s)+', r'\1', text, flags=re.MULTILINE)

def removeChangers(text):
    return re.sub(r'<\/?[ib]>', r'', text, flags=re.MULTILINE)

def initWord(text):
    text = re.sub(r'<text font="(3|11)">\s*(\d+.*)<\/text>', r'%%%C \2', text, flags=re.MULTILINE)
    return re.sub(r'<text font="(3|11)">\s*(\D+)<\/text>', r'%%%L \2', text, flags=re.MULTILINE)

def handleLanguages(text):
    return re.sub(r'<text font="0">(.*)<\/text>\s*\n((<text font="[^30]">(.*)<\/text>\s*)+)', r'@ \1\n@ \2', text, flags=re.MULTILINE)

def handleNotas(text):
    text = re.sub(r'<text font="9">(.*)<\/text>\s*', r'£ \1\n', text, flags=re.MULTILINE)
    return re.sub(r'([^>\s])\s*£ ',r'\1', text, flags=re.MULTILINE)

def handleSinVar(text):
    text=re.sub(r'^\s*(Vid.-)',r'$ \1', text, flags=re.MULTILINE)
    text=re.sub(r'^\s*(VAR\.-.*\n)',r'$ \1', text, flags=re.MULTILINE)
    return re.sub(r'^\s*(SIN\.-.*\n)',r'$ \1', text, flags=re.MULTILINE)

def handleFam(text):
    return re.sub(r'(%%%.*\n)(\s*\w+)',r'\1§ \2', text, flags=re.MULTILINE)

def getText(text):
    return re.sub(linha, r'\4', text, flags=re.MULTILINE)

def handleNumeros(text):
    return re.sub(r'\n\s*(\d+)\s*(%%%L)([^\n]*\n)',r'\n%%%C \1 \3', text, flags=re.MULTILINE)

def removeNL(text):
    return re.sub(r'\n\s*(\w)',r' \1', text, flags=re.MULTILINE)

def marcaE(text):
    global completos, incompletos
    entries = text.split('%%%')
    repetidos=0
    for elem in entries:
        if re.match(r'^C', elem):
            k,v = marcaEC(elem);
            #if k in dicionario:
            #    print("repetido em "+k)
            #    repetidos+=1
            dicionario[k] = v;
            completos+=1
        elif re.match(r'^L', elem):
            k,v = marcaEL(elem);
            dicionario[k] = v;
            incompletos+=1
    #print("Total repetidos: "+str(repetidos))


def removeStartEndSpaces(i):
    i = re.sub(r'^\s*(.*)', r'\1', i)
    i = re.sub(r'(.*\w)\s*$', r'\1', i)
    return i

def idiomasHandle(idiomas):
    es = ""
    en = ""
    pt = ""
    la = ""
    flag=""
    for i in idiomas:
        i = removeStartEndSpaces(i)
        if i == "es":
            flag="es"
        elif i == "en":
            flag="en"
        elif i == "pt":
            flag="pt"
        elif i == "la":
            flag="la"
        else:
            if flag == "es":
                es += i
            elif flag == "en":
                en += i
            elif flag == "pt":
                pt += i
            elif flag == "la":
                la += i

    es = es.split(';')
    en = en.split(';')
    pt = pt.split(';')
    la = la.split(';')

    return {'es':es, 'en':en, 'pt':pt, 'la':la}
            
def sinVarHandle(sinVar):
    sin=""
    var=""
    for i in sinVar:
        i = removeStartEndSpaces(i)
        if re.match(r'^SIN\.-(.*)', i):
            sin+=re.match(r'^SIN\.-(.*)', i).group(1)
        elif re.match(r'^VAR\.-(.*)', i):
            var+=re.match(r'^VAR\.-(.*)', i).group(1)

    sin = sin.split(';')
    i=0
    while i < len(sin):
        sin[i] = removeStartEndSpaces(sin[i])
        i+=1
    var = var.split(';')
    while i < len(var):
        var[i] = removeStartEndSpaces(var[i])
        i+=1


    return {'sin':sin, 'var':var}

def marcaEC(text):
    text = text.replace('C ', '')
    txt = text.split('\n')
    linha1 = re.match(r'(\d+)(( *[^\n]*)*)\s*(\w)\s?', txt[0])
    id = linha1.group(1)
    termo = linha1.group(2)
    termo = removeStartEndSpaces(termo)
    tipo = linha1.group(4)
    lIdiomas=[]
    lSinVar=[]
    notas=''
    areaT=''
    for i in txt:
        if i == "":
            continue
        elif i[0]=='§':
            areaT=i[1:]
            areaT = removeStartEndSpaces(areaT)
        elif i[0]=='@':
            lIdiomas.append(i[1:])
        elif i[0]=='$':
            lSinVar.append(i[1:])
        elif i[0]=='£':
            notas = re.sub(r'£\s*Nota\.-\s*(.*)', r'\1', i)
    idiomas={}
    sinVar={}
    if len(lIdiomas) > 0:
        idiomas = idiomasHandle(lIdiomas)
    if len(lSinVar) > 0:
        sinVar = sinVarHandle(lSinVar)

    sin = sinVar.get('sin',sinVar)
    var = sinVar.get('var',sinVar)

    return "C"+id, {'termo':termo, 'tipo':tipo, 'areaT':areaT, 'idiomas':idiomas, 'sin':sin, 'var':var, 'notas':notas}

def marcaEL(text):
    global idL
    text = text.replace('L ', '')
    txt = text.split('\n')
    termo = removeStartEndSpaces(txt[0])
    lVid=[]
    vid=""
    for i in txt:
        if i == "":
            continue
        elif i[0]=='$':
            lVid.append(i[1:])
    idx=0
    while idx < len(lVid):
        if re.match(r'^Vid\.-(.*)', lVid[idx]):
            vid+=re.match(r'^Vid\.-(.*)', lVid[idx]).group(1)
        idx+=1
    id = idL
    idL+=1
    return "L"+str(id), {'termo':termo, 'vid':vid}


#text = re.sub(linha, r'## \4', text, flags=re.MULTILINE)
#newText = ''
#for line in text.splitlines():
#    if re.match(linha, line):
#        newText += re.sub(linha, r'\4', line, flags=re.MULTILINE) + '\n'
txt=removeNotText(input)
txt=removeHeaderFooter(txt)
txt=removeSpaces(txt)
txt=fontX(txt)
txt=removeChangers(txt)
txt=removeEmpty(txt)
txt=initWord(txt)
txt=handleNotas(txt)
txt=handleLanguages(txt)
txt=getText(txt)
txt=handleSinVar(txt)
txt=handleFam(txt)
txt=handleNumeros(txt)
txt=removeNL(txt)

marcaE(txt)

print("Completos: "+str(completos))
print("Incompletos: "+str(incompletos))

fr = open('dic.json','w')
fr.write(json.dumps(dicionario, ensure_ascii=False, indent=4))

fo.write(txt)

