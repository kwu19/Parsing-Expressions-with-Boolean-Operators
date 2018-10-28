#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:29:24 2018

@author: kefei
"""

class Stack:
    def __init__(self):
        self.items = []  # data structure
        
    def is_empty(self):
        return self.items == []
    
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
            
        item = self.items[-1]
        del self.items[-1]
        return item
        # return self.items.pop()
    
    def peek(self):
        return self.items[-1]
    
    def size(self):
        return len(self.items) 
    
class BinaryTree:
    
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None
        
    def insert_left(self, new_node):
        if self.left_child == None:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t
            
    def insert_right(self, new_node):
        if self.right_child == None:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t
            
    def get_right_child(self):
        return self.right_child
    
    def get_left_child(self):
        return self.left_child
    
    def set_root_val(self, obj):
        self.key =obj
        
    def get_root_val(self):
        return self.key
    
def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insert_left('')
            pStack.push(currentTree)
            currentTree = currentTree.get_left_child()
        # boolean part starts from here
        elif i in ['and','or']:  # check if the string is boolean "and" or "or"
            currentTree.set_root_val(i)
            currentTree.insert_right('')
            pStack.push(currentTree)
            currentTree = currentTree.get_right_child()
        elif i in ['false','true']:  # check if it is a valid boolean value
            currentTree.set_root_val(i)
            parent = pStack.pop()
            currentTree = parent
        elif i == 'not':  # check if the string is "not"
            currentTree = pStack.pop()
            currentTree.set_root_val(i)
            currentTree = currentTree.get_left_child()
        elif i == ')' and pStack.size() == 0:
            #  because of the 'not' operator, pStack will be empty before reaching the ')'
            #  if this is the situation, we do not pop anything1
            currentTree = currentTree
            
        # arithmetic expression part starts from here
        elif i not in ['+',',','*','/',')']:
            currentTree.set_root_val(int(i))
            parent = pStack.pop()
            currentTree = parent
        elif i in ['+','-','*','/']:
            currentTree.set_root_val(i)
            currentTree.insert_right('')
            pStack.push(currentTree)
            currentTree = currentTree.get_right_child()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    
    return eTree

import operator
def evaluate(parse_tree):
    """for this method we use operator for arithmetic calculation but not for boolean"""
    opers = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    
    left_c = parse_tree.get_left_child()
    right_c = parse_tree.get_right_child()
    
    if left_c and right_c:
        if parse_tree.get_root_val() in ["+","-","*","/"]:
            fn = opers[parse_tree.get_root_val()]
            return fn(evaluate(left_c), evaluate(right_c))
        else:
            if parse_tree.get_root_val() == "and":
                if(evaluate(left_c) == "true" and evaluate(right_c) == "true"):  # only two true will become true
                    return "true"
                else:
                    return "false"
            elif parse_tree.get_root_val() == "or":
                if(evaluate(left_c) == "true" or evaluate(right_c) == "true"):  # only need one true
                    return "true"
                else:
                    return "false"
            else:
                if(evaluate(left_c) == "true"):  # for 'not' part, we return the opposite boolean value
                    return "false"
                else:
                    return "true"
    else:
        return parse_tree.get_root_val()
    
# Test build_parse_tree, and evaluate to show that boolean expressions 
# (with, or without arithmetic expressions mixed), work as expected.
pt = buildParseTree("( ( false or not ( false and true ) ) and ( false or true ) )")
a = evaluate(pt)

pt1 = buildParseTree("( false and true ) and not ( false or true )")
b = evaluate(pt1)

pt2 = buildParseTree("( ( 10 + 5 ) * 3 )")
c = evaluate(pt2)