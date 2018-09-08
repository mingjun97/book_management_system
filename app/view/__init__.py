from flask import Blueprint, render_template

view = Blueprint(__name__, 'view')

from .index import *