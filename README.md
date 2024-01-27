# Recap

## Backend Installation

### Primeros pasos
- Entrar a la carpeta recap-backend
  ```
  cd recap-backend
  ```
- Crear venv utilzando python 3.10.9, y activarlo.

### Instalar pytorch
- https://pytorch.org/
- En mi caso es (ya que tengo GPU):
  ```
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```
- En caso de tener solo CPU, creo que seria asi:
  ```
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```
### Creacion de variables de entorno
- Entrar a la carpeta recap-backend
- Crear el archivo .env
- Dentro de .env colocar lo siguiente:
  ```
  OPENAI_API_KEY=
  ELEVEN_LABS_API_KEY=
  ```
- Acceder a Open AI y a Eleven Labs para conseguir el API Key.
- Rellenar el archivo .env de la siguiente forma: (Notese que no se estan utilizando "")
  ```
  OPENAI_API_KEY=ASDNJNJ25151DS51DW8DW
  ELEVEN_LABS_API_KEY=FFDCDCDC6694D944CD
  ```

### Instalar los requirements.txt
```
pip install -r requirements.txt
```

## Chrome Extension installation
- Descargar la carpeta recap-chrome-extension
- Ver el siguiente video para instalarlo localmente: https://youtu.be/IG0J_ynkemI?t=1433
