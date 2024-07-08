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
        temp_input_path = temp_input.name  # Guardar la ruta del archivo para usar después de cerrar el bloque with
    
    # Asegurarse de que el archivo se cierra antes de pasarlo a lexer.exe
    process = subprocess.Popen(['analizador/lexer.exe'], stdin=open(temp_input_path, 'r', encoding='utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', cwd=os.path.dirname(os.path.abspath(__file__)))
    stdout, stderr = process.communicate()
    
    # Eliminar el archivo temporal después de usarlo
    os.remove(temp_input_path)
    
    if process.returncode != 0:
        return jsonify({'error': stderr}), 500
    return jsonify({'output': stdout})

if __name__ == '__main__':
    app.run(debug=True)