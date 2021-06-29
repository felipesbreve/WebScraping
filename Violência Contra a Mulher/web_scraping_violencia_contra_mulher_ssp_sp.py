import pandas as pd
import numpy as np
import urllib.request
import bs4

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://www.ssp.sp.gov.br/Estatistica/ViolenciaMulher.aspx"

html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

tables = []
crimes = []
capital = []
demacro = []
interior = []
total = []
data = []
mes = []
ano = []
ids_tabelas = []
periodo = []
tamanho = []

tabelas = soup.findAll('table')

for table in tabelas:
    ids_tabelas.append(table['id'])
    
texto = "Ocorrências Registradas no mês: Janeiro de 2018"
ini = soup('span', text = texto)

for i in ini:
    inicio = i

    
ids_tabelas = ids_tabelas[:(int(inicio.get('id').replace('conteudo_repPeriodo_lblPeriodo_', '')) - 1)]

for id in ids_tabelas:
    tables.append(soup.find('table', id = id))
    
    for table in tables:
        rows = table.findAll('tr')
        
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols if len(ele) > 0]
        if len(cols) > 0:
            data.append(cols)
            
for row in rows:
    a = row.find_all('td')
    a = [ele.text.strip() for ele in a if len(ele) > 0]
    if len(a) > 0:
            tamanho.append(a)
            
for i in data:
    crimes.append(i[0])
    capital.append(i[1])
    demacro.append(i[2])
    interior.append(i[3])
    total.append(i[4])
        
for id in range(len(ids_tabelas)):
    periodo.append(
        [soup.find(
            'span', id = 'conteudo_repPeriodo_lblPeriodo_' + str(id + 1)
        ).getText().split()[-3:]] * (len(tamanho))
    )
    
    
for i in periodo:
    for j in i:
        mes.append(j[0])
        ano.append(j[2])
    
df_dic = dict({
    'Crimes' : crimes,
    'Capital' : capital,
    'Demacro' : demacro,
    'Interior' : interior,
    'Total' : total,
    "Mês" : mes,
    "Ano" : ano
})


df = pd.DataFrame(df_dic)
df.to_csv('./data/violencia_contra_mulher_ssp_sp.csv', sep = ';', index = False, encoding = 'UTF-8')