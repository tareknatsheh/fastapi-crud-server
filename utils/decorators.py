import logging
from fastapi import HTTPException, Request
from functools import wraps
from datetime import datetime, timezone

from pydantic import ValidationError


logging.Formatter.converter = lambda *args: datetime.now(tz=timezone.utc).timetuple()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    filename='logs.log',  # Log to a file
    filemode='w'  # Overwrite log file each time
)

def handle_errors(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except HTTPException as http_error:
            raise http_error
        except ValidationError as error:
            print(error)
            raise HTTPException(status_code=400, detail="Validation error. Check the integrity of db or passed parameters")
        except Exception as error:
            print(error)
            raise HTTPException(status_code=500, detail="Internal server error. Check logs for more info")
    return wrapper

def log_it(fn):
    @wraps(fn)
    def wrapper(request: Request, *args, **kwargs):
        logging.info(f"got a {request.method} request to the endpoint {request.url.path}")
        try:
            res = fn(request, *args, **kwargs)
            return res
        except Exception as error:
            logging.error(f"{str(error).replace('\n', '-')}")
            raise error
    return wrapper