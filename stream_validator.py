from flask import Flask, request, Response
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Get stream keys from environment
VALID_KEYS = [
    os.getenv('YOUTUBE_KEY', ''),
    os.getenv('TWITCH_KEY', ''),
    os.getenv('KICK_KEY', ''),
    os.getenv('X_KEY', '')
]

@app.route('/validate', methods=['POST'])
def validate():
    stream_key = request.args.get('name', '')
    client_ip = request.remote_addr
    
    app.logger.info(f"Incoming validation request - Key: {stream_key}, IP: {client_ip}")
    
    # Remove any empty keys from validation
    valid_keys = [key for key in VALID_KEYS if key]
    
    if stream_key in valid_keys:
        app.logger.info(f"Valid key accepted from {client_ip}")
        return Response('OK', status=200)
    else:
        app.logger.warning(f"Invalid key rejected from {client_ip}: {stream_key}")
        app.logger.debug(f"Valid keys are: {valid_keys}")
        return Response('Invalid stream key', status=403)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)