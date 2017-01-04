from flask import Flask, render_template, session, redirect, request, url_for
from twitter_utilities import get_request_token, get_oauth_verifier_url, get_access_token
from database import Database
from user import User

app = Flask(__name__)
app.secret_key = '1234'

Database.initialize(user='postgres', password='admin', host='localhost', database='learning')

@app.route('/')
def homepage():
	return render_template('home.html')

@app.route('/login/twitter')
def twitterLogin():
	request_token = get_request_token()
	session['request_token'] = request_token

	return redirect(get_oauth_verifier_url(request_token))

@app.route('/auth/twitter')
def twitter_auth():
	oauth_verifier = request.args.get('oauth_verifier')
	access_token = get_access_token(session['request_token'], oauth_verifier)

	user = User.load_from_db_by_screen_name(access_token['screen_name'])
	if not user:
		user = User(access_token['screen_name'], access_token['oauth_token'],
					access_token['oauth_token_secret'], None)
		user.save_to_db()

	session['screen_name'] = user.screen_name

	return redirect(url_for('profile'))

@app.route('/profile')
def profile():
	return render_template('profile.html', screen_name=session['screen_name'])



app.run(port=5000, debug=True)
