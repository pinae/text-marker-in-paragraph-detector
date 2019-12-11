#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, send_file, send_from_directory, abort
from helpers import extract_pdf_page, compress_and_write_image
from PyPDF2 import PdfFileReader
from io import BytesIO
from os import path
import json
app = Flask(__name__)


@app.route('/<string:filename>', methods=['GET'])
def get_pdf_html_or_static(filename):
    if path.isfile(path.join("static", filename)):
        return send_from_directory("static", filename, as_attachment=True)
    if not path.isfile(path.join("dataset", "without_marker", filename)):
        return abort(400)
    pdf = PdfFileReader(open(path.join("dataset", "without_marker", filename), 'rb'))
    html = "<html><head><title>Rects for " + filename + "</title>"
    html += "<link rel=\"stylesheet\" href=\"style.css\" />"
    html += "<link rel=\"icon\" href=\"favicon.ico\" type=\"image/x-icon\" />"
    html += "<script type=\"application/javascript\" src=\"fabric.min.js\"></script>"
    html += "<script type=\"application/javascript\" src=\"rectDraw.js\"></script>"
    html += "</head><body>"
    saved_markers = {'rects': []}
    if path.isfile(path.join("dataset", "without_marker", filename.split('.')[0] + ".json")):
        with open(path.join("dataset", "without_marker", filename.split('.')[0] + ".json"), 'r') as json_file:
            saved_markers = json.load(json_file)
        if saved_markers['filename'] != filename:
            saved_markers = {'rects': []}
    for i in range(pdf.numPages):
        html += "<div>"
        html += "<canvas id=\"c_" + str(i) + "\"></canvas>"
        html += "<img src=\"" + filename + "/" + str(i) + "\" />"
        if len(saved_markers['rects']) > i:
            html += str(saved_markers['rects'][i])
        html += "</div>"
    html += "</body></html>"
    return html


@app.route('/<string:filename>/<int:page_no>', methods=['GET', 'POST'])
def get_pdf_img(filename, page_no):
    page_arr = extract_pdf_page(path.join('dataset', 'without_marker', filename), page_no)
    mem_file = BytesIO()
    compress_and_write_image(page_arr, mem_file)
    mem_file.seek(0)
    return send_file(mem_file, mimetype='image/jpeg',
                     as_attachment=True,
                     attachment_filename='%s.jpg' % filename.split('.')[0])
