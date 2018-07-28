# Requires Python 2.x, flask and pywin32
from flask import Flask
import flask

import win32com.client
import pythoncom
import os, os.path, sys, time

# Flask (Web Server)
ws = Flask(__name__)


@ws.route("/")
def root_index():
    files = os.listdir('.')
    response = []
    for f in files:
        if os.path.isfile(f) and f.lower()[-4:] == '.psd':
            response.append("""
<a href="/%s">%s</a><br/>
""" % (f, f))
        elif os.path.isfile(f) and f.lower()[-4:] == '.png':
            response.append("""
<a href="/%s?raw=1">%s</a><br/>
""" % (f, f))
    return ''.join(response)


@ws.route("/<filename>", methods=['GET'])
def view_file(filename):
    response = []

    raw = flask.request.args.get('raw')
    if raw == '1':
        return flask.send_file(os.path.join(os.getcwd(), filename), mimetype='image/png')

    if len(filename) <= 4 or filename[-4:] != '.psd':
        return ''

    pythoncom.CoInitialize()
    psApp = win32com.client.Dispatch("Photoshop.Application")

    doc = psApp.Open(os.path.join(os.getcwd(), filename))
    layerCount = doc.ArtLayers.Count
    for i in range(0, layerCount):
        response.append("""Layer : %s<br/>
""" % (doc.ArtLayers[i].Name))
        if doc.ArtLayers[i].Kind == 2:
            response.append("""
- Text : %s
<form method="post" action="/%s/%d">
<input type="text" name="text" />
<input type="submit" />
</form>
<br/>
""" % (doc.ArtLayers[i].TextItem.Contents, filename, i))
    doc.Close(2)
    return ''.join(response)


@ws.route("/<filename>/<layer>", methods=['POST'])
def change_text(filename, layer):
    response = []

    pythoncom.CoInitialize()
    psApp = win32com.client.Dispatch("Photoshop.Application")

    layer = int(layer)
    doc = psApp.Open(os.path.join(os.getcwd(), filename))

    if doc.ArtLayers[layer].Kind == 2:
        doc.ArtLayers[layer].TextItem.Contents = flask.request.form['text']

        f1 = filename + time.strftime(".%Y%m%d_%H%M%S") + '.png'
        pngFilename = os.path.join(os.getcwd(), f1)
        options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        options.Format = 13  # PNG
        options.PNG8 = False  # Sets it to PNG-24 bit
        doc.Export(ExportIn=pngFilename, ExportAs=2, Options=options)

        doc.Close(2)

        response.append('<a href="/%s?raw=1">%s</a>' % (f1, f1))

    return ''.join(response)


if __name__ == "__main__":
    ws.run(host='0.0.0.0', debug=True)
