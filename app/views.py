"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os, uuid, time, psycopg2
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename

# Note: that when using Flask-WTF we need to import the Form Class that we created
# in forms.py
from forms import MyForm
from models import FormData

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
   
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    myform = MyForm()
    
    if request.method == 'POST':
        if myform.validate_on_submit():
        
            firstname = myform.firstname.data
            lastname = myform.lastname.data
            email = myform.email.data
            location = myform.location.data
            biography = myform.biography.data
            gender = myform.gender.data
            photo = myform.photo.data
           
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            userid = str(uuid.uuid4())
            created_on = format_date_joined()
            
            db = connect_db()
            cur = db.cursor()
            query = "insert into Profiles (firstname, lastname, email, location, biography, gender, photo, userid, created_on) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            data = (firstname, lastname, email, location, biography, gender, filename, userid, created_on)
            cur.execute(query, data)
            db.commit()

            flash('Profile successfully added!', 'success')
            return redirect(url_for("profiles"))

        flash_errors(myform)
    return render_template('profile.html', form=myform)
  

@app.route('/profiles')
def profiles():
    """Render the website's profiles page."""
    
    db = connect_db()
    cur = db.cursor()
    cur.execute('select photo, firstname, lastname, gender, location, userid from profiles')
    profiles = cur.fetchall()
    
    return render_template('profiles.html', profiles=profiles)    
    
@app.route('/profile/<userid>')
def profile_userid(userid):
    """Render the website's profile/<userid> page."""
    
    user = FormData.query.filter_by(userid=userid).first()
    #user = db.session.query.profiles.userid()

    return render_template('profile_user.html', user=user)
    

def format_date_joined():
    """format date"""
    dtime = time.strftime("%B %d, %Y")
    return dtime

def connect_db():
    return psycopg2.connect(host="localhost",database="formdatabase", user="project1", password="testpass") 


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8081")