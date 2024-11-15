from flask import Flask, request, Response
import os
import logging
from urllib.parse import parse_qs

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
    # Get raw data and parse it
    raw_data = request.get_data(as_text=True)
    parsed_data = parse_qs(raw_data)
    
    # Extract the stream key from the 'name' parameter
    stream_key = parsed_data.get('name', [''])[0]
    client_ip = request.remote_addr
    
    # Debug logging
    app.logger.debug(f"Raw request data: {raw_data}")
    app.logger.debug(f"Parsed data: {parsed_data}")
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