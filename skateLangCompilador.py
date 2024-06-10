import sys
from abc import abstractmethod


class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value


obstaculo = "CORRIMAO"


class PrePro():
    def filter(self, source):
        formattedText = ""
        i = 0
        while i < len(source):
            if source[i] == '-':
                if i + 1 < len(source) and source[i + 1] == '-':
                    allLineCommented = False
                    if source[i - 1] == '\n':
                        allLineCommented = True
                    i += 1
                    while i < len(source) and source[i] != '\n':
                        i += 1
                    if not allLineCommented:
                        formattedText += "\n"
                else:
                    formattedText += source[i]
            elif source[i] == '\n':
                if i != 0:
                    formattedText += source[i]
                while i + 1 < len(source) and source[i + 1] == '\n':
                    i += 1
            else:
                formattedText += source[i]
            i += 1

        return formattedText


class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self):
        pass


class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def Evaluate(self):
        pass


class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self):
        for child in self.children:
            if child is not None:
                child.Evaluate()


class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self):
        print(self.children[0])


class RelationalOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        children0 = self.children[0][0]
        children1 = self.children[1][1]
        if self.value == 'EQ':
            return [int(children0 == children1), 'int']
        elif self.value == 'NEQ':
            return [int(children0 != children1), 'int']
        else:
            raise Exception('Invalid operation')


class IfStatement(Node):
    def __init__(self, condition, if_block, else_block=None):
        super().__init__(None, [condition, if_block, else_block])

    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()
        elif self.children[2]:
            self.children[2].Evaluate()


class WhileLoop(Node):
    def __init__(self, condition, block):
        super().__init__(None, [condition, block])

    def Evaluate(self):
        while self.children[0].Evaluate()[0]:
            for statement in self.children[1]:
                statement.Evaluate()


class Tokenizer():
    def __init__(self, source, position=0, next=None):
        no_comments_source = PrePro().filter(source)
        self.source = no_comments_source
        self.position = position
        self.next = next
        self.reserved = ['enquanto', 'se', 'senao', 'execute', 'obstaculo', 'corrimao', 'rampa', 'escada', 'ollie', 'kickflip', 'grind', 'heelflip']

    def selectNext(self):
        while self.position < len(self.source) and (self.source[self.position] == ' ' or self.source[self.position] == '\t'):
            self.position += 1

        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.next = Token('NEW_LINE', '\n')
                self.position += 1
            elif self.source[self.position].isalpha():
                identifier = ''
                while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_'):
                    identifier += self.source[self.position]
                    self.position += 1
                if identifier in self.reserved:
                    self.next = Token(identifier.upper(), identifier)
                else:
                    self.next = Token('IDENTIFIER', identifier)
            elif self.source[self.position] == "=":
                self.position += 1
                if self.source[self.position] == "=":
                    self.next = Token('EQ', '==')
                    self.position += 1
                else:
                    self.next = Token('ASSIGN', '=')
            elif self.source[self.position] == '!':
                self.position += 1
                if self.source[self.position] == '=':
                    self.next = Token('NEQ', '!=')
                    self.position += 1
                else:
                    raise Exception('Unexpected token')
            elif self.source[self.position] == ';':
                self.position += 1
                self.next = Token(';', ';')
            elif self.source[self.position] == '{':
                self.position += 1
                self.next = Token('BRACK_OPEN', '{')
            elif self.source[self.position] == '}':
                self.position += 1
                self.next = Token('BRACK_CLOSE', '}')
            elif self.source[self.position] == '(':
                self.position += 1
                self.next = Token('PAR_OPEN', '(')
            elif self.source[self.position] == ')':
                self.position += 1
                self.next = Token('PAR_CLOSE', ')')
            else:
                raise Exception('Unexpected token')
        else:
            self.next = None


