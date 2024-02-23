from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    files_dir = '/home/krishkillr-admin/server/files'
    archive_dir = '/home/krishkillr-admin/server/archive'

    # List files in directories
    files_list = os.listdir(files_dir)
    archive_list = os.listdir(archive_dir)

    return render_template('index.html', files=files_list, archives=archive_list)

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory('/home/krishkillr-admin/server/files', filename)

@app.route('/archive/<filename>')
def serve_archive(filename):
    return send_from_directory('/home/krishkillr-admin/server/archive', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
