#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.evalfnexprrules import *
from splparser.cmdparsers.common.simplefieldrules import *
from splparser.cmdparsers.common.simplevaluerules import *

from splparser.cmdparsers.headlexer import lexer, precedence, tokens

PARSETAB_DIR = 'parsetabs'
PARSETAB = 'head_parsetab'

start = 'cmdexpr'

def p_cmdexpr_head(p):
    """cmdexpr : headcmd"""
    p[0] = p[1]

def p_headcmd_head(p):
    """headcmd : HEAD"""
    p[0] = ParseTreeNode('HEAD')

def p_headcmd_head_int(p):
    """headcmd : HEAD int"""
    p[0] = ParseTreeNode('HEAD')
    p[0].add_child(p[2])

def p_headcmd_head_eval(p):
    """headcmd : HEAD evalfnexpr"""
    p[0] = ParseTreeNode('HEAD')
    p[0].add_child(p[2])

def p_headcmd_head_headopt(p):
    """headcmd : HEAD headoptlist"""
    p[0] = ParseTreeNode('HEAD') 
    p[0].add_children(p[2].children)

def p_headcmd_head_int_headopt(p):
    """headcmd : HEAD int headoptlist"""
    p[0] = ParseTreeNode('HEAD')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_headcmd_head_eval_headopt(p):
    """headcmd : HEAD evalfnexpr headoptlist"""
    p[0] = ParseTreeNode('HEAD')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_headoptlist(p):
    """headoptlist : headopt"""
    p[0] = ParseTreeNode('_HEAD_OPT_LIST')
    p[0].add_child(p[1])

def p_headoptlist_headopt(p):
    """headoptlist : headopt headoptlist"""
    p[0] = ParseTreeNode('_HEAD_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children) 

def p_headopt(p):
    """headopt : HEAD_OPT EQ simplevalue"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_headopt_commonopt(p):
    """headopt : COMMON_OPT EQ simplevalue"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in head parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "headparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    here = os.path.dirname(__file__)
    path_to_parsetab = os.path.join(here, PARSETAB_DIR, PARSETAB + '.py')
    
    try:
        parsetab = imp.load_source(PARSETAB, path_to_parsetab)
    except IOError: # parsetab files don't exist in our installation
        parsetab = PARSETAB

    try:
        os.stat(PARSETAB_DIR)
    except:
        try:
            os.makedirs(PARSETAB_DIR)
        except OSError:
            sys.stderr.write("ERROR: Need permission to write to ./" + PARSETAB_DIR + "\n")
            raise

    parser= ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule=parsetab, outputdir=PARSETAB_DIR)
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
