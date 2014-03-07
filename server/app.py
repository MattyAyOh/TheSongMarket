# encoding: utf-8

import jinja2
from urlparse import parse_qs
import cgi

pages = {
            '/'        : 'index.html',   \
            '/content' : 'content.html', \
            '/file'    : 'file.html',    \
            '/image'   : 'image.html',   \
            '/form'    : 'form.html',    \
            '/submit'  : 'submit.html',  \
            '404'      : '404.html',     \
           }

def app(environ, start_response):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]

    if environ['PATH_INFO'] in pages:
        status = '200 OK'
        template = env.get_template(pages[environ['PATH_INFO']])
    else:
        status = '404 Not Found'
        template = env.get_template(pages['404'])

    query = parse_qs(environ['QUERY_STRING']).items()
    args = {key : val[0] for key, val in query}
    args['path'] = environ['PATH_INFO']

    if environ['REQUEST_METHOD'] == 'POST':
        headers = {
                    'content-type':environ['CONTENT_TYPE'], \
                    'content-length':environ['CONTENT_LENGTH']
                  }
        form = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, environ=environ)
        args.update({key : form[key].value for key in form.keys()})

    start_response(status, response_headers)
    return [template.render(args).encode('utf-8')]

def make_app():
    return app
