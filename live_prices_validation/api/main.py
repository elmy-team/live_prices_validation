# from live_prices_validation.config import load_configuration
from live_prices_validation.api.routes import api
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)  # register the Blueprint
    return app

def main():
    # config = load_configuration()

    app = create_app()
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    main()