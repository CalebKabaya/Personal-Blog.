from flask import Flask
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy

from config import config_options
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_login import LoginManager
from flask_mail import Mail



bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()



photos = UploadSet('photos',IMAGES)
def create_app(config_name):

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://unngmhyxqdcpof:cf5aba91662b39adcd3d243dc7f6f6d4181e015991b461884663213d86fea0f1@ec2-54-86-224-85.compute-1.amazonaws.com:5432/d4gb8tg40m1mie'

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    # # configure UploadSet
    configure_uploads(app,photos)
    
    # # Registering the blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
      # setting config
    # from .requests import configure_request
    # configure_request(app)
  
  
    return app




