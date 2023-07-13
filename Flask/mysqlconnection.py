from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'book_rec'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        subject = request.form['subject']
    
        cursor = mysql.connection.cursor()
        condition = "subject = %s"
        cursor.execute("SELECT * FROM books WHERE " + condition, (subject,))
        books = cursor.fetchall()
        cursor.close()
    
        return render_template("profile.html", books=books, subject=subject)
    
    return "Method not allowed"


@app.route('/add_book')
def add_data():
    return render_template('add_data.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        subject = request.form.get('subject')
        name = request.form.get('name')
        author = request.form.get('author')
        link = request.form.get('link')

        # Perform the database operation to insert the book data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO books (subject, `Name of the Book`, Author, `Amazon Link`) VALUES (%s, %s, %s, %s)"
        values = (subject, name, author, link)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        
        return render_template('form.html')
   
    return "Method not allowed"


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
