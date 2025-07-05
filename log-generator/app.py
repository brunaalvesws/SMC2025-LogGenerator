from flask import Flask, request, jsonify  
from flask_cors import CORS  
  
app = Flask(__name__)  
CORS(app)  
  
@app.route('/generate', methods=['GET'])  
def run_script():  
    data = request.json  
    return jsonify({'received': data})  
  
if __name__ == '__main__':  
    app.run(port=5000)