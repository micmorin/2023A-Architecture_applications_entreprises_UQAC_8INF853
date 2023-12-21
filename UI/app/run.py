from flask import Flask
import app_init
import routes

if __name__ == "__main__":

    app = Flask(__name__)

    app_init.init_app(app)

    app.register_blueprint(routes.main)
    
    app.run(host='0.0.0.0',port=5000)

    