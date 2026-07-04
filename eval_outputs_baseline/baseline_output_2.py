from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/read_file', methods=['POST'])
def read_file():
    file_path = request.form['file_path']
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents