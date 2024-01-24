chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'getActiveTab') {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
      sendResponse(tabs[0]);
    });
    return true; // Esto es necesario para hacer la respuesta asincrónica
  }
});