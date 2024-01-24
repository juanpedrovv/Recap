(() => {
  let recap_interface;
  let currentVideo = "";
  let outputElement = null; // Declare outputElement here

  const newVideoLoaded = async () => {
    const bookmarkBtnExists = document.getElementsByClassName("summarize-btn")[0];

    if (!bookmarkBtnExists) {

      const summariseBtn = document.createElement("button");
      summariseBtn.id = "summarise";
      summariseBtn.type = "button";
      summariseBtn.innerText = "Summarise";
      summariseBtn.className = "ytp-summarize-btn " + "summarize-btn";
      
      const brElement = document.createElement("br");

      outputElement = document.createElement("p"); // Initialize outputElement here
      outputElement.id = "output";
      outputElement.innerText = ""; // Reset the text of outputElement

      const checkElement = setInterval(() => {
        recap_interface = document.querySelector("#related.style-scope.ytd-watch-flexy");

        if (recap_interface) {
          console.log(recap_interface);

          recap_interface.insertBefore(outputElement, recap_interface.firstChild);
          recap_interface.insertBefore(brElement, recap_interface.firstChild);
          recap_interface.insertBefore(summariseBtn, recap_interface.firstChild);

          summariseBtn.addEventListener("click", function(){

            summariseBtn.disabled = true;
            summariseBtn.innerText = "Summarising...";
            

            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://127.0.0.1:5000/summarize?url=" + currentVideo, true);
            xhr.onload = function(){
              var text = xhr.responseText;

              outputElement.innerText = text;

              summariseBtn.disabled = false;
              summariseBtn.innerText = "Summarise";
            }
            xhr.send();

          });

          
          clearInterval(checkElement);
        }

        

      }, 1000); // Comprueba cada segundo
      
    } else if (outputElement) {
      outputElement.innerText = ""; // Reset the text of outputElement when a new video is loaded
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