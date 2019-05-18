from classes import acervoLinks as ace

urlHome = 'http://www.inci.org.br/acervodigital/'

site = ace.acervoLinks()

site.postaPesquisaFotografias()
site.postaPesquisaCartas()

del site