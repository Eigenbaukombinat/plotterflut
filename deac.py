import axi
import time
from flask import Flask, render_template, request, make_response
from flask_api import status
import json
import gocept.cache.method


d = axi.Device()
d.pen_up()
d.disable_motors()
