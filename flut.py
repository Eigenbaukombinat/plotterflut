from flask import Flask, request
from flask_api import status
import axi
import gocept.cache.method
import json
import time


# do not change that, as this are the bounds of the plotter
MAX_STEPS_X, MAX_STEPS_Y = MAX_STEPS = (11, 8.5)

# configuration, should be the same aspect as the values above
MAX_GRID_X, MAX_GRID_Y = MAX_GRID = (104, 72)

# safetybelt
MAX_X = MAX_GRID_X-1
MAX_Y = MAX_GRID_Y-4

GRIDSIZE_X = MAX_STEPS_X / MAX_GRID_X
GRIDSIZE_Y = MAX_STEPS_Y / MAX_GRID_Y
blocked = False
path = []
d = None


def save_field(x,y,i):
	with open('drawing','a') as savefile:
		savefile.write(f"{x},{y},{i}\n")


def check_field(x,y):
	with open('drawing', 'r') as savefile:
		lines = savefile.readlines()

	koords = []
	for line in lines:
		kx,ky,i = line.split(',')
		koords.append((kx,ky))
	if (str(x),str(y)) in koords:
		return True
	return False


def pixel(intensity):
	intensity = intensity + 2
	stepping = 10/intensity
	path = []
	elem=0
	for x in range(intensity+1):
		elem+=1
		path.append(((x*stepping),10*(elem%2)))
	elem+=1
	for x in range(intensity+1):
		elem+=1
		path.append((10*(elem%2),(x*stepping)))
	return path

def steps_x(grid_x):
	return GRIDSIZE_X * grid_x


def steps_y(grid_y):
	return GRIDSIZE_Y * grid_y


def init():
	global d
	global path
	d = axi.Device(max_velocity=7, jog_max_velocity=11)
	d.pen_up()
	d.enable_motors()
	time.sleep(0.2)
	path.append((0, 0))
	d.disable_motors()


def goto_point_scaled(point, factor=1, deltax=0, deltay=0):
	global d
	global path
	x, y = point
	dx = (steps_x(x) / factor) + deltax
	dy = (steps_y(y) / factor) + deltay
	path.append((dx, dy))
	return (dx, dy)


def draw_in_position(intensity, pos):
	global d
	global path
	dx, dy = pos
	points = pixel(intensity)
	x,y = points.pop()
	last_point = goto_point_scaled((x,y), 10.0, dx, dy)
	d.run_path(path)
	d.wait()
	path = [last_point]
	d.pen_down()
	while points:
		x,y = points.pop()
		point = goto_point_scaled((x,y), 10.0, dx, dy)
	d.run_path(path)
	d.wait()
	d.pen_up()
	return point


def draw(data):
	global d
	global path
	global blocked
	try:
		x = data.get('x')
		y = data.get('y')
		intensity = int(data.get('intensity'))
		x = int(x)
		y = int(y)
		if x>MAX_X or y>MAX_Y:
			return False, f"x,y out of bounds. Maximum is {MAX_X},{MAX_Y}."
		if (intensity > 7) and (intensity != 23):
			return False, "Max intensity: 7"
		if x<0 or y<0 or intensity<0:
			return False, "Negative values are not allowed!"
	except (TypeError, ValueError):
		return False, "Parse error."
	if check_field(x,y):
		return False, "Field already drawn in this session."
	if blocked:
		return False, "Damn. Now plotter is blocked."

	blocked = True
	save_field(x,y,intensity)
	if intensity == 23:
		blocked = False
		return True, "Success"
	d.enable_motors()
	last_point = goto_point_scaled((x,y))
	d.run_path(path)
	d.wait()
	path=[last_point]
	dx, dy = last_point
	last_point = draw_in_position(intensity, (dx,dy))
	path=[last_point]
	#
	# uncomment the following for returning to home position 
	# after each point
	#
	#last_point = goto_point_scaled((x,y))
	#d.run_path(path)
	#d.wait()
	#path = [last_point]
	d.disable_motors()
	blocked = False
	return True, "Success"


# flask stuff


app = Flask("plotterflut")


def to_dict(args):
    outdict = {}
    for key, val in args.items():
        outdict[key] = val
    return outdict


@app.route('/plotterflut/api')
def index():
	global blocked
	if blocked:
		return "Plotter busy.", status.HTTP_409_CONFLICT
	data = to_dict(request.args)
	success, msg = draw(data)
	if success:
		return msg
	else:
		return msg, status.HTTP_402_PAYMENT_REQUIRED


@app.route('/plotterflut/home')
def home():
	global blocked
	global d
	global path
	if path == [(0,0)]:
		return "Already homed."
	if blocked:
		return "Plotter busy.", status.HTTP_409_CONFLICT
	blocked = True
	d.enable_motors()
	last_point = goto_point_scaled((0,0))
	d.run_path(path)
	d.wait()
	d.disable_motors()
	path=[last_point]
	blocked = False
	return "OK"


@gocept.cache.method.Memoize(5)
def load_data():
	with open('drawing', 'r') as savefile:
		lines = savefile.readlines()
	data = []
	for line in lines:
		x,y,i = line.split(',')
		data.append({"x":x,"y":y,"i":i.strip()})
	return json.dumps(data)


@app.route('/plotterflut/data')
def data():
	return load_data()


init()
