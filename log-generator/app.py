from flask import Flask, request, send_file  
from flask_cors import CORS  
import io
import csv
  
app = Flask(__name__)  
CORS(app)  
  
@app.route('/generate', methods=['POST'])  
def run_script():  
    data = request.json or []

    # Gera o CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nome', 'Idade'])  # Cabeçalhos
    for item in data:
        writer.writerow([item.get('nome'), item.get('idade')])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='resultado.csv'
    )  
  
if __name__ == '__main__':  
    app.run(port=5000)