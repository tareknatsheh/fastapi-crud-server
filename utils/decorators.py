from fastapi import HTTPException, Request
import time
from functools import wraps
from datetime import datetime, timezone

def handle_errors(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            print(error)
            raise HTTPException(status_code=500, detail="Internal server error. Check logs for more info")
    return wrapper

def log_it(fn):
    @wraps(fn)
    def wrapper(request: Request, *args, **kwargs):
        utc_timestamp = datetime.now(timezone.utc)
        print(f"{utc_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")} - got a {request.method} request to the endpint {request.url.path}")
        res = fn(request, *args, **kwargs)
        return res
    return wrapper