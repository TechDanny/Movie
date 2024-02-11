from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')

mysql = MySQL(app)

@app.route('/')
def index():
    # Fetch movies from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()

    return render_template('index.html', movies=movies, title="Home")

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')

    # Fetch movies based on the search query from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies WHERE name LIKE %s", ('%' + search_query + '%',))
    search_result = cur.fetchall()
    cur.close()

    return render_template('search.html', search_result=search_result, query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
