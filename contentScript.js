(() => {
  let recap_interface;
  let currentVideo = "";
  let outputElement = null; // Declare outputElement here
  let summariseBtn = null; // Declare summariseBtn here
  let outputParagraph = null; // Declare outputParagraph here
  let audioElement = null; // Declare audioElement here

  const newVideoLoaded = async () => {
    const bookmarkBtnExists = document.getElementsByClassName("summarize-btn")[0];

    if (!bookmarkBtnExists) {

      summariseBtn = document.createElement("button");
      summariseBtn.id = "summarise";
      summariseBtn.type = "button";
      summariseBtn.innerText = "Summarise";
      summariseBtn.className = "ytp-summarize-btn " + "summarize-btn";
      
      const brElement = document.createElement("br");

      outputElement = document.createElement("div"); // Initialize outputElement here
      outputElement.id = "output";
      outputElement.style.display = "none"; // Add this line to hide the div initially

      outputParagraph = document.createElement("p");
      outputParagraph.innerText = ""; // Reset the text of outputElement

      audioElement = document.createElement("audio"); // Create audio element
      audioElement.controls = true; // Add this line to show the audio controls

      outputElement.appendChild(outputParagraph);
      outputElement.appendChild(audioElement); // Append audio element to outputElement


      const checkElement = setInterval(() => {
        recap_interface = document.querySelector("#related.style-scope.ytd-watch-flexy");

        if (recap_interface) {
          console.log(recap_interface);

          recap_interface.insertBefore(outputElement, recap_interface.firstChild);
          recap_interface.insertBefore(brElement, recap_interface.firstChild);
          recap_interface.insertBefore(summariseBtn, recap_interface.firstChild);

          summariseBtn.addEventListener("click", function(){

            //El boton summarize no se puede volver a presionar hasta que termine de resumir
            summariseBtn.disabled = true;
            summariseBtn.innerText = "Summarising...";

            
            //Mandamos el request al servidor y esperamos la respuesta
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://127.0.0.1:5000/summarize?url=" + currentVideo, true);
            xhr.onload = function(){

              var response_summarized = JSON.parse(xhr.responseText);

              // Convertir el audio base64 a un Blob
              var audioData = atob(response_summarized.elevenlabs);
              var audioArray = new Uint8Array(audioData.length);
              for (var i = 0; i < audioData.length; i++) {
                audioArray[i] = audioData.charCodeAt(i);
              }
              var audioBlob = new Blob([audioArray], {type: 'audio/mpeg'});

              // Crear una URL de objeto para el Blob
              var audioUrl = URL.createObjectURL(audioBlob);

              // Establecer la URL del objeto como la fuente del elemento de audio
              audioElement.src = audioUrl;

              
              summariseBtn.style.display = "none"; //Ocultamos el boton de resumir
              summariseBtn.disabled = false;
              summariseBtn.innerText = "Summarise";

              outputElement.style.display = "block"; //Mostramos el div de output
              outputParagraph.innerText = "Aca esta tu resumen del video en formato audio:";
              

            }
            xhr.send();

          });

          
          clearInterval(checkElement);
        }

        

      }, 1000); // Comprueba cada segundo
      
    } else if (outputElement) {
      outputParagraph.innerText = ""; // Reset the text of outputElement when a new video is loaded
      outputElement.style.display = "none"; // Hide the outputElement
      summariseBtn.style.display = "block"; // Show the summariseBtn
      summariseBtn.disabled = false;
      summariseBtn.innerText = "Summarise";
    }

  };

  chrome.runtime.onMessage.addListener((obj, sender, response) => {
    const { type, value, videoId } = obj;

    if (type === "NEW") {
      currentVideo = videoId;
      newVideoLoaded();
    }
  });

})();