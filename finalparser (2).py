#Project 4 Types 
#Zetao Yang 931001023
#Xianglu Peng  930990871
#!/usr/bin/python3


import re, sys, string

debug = False
dict = { }
tokens = [ ]


class Lexer :
	
	
	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text )
		self.position = 0
		self.indent = [ 0 ]
	
	
	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def next( self ) :
		self.position = self.position + 1
		return self.peek( )

	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"
   


def error( msg ):
	#print msg
	sys.exit(msg)


def match(matchtok):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok





# Expression class and subclasses

class Expression( object ):
	def __str__(self):
		return "" 
	
class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
		
	def __str__(self):
		return str(self.op) + " " + str(self.left) + " " + str(self.right)


## New - meaning of an expression is always a value
	def value(self, state):
		left = self.left.value(state)
		right = self.right.value(state)
#and and or 
		if self.op == "and":
			return left and right
		elif self.op == "or":
			return left or right
#Arithmetic 
		elif self.op == "+":
			return left + right
		elif self.op == "-":
			return left - right
		elif self.op == "*":
			return left * right
		elif self.op == "/":
#relational 
			return left / right
		elif self.op == ">":
			return left > right
		elif self.op == "<":
			return left < right
		elif self.op == ">=":
			return left >= right
		elif self.op == "<=":
			return left <= right
		elif self.op == "==":
			return left == right
		elif self.op == "!=":
			return left != right

	def tipe(self, tm):
		Ltype = self.left.tipe(tm)
		Rtype = self.right.tipe(tm)

		if Ltype != Rtype:
			error("Type Error: Invalid operation")
		
		if self.op in ['and','or','>','<','<=','>=','==','!=']:
			 return "boolean"

		if Ltype == "number" and self.op in ['+','-','*','/']:
			 return "number"
		

    
class Number( Expression ):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return str(self.value)
	def value(self, state):
		return int(self.val)
	def tipe(self, tm):
		return "number"


#Build classes for ident (VarRef) and string (String) and add the necessary logic to factor.
class VarRef( Expression ):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return str(self.value)
	def value(self,state):
		return state[self.val]
	def tipe(self, tm):
		if self.val not in tm:
			error("Type Error: " + self.val + " is referenced before being defined!")
		else:
			return tm[self.val]

class String(Expression ):
	def __init__(self, value):
		self.val = value
	def __str__(self):
		return str(self.value)
	def value(self, state):
		return self.val
	def tipe(self, tm):
		error("Error: No string type ")



#Expression grammar

# expression = andExpr { "or" andExpr }
# andExpr    = relationalExpr { "and" relationalExpr }
# relationalExpr = addExpr [ relation addExpr ]
# addExpr    = term { ("+" | "-") term }
# term       = factor { ("*" | "/") factor }
# factor     = number | string | ident |  "(" expression ")" 




#Build parse routines for the expression nonterminals:
# expression, andExpr, relationalExpr


def expression():
	tok = tokens.peek( )
	if debug: print ("expression: ", tok)
	left = andExpr( )
	tok = tokens.peek( )
	while tok == "or":
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def andExpr():
	tok = tokens.peek( )
	if debug: print ("andExpr: ", tok)
	left =  relationalExpr( )
	tok = tokens.peek( )
	while tok == "and":
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def relationalExpr():
	tok = tokens.peek( )
	if debug: print ("relationalExpr: ", tok)
	left = addExpr( )
	tok = tokens.peek( )
	while re.match(Lexer.relational, tok):
		tokens.next()
		right = addExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left




def factor( ):
    # add identifier and string 
	tok = tokens.peek( )
	if debug: print ("Factor: ", tok)
	if re.match(Lexer.number, tok):
		expr = Number(tok)
		tokens.next( )
		return expr

	elif re.match(Lexer.identifier, tok):
		expr = VarRef(tok)
		tokens.next()
		return expr
	
	elif re.match(Lexer.string, tok):
		expr = String(tok)
		tokens.next()
		return expr

	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = expression( )
		tokens.peek( )
		tok = match(")")
		return expr
	

	error("Operand Error")
	return


def term( ):
	""" term    = factor { ('*' | '/') factor } """
	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

