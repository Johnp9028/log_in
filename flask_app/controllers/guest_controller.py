from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.guest import Guest
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('welcome.html')



@app.route('/register',methods=['POST'])
def register():

    if not Guest.validate(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Guest.save(data)
    print(id)
    session['guest_id'] = id

    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'guest_id' not in session:
        return redirect('/logout')
    guest_data ={
        'id': session['guest_id']
    }
    print(guest_data)
    return render_template("dashboard.html",guest=Guest.get_by_id(guest_data))

@app.route('/login',methods=['POST'])
def login():
    print(request.form)
    
    guest = Guest.get_by_email(request.form)
    print(guest)
    if not guest:
        flash("Invalid Email","login")
        return redirect('/')

    if not bcrypt.check_password_hash(guest.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['guest_id'] = guest.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')