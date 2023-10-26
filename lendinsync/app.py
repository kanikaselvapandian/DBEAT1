from flask import Flask, render_template
app = Flask(__name__,template_folder="templates/")

@app.route("/")
def hello():
  return render_template("login.html")


if __name__ == "__main__":
  app.run()