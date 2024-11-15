from flask import Flask, request, Response
import os
import logging

app = Flask(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get stream keys from environment
VALID_KEYS = [
    os.getenv('YOUTUBE_KEY', ''),
    os.getenv('TWITCH_KEY', ''),
    os.getenv('KICK_KEY', ''),
    os.getenv('X_KEY', '')
]

@app.route('/validate', methods=['POST'])
def validate():
    # Get key from proper parameter
    stream_key = request.args.get('key', '')
    client_ip = request.remote_addr
    
    # Debug logging
    app.logger.debug(f"Request args: {request.args}")
    app.logger.debug(f"Received stream key: '{stream_key}'")
    
    # Remove any empty keys from validation
    valid_keys = [key for key in VALID_KEYS if key]
    app.logger.debug(f"Valid keys: {valid_keys}")
    
    if stream_key in valid_keys:
        app.logger.info(f"Valid key accepted from {client_ip}")
        return Response('OK', status=200)
    else:
        app.logger.warning(f"Invalid key rejected from {client_ip}")
        app.logger.debug(f"Attempted key: '{stream_key}'")
        return Response('Invalid stream key', status=403)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)