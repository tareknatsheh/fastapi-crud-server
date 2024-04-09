import logging
from fastapi import HTTPException, Request
from functools import wraps
from datetime import datetime, timezone


logging.Formatter.converter = lambda *args: datetime.now(tz=timezone.utc).timetuple()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    filename='logs.log',  # Log to a file
    filemode='w'  # Overwrite log file each time
)

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
        logging.info(f"got a {request.method} request to the endpoint {request.url.path}")
        res = fn(request, *args, **kwargs)
        return res
    return wrapper