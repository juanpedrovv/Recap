# Summary

## Chrome extension archivos importantes:
- manifest.json
- contentScript.js
- background.js
- styles.css

No he utilizado:
- popup.js
- popup.html
- popup.css

## Chrome extension NOTAS
- Por el momento la extension solo modifica la pag de YT para poner un boton "Summarize", al hacerle click llama al Backend y este devuelve el resumen de este video.
- La idea es que cuando el backend ya devuelva un response a la extension, este boton desaparezca y aparezca un panel con: los timestamps y el chatbot.
## App.py (backend)
- Lo he hecho en Flask por practicidad. Falta configurar el CORS.
- YouTube Transcript API: Recoge las trasncripciones de un video de YT (hechas por el mismo creador o generadas automaticamente)
- Por el momento el output que genera /summarize es solo el resumen del video.
  
![image](https://github.com/juanpedrovv/Summary/assets/83739305/3040577c-ac18-4e17-b280-a5ca42cf3843)

- La idea es que el backend devuelva responses con los timestamps y el resumen de lo que contienen:
  ![Untitled](https://github.com/juanpedrovv/Summary/assets/83739305/c3dcd828-aa38-49b3-a41d-13a6a47898d8)

- Ademas tenemos que hacer un backend para el chatbot
  ![Untitled](https://github.com/juanpedrovv/Summary/assets/83739305/a80c62f7-0852-4075-81c2-cb752e1810d8)
