from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pins.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

# Главная страница
@app.route('/')
def index():
    pins = Pin.query.order_by(Pin.id.desc()).all()
    return render_template('index.html', pins=pins)

# Страница добавления нового пина
@app.route('/add', methods=['GET', 'POST'])
def add_pin():
    if request.method == 'POST':
        title = request.form['title']
        image_url = request.form['image_url']
        description = request.form['description']
        new_pin = Pin(title=title, image_url=image_url, description=description)
        db.session.add(new_pin)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pin.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
