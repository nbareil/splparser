#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.fieldslexer import precedence , tokens

start = 'cmdexpr'

def p_cmdexpr_fields(p):
    """cmdexpr : fieldscmd"""
    p[0] = p[1]

def p_cmdexpr_fields_debug(p):
    """fieldscmd : FIELDS"""
    p[0] = ParseTreeNode('FIELDS')

def p_fields_fieldlist(p):
    """fieldscmd : FIELDS fieldlist"""
    p[0] = ParseTreeNode('FIELDS')
    plus_node = ParseTreeNode('PLUS')
    plus_node.add_children(p[2].children)
    p[0].add_child(plus_node)

def p_fields_plus_fieldlist(p):
    """fieldscmd : FIELDS PLUS fieldlist"""
    p[0] = ParseTreeNode('FIELDS')
    plus_node = ParseTreeNode('PLUS')
    plus_node.add_children(p[3].children)
    p[0].add_child(plus_node)

def p_fields_minus_fieldlist(p):
    """fieldscmd : FIELDS MINUS fieldlist"""
    p[0] = ParseTreeNode('FIELDS')
    minus_node = ParseTreeNode('MINUS')
    minus_node.add_children(p[3].children)
    p[0].add_child(minus_node)
    
def p_error(p):
    raise SPLSyntaxError("Syntax error in fields parser input!") 