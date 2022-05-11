const microphoneIcon = document.querySelector('.microphone__image');

function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
      var recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'ru-RU';
      recognition.start();

      recognition.onresult = function (e) {
        document.getElementById('transcript').value = e.results[0][0].transcript;
        recognition.stop();
        document.getElementById('voiceAssistant').submit();
      };
      recognition.onerror = function (e) {
        recognition.stop();
      };
    }
  }

microphoneIcon.onclick = function() {
    startDictation();
  console.log('Ready to receive a command.');
};