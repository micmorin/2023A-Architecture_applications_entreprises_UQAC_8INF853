from flask import Flask
import routes

if __name__ == "__main__":

    app = Flask(__name__)

    app.register_blueprint(routes.main)
    
    app.run(host='0.0.0.0',port=5000)

    