document.getElementById('analyzeButton').addEventListener('click', function() {
  const inputText = document.getElementById('inputText').value;

  fetch('analyze', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ inputText })
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          document.getElementById('outputText').textContent = 'Error: ' + data.error;
      } else {
          document.getElementById('outputText').textContent = data.output;

          // Actualizar las estadísticas
          document.getElementById('words').textContent = data.statistics.words;
          document.getElementById('words-tilde').textContent = data.statistics.wordsWithTilde;
          document.getElementById('characters').textContent = data.statistics.characters;
          document.getElementById('vowels').textContent = data.statistics.vowels;
          document.getElementById('consonants').textContent = data.statistics.consonants;
          document.getElementById('puntuations').textContent = data.statistics.punctuations;
      }
  })
  .catch(error => {
      document.getElementById('outputText').textContent = 'Error: ' + error;
  });
});
