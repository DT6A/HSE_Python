import ast

import astunparse
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.pyplot import figure
from networkx.drawing.nx_pydot import graphviz_layout


class viz_walker(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.graph = nx.Graph()
        self.names = {}
        self.labeldict = {}
        self.colors = []

    def generic_visit(self, stmt):
        node_name = stmt.__class__.__name__
        if node_name in ['Load', 'LtE', 'Eq', 'Store', 'Sub', 'USub', 'Add']:
            return

        unp = astunparse.unparse(stmt).split()
        suf = ''
        color = 'lightblue'

        if node_name == 'Compare':
            suf = unp[1]
        elif node_name == 'Num':
            node_name = 'Constant'
            suf = unp[0]
            color = 'lightyellow'
        elif node_name == 'Name':
            node_name = 'Variable'
            # suf = 'Name: ' + unp[0]
            suf = f"`{unp[0]}`"
            color = 'lightgreen'
        elif node_name == 'Attribute':
            # suf = 'Name: ' + unp[0].split('.')[1]
            suf = f"`{unp[0].split('.')[1]}`"
            color = 'lightgreen'
        elif node_name == 'Call':
            color = 'lightcoral'
        elif node_name == 'BinOp':
            suf = unp[len(unp) // 2]
        elif node_name == 'UnaryOp':
            suf = unp[0][1]
        elif node_name == 'arg':
            node_name = 'Arg'
            suf = f"`{unp[0]}`"
            color = 'lightgreen'
        elif node_name == 'FunctionDef':
            node_name = 'FuncDef'

        if suf:
            node_name += f'\n{suf}'
        display_name = node_name

        if node_name not in self.names:
            self.names[node_name] = 0
        else:
            self.names[node_name] += 1
            node_name = node_name + "`" * self.names[node_name]
        self.labeldict[node_name] = display_name
        self.colors.append(color)

        parent_name = None

        if self.stack:
            parent_name = self.stack[-1]

        self.stack.append(node_name)

        self.graph.add_node(node_name)

        if parent_name:
            self.graph.add_edge(node_name, parent_name)

        super(self.__class__, self).generic_visit(stmt)

        self.stack.pop()


if __name__ == '__main__':
    figure(figsize=(20, 15))

    src = """
def fib(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]

    nums = [0, 1]
    for i in range(n - 2):
        nums.append(nums[-1] + nums[-2])

    return nums
    """
    ast_object = ast.parse(src)
    tree = ast.dump(ast_object)

    mw = viz_walker()

    mw.visit(ast_object)

    plt.figure(3, figsize=(20, 20), dpi=100)
    pos = graphviz_layout(mw.graph, prog="dot")
    nx.draw(mw.graph, pos, labels=mw.labeldict,
            node_shape="s", node_size=1200,
            font_size=7, with_labels=True,
            node_color=mw.colors)
    plt.savefig('result.png')
