#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes.searchregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA',
    'WILDCARD',
    'EQ',
    'IPV4ADDR', 'IPV6ADDR',
    'EMAIL','HOSTNAME', 'URL', 'PATH', 'US_PHONE',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'ID',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
]

reserved = {
    'xmlkv' : 'XMLKV',
    'maxinputs' : 'MAXINPUTS',
}

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_EQ = r'='

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.

states = (
    ('ipunchecked', 'inclusive'),
)

def is_ipv4addr(addr):
    addr = addr.replace('*', '0')
    addr = addr.strip()
    addr = addr.strip('"')
    port = addr.find(':')
    if port > 0:
        addr = addr[:port]
    slash = addr.find('/')
    if slash > 0:
        addr = addr[:slash]
    addr = addr.strip()
    import socket
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        return False
    return True

def is_ipv6addr(addr):
    addr = addr.replace('*', '0')
    addr = addr.strip()
    addr = addr.strip('"')
    addr = addr.strip('[')
    port = addr.find(']')
    if port > 0:
        addr = addr[:port]
    slash = addr.find('/')
    if slash > 0:
        addr = addr[:slash]
    addr = addr.strip()
    import socket
    try:
        socket.inet_pton(socket.AF_INET6, addr)
    except socket.error:
        return False
    return True

def type_if_reserved(t, default):
    return reserved.get(t.value, default)

def t_MACRO(t):
    r"""(`[^`]*`)"""
    return t

@TOKEN(ipv4_addr)
def t_ipunchecked_IPV4ADDR(t):
    if is_ipv4addr(t.value):
        return t
    t.lexer.lexpos -= len(t.value)
    t.lexer.begin('INITIAL')
    return

@TOKEN(ipv6_addr)
def t_ipunchecked_IPV6ADDR(t):
    if is_ipv6addr(t.value):
        return t
    t.lexer.lexpos -= len(t.value)
    t.lexer.begin('INITIAL')
    return

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(wildcard)
def t_WILDCARD(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(search_key)
def t_SEARCH_KEY(t):
    t.lexer.begin('ipunchecked')
    return(t)

def t_LITERAL(t):
    r'"(?:[^"]+(?:(\s|-|_)+[^"]+)+\s*)"'
    return(t)

@TOKEN(bin)
def t_BIN(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(oct)
def t_OCT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(hex)
def t_HEX(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(float)
def t_FLOAT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(word)
def t_WORD(t):
    t.type = type_if_reserved(t, 'WORD')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(int)
def t_INT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(id)
def t_ID(t):
    t.type = type_if_reserved(t, 'ID')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(email)
def t_EMAIL(t):
    t.type = type_if_reserved(t, 'EMAIL')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(hostname)
def t_HOSTNAME(t):
    t.type = type_if_reserved(t, 'HOSTNAME')
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(path)
def t_PATH(t):
    t.type = type_if_reserved(t, 'PATH')
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(url)
def t_URL(t):
    t.type = type_if_reserved(t, 'URL')
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(us_phone)
def t_US_PHONE(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(nbstr)
def t_NBSTR(t): # non-breaking string
    t.type = type_if_reserved(t, 'NBSTR')
    t.lexer.begin('ipunchecked')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    t.lexer.begin('ipunchecked')
    raise SPLSyntaxError("Illegal character in makemv lexer '%s'" % badchar)

def lex():
    return ply.lex.lex()

def tokenize(data, debug=False, debuglog=None):
    lexer = ply.lex.lex(debug=debug, debuglog=debuglog)
    lexer.input(data)
    lexer.begin('ipunchecked')
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: break
        tokens.append(tok)
    return tokens

if __name__ == "__main__":
    import sys
    print tokenize(' '.join(sys.argv[1:]))
