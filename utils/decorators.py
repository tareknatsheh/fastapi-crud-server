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
            raise HTTPException(status_code=400, detail={"message": "Validation error. Check the integrity of db or passed parameters", "error": f"{error}"})
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail={"message": "Data not found", "error": f"{error}"})
        except Exception as error:
            print(error)
            raise HTTPException(status_code=500, detail={"message": "Internal server error. Check logs for more info", "error": f"{error}"})
    return wrapper

def log_it(fn):
    @wraps(fn)
    def wrapper(request: Request, *args, **kwargs):
        logging.info(f"got a {request.method} request to the endpoint {request.url.path}")
        try:
            res = fn(request, *args, **kwargs)
            return res
        except Exception as error:
            no_newlines_error = str(error).replace('\n', '-')
            logging.error(f"{no_newlines_error}")
            raise error
    return wrapper