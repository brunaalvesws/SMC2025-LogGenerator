# -*- coding: utf-8 -*-

from Declare4Py.ProcessModels.DeclareModel import DeclareModel
from pm4py.objects.log.importer.xes.importer import apply as xes_importer
from Declare4Py.ProcessMiningTasks.ASPLogGeneration.asp_generator import AspGenerator
from pm4py.objects.conversion.log import converter as xes_converter
from pympler import asizeof
import random
import pandas as pd
import time



model_name = 'LogGeradorMP'
model: DeclareModel = DeclareModel().parse_from_file('./GeradorLog/Declare_model_example.decl')

# Number of cases that have be generated
num_of_cases = 3

# Minimum and maximum number of events a case can contain
(num_min_events, num_max_events) = (20, 50)


asp_gen: AspGenerator = AspGenerator(model, num_of_cases, num_min_events, num_max_events)
asp_gen.run()

asp_gen.to_xes(f'{model_name}.xes')

# Carregar o arquivo XES
log = xes_importer('./LogGeradorMP.xes')

df = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
df.drop('case:label', axis=1, inplace=True)

df['concept:name'].value_counts()

## equipes ##
df_equipes = pd.read_csv('./GeradorLog/Resource_model_example.csv', sep=";")
equipes = df_equipes.to_dict(orient='list')

equipes = { 
    case: [r.strip() for r in recursos.split(',')]
    for case, recursos in zip(equipes['case:concept:name'], equipes['concept:resources'])
}

print(equipes)


df['concept:team'] = ''
df['concept:resource'] = ''
df['concept:instance'] = 0


for i in df['case:concept:name'].unique():
  equipe = random.choice(list(equipes.keys())) ##não deve existir 
  df.loc[df['case:concept:name'] == i, 'concept:team'] = equipe

print(df)

id_instancia = 1
demanda = ''

# Iterando pelas linhas do DataFrame com iterrows
for index, row in df.iterrows():
    if demanda == '':
        demanda = row['case:concept:name']
    if demanda != row['case:concept:name']:
        demanda = row['case:concept:name']
        id_instancia = 1
    equipe = row['concept:team']
    recurso = random.choice(equipes[equipe])
    df.at[index, 'concept:resource'] = recurso
    df.at[index, 'concept:instance'] = id_instancia
    timestamp_inicio = pd.to_datetime(row['time:timestamp'])
    timestamp_final = pd.to_datetime(row['time:timestamp']) + pd.Timedelta(hours=2)
    df.at[index, 'time:timestamp'] = timestamp_final
    df.loc[len(df)] = [timestamp_inicio, 'begin', row['concept:name'],	row['case:concept:name'], row['concept:team'],	recurso, id_instancia]
    id_instancia += 1


df_ordenado = df.sort_values(['case:concept:name', 'concept:instance', 'lifecycle:transition'])
df_ordenado.drop('concept:team', axis=1, inplace=True)
df_reindexed = df_ordenado.reset_index(drop=True)

df_reindexed.to_csv('LogSinteticoProcessoOFICIAL.csv', sep=';', index=False)

df_reindexed["time:timestamp"] = pd.to_datetime(df_reindexed["time:timestamp"])

## acessos ## 
df_atividade_acesso = pd.read_csv("./GeradorLog/Access_model_example.csv", sep=";")
atividades = list(df_atividade_acesso.columns[1:]) #nome das at. sem contar primeira coluna(Data Objetcs)
print(atividades)
funcoes = df_atividade_acesso["Data Objects"].tolist()
print(funcoes)

atividades_acesso = {}

for atividade in atividades:
    acesso_funcao = {}
    for i, funcao in enumerate(funcoes):
      valor = df_atividade_acesso.at[i,atividade]
      if pd.isna(valor):
          acesso = []
      else:
          acesso = [j.strip() for j in valor.split(',')]
      acesso_funcao[funcao] = acesso
      atividades_acesso[atividade] = acesso_funcao

print(atividades_acesso)

df_acesso = pd.DataFrame()
df_acesso['case:concept:name'] = 0
df_acesso['concept:dataobj'] = ''
df_acesso['concept:operation'] = ''
df_acesso['time:timestamp'] = 0
df_acesso['concept:resource'] = ''
df_acesso['concept:instance'] = ''

for index, row in df_reindexed.iterrows():
  if row['lifecycle:transition'] == 'begin':
    atv = row['concept:name']
    acc = atividades_acesso[atv]
    for key, value in acc.items():
      for op in value:
        random_timestamp = random.uniform(row['time:timestamp'], df_reindexed.at[index+1,'time:timestamp'])
        if op.isupper() or random.randint(1,10) % 2 == 0:
          ope = op.lower()
          df_acesso.loc[len(df_acesso)] = [row['case:concept:name'], key, ope, random_timestamp, row['concept:resource'], row['concept:instance']]

df_acesso['lifecycle:transition'] = 'complete'


df_acesso.to_csv('LogSinteticoAcessoOFICIAL.csv', sep=';', index=False)
