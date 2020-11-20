import ast

class Test:
    def __init__(self):
        self.test = 3


test = Test()
print(str(test))
print(ast.literal_eval(repr(test)))