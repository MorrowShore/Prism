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
    stream_key = request.args.get('name', '')
    client_ip = request.remote_addr
    
    # Debug print all environment variables
    app.logger.debug("Environment variables:")
    app.logger.debug(f"YOUTUBE_KEY: {os.getenv('YOUTUBE_KEY')}")
    app.logger.debug(f"TWITCH_KEY: {os.getenv('TWITCH_KEY')}")
    app.logger.debug(f"KICK_KEY: {os.getenv('KICK_KEY')}")
    app.logger.debug(f"X_KEY: {os.getenv('X_KEY')}")
    
    # Debug print the incoming key
    app.logger.debug(f"Received stream key: '{stream_key}'")
    
    # Remove any empty keys from validation
    valid_keys = [key for key in VALID_KEYS if key]
    app.logger.debug(f"Valid keys: {valid_keys}")
    
    # Debug print exact comparison
    for key in valid_keys:
        app.logger.debug(f"Comparing '{stream_key}' with '{key}'")
        app.logger.debug(f"Length of received key: {len(stream_key)}")
        app.logger.debug(f"Length of valid key: {len(key)}")
        if stream_key == key:
            app.logger.debug("Match found!")
    
    if stream_key in valid_keys:
        app.logger.info(f"Valid key accepted from {client_ip}")
        return Response('OK', status=200)
    else:
        app.logger.warning(f"Invalid key rejected from {client_ip}")
        return Response('Invalid stream key', status=403)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)