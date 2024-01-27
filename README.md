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
### Instalar los requirements.txt
```
pip install -r requirements.txt
```

## Chrome Extension installation
- Descargar la carpeta chrome extension
- Ver el siguiente video para instalarlo localmente: https://youtu.be/IG0J_ynkemI?t=1433
