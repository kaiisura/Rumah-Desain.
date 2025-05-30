import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:  # Password should be hashed in production!
        login_user(user)
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = Question(name=data['name'], email=data['email'], question=data['question'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question received!'})

@app.route('/questions')
def get_questions():
    questions = Question.query.order_by(Question.id.desc()).all()
    return jsonify([
        {'name': q.name, 'email': q.email, 'question': q.question}
        for q in questions
    ])
@app.route("/konsultasi", methods=["GET", "POST"])
def konsultasi():
    if request.method == "POST":
        nama = request.form["nama"]
        pertanyaan = request.form["pertanyaan"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO konsultasi (nama, pertanyaan) VALUES (?, ?)", (nama, pertanyaan))
        conn.commit()
        conn.close()

        return render_template("berhasil.html", nama=nama)
    return render_template("konsultasi.html")
@app.route("/admin/users")
def daftar_user():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, username FROM user")
    users = c.fetchall()
    conn.close()
    return render_template("users.html", users=users)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
