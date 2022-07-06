'''
This the main app to run pySAMS as flask webapp
template language is Jinja2
'''


from flask import Flask
from database.pysamsdb import *  # this is the already instantiated MyDatabase object connecting the the AMS DB

__version__ = '2021-April-15'
__author__ = 'Ronny Friedrich'

# set logger name to the name of the module
logger.name = __name__

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
