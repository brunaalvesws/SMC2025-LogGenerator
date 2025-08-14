import zipfile
from flask import Flask, request, send_file  
from flask_cors import CORS  
import io
import csv
  
app = Flask(__name__)  
CORS(app)  
  
@app.route('/generate', methods=['POST'])  
def process_csvs():
    # Pegar os arquivos enviados
    declare = request.files.get('declare')
    org = request.files.get('organizational')
    access = request.files.get('access')
    activities_duration = request.form.get('activities')
    traces = request.args.get('traces')
    max_events = request.args.get('maxEvents')
    min_events = request.args.get('minEvents')
    print(max_events)
    print(activities_duration)
    print(traces)
    print(declare)
    print(org)

    # Aqui você faria o processamento real. Vamos simular resultado:
    process_log = "resultado_a,data\n1,abc\n2,def\n"
    access_log = "resultado_b,data\n10,xyz\n20,lmn\n"

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

