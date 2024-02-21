import os
import datetime
import statistics

from flask import Flask, request, jsonify, send_file


app = Flask(__name__)


FILES_FOLDER = 'files_folder'
if not os.path.exists(FILES_FOLDER):
    os.makedirs(FILES_FOLDER)

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_BYTES


@app.route('/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file.content_length > MAX_FILE_SIZE_BYTES:
        return jsonify({'error': f'File size exceeds the maximum allowed limit of {MAX_FILE_SIZE_BYTES} bytes'})
    
    filename = os.path.join(FILES_FOLDER, file.filename)
    file.save(filename)
    
    file_info = {
        'name': file.filename,
        'type': file.content_type,
        'size_bytes': os.path.getsize(filename),
        'datetime_uploaded': datetime.datetime.now().isoformat()
    }
    
    return jsonify({'message': f'File {file.filename} uploaded successfully', 'file_info': file_info})

@app.route('/file/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(FILES_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'})
    
@app.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(FILES_FOLDER, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({'message': f'File {filename} deleted successfully'})
    else:
        return jsonify({'error': 'File not found'})

@app.route('/file', methods=['GET'])
def list_files():
    files = os.listdir(FILES_FOLDER)
    
    filter_type = request.args.get('type')
    if filter_type:
        files = [f for f in files if f.endswith(filter_type)]
        
    sort_by_size = request.args.get('sort_by_size')
    if sort_by_size == 'asc':
        files.sort(key=lambda f: os.path.getsize(os.path.join(FILES_FOLDER, f)))
    elif sort_by_size == 'desc':
        files.sort(key=lambda f: os.path.getsize(os.path.join(FILES_FOLDER, f)), reverse=True)
        
    file_info = []
    for filename in files:
        file_path = os.path.join(FILES_FOLDER, filename)
        file_info.append({
            'name': filename,
            'type': os.path.splitext(filename)[1],
            'size_bytes': os.path.getsize(file_path),
            'datetime_uploaded': datetime.datetime.fromtimestamp(
                os.path.getctime(file_path)
            ).isoformat()
        })
        
    return jsonify({'files': file_info})

@app.route('/file/statistics', methods=['GET'])
def file_statistics():
    files = os.listdir(FILES_FOLDER)
    
    sizes = [os.path.getsize(os.path.join(FILES_FOLDER, f)) for f in files]
    num_files = len(files)
    total_size_bytes = sum(sizes)
    avg_size_bytes = total_size_bytes / num_files
    median_size_bytes = statistics.median(sizes)
    
    return jsonify({
        'num_of_files': num_files,
        'total_size_bytes': total_size_bytes,
        'avg_size_bytes': int(avg_size_bytes),
        'median_size_bytes': int(median_size_bytes)
    })
    
if __name__ == '__main__':
    app.run(debug=True)
