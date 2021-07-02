from flask import Flask, render_template, session
import pymysql
from flask import request
from flask import redirect

app = Flask(__name__)
# create a secret key used in encrypting the sessions
app.secret_key = "Wdg@#$%89jMfh2879mT"
connection = pymysql.connect(host='localhost', user='root', password='', database='Sierra')


@app.route("/")
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Items")
    rows = cursor.fetchall()
    return render_template('index.html', rows=rows)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  shopit_users WHERE email=%s AND password =%s", (email, password))
        if cursor.rowcount == 1:
            session['key'] = email
            return redirect('index.html')
        else:
            return render_template('login.html', msg="Failed to login, Please check your username and Password")
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO shopit_users(email,password,phone) VALUES(%s,%s,%s)", (email, password, phone))
            connection.commit()
        except:
            return render_template('register.html', msg1="Unable to create another account with {}".format(email))
        return render_template('register.html', msg1="Account Created Successfully")
    else:
        return render_template('register.html')


@app.route("/products")
def products():
    return "This will be products page"


@app.route('/single/<product_id>')
def single(product_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Items WHERE ProductID = %s", (product_id))
    product = cursor.fetchone()
    return render_template('single.html', product=product)


# logout
@app.route('/logout')
def logout():
    session.pop('key', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
