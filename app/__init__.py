from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KYZX234'
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"

#app.config['SQLALCHEMY_DATABASE_URI'] =  "postgresql://project1:testpass@localhost/formdatabase"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rrzkfijmhwpzxa:40a1f26aa7a8da35d1f89892156589da23b0435ac8e48741a906620c427dfd2a@ec2-54-243-210-70.compute-1.amazonaws.com:5432/decagt77j353d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)



from app import views