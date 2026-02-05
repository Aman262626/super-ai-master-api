from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import g4f
import base64
import io
import PyPDF2
import tempfile
import os
import json

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'Super AI Master API - GPT/Claude/Gemini Mixed - Ready!' })

@app.route('/v1/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get('messages', [])
    model = data.get('model', g4f.models.gpt_4o)
    try:
        response = g4f.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=False
        )
        return jsonify({'choices': [{'message': {'role': 'assistant', 'content': response}}]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/v1/vision', methods=['POST'])
def vision():
    data = request.get_json()
    messages = data['messages']
    image_b64 = data.get('image_b64')
    if image_b64:
        img_url = f"data:image/jpeg;base64,{image_b64}"
        messages[-1]['content'] = [
            {'type': 'text', 'text': messages[-1]['content']},
            {'type': 'image_url', 'image_url': {'url': img_url}}
        ]
    model = g4f.models.gpt_4_vision_preview
    response = g4f.ChatCompletion.create(model=model, messages=messages)
    return jsonify({'choices': [{'message': {'content': response}}]})

@app.route('/v1/analyze_file', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    prompt = request.form.get('prompt', 'Analyze for study/learning.')
    if file.filename.lower().endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = '\n'.join([page.extract_text() or '' for page in pdf_reader.pages])[:8000]
        messages = [{'role': 'user', 'content': f'{prompt}\n\nText: {text}'}]
    else:
        img_data = base64.b64encode(file.read()).decode()
        messages = [{'role': 'user', 'content': [{'type': 'text', 'text': prompt}, {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{img_data}'}}]}]
    model = g4f.models.gpt_4o
    response = g4f.ChatCompletion.create(model=model, messages=messages)
    return jsonify({'analysis': response})

@app.route('/v1/study', methods=['POST'])
def study():
    data = request.get_json()
    content = data['content']
    mode = data.get('mode', 'summarize')
    prompt = f"Expert tutor: {mode.upper()}. Make interactive for learning. Content: {content}"
    response = g4f.ChatCompletion.create(model=g4f.models.claude_3_5_sonnet, messages=[{'role': 'user', 'content': prompt}])
    return jsonify({'study_output': response})

@app.route('/v1/notebook', methods=['POST'])
def notebook():
    prompt = request.json['prompt']
    full_prompt = f"Generate full Jupyter .ipynb JSON file code for: {prompt}. Export ready."
    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4o, messages=[{'role': 'user', 'content': full_prompt}])
    nb_path = 'notebook.ipynb'
    with open(nb_path, 'w') as f:
        f.write(response)
    return send_file(nb_path, as_attachment=True, download_name='ai_notebook.ipynb')

@app.route('/v1/slide', methods=['POST'])
def slide():
    prompt = request.json['prompt']
    full_prompt = f"Generate PPT slides in Markdown format (## Slide1, bullets). Topic: {prompt}"
    response = g4f.ChatCompletion.create(model=g4f.models.gemini_1_5_pro, messages=[{'role': 'user', 'content': full_prompt}])
    return jsonify({'slides': response})

@app.route('/v1/image_gen', methods=['POST'])
def image_gen():
    prompt = request.json['prompt']
    try:
        img_response = g4f.ImageGeneration.create(model=g4f.models.dalle3, prompt=prompt)
        img_b64 = base64.b64encode(img_response).decode()
        return jsonify({'image_b64': img_b64})
    except:
        return jsonify({'error': 'Image gen fallback to desc', 'desc': g4f.ChatCompletion.create(model=g4f.models.gpt_4o, messages=[{'role': 'user', 'content': f'Describe image for {prompt}'}])})

@app.route('/v1/desk', methods=['POST'])  # Assume dashboard/discord code gen

def desk():
    prompt = request.json['prompt']
    full_prompt = f"Generate code for AI desk/dashboard/discord bot: {prompt}. Flask/Streamlit ready."
    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4o, messages=[{'role': 'user', 'content': full_prompt}])
    return jsonify({'desk_code': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)