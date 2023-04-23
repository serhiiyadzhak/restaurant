# restaurant
The first thing to do is to clone the repository:

$ git clone https://github.com/serhiiyadzhak/restaurant.git

$ cd restaurant

Create a virtual environment to install dependencies in and activate it:

$ python -m venv venv

$ venv\Scripts\activate

Then install the dependencies:

(venv)$ cd restaurant

(venv)$ pip install -r requirements.txt

Note the (venv) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by venv.

Once pip has finished downloading the dependencies:

(venv)$ python manage.py runserver
