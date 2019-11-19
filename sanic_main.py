#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# install using 'pip3 install sanic' under Python 3.6+
from sanic import Sanic
from sanic.response import json

from scraper import read_url, parse_page

# item [{"tag":"", "class":"", "where":"", "filter":"", "order": 1}, ... ]
# output ["<string>", "@<int: order_num>", ... ]

DEFAULT_URL = 'pasmi.ru/cat/news/'
DEFAULT_PARAM = '''{
"pass_through": 0, "return_container": 0,
"container": {"tag": "article", "class": ""},
"item": [
{"class": "time", "filter": "(\\\\d+.\\\\d+.\\\\d+)", "order": 3},
{"tag": "span", "class": "time", "filter": "(\\\\d+:\\\\d+)", "order": 4},
{"tag": "a", "class": "entry-title", "order": 2},
{"tag": "a", "class": "entry-title", "where": "href", "order": 1} ],
"output": ["<div>", "@1", "</div><br>\\n", "@2", "<br>\\n", "@3", " - ", "@4"]
}'''
DEFAULT_HEADER = { 'User-Agent': 'Mozilla/5.0 (Macintosh; '\
'Intel Mac OS X 10.13; rv:70.0) Gecko/20100101 Firefox/70.0' }

app = Sanic()

app.static('/', 'sanic_index.html', content_type='text/html; charset=utf-8')

@app.route('/default-config.json')
async def def_data(request):
    return json({'url': DEFAULT_URL,'param': DEFAULT_PARAM})

@app.route('/parse', methods=['POST',])
async def parse(request):

    data = {"form_data": request.json}

    target_url = request.json['url']
    parse_param = request.json['param']

    page = read_url(target_url, header=DEFAULT_HEADER)

    data['bytes_read'] = str(len(page))

    parse_results = parse_page(page, parse_param)

    data['parsed_output'] = parse_results
    data['raw_output'] = page

    return json(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
