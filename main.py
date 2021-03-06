#! /usr/bin/python3
"""
web frontend for SQL Queries of a backend database
"""
from flask import Flask, render_template, request
from scan import scanner
from net_calc import nflbx
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    """
    example pulled from flask docs
    """
    return render_template('does_not_exsist.html'), 404


@app.route('/')
def index():
    """
    defines a page
    """
    return render_template('index.html')


@app.route("/scanner", methods=['get', 'post'])
def scan():
    """
    defines a page
    """
    if request.method == 'POST':
        try:
            target = request.form['target']
            s_port = int(request.form['s_port'])
            e_port = int(request.form['e_port'])
            ports = scanner(target, s_port, e_port)
        except:
            return render_template("scanner.html")
        return render_template("scan_results.html", target=target,
                               s_port=s_port, e_port=e_port, ports=ports)
    return render_template("scanner.html")


@app.route("/subnet_calc", methods=['get', 'post'])
def subnet():
    """
    defines a page
    """
    if request.method == 'POST':
        address = request.form['address']
        cidr = request.form['cidr']
        info = nflbx(address + "/" + cidr)
        if info:
            return render_template("subnet_output.html", network=info[0],
                                   first=info[1], last=info[2],
                                   broadcast=info[3], neXt=info[4],
                                   hosts=info[5])
        return render_template("invalid_addr.html")
    return render_template("subnet_input.html")


if __name__ == "__main__":
    app.run(debug=True, port=8050)
