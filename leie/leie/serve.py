#!/usr/bin/env python3

"""
Run this with:

`FLASK_APP=serve.py flask run`
"""

import dateutil
import dicttoxml
from flask import Flask, make_response, request, Response, url_for
import math
import os
import simplejson as json
import sys
import subprocess

# Make sure we can load modules from this directory
sys.path.insert(0, os.path.dirname(__file__))

# Load my modules
import etl
import model

app = Flask("leie")

baseurl = ""

# Get a database connection, create db if needed
conn = model.LEIE("development", db_conf_file=os.path.join(etl.get_dbdir(), "dbconf.yml"))

def slurp(fname):
    """Read file named FNAME and return contents."""
    with open(fname) as fh:
        return fh.read()

@app.errorhandler(404)
def not_found(error):
        return make_response(json.dumps({'error': 'Not found'}), 404)

@app.route("/")
def home():
    return slurp("api.html")

@app.route("/exclusion", methods=["DELETE", "PATCH", "POST", "PUT"])
@app.route("/Exclusion", methods=["DELETE", "PATCH", "POST", "PUT"])
def method_not_allowed():
    return "", 405

def parse_param_date(param_date):
    """Try to parse the date. Return None if there's nothing there to parse."""
    if not param_date:
        return None
    return dateutil.parser.parse(param_date).date()

@app.route('/exclusion')
@app.route('/exclusion/<rowid>')
@app.route('/Exclusion')
@app.route('/Exclusion/<rowid>')
def get_exclusions(rowid=None):
    """Search the exclusions table and return rows.

    ROWID is the id of the exclusion record

    This function checks the http request parameter string for
    parameters whose names match fields in the exclusion table.  Anything
    specified there must be matched exactly by matching entries.

    Specify a PAGE param and (optionally) a PAGE_SIZE param to do
    paging.

    """
    # Handle parameters that apply to both single row and bundles
    params = {}
    filter = dict(busname=request.args.get('busname'),
                  firstname=request.args.get('firstname'),
                  lastname=request.args.get('lastname'),
                  npi=request.args.get('npi'),
                  rowid=rowid or request.args.get('rowid'), # rowid can come in as a param or part of the url
                  state=request.args.get('state'),
                  zip=request.args.get('zip'),
                  address=request.args.get('address'),
                  excltype=request.args.get('excltype'),
                  waiverstate=request.args.get('waiverstate'),
                  city=request.args.get('city'),
                  upin=request.args.get('upin'),
                  general=request.args.get('general'),
                  midname=request.args.get('midname'),
                  specialty=request.args.get('specialty'),
                  excldate=parse_param_date(request.args.get('excldate')),
                  waiverdate=parse_param_date(request.args.get('waiverdate')),
                  dob=parse_param_date(request.args.get('dob')),
                  reindate=parse_param_date(request.args.get('reindate')),
    )

    page = int(request.args.get('page') or 1) # default 1
    page_size = min(int(request.args.get('page_size') or 15), 100) # default 15, max 100
    params.update(dict(page=page, page_size=page_size, **filter))

    func_name = sys._getframe().f_code.co_name # get name of current function
    exclusions = [e.fhir() for e in conn.get_exclusions(limit=page_size, page=page, filter=filter, form="dict")]

    if rowid and len(exclusions) == 1:
        ret = exclusions[0]
        ret['link'] = [{"relation": "self", "url": baseurl + url_for(func_name, **params)}]
    else:

        # Make the paging stuff for the bundle
        num_pages = math.ceil(conn.count_exclusions() / page_size)
        ret = {
            "resourceType": "Bundle",
            "link": [
                {"relation": "self", "url": baseurl + url_for(func_name, **params)},
                {"relation": "first", "url": baseurl + url_for(func_name, **dict(params.items(), page=1))},
                {"relation": "previous", "url": baseurl + url_for(func_name, **dict(params.items(), page=max([page-1, 1])))},
                {"relation": "next", "url": baseurl + url_for(func_name, **dict(params.items(), page=min([page+1, num_pages])))},
                {"relation": "last", "url": baseurl + url_for(func_name, **dict(params.items(), page=num_pages))}
            ],
            "meta":{"tag":[]},
            "total":len(exclusions),
            "type":"searchset",
            "entry":[{"fullUrl":baseurl + url_for(func_name, rowid=e['id']),
                      "resource":e} for e in exclusions]
        }

        # If this is a subset, indicate that in the output
        if num_pages > 1:
            ret['meta']['tag'].append("SUBSETTED")

    if requested_mimetype() == 'json':
        return Response(
                json.dumps(ret, indent=2, sort_keys=True),
                mimetype='application/fhir+json'
        )
    else:
        return Response(
                dicttoxml.dicttoxml(ret),
                mimetype='application/fhir+xml'
        )

def requested_mimetype():
    """Check the '_format' query parameter and the 'Accept:' header (in that
    order) to determine whether to respond with JSON or XML."""

    allowed_mimetypes = [
        'application/xml',
        'application/fhir+xml',
        'application/xml+fhir',
        'text/xml',
        'application/json',
        'application/fhir+json',
        'application/json+fhir',
    ]
    allowed_format_types = allowed_mimetypes + ['json', 'xml']
    if request.args.get('_format') in allowed_format_types:
        best = request.args.get('_format')
    else:
        best = request.accept_mimetypes.best_match(allowed_mimetypes)

    if 'xml' in best:
        return 'xml'
    else:
        return 'json'

def build_docs():
    """Build documentation in the current directory."""
    # Doing this the old-fashioned way, instead of with 'with',
    # because we'll be renaming the file.
    output = open("api.html.tmp", "w")
    try:
        subprocess.run(["pandoc", "api.mdwn"], stdout=output)
        output.close()
        os.rename("api.html.tmp", "api.html")
    except FileNotFoundError as e:
        # 'pandoc' not installed, so warn and give up.
        output.close() # this never ran in the 'try', so do it here
        s = ""
        if os.path.exists("api.html"):
            s = "re"
        sys.stderr.write( 
            "WARNING: The 'pandoc' program was not available, so the\n")
        sys.stderr.write(
            "         'api.html' file has not been %sgenerated.\n" % s)
        sys.stderr.write(
            "         Install pandoc (https://pandoc.org/) to make\n")
        sys.stderr.write(
            "         this warning go away.\n")
    if os.path.exists("api.html.tmp"):
        os.remove("api.html.tmp")

if __name__ == "__main__":
    # See https://github.com/SolutionGuidance/cavetl/issues/12 about
    # whether we should be building docs at application launch time.
    build_docs()
    app.run()
