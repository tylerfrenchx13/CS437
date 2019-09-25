# CS437

# ENVIRONMENT SETUP:
# Virtual Environment ("venv")
1. On your local machine, inside the CS437 directory, run the following command:
$ python -m venv	// creates the venv folder and need dependencies
2. If on Windows, run:
$ source venv/Scripts/activate
If on Linux, run:
$ . venv/bin/activate
// basically, you want to run the activate script

# Flask Installation
Run:
$ pip install Flask
$ pip install python-dotenv

## You're all done!
### "Help! I don't have the venv thing installed!"
Run:
$ pip install virtualenv

# How Flask Development Works:
### app/
All the good stuff you want to mess with is in there
### app/__init__.py
Initializes the Flask application
### app/routes.py
Provides that routes/endpoints at which the app is displayed.
### app/templates/
This directory has the HTML templates through which we'll show off our awesome work
### app/static/
This directory has the CSS for that HTML mentioned previously
### app/TextManager.py
This is the python class containing text processing functionality
### searchIR.py
Flask needs this to run
