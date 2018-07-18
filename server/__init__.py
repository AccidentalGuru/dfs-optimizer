from flask import Flask

app = Flask(__name__)

from app import routes # at bottom as workaround for circular imports, a common problem with Flask apps
