window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('voiceSynthesis');
  const span = document.getElementById('toSpeech');
  let currentVoice;

  const populateVoices = () => {
    const availableVoices = speechSynthesis.getVoices();
    currentVoice = availableVoices.filter(function (voice) { return voice.name == 'Microsoft Irina - Russian (Russia)'; })[0];
  };
  populateVoices();
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = populateVoices;
  }

  const readMessage = () => {
    const toSay = span.innerHTML.trim();
    const utterance = new SpeechSynthesisUtterance(toSay);
    utterance.voice = currentVoice;
    speechSynthesis.speak(utterance);
  };

  form.addEventListener('click', event => {
    event.preventDefault();
    readMessage();
  });

  setTimeout(() => {
    readMessage();
  });
});