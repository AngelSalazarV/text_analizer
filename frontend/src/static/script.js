document.getElementById('analyzeButton').addEventListener('click', function() {
  const inputText = document.getElementById('inputText').value;
  console.log('inputText:', inputText)

  fetch('/analyze', {
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
      }
  })
  .catch(error => {
      document.getElementById('outputText').textContent = 'Error: ' + error;
  });
});