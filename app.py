#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module deals both with the minimal routing, responses etc. required with 
Flask in addition to processing the query and evaluating it. The process function
first tries to decode the given query string and prepares the string for the 
recursion. 

The recursive evaluate function first evaluates anything inside parenthesis. 
When parenthesis have been eliminated, the function divides the string according
to the order of operations. Note that the unary minus has the highest precedence
of operations contrary to common belief. Upon encountering an error, the
recursive function stops evaluating and returns 0 while setting error to be true

Errors seem to be handled a little all over the place. However the syntax errors
in a calculator query are not always trivial and best caught while going through
the syntax like the evaluate function does. For this reason the syntax error 
catching is incorporated inside the evaluate function save for one specific
error below. 

Below is the specification for the API:
    
Endpoint:
GET /calculus?query=[input]

input: UTF-8 with BASE64 encoding

syntax for query:

output:

"""
from flask import Flask
from flask import request
import base64

app = Flask(__name__)

#The dual duty of the minus symbol as both a binary and an unary operator causes
#problems and these operators need to be separated. The binary minus is replaced
#with '_'.
def separate_minusoperators(query):
    is_unary = True
    q_list = list(query)
    for idx, sym in enumerate(q_list):
        if sym is '-' and not is_unary:
            q_list[idx] = '_'
        is_unary = False
        if sym is '(':
            is_unary = True
    return "".join(q_list)

def JSONoutput(error, contents):
    if error is True:
        return "{ error: true, message: " + contents + " }", 400
    else:
        return "{ error: false, result: " + contents + " }"


@app.route('/calculus')
def process():
    query=""
    try:
        query=base64.b64decode(request.args.get('query')) \
            .decode("ASCII") \
            .replace(" ", "")
    except:
        return JSONoutput(True, "encoding error")
     
    error = False
    zero_div = False
    query = separate_minusoperators(query)
    
    def evaluate(query):
        nonlocal error
        if error is True:
            return 0
        
        if len(query) is 0:
            return 0
        
        beg_paren = -1
        for idx, char in enumerate(query):
            if char is '(':
                beg_paren = idx
            if char is ')':
                if beg_paren is -1:
                    error = True
                    return 0
                inner = evaluate(query[slice(beg_paren + 1, idx)])
                return evaluate(query[slice(0, beg_paren)] + inner 
                                      + query[slice(idx + 1, None)])
            if beg_paren != -1 and idx is len(query):
                error = True
                return 0
    
        for idx, char in reversed(list(enumerate(query))):
            if char is '+' or char is '_':
                if idx is 0 or idx is len(query) - 1:
                    error = True
                    return 0
                if char is '+':
                    return str(float(evaluate(query[slice(0, idx)])) 
                              + float(evaluate(query[slice(idx + 1, len(query))])))
                if char is '_':
                    return str(float(evaluate(query[slice(0, idx)])) 
                              - float(evaluate(query[slice(idx + 1, len(query))])))
        
        for idx, char in reversed(list(enumerate(query))):
            if char is '/' or char is '*':
                if idx is 0 or idx is len(query) - 1:
                    error = True
                    return 0
                if char is '*':
                    return str(float(evaluate(query[slice(0, idx)])) 
                              * float(evaluate(query[slice(idx + 1, len(query))])))
                if char is '/':
                    second_arg = float(evaluate(query[slice(idx + 1, len(query))]))
                    if second_arg == 0:
                        nonlocal zero_div
                        zero_div = True
                        error = True
                        return 0
                    return str(float(evaluate(query[slice(0, idx)])) 
                              / float(evaluate(query[slice(idx + 1, len(query))])))
        
        if len(query) > 1 and query[0] is '-' and query[1] in ['-', '_']:
            return query[2:]
        
        is_decimal = False
        if query is '-':
            error = True
            return 0        
        for idx, char in enumerate(query):
            if char is '.':
                if is_decimal is True:
                    error = True
                    return 0
                is_decimal = True
            elif char not in set("0123456789") and not (idx is 0 and char is '-'):
                error = True
                return 0
            
        return query
    
    return_val = evaluate(query)
    if error is True:
        if zero_div is True:
            return JSONoutput(error, "zero division error")
        return JSONoutput(error, "syntax error")
    return JSONoutput(error, return_val)

if __name__ == "__main__":
	app.run()
