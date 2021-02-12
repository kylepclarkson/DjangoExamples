import uuid


def get_random_code():
    """ Return a random string of length 8 in lowercase. """
    code = str(uuid.uuid4())[:8].replace('-','').lower()
    return code

