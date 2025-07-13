from flask import Flask, render_template, request, redirect, url_for, session
import random
import string
app = Flask(__name__)
app.secret_key = 'your_secret_key'  
users = {}            
url_map = {}           
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('home.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            return "User already exists", 400
        users[username] = password
        return redirect(url_for('signin'))
    return render_template('signup.html')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users.get(username) == password:
            session['user'] = username
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('signin.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))
@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user' not in session:
        return redirect(url_for('signin'))
    original_url = request.form.get('original_url')
    custom_code = request.form.get('custom_code', '').strip()
    if custom_code:
        if custom_code in url_map:
            return "Custom code already taken", 400
        short_code = custom_code
    else:
        short_code = generate_short_id()
        while short_code in url_map:
            short_code = generate_short_id()
    url_map[short_code] = original_url
    short_url = request.host_url + short_code
    return render_template('home.html', short_url=short_url)
@app.route('/<short_code>')
def redirect_short_url(short_code):
    original_url = url_map.get(short_code)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True,port=5001)


