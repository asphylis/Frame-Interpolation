from flask import Flask, request, render_template, send_file
import runway
import os
from PIL import Image
import io

app = Flask(__name__)

# Connect to Runway ML model
runway_model_url = 'https://app.runwayml.com/video-tools/teams/Username/ai-tools/frame-interpolation'  # Replace with your Runway model URL
runway_api = runway.connect(runway_model_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blend', methods=['POST'])
def blend():
    image1 = request.files['image1']
    image2 = request.files['image2']

    image1_path = os.path.join('static', image1.filename)
    image2_path = os.path.join('static', image2.filename)

    image1.save(image1_path)
    image2.save(image2_path)

    # Prepare images for Runway ML
    image1_pil = Image.open(image1_path)
    image2_pil = Image.open(image2_path)

    image1_bytes = io.BytesIO()
    image2_bytes = io.BytesIO()
    image1_pil.save(image1_bytes, format='PNG')
    image2_pil.save(image2_bytes, format='PNG')

    # Send images to Runway ML
    inputs = {
        'image1': image1_bytes.getvalue(),
        'image2': image2_bytes.getvalue()
    }
    outputs = runway_api.query(inputs)

    blended_image = Image.open(io.BytesIO(outputs['blended_image']))

    blended_image_path = os.path.join('static', 'blended.png')
    blended_image.save(blended_image_path)

    return send_file(blended_image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)