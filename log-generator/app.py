import zipfile
from flask import Flask, request, send_file  
from flask_cors import CORS  
import io
import csv
import LogGenerator
import tempfile
import json

  
app = Flask(__name__)  
CORS(app)  
  
@app.route('/generate', methods=['POST'])  
def process_csvs():
    # Pegar os arquivos enviados
    declare = request.files.get('declare')
    org = request.files.get('organizational')
    access = request.files.get('access')
    activities = request.form.get('activities')
    traces = request.args.get('traces')
    max_events = request.args.get('maxEvents')
    min_events = request.args.get('minEvents')
    
    resource_model = io.StringIO(org.stream.read().decode("utf-8"))
    access_model = io.StringIO(access.stream.read().decode("utf-8"))
    
    activities_duration = json.loads(activities)  
    activities_duration = {a["name"]: (a["min_duration"], a["max_duration"]) for a in activities_duration}
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".decl") as tmp_decl:
        decl_path = tmp_decl.name
        declare.save(tmp_decl)

    process_log, access_log = LogGenerator.generate(traces,min_events,max_events,activities_duration,decl_path,resource_model,access_model)

    # Gerar arquivos CSV em memória
    memory_zip = io.BytesIO()
    with zipfile.ZipFile(memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("process_log.xes", process_log)
        zf.writestr("access_log.xes", access_log)

    memory_zip.seek(0)
    return send_file(
        memory_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name='generated_logs.zip'
    )
  
if __name__ == '__main__':  
    app.run(port=5000)

