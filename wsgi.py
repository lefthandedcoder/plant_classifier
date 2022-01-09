# import flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa

if __name__ == "__main__":
    application.run()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
