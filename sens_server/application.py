import io
import flask
import sens.status
import sens.application

app = flask.Flask(__name__)

@app.route('/<channel_name>')
def image(channel_name):
    try:
        image = sens.application.build_image(channel_name)
    except sens.status.ChannelNotFoundError as e:
        flask.abort(404)
    except sens.status.TwitchError as e:
        flask.abort(400)
    fp = io.BytesIO()
    image.save(fp, 'png')
    fp.seek(0)
    return flask.send_file(fp, mimetype='image/png')

def main():
    app.debug = True
    app.run(host='0.0.0.0')
