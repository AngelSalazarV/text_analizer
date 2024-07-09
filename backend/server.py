from flask import Flask, request, jsonify, render_template
import subprocess
import tempfile
import os

app = Flask(__name__, static_folder="../frontend/src/static", template_folder="../frontend/src/templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.json.get('inputText')
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_input:
        temp_input.write(input_text)
        temp_input.flush()
        temp_input_path = temp_input.name

    # Mantener el archivo de salida abierto para escribir durante la ejecución del proceso
    temp_output = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
    temp_output_path = temp_output.name
    temp_output.close()
    
    process = subprocess.Popen(
        ['analizador/lexer.exe'], 
        stdin=open(temp_input_path, 'r', encoding='utf-8'), 
        stdout=open(temp_output_path, 'w', encoding='utf-8'), 
        stderr=subprocess.PIPE, 
        text=True, 
        encoding='utf-8', 
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    stdout, stderr = process.communicate()
    
    os.remove(temp_input_path)
    
    if process.returncode != 0:
        return jsonify({'error': stderr}), 500

    with open(temp_output_path, 'r', encoding='utf-8') as temp_output:
        lexer_output = temp_output.read()

    os.remove(temp_output_path)
    
    # Parsear la salida del lexer para extraer las estadísticas
    output_lines = lexer_output.split('\n')
    output_text = []
    statistics = {
        'words': 0,
        'wordsWithTilde': 0,
        'characters': 0,
        'vowels': 0,
        'consonants': 0,
        'punctuations': 0
    }

    for line in output_lines:
        if line.startswith("PALABRA:") or line.startswith("PALABRA CON TILDE:") or line.startswith("OPERADOR:") or line.startswith("NUMERO:") or line.startswith("PUNTUACION:"):
            output_text.append(line)
        elif line.startswith("PALABRAS:"):
            statistics['words'] = int(line.split(':')[1].strip())
        elif line.startswith("PALABRAS CON TILDE:"):
            statistics['wordsWithTilde'] = int(line.split(':')[1].strip())
        elif line.startswith("CARACTERES:"):
            statistics['characters'] = int(line.split(':')[1].strip())
        elif line.startswith("VOCALES:"):
            statistics['vowels'] = int(line.split(':')[1].strip())
        elif line.startswith("CONSONANTES:"):
            statistics['consonants'] = int(line.split(':')[1].strip())
        elif line.startswith("PUNTUACIONES:"):
            statistics['punctuations'] = int(line.split(':')[1].strip())
    
    return jsonify({'output': '\n'.join(output_text), 'statistics': statistics})

if __name__ == '__main__':
    app.run(debug=True)