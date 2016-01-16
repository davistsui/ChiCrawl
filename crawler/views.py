from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django import forms
from datetime import datetime
from django.db import models
from search import main
import sys
import csv
import os
import json

'''
build_dropdown function is referenced from PA2 views.py written by Gustav
The form class and validation class are written with help from Django
online documentation at https://docs.djangoproject.com/en/1.7/ref/forms/api/
'''


NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

# Files for dropdown menu and neighborhood center coordinates
NEIGHBOR_FILE = os.path.join(RES_DIR, 'neighborhood.csv')
NEIGHBOR_COOR = os.path.join(RES_DIR, 'neighbor_coord.json')

# Load list of neighborhoods from the file
def load_column(filename):
    with open(filename) as f:
        col = []
        for row in csv.reader(f):
            col.append(row[0])
    return col

# Cite pa2 django function written by Gustav
def build_dropdown(options):
    #Converts a list to (value, label) tuples for <option> tag
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

# Variables to be passed in dropdown menu and checkbox values
NEIGHBOR = build_dropdown([None] + load_column(NEIGHBOR_FILE))
PRICE = ((1, '$'), (2, '$$'),
         (3, '$$$'), (4, '$$$$'))

# Returns a list of lat/lon pair from the neighborhood json file
def get_origin_coord(filename, key):
    with open(filename) as f:
        data = json.load(f)
    lat = data[key]['location']['latitude']
    lon = data[key]['location']['longitude']
    return [lat, lon]

# Create your views here.
# Form validatations
class ChicagoNeighbor(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.ChoiceField(label='Neighborhood', choices=NEIGHBOR, required=False))
        super(ChicagoNeighbor, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, values):
        if len(values) == 2:
            if values[0] is None or not values[1]:
                raise forms.ValidationError("Must specify both.")
            if values[0] < 0:
                raise forms.ValidationError("Distance must be non-negative.")
        return values

def validate_num_bars(value):
    if value > 6:
        raise forms.ValidationError("Too late! Go back home!")

# Create the form
class SearchForm(forms.Form):
    search = forms.CharField(required=False)
    num_bars = forms.IntegerField(required=True, validators=[validate_num_bars])
    prices = forms.MultipleChoiceField(required=False,
                                       widget=forms.CheckboxSelectMultiple,
                                       choices=PRICE)
    neighborhood = ChicagoNeighbor(
           help_text='e.g. 2 miles within Hyde Park',
           required=False,
           widget=forms.widgets.MultiWidget(
                    widgets=(forms.widgets.NumberInput,
                             forms.widgets.Select(choices=NEIGHBOR))))
   
# Home function returns a rendered dictionary containing results from search
def home(request):
    c = {}
    coord = []
    num = 5
    query = None # our query function (from a python file)
    if request.method == 'GET':
        form = SearchForm(request.GET)
        # Check if it's valid
        if form.is_valid():
            # convert form data to an args dictiionary
            args = {}
            if form.cleaned_data['search']:
                args['terms'] = form.cleaned_data['search']
            if form.cleaned_data['num_bars']:
                args['num_bars'] = form.cleaned_data['num_bars']
                num = args['num_bars']
            if form.cleaned_data['prices']:
                args['price'] = form.cleaned_data['prices']
                args['price'] = int(args['price'][0])
            neighbor = form.cleaned_data['neighborhood']
            if neighbor:
                args['distance'] = neighbor[0]
                args['neighbor'] = neighbor[1]
                coord = get_origin_coord(NEIGHBOR_COOR, args['neighbor'])
           
            if len(coord) == 0:
                query = None 
            else:
                query = main(args, coord[0], coord[1])
    else:
        form = SearchForm()
    if query is None:
        c['result'] = None
    else:
        # list of tuples [(name, lon, lat, weight, distance),..]
        if len(query) < num:
            num = len(query)
        result = query[:num]
        c['result'] = result
        # parameters for starting location/js
        c['origin_lat'] = coord[0]
        c['origin_lon'] = coord[1]
        # parameters for directions
        c['lat_list'] = get_lat(result, num)
        c['lon_list'] = get_lon(result, num) 
        c['name_list'] = mark_safe(get_names(result, num))
    
    c['form'] = form

    return render(request, 'index.html', c)

# Functions for creating list of bar nameslat/lon
# to be rendered to base.html/index.html
def get_lon(result, n):
    lon = []
    for i in range(n):
        lon.append(result[i][1])
    return lon

def get_lat(result, n):
    lat = []
    for i in range(n):
        lat.append(result[i][2])
    return lat

def get_names(result, n):
    name = []
    for i in range(n):
        name.append(str(result[i][0]))
    return name



