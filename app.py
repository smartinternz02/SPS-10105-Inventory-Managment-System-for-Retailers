
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib


  
app = Flask(__name__)
  
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'vyWNKls464'
app.config['MYSQL_PASSWORD'] = 'K5BrW5S75H'
app.config['MYSQL_DB'] = 'vyWNKls464'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'c@gmail.com'
app.config['MAIL_PASSWORD'] = ' '
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mysql = MySQL(app)
from sendmail_g import sendmail

def notify_stock():
   
    print('***********Running Notify**************')
    if 'username' in session:
        print('***********Executing Notify************')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM stock;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()

        print('***********Executing Mail************')
        subject = 'Stock Shortage Notification: Invetory Management System'
        

        for item in items:
            if item[6] < item[8]:
                to_mail = [item[3]]
                print('To mail:', to_mail)
                message = f'Hi, Your stock {item[4]} with Iventory ID {item[0]} is below the reoder level. Please refill it as soon as possible to ignore the shortage of product in your shop. Stock Shortage Notification: Invetory Management System. For any query contact us at chandanam757@gmail.com. Thank you'
                sendmail(subject, message, to_mail)
                print('Mail has been sent.')
    else:
        print('*********Session is Empty**********')
    

@app.route('/')
def homer():
    notify_stock()
    return render_template('home.html')
    

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        mysql.connection.commit()
        user_data = cursor.fetchone()
        cursor.close()
        print (user_data)
        if user_data:
            session['loggedin'] = True
            session['id'] = user_data[0]
            userid=  user_data[0]
            session['username'] = user_data[1]
            msg = 'Logged in successfully !'
            
            
            subject = 'login: Invetory Management System'
            to_mail = [email]
            print('To mail:', to_mail)
            message = f'Hi,Thank you for Loging into inventory management system, you can now manage your retails easily and keep track of your goods. For any query contact us at chandanam757@gmail.com. Thank you'
            sendmail(subject, message, to_mail)
            print('Mail has been sent.')
            
            
            return render_template('dashboard.html', msg = msg)
    return render_template('login.html', msg = msg)
    

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user_data = cursor.fetchone()
        print(user_data)
        if user_data:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s, % s)', (username, email, phone, address, password))
            mysql.connection.commit()
            msg1 = 'You have successfully registered !'
            subject = 'Register: Invetory Management System'
            to_mail = [email]
            print('To mail:', to_mail)
            message = f'Hi,Thank you for Registering into inventory management system,you account has been successfully created. To manage your retails login with your username and password,. For any query contact us at chandanam757@gmail.com. Thank you'
            sendmail(subject, message, to_mail)
            print('Mail has been sent.')
            
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    
    
@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')
    
@app.route('/about')
def abt():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user_data = cursor.fetchone()
        print(user_data)
        if user_data:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO about VALUES (NULL, % s, % s, % s, % s, % s)', (username, email, subject, message))
            mysql.connection.commit()
            msg1 = 'Your message has been received !'
            
            
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('about.html', msg = msg)
     
         
     
    
    
    
@app.route('/contact')
def contact():
    
    return render_template('contact.html')    
    
    

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         orgname = request.form['orgname']
         email = request.form['email']
         proname = request.form['proname']
         description = request.form['description']
         quantity = request.form['quantity']
         price = request.form['price']
         reord = request.form['reord']
         
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT * FROM stock WHERE username = % s', (username, ))
         user_data = cursor.fetchone()
         
         notify_stock()
         print(user_data)
         if user_data:
            msg = 'You may enter the details'
            return render_template('apply.html', msg = msg)

         
         
         
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO stock VALUES (NULL, % s, % s, % s,% s, % s, % s, % s, %s)', (username, orgname, email, proname, description, quantity, price, reord ))
         mysql.connection.commit()
         msg = 'You have successfully added your stock !'
         session['loggedin'] = True
         TEXT = "Hello"
         
         
         
         
         
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('apply.html', msg = msg)
     
     
@app.route('/display')
def dis():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stock;')
    mysql.connection.commit()
    items = cursor.fetchall()
    cursor.close()
    notify_stock()
    return render_template('display.html', items=items)
    
    
    
@app.route('/updateitem/<int:id>')
def updateitem(id):
    # This function set the previous values in input box on update page
    id = id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stock WHERE id=%s', (id,))
    mysql.connection.commit()
    data = cursor.fetchone()
    cursor.close()
    mydata = {'id': data[0], 'username': data[1], 'proname': data[4], 'description': data[5],
              'quantity': data[6], 'price': data[7], 'reord': data[8]}
    notify_stock()
    return render_template('updateitem.html', data=mydata)


@app.route('/updateprod', methods=['GET', 'POST'])
def update():
    # This function perform the update
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        proname = request.form['proname']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        reord = request.form['reord']

        cursor = mysql.connection.cursor()
        cursor.execute('Update stock SET username=%s, proname=%s, description=%s, quantity=%s, price=%s, reord=%s WHERE id=%s',
                       (username, proname, description, quantity, price, reord, id))

        mysql.connection.commit()
        cursor.close()
        msg = 'Successfully updated!'

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM stock;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
        notify_stock()
        return render_template('display.html', msg=msg, items=items)    
    
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    # This function set id in input box of delete page
    id = id
    notify_stock()
    return render_template('deleteitem.html', id=id)
      
    
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM stock where id = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        notify_stock()
        msg = "You have successfully deleted the item."

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM stock;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
            
        return render_template('display.html', msg=msg, items=items)
        
        
        
@app.route('/cusdis')
def cusdis():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stock;')
    mysql.connection.commit()
    items = cursor.fetchall()
    cursor.close()
    notify_stock()
    return render_template('cusdis.html', items=items)        
        
        
@app.route('/buyitem/<int:id>')
def buyitem(id):
    # This function set the previous values in input box on update page
    id = id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stock WHERE id=%s', (id,))
    mysql.connection.commit()
    data = cursor.fetchone()
    cursor.close()
    mydata = {'id': data[0], 'username': data[1], 'orgname': data[2], 'proname': data[4], 'description': data[5],
              'quantity': data[6], 'price': data[7]}
    notify_stock()
    return render_template('buyitem.html', data=mydata)


@app.route('/buyprod', methods=['GET', 'POST'])
def buy():
    
    # This function perform the update
    if request.method == 'POST':
        
        id = request.form['id']
        proname = request.form['proname']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        quant = request.form['quant']
        new= int(quantity)- int(quant)
        cursor = mysql.connection.cursor()
        cursor.execute('Update stock SET proname=%s, description=%s, quantity=%s, price=%s WHERE id=%s',
                       ( proname, description, new, price, id))

        mysql.connection.commit()
        cursor.close()
        msg = 'Successfully updated!'

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM stock;')
        mysql.connection.commit()
        items = cursor.fetchall()
        cursor.close()
        notify_stock()
        return render_template('cusdis.html', msg=msg, items=items)          
            

   


@app.route('/logout')

def logout():
   
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')


    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 9000)