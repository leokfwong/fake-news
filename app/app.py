import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sklearn, pickle
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import coo_matrix, hstack

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
model = pickle.load(open('models/RF_model.pkl', 'rb'))
tfidf = pickle.load(open('models/tfidf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['term']
    category = request.form['category']
    print(term)
    print(category)
    
    data_file = "author_names" if category == "author" else "context_clean"
    print(data_file)
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json/", data_file + ".json")
    json_data = json.loads(open(json_url).read())
    print (json_data)
    print (json_data[0])
    
    print(term.lower())
    print(type(json_data))
    print([v for v in json_data])
    filtered_dict = [v for v in json_data if term.lower() in v.lower()] 
    #print(filtered_dict)
    
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp

@app.route('/predict', methods=['POST'])
def predict():

    features = [x for x in request.form.values()]
    quote = np.array([features[0]])
    print(quote)
    X_test =  coo_matrix(tfidf.transform(quote))

    prediction = model.predict(X_test)[0]

    prediction_labels = ['False', 'True']

    output = "PREDICTION!!!"

    return render_template('index.html', prediction_text=prediction_labels[prediction], quote_text=quote[0])

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)