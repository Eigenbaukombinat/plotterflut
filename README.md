# plotterflut

Plotterflut known from diVOC 2020


## Requirements

* Axidraw v3 Plotter
* Python 3

## Installation

```bash
git checkout https://github.com/Eigenbaukombinat/plotterflut
cd plotterflut
python3 -m venv .
git checkout https://github.com/fogleman/axi
bin/pip install axi/
bin/pip install -r requirements.txt
```

## Running

Create an empty new drawing:

```bash
touch drawing
```

Connect your Axidraw v3 and run:

```bash
FLASK_APP=flut.py bin/flask run 
```

Now you can use the provided API. See web/index.html for instructions.

To start a new drawing, simply delete or move the current "drawing" file, and create a new empty one (no need to stop the process, as the file is changed and read on every request).

## Webinterface

Expose the web-Directory and access via a browser. Maybe you have to change URLs to your API in some of the files.


## Examples

See the provided draw_it.py to draw png files, or check out https://github.com/n-st/plotterflut-client for a simple shell script. With the golang script at https://gitlab.spline.inf.fu-berlin.de/jrt/goplot you can plot png files and qr codes.
