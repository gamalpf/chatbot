# chatbot
import nltk
import json
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model

import nltk
from nltk.stem import PorterStemmer

# Descargar los datos necesarios de NLTK
nltk.download('punkt')

# Crear el objeto stemmer
stemmer = PorterStemmer()

# Leer el archivo intents.json
with open('intents.json') as file:
    data = json.load(file)

# Inicializar las listas necesarias
words = []
labels = []
docs_x = []
docs_y = []


# Recorrer los patrones en el archivo JSON
for intent in data['intents']:
    for pattern in intent['patterns']:
        # Tokenizar las palabras
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        # Agregar los patrones y las etiquetas correspondientes
        docs_x.append(wrds)
        docs_y.append(intent['tag'])

    # Agregar las etiquetas a la lista
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

# Eliminar duplicados y ordenar la lista de palabras
words = sorted(list(set([stemmer.stem(w.lower()) for w in words])))

# Ordenar la lista de etiquetas
labels = sorted(labels)

# Crear una matriz de entrada para el modelo
training = []
output = []
out_empty = [0] * len(labels)

for idx, doc in enumerate(docs_x):
    # Crear una bolsa de palabras para cada patrón
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    # Crear una matriz de salida con la etiqueta correspondiente
    output_row = out_empty[:]
    output_row[labels.index(docs_y[idx])] = 1

    training.append(bag)
    output.append(output_row)

# Convertir las listas en arrays de Numpy
training = np.array(training)
output = np.array(output)


# Definir el modelo de la red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(len(training[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(output[0]), activation='softmax'))
# Compilar y entrenar el modelo
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True), metrics=['accuracy'])
model.fit(training, output, epochs=200, batch_size=5, verbose=1)

# Guardar el modelo
model.save('chatbot_model.h5')

# Cargar el modelo
model = load_model('chatbot_model.h5')

# Función para procesar las entradas de usuario y generar respuestas
def process_input(user_input):
    # Tokenizar y stemmizar la entrada del usuario
    user_words = nltk.word_tokenize(user_input)
    user_words = [stemmer.stem(word.lower()) for word in user_words]

    # Crear una bolsa de palabras para la entrada del usuario
    user_bag = [0] * len(words)
    for word in user_words:
        for i, w in enumerate(words):
            if w == word:
                user_bag[i] = 1

    # Hacer una predicción con el modelo
    prediction = model.predict(np.array([user_bag]))[0]
    predicted_label = labels[np.argmax(prediction)]

    # Seleccionar una respuesta aleatoria de las respuestas correspondientes a la etiqueta predicha
    response = random.choice([intent['responses'] for intent in data['intents'] if intent['tag'] == predicted_label][0])

    return response

# Función para interactuar con el usuario
def chat():
    print("¡Bienvenido al chatbot! Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break

        response = process_input(user_input)
        print("Chatbot:", response)

# Iniciar el chatbot
chat()


