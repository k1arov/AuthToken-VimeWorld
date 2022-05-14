from functools import wraps
from flask import Flask, redirect, render_template, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "dmkfsdkfmksdmkfrtmeskekrosrokolkers"

client = MongoClient("tyt connect k mongoclient")
db = client['Test']
sql = db['Test']

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')