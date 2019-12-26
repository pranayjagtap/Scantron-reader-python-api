from flask import Flask, jsonify, request
import sys
import omrreader
import werkzeug

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    content = request.args.get('path')
    prediction = None

    try:
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save(filename)
        prediction = omrreader.process('/home/jilia/'+filename)
    except:
        filename = ""


    return jsonify({"score": prediction, "filename": filename})

if __name__ == "__main__":
    app.run()