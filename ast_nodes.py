# ast_nodes.py - Clases del árbol de sintaxis abstracta (AST)

class NumberNode:
    def __init__(self, valor):
        self.valor = valor

class VarNode:
    def __init__(self, nombre):
        self.nombre = nombre

class BinaryOpNode:
    def __init__(self, op, izq, der):
        self.op = op
        self.izq = izq
        self.der = der

class UnaryOpNode:  # Añadido para el menos unario de la ampliación
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class AssignNode:
    def __init__(self, nombre, expr):
        self.nombre = nombre
        self.expr = expr

class PrintNode:
    def __init__(self, expr):
        self.expr = expr

class IfNode:
    def __init__(self, cond, entonces, si_no=None):
        self.cond = cond
        self.entonces = entonces
        self.si_no = si_no

def muestra(nodo, sangria=0):
    s = "    " * sangria
    if isinstance(nodo, list):
        for n in nodo:
            muestra(n, sangria)
    elif isinstance(nodo, NumberNode):
        print(s + "Número", nodo.valor)
    elif isinstance(nodo, VarNode):
        print(s + "Variable", nodo.nombre)
    elif isinstance(nodo, BinaryOpNode):
        print(s + "Operación", nodo.op)
        muestra(nodo.izq, sangria + 1)
        muestra(nodo.der, sangria + 1)
    elif isinstance(nodo, UnaryOpNode):
        print(s + "Operación Unaria", nodo.op)
        muestra(nodo.expr, sangria + 1)
    elif isinstance(nodo, AssignNode):
        print(s + "Asignación", nodo.nombre)
        muestra(nodo.expr, sangria + 1)
    elif isinstance(nodo, PrintNode):
        print(s + "Print")
        muestra(nodo.expr, sangria + 1)
    elif isinstance(nodo, IfNode):
        print(s + "If")
        muestra(nodo.cond, sangria + 1)
        print(s + "Entonces")
        muestra(nodo.entonces, sangria + 1)
        if nodo.si_no is not None:
            print(s + "Si no")
            muestra(nodo.si_no, sangria + 1)