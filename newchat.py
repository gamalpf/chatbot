{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f406dfb",
   "metadata": {},
   "outputs": [],
   "source": [
    "import nltk\n",
    "import json\n",
    "import random\n",
    "import numpy as np\n",
    "from tensorflow.keras.models import Sequential\n",
    "from tensorflow.keras.layers import Dense, Dropout\n",
    "from tensorflow.keras.optimizers import SGD\n",
    "from tensorflow.keras.models import load_model\n",
    "\n",
    "import nltk\n",
    "from nltk.stem import PorterStemmer\n",
    "\n",
    "# Descargar los datos necesarios de NLTK\n",
    "nltk.download('punkt')\n",
    "\n",
    "# Crear el objeto stemmer\n",
    "stemmer = PorterStemmer()\n",
    "\n",
    "# Leer el archivo intents.json\n",
    "with open('intents.json') as file:\n",
    "    data = json.load(file)\n",
    "\n",
    "# Inicializar las listas necesarias\n",
    "words = []\n",
    "labels = []\n",
    "docs_x = []\n",
    "docs_y = []\n",
    "\n",
    "\n",
    "# Recorrer los patrones en el archivo JSON\n",
    "for intent in data['intents']:\n",
    "    for pattern in intent['patterns']:\n",
    "        # Tokenizar las palabras\n",
    "        wrds = nltk.word_tokenize(pattern)\n",
    "        words.extend(wrds)\n",
    "        # Agregar los patrones y las etiquetas correspondientes\n",
    "        docs_x.append(wrds)\n",
    "        docs_y.append(intent['tag'])\n",
    "\n",
    "    # Agregar las etiquetas a la lista\n",
    "    if intent['tag'] not in labels:\n",
    "        labels.append(intent['tag'])\n",
    "\n",
    "# Eliminar duplicados y ordenar la lista de palabras\n",
    "words = sorted(list(set([stemmer.stem(w.lower()) for w in words])))\n",
    "\n",
    "# Ordenar la lista de etiquetas\n",
    "labels = sorted(labels)\n",
    "\n",
    "# Crear una matriz de entrada para el modelo\n",
    "training = []\n",
    "output = []\n",
    "out_empty = [0] * len(labels)\n",
    "\n",
    "for idx, doc in enumerate(docs_x):\n",
    "    # Crear una bolsa de palabras para cada patrón\n",
    "    bag = []\n",
    "    wrds = [stemmer.stem(w.lower()) for w in doc]\n",
    "\n",
    "    for w in words:\n",
    "        if w in wrds:\n",
    "            bag.append(1)\n",
    "        else:\n",
    "            bag.append(0)\n",
    "\n",
    "    # Crear una matriz de salida con la etiqueta correspondiente\n",
    "    output_row = out_empty[:]\n",
    "    output_row[labels.index(docs_y[idx])] = 1\n",
    "\n",
    "    training.append(bag)\n",
    "    output.append(output_row)\n",
    "\n",
    "# Convertir las listas en arrays de Numpy\n",
    "training = np.array(training)\n",
    "output = np.array(output)\n",
    "\n",
    "\n",
    "# Definir el modelo de la red neuronal\n",
    "model = Sequential()\n",
    "model.add(Dense(128, input_shape=(len(training[0]),), activation='relu'))\n",
    "model.add(Dropout(0.5))\n",
    "model.add(Dense(64, activation='relu'))\n",
    "model.add(Dropout(0.5))\n",
    "model.add(Dense(32, activation='relu'))\n",
    "model.add(Dropout(0.5))\n",
    "model.add(Dense(len(output[0]), activation='softmax'))\n",
    "# Compilar y entrenar el modelo\n",
    "model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True), metrics=['accuracy'])\n",
    "model.fit(training, output, epochs=200, batch_size=5, verbose=1)\n",
    "\n",
    "# Guardar el modelo\n",
    "model.save('chatbot_model.h5')\n",
    "\n",
    "# Cargar el modelo\n",
    "model = load_model('chatbot_model.h5')\n",
    "\n",
    "# Función para procesar las entradas de usuario y generar respuestas\n",
    "def process_input(user_input):\n",
    "    # Tokenizar y stemmizar la entrada del usuario\n",
    "    user_words = nltk.word_tokenize(user_input)\n",
    "    user_words = [stemmer.stem(word.lower()) for word in user_words]\n",
    "\n",
    "    # Crear una bolsa de palabras para la entrada del usuario\n",
    "    user_bag = [0] * len(words)\n",
    "    for word in user_words:\n",
    "        for i, w in enumerate(words):\n",
    "            if w == word:\n",
    "                user_bag[i] = 1\n",
    "\n",
    "    # Hacer una predicción con el modelo\n",
    "    prediction = model.predict(np.array([user_bag]))[0]\n",
    "    predicted_label = labels[np.argmax(prediction)]\n",
    "\n",
    "    # Seleccionar una respuesta aleatoria de las respuestas correspondientes a la etiqueta predicha\n",
    "    response = random.choice([intent['responses'] for intent in data['intents'] if intent['tag'] == predicted_label][0])\n",
    "\n",
    "    return response\n",
    "\n",
    "# Función para interactuar con el usuario\n",
    "def chat():\n",
    "    print(\"¡Bienvenido al chatbot! Escribe 'salir' para terminar.\")\n",
    "    while True:\n",
    "        user_input = input(\"Tú: \")\n",
    "        if user_input.lower() == \"salir\":\n",
    "            break\n",
    "\n",
    "        response = process_input(user_input)\n",
    "        print(\"Chatbot:\", response)\n",
    "\n",
    "# Iniciar el chatbot\n",
    "chat()\n",
    "\n",
    "\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
