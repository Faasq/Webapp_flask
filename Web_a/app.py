from flask import Flask, render_template, request, redirect, url_for
import couchdb

app = Flask(__name__)

COUCHDB_SERVERS = {
    'db1': {'url': 'http://admin:password@couchdb1:5984', 'db': 'usernames'},
    'db2': {'url': 'http://admin:password@couchdb2:5984', 'dbs': ['usernames', 'games']},
    'db3': {'url': 'http://admin:password@couchdb3:5984', 'dbs': ['usernames', 'movies']}
}

def connect_to_db(server_url, db_name):
    couch = couchdb.Server(server_url)
    try:
        db = couch[db_name]
    except:
        db = couch.create(db_name)
    return db

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        db = connect_to_db(COUCHDB_SERVERS['db1']['url'], 'usernames')
        db.save({'first_name': first_name, 'last_name': last_name})
        
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        favorite_game = request.form['favorite_game']
        db = connect_to_db(COUCHDB_SERVERS['db2']['url'], 'games')
        db.save({'favorite_game': favorite_game})
        
        return redirect(url_for('movie'))
    return render_template('game.html')

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        favorite_movie = request.form['favorite_movie']
        db = connect_to_db(COUCHDB_SERVERS['db3']['url'], 'movies')
        db.save({'favorite_movie': favorite_movie})
        
        return "Thank you for submitting your information!"
    return render_template('movie.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)