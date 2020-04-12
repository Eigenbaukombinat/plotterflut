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

Connect your Axidraw v3 and run:

```bash
FLASK_APP=flut.py bin/flask run 
```

Now you can use the provided API. See web/index.html for instructions.


## Webinterface

Expose the web-Directory and access via a browser. Maybe you have to change URLs to your API in some of the files.