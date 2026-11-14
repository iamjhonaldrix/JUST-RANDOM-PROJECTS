from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1sberrg-super-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_roadmap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# 1. DATABASE MODELS
# ==========================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    challenges = db.relationship('Challenge', backref='category', lazy=True)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Integer, default=0)
    primer_text = db.Column(db.Text, nullable=False)
    flag = db.Column(db.String(255), nullable=False)
    arvin_debrief = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=10)
    
# ==========================================
# 2. AUTHENTICATION DECORATORS & ROUTES
# ==========================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        request.user_id = session['user_id']
        return f(*args, **kwargs)
    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Access keys do not match. Try again.", "error")
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash("Operative alias already in use.", "error")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. You may now establish a link.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash("Invalid alias or access key. Connection refused.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ==========================================
# 3. CORE PLATFORM ROUTES
# ==========================================

@app.route('/')
@login_required
def home():
    """Main dashboard showing only category cards."""
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


@app.route('/category/<slug>')
@login_required
def category_page(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    return render_template('category.html', category=category)


@app.route('/api/challenges/<int:challenge_id>/submit', methods=['POST'])
@login_required
def submit_flag(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)

    data = request.get_json(silent=True) or {}
    submitted = (data.get('flag') or '').strip()

    if submitted != challenge.flag:
        return jsonify(status='error', message='Invalid flag. Keep digging.')

    return jsonify(
        status='success',
        arvin_debrief=challenge.arvin_debrief
    )

# ==========================================
# 4. INITIALIZATION & SEEDER
# ==========================================

def seed_database():
    """Populates the database with all a1sberrg cybersecurity learning tracks if empty."""
    if Category.query.count() == 0:
        categories_data = [
            ("web", "Web Exploitation", "Examine client-side mechanics, intercept requests, and manipulate input to uncover hidden surface vulnerabilities."),
            ("crypto", "Cryptography", "Learn how ciphers, encoding schemes, and cryptographic weaknesses expose secret data."),
            ("forensics", "Digital Forensics", "Investigate digital evidence, recover deleted artifacts, and analyze system timelines."),
            ("stego", "Steganography", "Uncover hidden payloads, data, and secret messages concealed inside media files."),
            ("reverse_eng", "Reverse Engineering", "Deconstruct compiled binaries, analyze control flow, and extract hardcoded keys."),
            ("pwn", "Binary Exploitation", "Explore memory corruption, stack overflows, and control flow hijacking."),
            ("osint", "Open-Source Intelligence", "Gather actionable intelligence from public sources, metadata, and OSINT frameworks."),
            ("misc", "Miscellaneous", "Solve out-of-the-box puzzles, scripting challenges, and logic hurdles."),
        ]

        for slug, name, desc in categories_data:
            cat = Category(slug=slug, name=name, description=desc)
            db.session.add(cat)
        
        db.session.commit()

        # Add starting Level 0 Challenge for Web Exploitation
        web_cat = Category.query.filter_by(name="Web Exploitation").first()
        if web_cat:
            chal_0 = Challenge(
                category_id=web_cat.id,
                title="Level 0: The Web Surface",
                level=0,
                primer_text="Websites hide mechanics beneath their visual surface. Security analysts look underneath the hood to find weaknesses.",
                flag="a1sberrg{dev_tools_master}",
                arvin_debrief="Outstanding work! You've successfully navigated the surface tier of web inspection. Always remember: client-side checks can never replace server-side security.",
                points=10
            )
            db.session.add(chal_0)
            db.session.commit()

        print("Database seeded with all a1sberrg learning tracks.")
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', port=8000, debug=False)