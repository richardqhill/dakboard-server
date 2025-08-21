import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any

def create_session():
    """Create a requests session with retry logic for handling SSL and connection errors"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def request_with_retry(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 30):
    """
    Make a robust HTTP request with error handling and retry logic.
    
    Args:
        url: The URL to request
        params: Query parameters
        timeout: Request timeout in seconds
        
    Returns:
        Response object if successful, None if failed
    """
    session = create_session()
    
    try:
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response
        
    except requests.exceptions.SSLError as e:
        print(f"SSL Error connecting to {url}: {e}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request Error connecting to {url}: {e}")
        return None
        
    except Exception as e:
        print(f"Unexpected error making request to {url}: {e}")
        return None
