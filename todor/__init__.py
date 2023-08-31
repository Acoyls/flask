from flask import Flask,render_template, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # extencion de base de datos

def create_app():
    
    app = Flask(__name__)

    #Configuracion de proyecto 
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    
    )
    #Connecion base de datos
    db.init_app(app)

    #Registro de blueprint
    from . import todo
    app.register_blueprint(todo.bp)
    
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
  
    with app.app_context():
        db.create_all()
    
    return app
    





