import sys

def response_status_code_is_2xx(code):
    if code >= 300 or code <= 100:
        print(f"Something went wrong. Recieved code {code}", file=sys.stderr)
        return False
    return True