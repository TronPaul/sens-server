import io
import flask
import sens.status
import sens.image

app = flask.Flask(__name__)

@app.route('/<channel_name>')
def image(channel_name):
    status = sens.status.get_status(channel_name)
    image = sens.image.build_image(status)
    fp = io.BytesIO()
    image.save(fp, 'png')
    fp.seek(0)
    return flask.send_file(fp, mimetype='image/png')

def main():
    app.debug = True
    app.run(host='0.0.0.0')
