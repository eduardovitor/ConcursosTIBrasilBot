from bs4 import BeautifulSoup
import requests
import validators

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
URL = "https://www.pciconcursos.com.br"
CARGOS_ANALISTA = ("Analista de Tecnologia", "Analista de Sistemas")
CARGOS_PROFESSOR = ("Professor de informática efetivo", "Professor de informática substituto")
CARGOS_TECNICO = ("Técnico de informática", "Técnico em informática")
CARGOS = CARGOS_ANALISTA + CARGOS_PROFESSOR + CARGOS_TECNICO
VAGAS_LINK_DIC =  {
   CARGOS[0]:"/cargos/analista-de-tecnologia-da-informacao",
   CARGOS[1]:"/cargos/analista-de-sistemas",
   CARGOS[2]:"/cargos/professor-de-informatica",
   CARGOS[3]:"/cargos/professor-substituto-informatica",
   CARGOS[4]:"/cargos/tecnico-de-informatica",
   CARGOS[5]:"/cargos/tecnico-em-informatica"
}

def scrapy_vagas(uri):
  scrapy_url = "{}{}".format(URL,uri)
  doc_html = requests.get(scrapy_url,headers=HEADERS)
  soup_html = BeautifulSoup(doc_html.content,'lxml')
  vagas_html = soup_html.find_all("ul",class_="link-d")
  dics_concursos = []
  for vaga in vagas_html:
        if vaga.li.a.text.isupper()==False:
          if validar_dados(vaga.li.a["href"],vaga.li.a.text):
            dic = {"concurso":vaga.li.a.text,"link":vaga.li.a["href"]}
            dics_concursos.append(dic)
  return dics_concursos if len(dics_concursos)>0 else "Não há vagas para este cargo disponíveis no momento"

def validar_dados(link,titulo):
    return validators.url(link) and len(titulo) > 0

def formatar_msg(dics_concursos):
  if isinstance(dics_concursos, str):
    return dics_concursos
  else:
    dic_tam = len(dics_concursos)
    i = 0
    dic_msg=[]
    while(i<dic_tam):
      dic_msg.append("{}\n\n{}\n\n".format(dics_concursos[i]['concurso'],dics_concursos[i]['link']))
      i+=1
    msg="".join(dic_msg)
  return msg
