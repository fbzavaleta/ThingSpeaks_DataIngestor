from flask import Flask, request
import pandas as pd
import datetime
import json
import load_model
import numpy as np

app = Flask(__name__)

#carregando modelo
load = load_model.LoadLoad('finalized_model.sav')


def tratative(df, hrs_ago):
  df = df.drop(columns=['hrs_ago'])
  
  df['date_c'] = pd.to_datetime(df['date_create'])
  df['date_c'] = df['date_c'].map(datetime.datetime.toordinal)
  del df['date_create']
  df['time_float'].iloc[0] = df['time_float'].iloc[0] - hrs_ago
  return df

@app.route('/', methods=['GET'])
def get():
  return 'API previcao funcionando {}'.format(datetime.datetime.date())

@app.route("/predict", methods=['POST'])
def predict():
  try:
    params = request.get_json()        
    data = pd.io.json.json_normalize(params)    
    hrs_predict = data.iloc[0]['hrs_ago']    
    data = tratative(data, hrs_predict)
    
    pred = load.model.predict(data)     
    r_pred = pd.DataFrame(list(np.array(pred)), columns=['eTVOC', 'eCO2'])
    print(r_pred) 
    result = {}
    result['process'] = True
    result['msg'] = 'A predicao nas proximas {} horas a partir desses parametros (eTV0C: {}), (eC01: {})'.format(hrs_predict, r_pred['eTVOC'].iloc[0], r_pred['eCO2'].iloc[0])
    result['data'] = r_pred.to_json()
    
    return json.dumps(result, indent=1, ensure_ascii=False).encode('utf8'), 200
  except Exception as e:
    return 'Error: ' + str(e), 400

if __name__ == '__main__':
  #app.run(host='localhost', port=8080)
  app.run(host='0.0.0.0')
  print('Rodando...')