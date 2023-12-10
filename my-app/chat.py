import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from controllers.funciones_home import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

#funcion donde ponemos un mensaje y luego recibimos una respuesta:
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    if '' in msg:
        nombre_libro = msg.split('buscar libro')[-1].strip()  # Extrae el nombre del libro del mensaje
        resultado_busqueda = buscarLibrobot(nombre_libro)
        if resultado_busqueda:
            return f"Encontré estos libros: {resultado_busqueda}"
        #else:
         #   return f"No encontré ningún libro con el nombre {nombre_libro}"
    return "Disculpa, no entiendo..."



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

