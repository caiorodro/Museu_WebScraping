import bs4
import requests
from bs4 import BeautifulSoup as bs
import lxml.html as lh
import json
import pandas as pd

class acervoLinks:

    _page = None

    listOfLinks = ['fotografias.php', 'mapas.php', 'cartas.php', 'livros.php', 'requerimentos.php', 'jornais.php', 'passageiros.php']

    TB_FOTOGRAFIA = []
    TB_CARTAS = []

    idComboLocal = 'local'
    idComboYear = 'Ano_ini'

    listLocals = []
    listYears = []

    def __init__(self, url=None):

        self.urlHome = 'http://www.inci.org.br/acervodigital/'

        if url != None:
            self.parsePage(url)
            self.urlHome = url

    def listJsonToString(self):
        strJson = '['

        for item in self.TB_FOTOGRAFIA:
            strJson += str(item) + ','

        strJson += ']'

        df = pd.DataFrame(eval(strJson))

        return df

    def createTextFile(self, text, fileName):
        file = open(fileName,"w") 
        file.write(text) 
 
        file.close() 

    def parsePage(self, url):
        html = requests.get(url)
        page = bs(html.content, "html.parser")

        self._page = page

    def comboBox(self, id):
        comboOf = self._page.find("select", {"id": id}).findAll('option')

        listOf = []

        for item in comboOf:
            listOf.append(item['value'])

        if id == 'local':
            self.listLocals = listOf

        if id == 'Ano_ini':
            self.listYears = listOf

    def hRefsHome(self):
        listOfAs = self._page.findAll("a")

        listOf = []

        for a in listOfAs:
            link = a['href']

            if link != None and link not in listOf and a.find('target') == None and link in self.listOfLinks:
                listOf.append(link)

        return listOf

        self._page.text
        tables = self._page.findAll('table')

        for table in tables:
            item = table

    def gelHtmlCell(self, start, end, strHtml):
        idxStart = strHtml.find(start)
        strHtml = strHtml[idxStart:]

        idxEnd = strHtml[0:].find(end)

        column = strHtml[0 : idxEnd + len(end)]
        columnAutor = '<td class="textocolorido"><strong>Autor'

        if column.startswith(columnAutor):
            column = column.replace(columnAutor, '<td class="textocolorido"><span class="texto"><em><strong>Autor')
            column = column.replace('</td>', '</span></td>')
            column = column.replace('</strong>', '</strong></em>')
        
        content = lh.fromstring(column)
        tdElement = content.xpath('//td')

        return tdElement

    def lineOfResults_FOTOGRAFIA(self, strHtml):

        tags = []
        tags.append('<td width="146" rowspan="4" valign="middle" class="textocolorido">')
        tags.append('<td colspan="2" class="textocolorido"><span class="texto"><em class="texto"><strong>Legenda')
        tags.append('<td width="388" class="textocolorido"><span class="texto"><em class="texto"><strong>Tema')
        tags.append('<td width="316" class="textocolorido"><span class="texto"><em><strong>Local')
        tags.append('<td class="textocolorido"><span class="texto"><em><strong>Data')
        tags.append('<td class="textocolorido"><span class="texto"><em><strong>Formato')
        tags.append('<td class="textocolorido"><span class="texto"><em><strong>Material')
        tags.append('<td class="textocolorido"><span class="texto"><em><strong>N&ordm; Topogr&aacute;fico')
        tags.append('<td class="textocolorido"><strong>Autor')
        tags.append('<td  class="textocolorido"><span class="texto"><em class="texto"><strong>Palavra-chave')
        
        while '<td width="146" rowspan="4" valign="middle" class="textocolorido">' in strHtml:

            foto = ''
            legenda = ''
            tema = ''
            local = ''
            Data = ''
            formato = ''
            material = ''
            topografico = ''
            autor = ''
            palavraChave = ''

            end = '</td>'
            i = 0

            for i in range(len(tags)):
                tdElement = self.gelHtmlCell(tags[i], end, strHtml)

                if i == 0:
                    foto = self.urlHome + tdElement[0][0][0].attrib['href']

                elif i == 1:
                    legenda = tdElement[0][0][0].tail
                
                elif i == 2:
                    tema = tdElement[0][0][0].tail

                elif i == 3:
                    local = tdElement[0][0][0].tail

                elif i == 4:
                    Data = tdElement[0][0][0].tail

                elif i == 5:
                    formato = tdElement[0][0][0].tail

                elif i == 6:
                    material = tdElement[0][0][0].tail

                elif i == 7:
                    topografico = tdElement[0][0][0].tail

                elif i == 8:
                    autor = tdElement[0][0][0].tail

                elif i == 9:
                    palavraChave = tdElement[0][0][0].tail
                    idx = strHtml.find(tags[i])
                    strHtml = strHtml[idx + len(tags[i]) :]

            legenda = legenda.replace(':', '').replace('"', '')
            tema = tema.replace(':', '').replace('"', '')
            local = local.replace(':', '').replace('"', '')
            Data = Data.replace(':', '').replace('"', '')
            formato = formato.replace(':', '').replace('"', '')
            material = material.replace(':', '').replace('"', '')
            topografico = topografico.replace(':', '').replace('"', '')
            autor = autor.replace(':', '').replace('"', '')
            palavraChave = palavraChave.replace(':', '').replace('"', '')

            str1 = '{ "FOTO": "' + foto + '", "LEGENDA": "' + legenda + '", "TEMA": "' + tema + '", '
            str1 += '"LOCAL": "' + local + '", "DATA": "' + Data + '", "FORMATO": "' + formato + '", '
            str1 += '"MATERIAL": "' + material + '", "TOPOGRAFICO": "' + topografico + '", "AUTOR": "' + autor + '", '
            str1 += '"PALAVRA_CHAVE": "' + palavraChave + '" }'

            try:
                _dict = json.loads(str1)
            except:
                print(str1)

            self.TB_FOTOGRAFIA.append(_dict)

    def lineOfResults_CARTAS(self, strHtml):

        tags = []

        tags.append('<td width="286" class="textocolorido"><span class="texto"><em class="texto"><strong>Tombo')
        tags.append('<td width="251" class="textocolorido"><span class="texto"><em class="texto"><strong>Data Limite')
        tags.append('<td width="313" rowspan="3" class="textocolorido">')
        tags.append('<td class="textocolorido"><span class="texto"><span class="texto"><em><strong>Denominacao')
        tags.append('<td class="textocolorido"><span class="texto"><span class="texto"><em><strong>Assunto')
        tags.append('<td class="textocolorido"><span class="texto"><span class="texto"><em><strong>T&iacute;tulo')
        tags.append('<td class="textocolorido"><span class="texto"><em class="texto"><strong>Origem')
        tags.append('<td colspan="3" class="textocolorido"><span class="texto"><em class="texto"><strong>Descri&ccedil;&atilde;o')

        while '<td width="286" class="textocolorido">' in strHtml:

            tombo = ''
            dataLimite = ''
            pdf = ''
            denominacao = ''
            assunto = ''
            titulo = ''
            origem = ''
            descricao = ''

            end = '</td>'
            i = 0

            for i in range(len(tags)):
                tdElement = self.gelHtmlCell(tags[i], end, strHtml)

                if i == 0:
                    tombo = tdElement[0][0][0].tail

                elif i == 1:
                    dataLimite = tdElement[0][0][0].tail

                elif i == 2:
                    pdf = self.urlHome + tdElement[0][0].attrib['href']

                elif i == 3:
                    denominacao = tdElement[0][0][0].tail

                elif i == 4:
                    assunto = tdElement[0][0][0].tail

                elif i == 5:
                    titulo = tdElement[0][0][0].tail

                elif i == 6:
                    origem = tdElement[0][0][0].tail

                elif i == 7:
                    descricao = tdElement[0][0][0].tail
                    idx = strHtml.find(tags[i])
                    strHtml = strHtml[idx + len(tags[i]) :]

            cells = [tombo, dataLimite, pdf, denominacao, assunto, titulo, origem, descricao]

            map(lambda x: x.replace(':', '').replace('"', ''), cells)

            tombo = cells[0]
            dataLimite = cells[1]
            pdf = cells[2]
            denominacao = cells[3]
            assunto = cells[4]
            titulo = cells[5]
            origem = cells[6]
            descricao = cells[7]

            str1 = '{ "TOMBO": "' + tombo + '", "DATA LIMITE": "' + dataLimite + '", "PDF": "' + pdf + '", '
            str1 += '"DENOMINACAO": "' + denominacao + '", "ASSUNTO": "' + assunto + '", "TITULO": "' + titulo + '", '
            str1 += '"ORIGEM": "' + origem + '", "DESCRICAO": "' + descricao + '" }'

            try:
                _dict = json.loads(str1)
            except:
                print(str1)

            self.TB_CARTAS.append(_dict)

    def postaPesquisaFotografias(self):

        pagina = 1

        for pagina in range(1, 538):

            print('Fotografias - Importando a página ' + str(pagina) + '...')

            search = self.urlHome + 'fotografias.php?pesq=1&tema=&local=&Ano_ini=&descricao=&palavra_chave=&topografico=&Reset2=Pesquisar&pagina=' + str(pagina)
            html = requests.get(search)
            html.encoding = 'utf-8'
            htmlString = html.text

            self.lineOfResults_FOTOGRAFIA(htmlString)

        df = self.listJsonToString()

        writer = pd.ExcelWriter("fotografias.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name = 'fotografias', index=False)
        writer.save() 

        print('Fotografias.php importado!')

    def postaPesquisaCartas(self):
        pagina = 1

        for pagina in range(1, 150):

            print('Cartas de chamada - Importando a página ' + str(pagina) + '...')

            search = self.urlHome + 'cartas.php?pesq=1&AssuntoPrincipal=&Titulo=&Origem=&Descricao=&Ano_Ini=&Ano_Fim=&pagina=' + str(pagina)
            html = requests.get(search)
            html.encoding = 'utf-8'
            htmlString = html.text

            self.lineOfResults_CARTAS(htmlString)

        df = self.listJsonToString()

        writer = pd.ExcelWriter("cartas.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name = 'Cartas chamada', index=False)
        writer.save() 

        print('cartas.php importado!')

    def __del__(self):
        pass