from flask import Flask, render_template, request, jsonify
#from flask_cors import CORS
from chat import get_response

app = Flask(__name__)
application = app
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

@app.get("/")
def index_get():
    return render_template(("public/base_cpanel2.html"))

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)