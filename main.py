import ast
import astor
import random

class RenameIdentifiers(ast.NodeTransformer):
    def __init__(self):
        self.rename_map = {}

    def gen_random_names(self):
        return 'n' + ''.join(random.choices('0n_', k=random.randint(50, 100))) + '__' + ''.join(random.choices('0n_', k=random.randint(1000, 2000))) + 'n'

    def FunctionDef(self, node):
        new_name = self.gen_random_names()
        self.rename_map[node.name] = new_name
        node.name = new_name
        for arg in node.args.args:
            new_arg_name = self.gen_random_names()
            self.rename_map[arg.arg] = new_arg_name
            arg.arg = new_arg_name
        self.generic_visit(node)
        return node

    def ClassDef(self, node):
        new_name = self.gen_random_names()
        self.rename_map[node.name] = new_name
        node.name = new_name
        self.generic_visit(node)
        return node

    def Name(self, node):
        if node.id == 'print':
            return node
        if node.id not in self.rename_map:
            new_name = self.gen_random_names()
            self.rename_map[node.id] = new_name
        node.id = self.rename_map[node.id]
        return node

    def Attribute(self, node):
        if node.attr not in self.rename_map:
            new_name = self.gen_random_names()
            self.rename_map[node.attr] = new_name
        node.attr = self.rename_map[node.attr]
        self.generic_visit(node)
        return node

    def Import(self, node):
        for alias in node.names:
            new_alias = self.gen_random_names()
            self.rename_map[alias.asname if alias.asname else alias.name] = new_alias
            alias.asname = new_alias
        return node

    def ImportFrom(self, node):
        if node.module:
            new_alias = self.gen_random_names()
            self.rename_map[node.module] = new_alias
            node.module = new_alias
        return node

def obfuscation(source_code):
    tree = ast.parse(source_code)
    transformer = RenameIdentifiers()
    transformed_tree = transformer.visit(tree)
    return astor.to_source(transformed_tree)

code = """  """ # put your code to obfuscate

obf_code = obfuscation(code)

with open('obfuscated_code.py', 'w') as file: # in this file save new code
    file.write(obf_code)
