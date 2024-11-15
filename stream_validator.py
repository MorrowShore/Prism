from flask import Flask, request, Response
import os
import hmac
import hashlib

app = Flask(__name__)

# Get the secret key from environment variable or use a default for development
SECRET_KEY = os.getenv('STREAM_SECRET_KEY', 'change-this-in-production')

# Dictionary to store valid stream keys
VALID_STREAM_KEYS = {
    'youtube': os.getenv('YOUTUBE_KEY', ''),
    'facebook': os.getenv('FACEBOOK_KEY', ''),
    'instagram': os.getenv('INSTAGRAM_KEY', ''),
    'cloudflare': os.getenv('CLOUDFLARE_KEY', ''),
    'kick': os.getenv('KICK_KEY', ''),
    'x': os.getenv('X_KEY', ''),
    # Add other services as needed
}

def validate_stream_key(name, key):
    """
    Validate the stream key using HMAC
    """
    if not key:
        return False
        
    # Get the stored key for the service
    valid_key = VALID_STREAM_KEYS.get(name)
    if not valid_key:
        return False
    
    # Compare using constant-time comparison
    return hmac.compare_digest(key, valid_key)

@app.route('/validate', methods=['POST'])
def validate():
    # Get the stream key from the request
    stream_key = request.args.get('name', '')
    
    # Get the client IP
    client_ip = request.remote_addr
    
    # Log validation attempt (optional)
    app.logger.info(f"Stream key validation attempt from {client_ip}")
    
    # Split the stream key into service and key parts
    try:
        service, key = stream_key.split('_', 1)
    except ValueError:
        return Response('Invalid stream key format', status=403)
    
    # Validate the key
    if validate_stream_key(service, key):
        app.logger.info(f"Valid stream key used for {service} from {client_ip}")
        return Response('OK', status=200)
    else:
        app.logger.warning(f"Invalid stream key attempt for {service} from {client_ip}")
        return Response('Invalid stream key', status=403)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)