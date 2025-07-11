# -*- coding: utf-8 -*-

from Declare4Py.ProcessModels.DeclareModel import DeclareModel
from pm4py.objects.log.importer.xes.importer import apply as xes_importer
from Declare4Py.ProcessMiningTasks.ASPLogGeneration.asp_generator import AspGenerator
from pm4py.objects.conversion.log import converter as xes_converter
from pympler import asizeof
import random
import pandas as pd
import time

times = {'basic log': [], 'complete log': [], 'access log': []}
sizes = {'basic log': [], 'complete log': [], 'access log': []}
for i in range(30):
  start_time = time.time() 
  model_name = 'LogGeradorMP'
  model: DeclareModel = DeclareModel().parse_from_file('./Projeto/Modelo_Log_Sintetico_OFICIAL.decl')

  # Number of cases that have be generated
  num_of_cases = 2000

  # Minimum and maximum number of events a case can contain
  (num_min_events, num_max_events) = (20, 50)


  asp_gen: AspGenerator = AspGenerator(model, num_of_cases, num_min_events, num_max_events)
  asp_gen.run()

  asp_gen.to_xes(f'{model_name}.xes')
  end_time = time.time() 
  execution_time = end_time - start_time

  times['basic log'].append(execution_time)
  start_time = time.time() 
  # Carregar o arquivo XES
  log = xes_importer('./LogGeradorMP.xes')

  df = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
  print(f"Uso real de memória: {asizeof.asizeof(df) / (1024 * 1024):.2f} MB")
  sizes['basic log'].append(asizeof.asizeof(df) / (1024 * 1024))
  df.drop('case:label', axis=1, inplace=True)

  df['concept:name'].value_counts()

  equipes = {'e1': ['re1', 're2', 're3', 're4'],
  'e2': ['re2', 're4', 're5'],
  'e3': ['re5', 're6', 're7', 're8', 're9'],
  'e4': ['re7', 're10', 're11'],
  'e5': ['re12', 're13'],
  'e6': ['re1', 're2', 're14'],
  'e7': ['re7', 're10', 're11']}

  atividades = {
  'Manutencao de funcionalidade': [4, 8, 12, 16, 24],
  'Atualizacao de requisitos funcionais': [2, 4, 6, 8, 12, 16],
  'Construcao de funcionalidade': [4, 8, 12, 16, 24],
  'Documentacao de requisitos funcionais': [2, 4, 6, 8, 12, 16],
  'Contagem de ponto de funcao': [1, 2, 4, 8],
  'Gestao da demanda': [1, 2, 4, 8],
  'Planejamento de entrega': [1, 2, 4, 6],
  'Review da entrega': [1, 2, 4, 6],
  'Publicar solucao': [1, 2, 4, 6],
  'Elaborar caso de teste': [2, 4, 8, 12],
  'Executar teste': [1, 2, 4, 8],
  'Corrigir erro': [2, 4, 6, 8],
  }

  df['concept:team'] = ''
  df['concept:resource'] = ''
  df['concept:instance'] = 0


  for i in df['case:concept:name'].unique():
    equipe = random.choice(list(equipes.keys()))
    df.loc[df['case:concept:name'] == i, 'concept:team'] = equipe


  df.value_counts('concept:team')


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
      duracao = random.choice(atividades[row['concept:name']])
      timestamp_inicio = pd.to_datetime(row['time:timestamp'])
      timestamp_final = pd.to_datetime(row['time:timestamp']) + pd.Timedelta(hours=duracao)
      df.at[index, 'time:timestamp'] = timestamp_final
      df.loc[len(df)] = [timestamp_inicio, 'begin', row['concept:name'],	row['case:concept:name'], row['concept:team'],	recurso, id_instancia]
      id_instancia += 1


  df_ordenado = df.sort_values(['case:concept:name', 'concept:instance', 'lifecycle:transition'])
  print(f"Uso real de memória: {asizeof.asizeof(df_ordenado) / (1024 * 1024):.2f} MB")
  sizes['complete log'].append(asizeof.asizeof(df_ordenado) / (1024 * 1024))
  df_ordenado.drop('concept:team', axis=1, inplace=True)
  df_reindexed = df_ordenado.reset_index(drop=True)

  df_reindexed.to_csv('LogSinteticoProcessoOFICIAL.csv', sep=';', index=False)
  
  end_time = time.time() 
  execution_time = end_time - start_time

  times['complete log'].append(execution_time)

  start_time = time.time() 

  df_reindexed["time:timestamp"] = pd.to_datetime(df_reindexed["time:timestamp"])

  atividades_acesso = {
  'Manutencao de funcionalidade': {'Gestao':['c','r','U','d'], 'Codigo': ['r', 'U', 'd'], 'Requisito': ['r'], 'PF': [], 'Teste': ['r']},
  'Atualizacao de requisitos funcionais': {'Gestao':['c','r','U','d'], 'Codigo': ['r'], 'Requisito': ['r', 'U', 'd'], 'PF': [], 'Teste': ['r']},
  'Construcao de funcionalidade': {'Gestao':['c','r','U','d'], 'Codigo': ['C', 'r', 'u', 'd'], 'Requisito': ['r'], 'PF': [], 'Teste': ['r']},
  'Documentacao de requisitos funcionais': {'Gestao':['c','r','U','d'], 'Codigo': ['r'], 'Requisito': ['C', 'r', 'u', 'd'], 'PF': [], 'Teste': ['r']},
  'Contagem de ponto de funcao': {'Gestao':['c','r','U','d'], 'Codigo': ['r'], 'Requisito': ['r'], 'PF': ['C', 'r', 'u', 'd'], 'Teste': []},
  'Gestao da demanda': {'Gestao':['c','r','U','d'], 'Codigo': [], 'Requisito': [], 'PF': [], 'Teste': []},
  'Planejamento de entrega': {'Gestao':['c','r','U','d'], 'Codigo': [], 'Requisito': ['r'], 'PF': ['r'], 'Teste': ['r']},
  'Review da entrega': {'Gestao':['c','r','U','d'], 'Codigo': [], 'Requisito': ['r'], 'PF': [], 'Teste': ['r']},
  'Publicar solucao': {'Gestao':['c','r','U','d'], 'Codigo': [], 'Requisito': [], 'PF': [], 'Teste': []},
  'Elaborar caso de teste': {'Gestao':['c','r','U','d'], 'Codigo': ['r'], 'Requisito': ['r'], 'PF': [], 'Teste': ['C', 'r', 'u', 'd']},
  'Executar teste': {'Gestao':['c','r','U','d'], 'Codigo': ['r'], 'Requisito': ['r'], 'PF': [], 'Teste': ['r', 'u']},
  'Corrigir erro': {'Gestao':['c','r','U','d'], 'Codigo': ['c','r', 'U', 'd'], 'Requisito': ['r'], 'PF': [], 'Teste': ['r']},
  }

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

  print(f"Uso real de memória: {asizeof.asizeof(df_acesso) / (1024 * 1024):.2f} MB")
  sizes['access log'].append(asizeof.asizeof(df_acesso) / (1024 * 1024))
  df_acesso.to_csv('LogSinteticoAcessoOFICIAL.csv', sep=';', index=False)
  
  end_time = time.time() 
  execution_time = end_time - start_time

  times['access log'].append(execution_time)

with open("times.txt", "w") as file:  # "w" creates the file if it doesn't exist
    file.write(str(times))
    
with open("sizes.txt", "w") as file:  # "w" creates the file if it doesn't exist
    file.write(str(sizes))