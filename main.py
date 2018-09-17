import pycurl
from flask import jsonify
from io import BytesIO

### GLOBALS ###
timeout = 10

def request_pycurl(request):
    """Http monitor.
    Args:
        page: valid url.
    Returns:
        Response code and timing
    """
    request_json = request.get_json()
    if request.args and 'page' in request.args:
        page = request.args.get('page')
    elif request_json and 'page' in request_json:
        page = request_json['page']
    else:
        return "Invalid parameters!",500
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, page)
    c.setopt(pycurl.TIMEOUT, timeout)
    c.setopt(c.WRITEDATA, buffer)
    try:
    	c.perform()
    except pycurl.error as e:
        if e.args[0] == pycurl.E_COULDNT_CONNECT and c.exception:
            return "Error!!!: " + str(c.exception), 500
        else:
            return "Error!!!: " + str(e), 500
    
    data = {}
    data['response_code'] = c.getinfo(c.RESPONSE_CODE)
    data['namelookup'] = c.getinfo(c.NAMELOOKUP_TIME)
    data['connect'] = c.getinfo(c.CONNECT_TIME)
    data['starttransfer'] = c.getinfo(c.STARTTRANSFER_TIME)
    data['total_time'] =  c.getinfo(c.TOTAL_TIME)
    
    c.close()
    
    return jsonify(data)
