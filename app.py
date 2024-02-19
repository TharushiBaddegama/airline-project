from flask import Flask, request, jsonify
import pickle
import json
import os

app = Flask(__name__)

# Load the trained model from the pickle file
file_path = os.path.join(os.path.dirname(__file__), 'airline_model.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

def process_data(data):
    for (key, value) in data.items():
        if type(value) == str:
            try:
                with open("category_columns.json", 'r') as f:
                    json_obj = json.load(f)

                if key in json_obj:
                    index = json_obj[key].index(value)
                    data[key] = index
                else:
                    data[key] = "Key not found in the JSON object"
            except ValueError:
                data[key] = 0

    return data

@app.route('/', methods=['POST'])
def get_predict():
    # Get the data from the request
    data = request.get_json()

    # Process data and replace strings with index values
    processed_data = process_data(data)

    # Perform prediction using the loaded model
    prediction = model.predict([list(processed_data.values())])

    #predicted
    if prediction[0] == 0:
        return "Plane will not be delayed"
    else:
        return "Plane will be delayed"