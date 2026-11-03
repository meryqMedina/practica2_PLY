# parser.py - Analizador sintáctico y traductor a AST
from analizador import tokens, lexer
from ast_nodes import *

# Definición de la tabla de precedencia y asociatividad (Apartado 3.3 y 3.6)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQ', 'GT', 'LT', 'GE', 'LE', 'NE'), # Comparaciones sin asociatividad
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'), # Menos unario
)

def p_programa(p):
    '''programa : lista_sentencias'''
    p[0] = p[1]

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_sentencia_asignacion(p):
    '''sentencia : ID ASSIGN expresion PUNTOCOMA'''
    p[0] = AssignNode(p[1], p[3])

def p_sentencia_print(p):
    '''sentencia : PRINT expresion PUNTOCOMA'''
    p[0] = PrintNode(p[2])

def p_sentencia_if(p):
    '''sentencia : IF expresion DOSPUNTOS lista_sentencias ELSE DOSPUNTOS lista_sentencias ENDIF PUNTOCOMA
                 | IF expresion DOSPUNTOS lista_sentencias ENDIF PUNTOCOMA'''
    if len(p) == 10:
        p[0] = IfNode(p[2], p[4], p[7])
    else:
        p[0] = IfNode(p[2], p[4])

def p_expresion_binaria(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MOD expresion
                 | expresion EQ expresion
                 | expresion GT expresion
                 | expresion LT expresion
                 | expresion GE expresion
                 | expresion LE expresion
                 | expresion NE expresion
                 | expresion AND expresion
                 | expresion OR expresion'''
    p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_expresion_unaria(p):
    '''expresion : MINUS expresion %prec UMINUS
                 | NOT expresion'''
    p[0] = UnaryOpNode(p[1], p[2])

def p_expresion_grupo(p):
    '''expresion : LPAREN expresion RPAREN'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : NUMBER'''
    p[0] = NumberNode(p[1])

def p_expresion_variable(p):
    '''expresion : ID'''
    p[0] = VarNode(p[1])

def p_error(p):
    if p:
        print(f"Error sintáctico: Token '{p.type}' inesperado (valor: '{p.value}') en la línea {p.lineno}")
    else:
        print("Error sintáctico: Fin de fichero inesperado (falta algún cierre como ENDIF o punto y coma).")

import ply.yacc as yacc
parser = yacc.yacc()