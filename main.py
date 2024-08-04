from flask import Flask, request, make_response, render_template, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def index():
  resp = make_response(render_template("index.html"))
  resp.headers.add('Access-Control-Allow-Origin', '*')
  return resp

@app.route('/setprocksy/', methods=["POST"])
def setcookie():
  rooturl = request.form.get("rooturl")
  resp = make_response(redirect(url_for("display")))
  resp.headers.add('Access-Control-Allow-Origin', '*')
  resp.set_cookie("rooturl", rooturl)
  return resp

@app.route('/procksy/<path:url>')
def p(url):
  rooturl = request.cookies.get("rooturl")
  if not rooturl:
    resp = make_response(redirect(url_for("index")))
    return resp
  fullurl = request.cookies.get("rooturl") + url
  r = requests.get(fullurl)
  resp = make_response(r.text)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  return resp

@app.route('/procksy/')
def display():
  url = request.cookies.get("rooturl")
  if url is None:
    resp = make_response(redirect(url_for("index")))
    return resp
  r = requests.get(url)
  resp = make_response(r.text)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  return resp

@app.route('/<path:url>')
def p2(url):
  rooturl = request.cookies.get("rooturl")
  if not rooturl:
    resp = make_response(redirect(url_for("index")))
    return resp
  fullurl = rooturl + (url if url[0] == "/" else "/" + url)
  r = requests.get(fullurl)
  resp = make_response(r.text)
  resp.headers.add('Access-Control-Allow-Origin', '*')
  return resp


from threading import Thread

def run():
  app.run(host='0.0.0.0',port=8080)



def keep_alive():  

  t = Thread(target=run)

  t.start()