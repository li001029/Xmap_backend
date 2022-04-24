from app import application 
from flask import jsonify

@application.route("/")
def hello():
  return "Hello World!"
  
if __name__ == "__main__":
    application.run()