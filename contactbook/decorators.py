from rest_framework.response import Response
from rest_framework.status import *


# our wrapper
def authorize(privilege_required):
    def check_and_execute(func):
        def wrapper(*args, **kwargs):
            if (privilege_required is None)or(privilege_required in args[1].privileges):
                return func(*args, **kwargs)
            else:
                return 403, "Unauthorized access requested.", None  # add error response
        return wrapper

    return check_and_execute

