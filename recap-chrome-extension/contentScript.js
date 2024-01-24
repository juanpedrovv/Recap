(() => {
  let recap_interface;
  let currentVideo = "";


  const newVideoLoaded = async () => {
    const bookmarkBtnExists = document.getElementsByClassName("summarize-btn")[0];

    if (!bookmarkBtnExists) {

      const summariseBtn = document.createElement("button");
      summariseBtn.id = "summarise";
      summariseBtn.type = "button";
      summariseBtn.innerText = "Summarise";
      summariseBtn.className = "ytp-summarize-btn " + "summarize-btn";
      
      const brElement = document.createElement("br");

      const outputElement = document.createElement("p");
      outputElement.id = "output";
      

      const checkElement = setInterval(() => {
        recap_interface = document.querySelector("#related.style-scope.ytd-watch-flexy");

        if (recap_interface) {
          console.log(recap_interface);

          recap_interface.insertBefore(outputElement, recap_interface.firstChild);
          recap_interface.insertBefore(brElement, recap_interface.firstChild);
          recap_interface.insertBefore(summariseBtn, recap_interface.firstChild);

          /* https://youtu.be/IG0J_ynkemI?t=992

          Se inserta en el YT DOM como si fuera:

          <button id="summarise" type="button" class="ytp-summarize-btn summarize-btn">Summarise</button>
          <br>
          <p id="output">Output</p>
          
          */

          summariseBtn.addEventListener("click", function(){
            summariseBtn.disabled = true;
            summariseBtn.innerText = "Summarising...";
            

            chrome.runtime.sendMessage({message: 'getActiveTab'}, function(response) {
              var url = response.url;

              //quiero only el video id de la url: https://www.youtube.com/watch?v=9AXP7tCI9PI
              var videoId = url.split("v=")[1];

              var xhr = new XMLHttpRequest();
              xhr.open("GET", "http://127.0.0.1:5000/summarize?url=" + videoId, true);
              xhr.onload = function(){
                var text = xhr.responseText;
            
                outputElement.innerText = text;
                
                summariseBtn.disabled = false;
                summariseBtn.innerText = "Summarise";
              }
              xhr.send();
            });
    

          });

          
          clearInterval(checkElement);
        }

        

      }, 1000); // Comprueba cada segundo
      
    }

  };

  chrome.runtime.onMessage.addListener((obj, sender, response) => {
    const { type, value, videoId } = obj;

    if (type === "NEW") {
      currentVideo = videoId;
      newVideoLoaded();
    }
  });

  newVideoLoaded();
})();