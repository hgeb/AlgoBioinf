# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 17:16:50 2021

@author: hanne
"""
from BinaryTree import *

###############################
### CONSTANTS
###############################

DIGITS = "0123456789"


###############################
### Errors
###############################
            
class Error: #!ToDo: Add Error description
    """
    Error class that acts as a base class for more specific errors.
    """
    
    def __init__(self, name):
        self.name = name
    def as_string(self):
        result = f"{self.name}"
        return result
    
class IllegalCharError(Error):
    """
    Error, when an illegal character is found in input.
    """
    def __init__(self):
        super().__init__("Illegal Character")
              

class InvalidSyntaxError(Error):
    """
    Error, when a syntax error is found.
    """
    def __init__(self):
        super().__init__("Invalid Syntax")


###############################
### Token
###############################


TT_INT = "INT"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_COMMA = "COMMA"
TT_EOF = "EOF"

class Token:
    
    """
    Wrapper class for tokens.
    """
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
  
        
###############################
### Lexer
###############################

class Lexer:
    """
    Lexer is used to tokenize the input.
    """
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
        
    def advance(self):
        """
        Keeps track of position and current char of input.

        Returns
        -------
        None.

        """
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def make_tokens(self):
        """
        Generates the tokens from the input.

        Returns
        -------
        Token list
            a list of tokens from the input, if an error arises the return value
            will be None
        Error
            Returns an Error if a wrong character is found in input. None if no
            Error arises.

        """
        tokens = []
        
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ",":
                tokens.append(Token(TT_COMMA))
                self.advance()
            else:
                return [], IllegalCharError()
        
        tokens.append(Token(TT_EOF))
        return tokens, None
    
    def make_number(self):
        
        """
        Generates a number from input number string.
        
        Returns
        -------
        Token
            A Int token with it's corrisponding value.
        """
        
        num_str = ""
        while self.current_char != None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        
        return Token(TT_INT, int(num_str))


#######################################
### Nodes
#######################################

class LeafNode:
    """
    Represents leaf node in parse tree.
    """
    def __init__(self, tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'
    
class InternalNode:
    """
    Represents internal node in parse tree.
    """
    def __init__(self,left,right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f'({self.left},{self.right})'
    

#######################################
### PARSE RESULT
#######################################

class ParseResult:
    """
    Class contains parse tree and arising errors.
    """
    def __init__(self):
        self.error = None
        self.node = None

    def success(self, node):
        """
        Gets called, when tokens are parsed without error.

        Parameters
        ----------
        node : node
            Node for the parse tree.

        Returns
        -------
        ParseResult
            itself.

        """
        self.node = node
        return self

    def failure(self, error):
        """
        Gets called, when an error arises while parsing.

        Parameters
        ----------
        error : InvalidSyntaxError
            contains description of error.

        Returns
        -------
        ParseResult
            itself.
        """
        
        self.error = error
        return self
           
#######################################
### PARSER
#######################################   

class Parser():
    """
    Parser is used to parse the tokens from the lexer and generates a parse tree.
    A InvalidSyntaxError will be created if a wrong syntax is passed.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        
    def advance(self):
        """
        Keeps track of position and current token of tokenlist.

        Returns
        -------
        None.

        """
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        """
        Starts the parse process.
        

        Returns
        -------
        ParseResult
            ParseResult that contains parse tree and error, if it arises.

        """
        
        res = self.tree()
        
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError())
        
        return res
    
    
    def tree(self):
        """
        This function is not nesessary.
        Returns
        -------
        ParseResult
            returnes subtree of tree.

        """
        
        return self.subtree()
    
    def subtree(self):
        """
        Parses subtree.

        Returns
        -------
        ParseResult
            Returns parse result for a subtree, the node type is either InternalNode
            or LeafNode.
            If an error occures, then the parse result will contain an error.

        """
        
        res = ParseResult()
        
        tok = self.current_tok
        
        if tok.type == TT_INT:
            return self.leaf()
        
        elif tok.type == TT_LPAREN:
            self.advance()
            
            left = self.subtree().node
            
            if self.current_tok.type == TT_COMMA:
                self.advance()
                
                right = self.subtree().node
                
                if self.current_tok.type == TT_RPAREN:
                    
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError())
            else:
                return res.failure(InvalidSyntaxError())
            
            return res.success(InternalNode(left, right))
            
            
        
    def leaf(self):
        """
        Returns
        -------
        ParseResult
            the ParseResult contains a LeafNode.

        """
        res = ParseResult()
        tok = self.current_tok
        self.advance()
        return res.success(LeafNode(tok))
        

#######################################
### INTERPRETER
#######################################

class Interpreter:
    """
    Interprets the parse tree from the parser.
    """
    
    def __init__(self):
        self.bt = BinaryTree()
        
    
    def getTree(self,node):
        """
        Gets a binary tree with structure from the parse result.

        Parameters
        ----------
        node : InternalNode or LeafNode
            RootNote from the parse tree.

        Returns
        -------
        BinaryTree
            The binary tree has the structure specified in the input.

        """
        
        self.bt.setRoot(self.visit(node))
        return self.bt
    
    def visit(self, node):
        """
        Defines visit method for different node types.

        Parameters
        ----------
        node : LeafNode or InternalNode
            Node on which a visit method will be called.

        Returns
        -------
        BinaryTree.Node
            returns either a BinaryTree.LeafNode or a BinaryTree.InternalNode

        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self, node):
        """
        Standard method if there is no corresponding visit function for a note.

        Parameters
        ----------
        node : Node
            A nod from the parseTree

        Raises
        ------
        Exception
            If there is no corresponding functionn for the note.

        Returns
        -------
        None.

        """
        raise Exception(f'No visit_{type(node).__name__} method defined')
        
    def visit_LeafNode(self, node):
        """
        Gets called when LeafNode in parse tree is visited.

        Parameters
        ----------
        node : LeafNode
            LeafNode in parse tree.

        Returns
        -------
        leaf : BinaryTree.LeafNode
            Adds a leaf to the binary tree.

        """
        
        leaf = BinaryTree.LeafNode(node.tok.value)
        self.bt.addLeaf(leaf)
        return leaf
    
    def visit_InternalNode(self,node):
        """
        Gets called when InternalNode in parse tree is visited.

        Parameters
        ----------
        node : InternalNode
            InternalNode in parse tree.

        Returns
        -------
        internal : BinaryTree.InternalNode
            Adds a internal node to the binary tree.

        """
        
        left = self.visit(node.left)
        right = self.visit(node.right)
        internal = BinaryTree.InternalNode(left, right)
        
        left.parent = internal #set parent
        right.parent = internal #setparent
        
        return internal
        
#######################################
### RUN
#######################################


def run(text):
    """
    Uses the Lexer, Parser and Interpreter to process the input.

    Parameters
    ----------
    text : String
        The input text, should be in newick format for binary trees.

    Returns
    -------
    result : BinaryTree
        Binary tree generated frome the input.
    Error
        Error, if there occures one.

    """
    #tokenize input
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    #parse input
    parser = Parser(tokens)
    parseTree = parser.parse()
    
    if parseTree.error: return None, parseTree.error
    
    #interpret parse tree
    
    interpreter = Interpreter()
    result = interpreter.getTree(parseTree.node)
    
    return result, None

