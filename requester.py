import requests
import base64

# Hacer una solicitud GET a tu servidor Flask
response = requests.get('http://127.0.0.1:5000/summarize?url=m4-HM_sCvtQ')

# Imprime la respuesta para ver qué estás recibiendo
print(response.text)

# Obtener el audio del response
audio_base64 = response.json()['elevenlabs']  # Cambia 'response_elevenlabs' a 'elevenlabs'

# Convertir el audio a un archivo .mp3
audio = base64.b64decode(audio_base64)
with open('output.mp3', 'wb') as f:
    f.write(audio)

#Convertir el response gpt a un archivo de texto
with open('response.txt', 'w') as f:
    f.write(response.json()['gpt'])