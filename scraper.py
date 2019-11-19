#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json as py_json
import re

from bs4 import BeautifulSoup


MSG_TAG_OR_CLASS = "You must specify at least 'tag' or 'class' or both."

def read_url(adress,protocol='https',coding='utf-8',header = ''):
    try:
        req = urllib.request.Request(protocol + '://' + adress, headers=header)
        fid = urllib.request.urlopen(req)
        webpage=fid.read().decode(coding)

    except Exception as e: return str(e)
    return webpage


def gr (x, g=0): # re helper
    try: y = x.group(g)
    except: return x
    return y


def getkey(c, x):
    if x in c: return c[x]
    else: return None


def parse_item(item, conf):
    if not conf: return item

    output = {}
    c = 0

    for x in conf:
        c += 1
        tag = getkey(x, 'tag')
        cls = getkey(x, 'class')


        if (tag and cls):
            res1 = item.find(tag, attrs={'class':cls})
        elif tag:
            res1 = item.find(tag)
        elif cls:
            res1 = item.find(True, attrs={'class':cls})
        else:
            return MSG_TAG_OR_CLASS


        where = getkey(x, "where") or "text"

        if where == "text":
            res2 = res1.get_text()
        elif where == "href":
            res2 = res1.get(where)
        else:
            res2 = res1

        filter = getkey(x, "filter")

        if filter:
            match = re.search(filter,res2)
            res3 = gr(match)

        else:
            res3 = res2

        order = getkey(x, "order")

        if order:
            output[order] = res3

    return output


def format_output(p_item, conf):

    output = ""

    for x in conf:
        if x.startswith("@"):
            output += getkey(p_item, int(x[1:]))
        else:
            output += x

    return output


def parse_page(text, param):
    soup = BeautifulSoup(text,'html.parser')

    try: conf = py_json.loads(param)
    except Exception as e: return str(e)


    if getkey(conf, 'pass_through'): return text


    container = getkey(conf, 'container')
    if container:
        tag = getkey(container, 'tag')
        cls = getkey(container, 'class')

        if (tag and cls):
            results = soup.find_all(tag, attrs={'class':cls})
        elif tag:
            results = soup.find_all(tag)
        elif cls:
            results = soup.find_all(True, attrs={'class':cls})
        else:
            return MSG_TAG_OR_CLASS

        if getkey(conf, 'return_container'): return str(results)

    else: return "You must specify 'container' configuration block."

    output = ""

    o_format = getkey (conf, "output")

    for item in results:
        elm = parse_item(item, getkey(conf, 'item'))

        if o_format:
            f_elm = format_output(elm, o_format)
        else:
            f_elm = elm

        output += f_elm + "\n\n"

    return output
