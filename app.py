from flask import Flask, render_template, request, redirect, send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'MLXH243rjBDIBibiBIbibIeffi43BBkkfbp15WS7FDhdwYF56wPj8'

db = SQLAlchemy(app)
class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(5000), nullable = True)
    video = db.Column(db.BLOB)
    
    def __init__(self, title, description, video):
        self.title = title
        self.description = description
        self.video = video

@app.route('/')
def index():
    videos = Videos.query.all()
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        video = request.files['videoUpload']
        title = request.form.get('videoTitle')
        description = request.form.get('videoDescription')
        newVideo = Videos(title=title, description=description, video=video.read())
        db.session.add(newVideo)
        db.session.commit()
        return redirect('/')
    return render_template('upload.html', videos=False)

@app.route('/playVideo/<int:id>')
def playVideo(id):
    video = Videos.query.get(id)
    if video:
        print(send_file(BytesIO(video.video), mimetype='video/mp4'))
        return send_file(BytesIO(video.video), mimetype='video/mp4')
        # return render_template('play.html', video=video)
    else:
        return "Video not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')