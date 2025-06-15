import math
import ast
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def root(n, x):
    return x ** (1 / n)

allowed_funcs = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log,
    'root': root,
    'pow': math.pow,
    'pi': math.pi,
    'e': math.e,}

def eval_expr(expr):
    try:
        tree = ast.parse(expr, mode='eval')
        return str(_eval(tree.body))
    except Exception as e:
        return f"Error: {str(e)}"

def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp): 
        return operators[type(node.op)](_eval(node.operand))
    elif isinstance(node, ast.Call): 
        func_name = node.func.id
        if func_name in allowed_funcs:
            args = [_eval(arg) for arg in node.args]
            return allowed_funcs[func_name](*args)
        else:
            raise ValueError(f"Unsupported function: {func_name}")
    elif isinstance(node, ast.Name):
        if node.id in allowed_funcs:
            return allowed_funcs[node.id]
        else:
            raise ValueError(f"Unsupported variable or constant: {node.id}")
    else:
        raise TypeError(f"Unsupported expression: {node}")