def addExpr( ):
	""" addExpr    = term { ('+' | '-') term } """
	tok = tokens.peek( )
	if debug: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		tokens.next()
		right = term( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left












#bulid statement class
class StatementList( object ):
	def __init__(self):
		self.statementList = []

	def addStatement(self, statement):
		self.statementList.append(statement)

	def __str__(self):
		Str = ''
		for statement in self.statementList:
			Str += str(statement)
		return Str
#new meaning function 
	def meaning(self,state):
		for statement in self.statementList:
			statement.meaning(state)
		return state
	

	def tipe(self, tm):
		for statement in self.statementList:
			statement.tipe(tm)



# Statement class and subclasses
class Statement( object ):
	def __str__(self):
		return ""

class Assignment( Statement ):
	def __init__(self, identifier, expression):
		self.expression = expression
		self.identifier = identifier
		
	def __str__(self):
		return "= " + str(self.identifier) + " " + str(self.expression) + "\n"
    ## new 
	def meaning(self, state):
		state[self.identifier] = self.expression.value(state)
		return state
    

	def tipe(self, tm):
		tipe = self.expression.tipe(tm)
		if tipe == " ":
			error("Error: Undefined Variable")

		if self.identifier not in tm:
			tm[self.identifier] = tipe

			print (self.identifier,tipe)

		elif tm[self.identifier] != tipe:
			error("Type Error: " + tm[self.identifier] + " = " + tipe + "!")


class WhileStatement( Statement ):
	def __init__(self, expression, block):
		self.expression = expression
		self.block = block
	def __str__(self):
		return "while " + str(self.expression) + "\n" + str(self.block) + "endwhile\n"
    
	def meaning(self, state):
		while self.expression.value(state):
			self.block.meaning(state)

	def tipe(self, tm):
		if self.expression.tipe(tm) != "boolean":
			error("Type Error: No boolean in while loop ")
		self.block.tipe(tm)
    

class IfStatement( Statement ):
	def __init__(self, expression, ifBlock, elseBlock):
		self.expression = expression
		self.ifBlock = ifBlock
		self.elseBlock = elseBlock

	def __str__(self):
		return "if " + str(self.expression) + "\n" + str(self.ifBlock) + "else\n" + str(self.elseBlock) + "endif\n"

	def meaning(self, state):
		if self.expression.value(state):
			self.ifBlock.meaning(state)
		else:
			if self.elseBlock != "":
				self.elseBlock.meaning(state)
		return state
    
	def tipe(self, tm):
		if self.expression.tipe(tm) != "boolean":
			error("Type Error: No boolean in IF statement")

		self.ifBlock.tipe(tm)

		if self.elseBlock != "":
			self.elseBlock.tipe(tm)

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.
def parse( text ) :
	global tokens
	tokens = Lexer( text )
	# expr = addExpr( )
	# print (str(expr))
	#     Or:
	stmtlist = parseStmtList()
	#print (stmtlist)
	return stmtlist


#statement grammar
# stmtList =  {  statement  }
# statement = ifStatement |  whileStatement  |  assign
# assign = ident "=" expression  eoln
# ifStatement = "if" expression block   [ "else" block ] 
# whileStatement = "while"  expression  block
# block = ":" eoln indent stmtList undent

def parseStmtList(  ):

	tok = tokens.peek( )
	statementList = StatementList()
	while tok not in [None ,"~"]: 
		statement = parseStatement()
		statementList.addStatement(statement)
		tok = tokens.peek()
	return statementList


def parseStatement():

	tok = tokens.peek()
	if debug: print ("Statement: ", tok)
	if tok == "if":
		return parseIf()
	elif tok == "while":
		return parseWhile()
	elif re.match(Lexer.identifier, tok):
		return Assign()
	error("Invalid not if or while statement")
	return


def Assign():

	identifier = tokens.peek()
	if debug: print ("Assign statement:")

	if tokens.next() != "=":
		error("TThere is no equal sign")
	tokens.next()
	exp = expression()

	tok = tokens.peek()
	if tok != ";":
		error("No end of line.")
	tokens.next()
	return Assignment(identifier, exp)
	


def parseIf():
	tok = tokens.next()
	if debug: print ("If statement: ", tok)
	expr = expression()
	ifBlock = parseBlock()
	elseBlock = ''
	if tokens.peek() == "else":
		tok = tokens.next()
		if debug: print ("Else statement: ", tok)
		elseBlock = parseBlock()

	return IfStatement(expr, ifBlock, elseBlock)


def parseWhile():
	tok = tokens.next()
	if debug: print ("While statement: ", tok)
	expr = expression()
	block = parseBlock()
	return WhileStatement(expr, block)


# block = ":" eoln indent stmtList undent
def parseBlock():

	tok = tokens.peek()
	if debug: print ("Block: ", tok)
	
	if tok != ":":
		error("There is no : sign ")
	tok = tokens.next()

	if tok != ";":
		error("Block is missing end of line character.")
	tok = tokens.next()

	if tok != "@":
		error("No identation")
	tok = tokens.next()

	stmtList = parseStmtList()

	if tokens.peek() != "~":
		error("it is unidented")
	tokens.next()

	return stmtList




def semanticState(statementList):
	statedic = {}
	statedic = statementList.meaning(statedic)
	print ("\n" + printState(statedic))
	return



def printState(stateDictionary):
	line = "{"
	for key, value in stateDictionary.items():
		line += "<" + str(key) + ", " + str(value) + ">, " 
	return line[:-2] + "}"


def typechecker(statementList):
	tc = {} 
	statementList.tipe(tc)



#Do not need to change 


def chkIndent(line):
	ct = 0
	for ch in line:
		if ch != " ": return ct
		ct += 1
	return ct
		

def delComment(line):
	pos = line.find("#")
	if pos > -1:
		line = line[0:pos]
		line = line.rstrip()
	return line


def mklines(filename):
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
		#print (line, end = "")
		ct += 1
		line = line.rstrip( )+";"
		line = delComment(line)
		if len(line) == 0 or line == ";": continue
		indent = chkIndent(line)
		line = line.lstrip( )
		if indent > pos[-1]:
			pos.append(indent)
			line = '@' + line
		elif indent < pos[-1]:
			while indent < pos[-1]:
				del(pos[-1])
				line = '~' + line
		
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines



def main():
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	statement = parse("".join(mklines(sys.argv[1+ct])))
	#semanticState(statement)
	typechecker(statement)
	return

main()

