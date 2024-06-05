
from flask import Flask, request, jsonify, make_response
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CO2_predict = joblib.load('GlobalTemp_Change.joblib')
print(type(CO2_predict))

@app.route('/co2_pred', methods=['POST', 'GET'])
def handle_data():
   try:

      if request.method == 'POST':
         jdata = request.json
         jdata_df = pd.DataFrame([jdata])
         
      elif request.method == 'GET':
         # Get parameters from query string
         params = ["Emissions"]
         jdata = {param : float (request.args.get(param , 0)) for param in params}
         jdata_df = pd.DataFrame([jdata])

      # Call predict on the model, reshape for single sample
      CO2_emission_prediction = CO2_predict.predict(jdata_df)
      CO2_emission_prediction = CO2_emission_prediction.tolist()

# Create response with CORS headers
      response = make_response(jsonify({'CO2_emission': CO2_emission_prediction[0]}))
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

      return response

   except Exception as e :
      response = make_response(jsonify({'error' : str(e)}), 400)

      return response

if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0', port=3000)


