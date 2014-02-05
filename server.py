from mod_python import apache

def handler(req):
        req.send_http_header()
        req.write("hello %s" % req.remote_host)
        return apache.OK
