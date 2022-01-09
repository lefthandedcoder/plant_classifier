# import flask app but need to call it "application" for WSGI to work
from app import app
from app import create_app  # noqa

if __name__ == "__main__":
    app.run()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
