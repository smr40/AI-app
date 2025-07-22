import os
import uuid
from flask import Flask, render_template, request, send_from_directory
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    text = request.form['text']
    image = request.files['image']

    # Save uploaded image
    img_filename = f"{uuid.uuid4()}.jpg"
    img_path = os.path.join(UPLOAD_FOLDER, img_filename)
    image.save(img_path)

    # Generate audio from text
    tts = gTTS(text=text, lang='en')
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    tts.save(audio_path)

    # Create video from image + audio
    video_filename = f"{uuid.uuid4()}.mp4"
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)

    img_clip = ImageClip(img_path).set_duration(AudioFileClip(audio_path).duration)
    img_clip = img_clip.set_audio(AudioFileClip(audio_path))
    img_clip.write_videofile(video_path, fps=24)

    return render_template("index.html", video_file=video_filename)

@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

