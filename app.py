import os
import subprocess
import uuid
import io
from flask import Flask, request, jsonify, send_file, send_from_directory, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'wmv', 'flv', 'm4v'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    fps = request.form.get('fps', '10')
    width = request.form.get('width', '480')
    start_time = request.form.get('start_time', '0')
    duration = request.form.get('duration', '')

    try:
        fps = max(1, min(30, int(fps)))
        width = int(width)
        float(start_time)
        if duration:
            float(duration)
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400

    uid = uuid.uuid4().hex
    original_name = secure_filename(file.filename)
    base_name = os.path.splitext(original_name)[0]
    input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{original_name}")
    palette_path = os.path.join(UPLOAD_FOLDER, f"{uid}_palette.png")
    output_path = os.path.join(UPLOAD_FOLDER, f"{uid}_output.gif")

    file.save(input_path)

    try:
        time_args = ['-ss', str(start_time)]
        if duration:
            time_args += ['-t', str(duration)]

        vf_palette = f"fps={fps},scale={width}:-1:flags=lanczos,palettegen=stats_mode=diff"
        palette_cmd = ['ffmpeg', '-y'] + time_args + [
            '-i', input_path,
            '-vf', vf_palette,
            palette_path
        ]
        result = subprocess.run(palette_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return jsonify({'error': f'Palette generation failed: {result.stderr[-500:]}'}), 500

        vf_gif = f"fps={fps},scale={width}:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
        gif_cmd = ['ffmpeg', '-y'] + time_args + [
            '-i', input_path,
            '-i', palette_path,
            '-lavfi', vf_gif,
            output_path
        ]
        result = subprocess.run(gif_cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return jsonify({'error': f'GIF conversion failed: {result.stderr[-500:]}'}), 500

        with open(output_path, 'rb') as f:
            gif_data = f.read()

        size_mb = round(len(gif_data) / (1024 * 1024), 2)
        output_filename = f"{base_name}.gif"

        response = make_response(send_file(
            io.BytesIO(gif_data),
            mimetype='image/gif',
            as_attachment=False,
            download_name=output_filename
        ))
        response.headers['X-File-Size-MB'] = str(size_mb)
        response.headers['X-File-Name'] = output_filename
        response.headers['Access-Control-Expose-Headers'] = 'X-File-Size-MB, X-File-Name'
        return response

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Conversion timed out (300s limit)'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        for f in [input_path, palette_path, output_path]:
            try:
                os.remove(f)
            except:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
