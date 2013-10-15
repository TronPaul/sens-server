import io
import tempfile
import flask
import flask.ext.cache
import sens.status
import sens.application
import sens_server.request_handler as req_handler

app = flask.Flask(__name__)

@app.route('/<channel_name>')
def image(channel_name):
    try:
        image = sens.application.build_image(channel_name)
    except sens.status.ChannelNotFoundError as e:
        app.logger.info(('Requested channel {channel_name} '
                'not found by Twitch').format(channel_name=channel_name))
        flask.abort(404)
    except sens.status.TwitchError as e:
        app.logger.info(('Requested channel {channel_name} '
                'recieved error response from '
                'Twitch').format(channel_name=channel_name))
        flask.abort(404)
    fp = io.BytesIO()
    image.save(fp, 'png')
    fp.seek(0)
    return flask.send_file(fp, mimetype='image/png', cache_timeout=60)

def main():
    app.debug=True
    app.run(host='0.0.0.0', request_handler=req_handler.TimedRequestHandler)
