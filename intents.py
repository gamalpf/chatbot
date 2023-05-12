from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

# Descargar los datos necesarios de NLTK
nltk.download('punkt')

# Crear el objeto stemmer
stemmer = PorterStemmer()

{
  "intents": [
    {
      "tag": "saludo",
      "patterns": ["Hola", "¡Hola!", "Buenos días"],
      "responses": ["¡Hola! ¿En qué puedo ayudarte?", "¡Hola! ¿Cómo puedo asistirte hoy?"]
    },
    {
      "tag": "despedida",
      "patterns": ["Adiós", "Hasta luego", "Nos vemos"],
      "responses": ["¡Hasta luego!", "¡Adiós! Espero haberte ayudado."]
    },
    {
      "tag": "agradecimiento",
      "patterns": ["Gracias", "Muchas gracias", "Te agradezco"],
      "responses": ["De nada", "¡De nada! Siempre estoy aquí para ayudar."]
    },
    {
      "tag": "informacion",
      "patterns": ["¿Cuál es tu nombre?", "¿Cómo te llamas?", "¿Quién eres?"],
      "responses": ["Soy un modelo de lenguaje desarrollado por OpenAI llamado ChatGPT."]
    },
    {
      "tag": "informacion",
      "patterns": ["¿Cuál es tu función?", "¿Para qué sirves?"],
      "responses": ["Mi función principal es responder preguntas y brindar información en diferentes temas."]
    },
    {
      "tag": "informacion",
      "patterns": ["¿Cuál es tu conocimiento actualizado?", "¿Cuándo te entrenaron?"],
      "responses": ["Fui entrenado con datos hasta septiembre de 2021, por lo que mi conocimiento se encuentra actualizado hasta esa fecha."]
    },
    {
      "tag": "informacion",
      "patterns": ["¿Cómo puedo contactarte?", "¿Cuál es tu contacto?"],
      "responses": ["No tengo un contacto directo, pero puedes hacerme preguntas aquí."]
    },
    {
      "tag": "ayuda",
      "patterns": ["Necesito ayuda", "¿Puedes ayudarme?", "Estoy perdido"],
      "responses": ["Claro, estaré encantado de ayudarte. ¿En qué puedo asistirte?"]
    },
    {
      "tag": "ayuda",
      "patterns": ["No entiendo", "No sé qué hacer", "¿Puedes explicarme?"],
      "responses": ["Por supuesto, puedo brindarte explicaciones y responder tus preguntas. ¿Qué necesitas saber?"]
    },
    {
      "tag": "desconocido",
      "patterns": ["*"],
      "responses": ["Lo siento, no entiendo. ¿Podrías reformular tu pregunta o consulta?"]
    }
  ]
}