class Parser():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseBlock(self):
        children = []
        while self.tokenizer.next is not None:
            a = self.parseStatement()
            children.append(a)
        return Block(children)

    def parseStatement(self):
        global obstaculo
        if self.tokenizer.next.type == 'EXECUTE':
            self.tokenizer.selectNext()
            actions = ['ollie', 'kickflip', 'heelflip', 'grind']
            actionType = self.tokenizer.next.type
            if self.tokenizer.next.type.lower() not in actions:
                raise Exception('Invalid Syntax')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != ';':
                raise Exception('Invalid Syntax')
            self.tokenizer.selectNext()
            return Print([actionType])
        if self.tokenizer.next.type == 'OBSTACULO':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'ASSIGN':
                raise Exception('Unexpected Token')
            self.tokenizer.selectNext()
            obstaculos = ['CORRIMAO', 'RAMPA', 'ESCADA']
            obs = self.tokenizer.next.type
            if obs not in obstaculos:
                raise Exception('Unexpected Token')
            obstaculo = obs
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != ';':
                raise Exception('Unexpected Token')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
        elif self.tokenizer.next.type == 'SE':
            self.tokenizer.selectNext()
            condition = self.parseRelExpression()
            if self.tokenizer.next.type != 'BRACK_OPEN':
                raise Exception('Expected {')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
            if_block = self.parseStatement()
            if self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'BRACK_CLOSE':
                raise Exception('Expected }')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'SENAO':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != 'BRACK_OPEN':
                    raise Exception('Expected {')
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != 'NEW_LINE':
                    raise Exception('Expected \\n')
                self.tokenizer.selectNext()
                else_block = self.parseStatement()
                if self.tokenizer.next.type != 'BRACK_CLOSE':
                    raise Exception('Expected }')
                self.tokenizer.selectNext()
            else:
                else_block = None
            if self.tokenizer.next is not None and self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
            return IfStatement(condition, if_block, else_block)
        elif self.tokenizer.next.type == 'ENQUANTO':
            self.tokenizer.selectNext()
            condition = self.parseRelExpression()
            if self.tokenizer.next.type != 'BRACK_OPEN':
                raise Exception('Expected {')
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
            statements = []
            while self.tokenizer.next.type != 'BRACK_CLOSE':
                statements.append(self.parseStatement())
            self.tokenizer.selectNext()
            if self.tokenizer.next is not None and self.tokenizer.next.type != 'NEW_LINE':
                raise Exception('Expected \\n')
            self.tokenizer.selectNext()
            return WhileLoop(condition, statements)
        elif self.tokenizer.next.type == 'NEW_LINE':
            self.tokenizer.selectNext()
            return NoOp()
        else:
            raise Exception('Unexpected token')

    def parseFactor(self):
        if (self.tokenizer.next.type == 'OBSTACULO'):
            self.tokenizer.selectNext()
            return [obstaculo, 'OBSTACULO']
        elif self.tokenizer.next.type == 'CORRIMAO':
            self.tokenizer.selectNext()
            return [obstaculo, 'CORRIMAO']
        elif self.tokenizer.next.type == 'RAMPA':
            self.tokenizer.selectNext()
            return [obstaculo, 'RAMPA']
        elif self.tokenizer.next.type == 'ESCADA':
            self.tokenizer.selectNext()
            return [obstaculo, 'ESCADA']
        if self.tokenizer.next is not None and self.tokenizer.next.type == 'PAR_OPEN':
            self.tokenizer.selectNext()
            number = self.parseRelExpression()
            if self.tokenizer.next.type != 'PAR_CLOSE':
                raise Exception('Unexpected token')
            self.tokenizer.selectNext()
            return number
        else:
            raise Exception('Unexpected token')

    def parseRelExpression(self):
        result = self.parseFactor()
        if self.tokenizer.next.type in ['EQ', 'NEQ']:
            token_type = self.tokenizer.next.type
            self.tokenizer.selectNext()
            return RelationalOp(token_type, [result, self.parseFactor()])
        else:
            return result

    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        result = self.parseBlock()
        result = result.Evaluate()
        if self.tokenizer.next is not None:
            raise Exception('Unexpected token')
        return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py 'expression'")
        sys.exit(1)

    file = sys.argv[1]

    if not file.endswith(".lua"):
        print("Invalid file extension")
        sys.exit(1)

    with open(file, 'r') as f:
        expression = f.read()

    tokenizer = Tokenizer(expression)
    parser = Parser(tokenizer)
    parser.run(expression)
