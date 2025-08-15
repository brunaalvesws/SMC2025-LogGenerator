from Declare4Py.ProcessModels.DeclareModel import DeclareModel
from pm4py.objects.log.importer.xes.importer import apply as xes_importer
from Declare4Py.ProcessMiningTasks.ASPLogGeneration.asp_generator import AspGenerator
from pm4py.objects.conversion.log import converter as xes_converter
import random
import pandas as pd

def generate(cases, min_events, max_events, activities_duration, declare_model, resource_model, access_model):

  model_name = 'LogGeneratorMP'
  model: DeclareModel = DeclareModel().parse_from_file(declare_model)

  # Number of cases that have be generated
  num_of_cases = cases

  # Minimum and maximum number of events a case can contain
  num_min_events = min_events
  num_max_events = max_events


  asp_gen: AspGenerator = AspGenerator(model, int(num_of_cases), int(num_min_events), int(num_max_events))
  asp_gen.run()

  asp_gen.to_xes(f'{model_name}.xes')

  # Load XES file
  log = xes_importer(f'{model_name}.xes')

  df = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
  df.drop('case:label', axis=1, inplace=True)

  ## Resources ##
  df_resources= pd.read_csv(resource_model, sep=";")
  resources = df_resources.to_dict(orient='list')

  resources = { 
      case: [r.strip() for r in recursos.split(',')]
      for case, recursos in zip(resources['case:concept:name'], resources['concept:resources'])
  }

  df['concept:resource'] = ''
  df['concept:instance'] = 0
  
  def generates_activity_duration(act_name):
    min_dur, max_dur = activities_duration[act_name]
    return pd.Timedelta(hours=random.randint(min_dur, max_dur))
  
  def set_resource(case):
      resource_chosen = random.choice(resources[case])
      return resource_chosen
  
  unique_cases = set(df['case:concept:name'].unique())
  if unique_cases != resources.keys():
    raise KeyError('The cases to be generated must be specified on Resource model, take a look if the Resource model is following the name pattern or if the number of cases to be generated is in accordance with the cases specified on the model.')
  df['concept:resource'] = df['case:concept:name'].apply(set_resource)
  df['concept:instance'] = df.groupby('case:concept:name').cumcount() + 1
  df['timestamp_begin'] = pd.to_datetime(df['time:timestamp'])
  df['time:timestamp'] = df['time:timestamp'] + df['concept:name'].apply(generates_activity_duration)
  df_begin = df.copy()
  df_begin['time:timestamp'] = df_begin['timestamp_begin']
  df_begin['lifecycle:transition'] = 'begin'
  df = pd.concat([df, df_begin], ignore_index=True).drop(columns=['timestamp_begin'])


  df_sorted = df.sort_values(['case:concept:name', 'concept:instance', 'lifecycle:transition'])
  df_reindexed = df_sorted.reset_index(drop=True)

  df_reindexed["time:timestamp"] = pd.to_datetime(df_reindexed["time:timestamp"])

  ## Access ## 
  df_activity_access = pd.read_csv(access_model, sep=";")
  activities = list(df_activity_access.columns[1:]) #activities names without first column (Data Objetcs)
  data_objects = df_activity_access["Data Objects"].tolist()
  
  unique_cases = set(df_reindexed['concept:name'].unique())
  if unique_cases != activities:
    raise KeyError('There are specified activities on Declare model that were not in Access model, please take a look on the Access model to fix it')

  activities_access = {}

  for activity in activities:
      access_dtobj = {}
      for i, dtobj in enumerate(data_objects):
        value = df_activity_access.at[i,activity]
        if pd.isna(value):
            access = []
        else:
            access = [j.strip() for j in value.split(',')]
        access_dtobj[dtobj] = access
        activities_access[activity] = access_dtobj

  df_access = pd.DataFrame()
  df_access['case:concept:name'] = 0
  df_access['concept:dataobj'] = ''
  df_access['concept:operation'] = ''
  df_access['time:timestamp'] = 0
  df_access['concept:resource'] = ''
  df_access['concept:instance'] = ''

  for index, row in df_reindexed.iterrows():
    if row['lifecycle:transition'] == 'begin':
      atv = row['concept:name']
      acc = activities_access[atv]
      for key, value in acc.items():
        for op in value:
          random_timestamp = random.uniform(row['time:timestamp'], df_reindexed.at[index+1,'time:timestamp'])
          if op.isupper() or random.randint(1,10) % 2 == 0:
            ope = op.lower()
            df_access.loc[len(df_access)] = [row['case:concept:name'], key, ope, random_timestamp, row['concept:resource'], row['concept:instance']]

  df_access['lifecycle:transition'] = 'complete'
  
  process_log_str = df_reindexed.to_csv(index=False)
  access_log_str = df_access.to_csv(index=False)
  
  return process_log_str, access_log_str
