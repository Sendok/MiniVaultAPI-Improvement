# Import the Limiter class to enable rate limiting
from slowapi import Limiter

# Import a utility function to get the client's IP address
from slowapi.util import get_remote_address

# Initialize the limiter using the client's IP address as the unique key
limiter = Limiter(key_func=get_remote_address)
