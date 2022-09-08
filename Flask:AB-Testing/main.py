# project: p4
# submitter: zzhou443
# partner: none
# hours: 7


import pandas as pd
from flask import Flask, request, jsonify
import re

app = Flask(__name__)
df = pd.read_csv("main.csv")

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()

    return html

@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()

    return html + df.to_html()


@app.route('/email', methods=["POST"])
def email():
    num_subscribed = 0
    email = str(request.data, "utf-8")
    
    if re.match(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        with open("emails.txt", "r") as f:
            for i in f:
                num_subscribed = num_subscribed + 1
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify("we can not find the correct e-mail, please try again") # 3


@app.route("/donate.html")
def donate():
    with open("donate.html") as f:
        html = f.read()
    return html


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.