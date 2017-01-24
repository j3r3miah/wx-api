from flask import render_template
from flask import Flask
import enum

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/foo')
def foo():
    return mkstr('jer')

def mkstr(name: str) -> str:
    return 'Hello {}'.format(name)
