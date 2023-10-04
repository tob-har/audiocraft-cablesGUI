from flask import Flask, jsonify, make_response, request, send_from_directory, url_for
from flask_cors import CORS
import os
from collections import OrderedDict

import createaudio  # Assuming createaudio.py is in the same directory and its logic can be executed by importing it

flask_createaudio = Flask(__name__)
CORS(flask_createaudio)

model_status = "not_loaded"


@flask_createaudio.before_first_request
def load_model():
    global model_status
    try:
        createaudio.model  # Accessing the model instance from your createaudio script.
        model_status = "loaded"
    except:
        model_status = "error_loading"


@flask_createaudio.route("/check_model_status", methods=['GET'])
def check_model_status():
    return jsonify({"status": model_status})


@flask_createaudio.route('/run-script', methods=['POST'])
def run_script():
    try:
        data = request.get_json()  # Get JSON data from the request
        
        model_name = data.get("model_name", 'facebook/musicgen-small')  # Use a default value if it's not provided
        descriptions = data.get("descriptions", [])  # Extract 'descriptions' from the data
        top_k = data.get("top_k", 250)
        top_p = data.get("top_p", 0)
        temperature = data.get("temperature", 1)
        cfg_coef = data.get("cfg_coef", 6.0)
        duration = data.get("duration", 2)

        generated_files = createaudio.run(
            model_name=model_name,
            descriptions=descriptions,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            cfg_coef=cfg_coef,
            duration=duration
        )
        
        # List all files in the output_cables directory
        valid_extensions = ['.mp3', '.wav']
        all_files = [f for f in os.listdir('output_cables') if os.path.isfile(os.path.join('output_cables', f)) and os.path.splitext(f)[1] in valid_extensions]

        server_url = request.url_root # Get the base URL of the current server

        
        response_data = OrderedDict([
            ("status", "success"),
            ("generated_files", generated_files),
            ("server_url", server_url),
            ("all_files", all_files)
        ])

        response = make_response(jsonify(response_data))
            
        
        # Add cache-control headers
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@flask_createaudio.route('/output_cables/<path:filename>')
def serve_file(filename):
    if filename.endswith('.json'):
        return send_from_directory('output_cables/json', filename)
    return send_from_directory('output_cables', filename)


@flask_createaudio.route('/serve_filename', methods=['GET'])
def serve_filename():
    try:
        valid_extensions = ['.mp3', '.wav']
        all_files = [f for f in os.listdir('output_cables') if os.path.isfile(os.path.join('output_cables', f)) and os.path.splitext(f)[1] in valid_extensions]
        
        return jsonify({"status": "success", "files": all_files})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



# let cables etc. allow to access files etc...
#cors = CORS(flask_createaudio, origins=["https://cables.gl", "https://dev.cables.gl", "https://sandbox.cables.gl", "http://localhost:8000"])
cors = CORS(flask_createaudio, resources={
    r"/run-script": {"origins": ["https://cables.gl", "https://dev.cables.gl", "https://sandbox.cables.gl", "http://localhost:8000"]},
    r"/serve_filename": {"origins": ["https://cables.gl", "https://dev.cables.gl", "https://sandbox.cables.gl", "http://localhost:8000"]},
    r"/check_model_status": {"origins": ["https://cables.gl", "https://dev.cables.gl", "https://sandbox.cables.gl", "http://localhost:8000"]},
    r"/output_cables/*": {"origins": ["https://cables.gl", "https://dev.cables.gl", "https://sandbox.cables.gl", "http://localhost:8000"]}
})


if __name__ == '__main__':
    flask_createaudio.run(debug=True, port=5001, use_reloader=False)  # Using 5001 as an example port