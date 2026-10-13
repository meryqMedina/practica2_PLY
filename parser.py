"""Practica 2: analisis sintactico y construccion del AST con PLY yacc.

Utiliza los nombres de tokens de la Practica 1 del Grupo 3.
La construccion adicional elegida (apartado 3.6) es el modulo (%).
"""
import ply.yacc as yacc
from analizador import tokens, lexer
from ast_nodes import *

# Orden de menor a mayor precedencia (apartado 3.3).
precedence = (
    ('nonassoc', 'EQUALS', 'GREATER_THAN', 'LESS_THAN'),
    ('left', 'ADD', 'SUBTRACT'),
    ('left', 'MULTIPLY', 'DIVIDE', 'REMAINDER'),
)

# Simbolo inicial: lista de instrucciones.
start = 'programa'
hubo_error = False


def p_programa(p):
    'programa : lista_sentencias'
    p[0] = p[1]


def p_lista_sentencias_varias(p):
    'lista_sentencias : lista_sentencias sentencia'
    p[0] = p[1] + [p[2]]


def p_lista_sentencias_una(p):
    'lista_sentencias : sentencia'
    p[0] = [p[1]]


def p_sentencia_asignacion(p):
    'sentencia : ID ASSIGNMENT expresion SEMICOLON'
    p[0] = AssignNode(p[1], p[3])


def p_sentencia_print(p):
    'sentencia : PRINT expresion SEMICOLON'
    p[0] = PrintNode(p[2])


def p_sentencia_if(p):
    '''sentencia : IF expresion COLON lista_sentencias ENDIF SEMICOLON
                 | IF expresion COLON lista_sentencias ELSE COLON lista_sentencias ENDIF SEMICOLON'''
    if len(p) == 7:
        p[0] = IfNode(p[2], p[4])
    else:
        p[0] = IfNode(p[2], p[4], p[7])


def p_expresion_aritmetica(p):
    '''expresion : expresion ADD expresion
                 | expresion SUBTRACT expresion
                 | expresion MULTIPLY expresion
                 | expresion DIVIDE expresion
                 | expresion REMAINDER expresion'''
    p[0] = BinaryOpNode(p[2], p[1], p[3])


def p_expresion_comparacion(p):
    '''expresion : expresion EQUALS expresion
                 | expresion GREATER_THAN expresion
                 | expresion LESS_THAN expresion'''
    p[0] = BinaryOpNode(p[2], p[1], p[3])


def p_expresion_grupo(p):
    'expresion : OPEN_PARENTHESIS expresion CLOSED_PARENTHESIS'
    p[0] = p[2]


def p_expresion_numero(p):
    '''expresion : LIT_INT
                 | LIT_FLOAT'''
    p[0] = NumberNode(p[1])


def p_expresion_variable(p):
    'expresion : ID'
    p[0] = VarNode(p[1])


def p_error(p):
    global hubo_error
    hubo_error = True
    if p is None:
        print('Error sintactico: fin inesperado del programa (falta algo, por ejemplo ENDIF).')
    else:
        print('Error sintactico: token %s, valor %r, linea %d' %
              (p.type, p.value, p.lineno))


analizador_sintactico = yacc.yacc(debug=False, write_tables=False)


def analizar(codigo):
    global hubo_error
    hubo_error = False
    lexer.lineno = 1
    resultado = analizador_sintactico.parse(codigo, lexer=lexer)
    if hubo_error or resultado is None:
        print('No se genera AST: programa con errores sintacticos.')
        return None
    muestra(resultado)
    return resultado


if __name__ == '__main__':
    pruebas = [
        ('Principal (apartado 3.7)', '''precio = 12.5;
unidades = 4;
total = precio * unidades - 3;
IF total > (unidades + 30) :
    PRINT total;
    total = total - 10;
ELSE :
    PRINT 0;
ENDIF;'''),
        ('Precedencia: suma y multiplicacion', 'x = 2 + 3 * 4;'),
        ('Precedencia: resta por la izquierda', 'x = 10 - 3 - 2;'),
        ('Comparacion encadenada: debe fallar', 'x = a < b < c;'),
        ('Construccion nueva: modulo', 'x = 10 % 3;'),
        ('IF sin ELSE', 'IF x > 0 : PRINT x; ENDIF;'),
        ('Error: falta punto y coma', 'x = 5'),
        ('Error: condicion incompleta', 'IF x > : PRINT x; ENDIF;'),
    ]
    for nombre, codigo in pruebas:
        print('\n' + '=' * 60)
        print(nombre)
        print('=' * 60)
        analizar(codigo)
