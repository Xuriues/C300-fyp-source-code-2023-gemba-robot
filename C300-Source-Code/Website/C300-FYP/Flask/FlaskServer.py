from flask import Flask, Response, render_template, request, redirect, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import AIModelsFlask
import UtilityFunction


modelPPE = YOLO("weights\\ppe_weights\\best.pt")
modelBoxes = YOLO("weights\\boxes_weights\\best.pt")
modelMHE = YOLO("weights\\mhe_weights\\best.pt")

app = Flask(__name__)
CORS(app, resources={r"/flaskURL" : {"origins": "http://localhost//FYP-Toll:8080"}})

@app.route('/')
def index():
    data = request.args.get('data', '')
    return render_template('loadStreamVideo.html', data=data)

@app.route('/ppeModel')
def loadPPE():
    return Response(AIModelsFlask.Jordon_Model(modelPPE, "PPE"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/boxesModel')
def loadBoxes():
    return Response(AIModelsFlask.Jordon_Model(modelBoxes, "Boxes"), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mheModel')
def loadMHE():
    return Response(AIModelsFlask.Shaun_Model(modelMHE), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    if request.method == 'POST':
        data = request.get_json()
        prompt = data.get('inputText')
        print(prompt)
        ans = AIModelsFlask.chatbotAnswer(prompt)
        response = {"result": ans}
        UtilityFunction.generateSpeech(ans)
        return jsonify(response)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
