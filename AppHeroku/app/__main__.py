

from flask import Flask, request, jsonify
from app.utils import transform_audio
from app.cry_detection.createModel      import is_it_crying
from app.cry_classification.createModel import classification

from typing import BinaryIO


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav', 'ogg'}

def allowed_file(filename:str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.before_first_request
# class detectionmodel:
#     def __init__():
#         pass


@app.route('/', methods=["POST"])
def index():
    return "<h1> APPLICATION ON HEROKU IS RUNNING</h1>"

@app.route('/predict', methods=["POST"])
def predict():

    file:BinaryIO = request.files.get('file')

    if file is None or file.filename == "":
        return jsonify({"erorr": "NO FILE"})

    if not allowed_file(file.filename):
        return jsonify({"error": "FORMAT NOT SUPPORTED"})

    try:
        audio_bytes = file.read()

        spectrom = transform_audio(audio_bytes)

        outputs_detection = is_it_crying(spectrom)

        # labels = ["belly pain", "burping", "discomfort", "hungry", "tired"]
        # labels = ['Crying baby', 'Silence', 'Noise', 'Baby laugh']

        if(max(outputs_detection, key=outputs_detection.get) == "Crying baby"):

            outputs_classification = classification(spectrom)

        else:
            outputs_classification = None
        

        return jsonify({"output_detection"       : outputs_detection,
                        "outputs_classification" : outputs_classification})

    except BaseException as err:
        return jsonify({"error": str(err)+"\nERROR IN READ/TRASFORM/PREDICTION"})




if __name__ == '__main__':
    app.run(debug=True)
        
