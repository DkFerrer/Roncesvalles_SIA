import os
from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "SECRET_KEY_RONCESVALLES22"
oauth = OAuth(app)

# Configure GitHub OAuth
github = oauth.register(
    name='github',
    client_id='Ov23liqbgdBpCAsAz5aJ',
    client_secret='f6f52c0aeec2aa332a694763fc99c14a952d9eb4',  
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Route: Home
@app.route('/')
def index():
    return '<a href="/login">Login with GitHub</a>'

# Login Route
@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

# Callback Route
@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()
    
    session['user'] = user
    return redirect('/profile')

# Protected Profile Route
@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401
    user = session['user']
    return jsonify(user)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)