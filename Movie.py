from flask import Flask, render_template, url_for, request, redirect, session
import mysql.connector
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'
my = mysql.connector.connect(host="localhost", user="root", passwd="Akash@2022", database='moviebooking')

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = my.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['email'] = email
            return redirect(url_for('book'))
        else:
            return redirect(url_for('loginfail'))
    else:
        return render_template('login.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST': 
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        error_message = "Passwords do not match"
        if password != confirmpassword:
            return render_template('register.html', error_message=error_message)
        else:
            cur = my.cursor()
            cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",(fname,lname,email,password))
            my.commit()
            cur.close()
            return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/loginfail')
def loginfail():
    return render_template('loginfail.html')

@app.route('/finalmessage.html')
def finalmessage():
    return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('logout.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/book", methods=["GET", "POST"])
def book():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        movie_name = request.form['movie']
        time = request.form['time']
        ticket_id = str(uuid.uuid4())
        cur = my.cursor(buffered=True)
        cur.execute("INSERT INTO movie_tickets (user_email, movie_name, time, ticket_id) "
            "VALUES (%s, %s, STR_TO_DATE(%s, '%h:%i %p'), %s)",
            (session['email'], movie_name, time, ticket_id))

        my.commit()
        cur.close()
        return render_template('finalmessage.html', ticket_id=ticket_id)
    else:
        return render_template("book.html")
if __name__=="__main__":
    app.run(debug=True)

