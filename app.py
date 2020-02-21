from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration with MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating the model for our CRUD Database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# There is where we define the routes
# We also program to query data

@app.route('/')
def index():

    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)



#This is the route for inserting Data to the database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('index'))
    
    else:
        print(flash("Something Went Wrong. Please Try Again"))


#This is where we update the employee data
@app.route('/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        flash("Employee Updated Successfully")
        return redirect(url_for('index'))


# this is route for deleting our employee
@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))



        

    


if __name__=='__main__':
    app.run(debug=True)