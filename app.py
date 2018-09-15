#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 19:16:45 2018

@author: stobe
"""
import os
from flask import Flask
from flask import request
import base64

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )

    return app

def double_minus_start_error(query):
    if len(query) < 2:
        return False
    return query[0] is '-' and query[1] is '-'

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

@app.route('/calculus')
def process():
    query=base64.b64decode(request.args.get('query')) \
            .decode("ASCII") \
            .replace(" ", "")
    
    error = double_minus_start_error(query)
    query = separate_minusoperators(query)
    
    def evaluate(query):
        print("evalissa, current query:", query)
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
                print("sulkuongelma")
                error = True
                return 0
        
        for idx, char in enumerate(query):
            if char is '/' or char is '*':
                if idx is 0 or idx is len(query) - 1:
                    print("last/first symbol is / or *")
                    error = True
                    return 0
                if char is '*':
                    return str(float(evaluate(query[slice(0, idx)])) 
                              * float(evaluate(query[slice(idx + 1, len(query))])))
                if char is '/':
                    second_arg = float(evaluate(query[slice(idx + 1, len(query))]))
                    if second_arg == 0:
                        print("division by 0")
                        error = True
                        return 0
                    return str(float(evaluate(query[slice(0, idx)])) 
                              / float(evaluate(query[slice(idx + 1, len(query))])))
                    
        
        for idx, char in enumerate(query):
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
        
        if query[0] is '-' and query[1] is '-':
            return query[2:]
        
        is_decimal = False
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
        return "erroneous query", 400
    return return_val
