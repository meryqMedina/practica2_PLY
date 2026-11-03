"""Analizador sintactico de la practica 2."""
import ply.yacc as yacc
from analizador import tokens, lexer
from ast_nodes import *

precedence = (
    ('nonassoc', 'EQUALS', 'GREATER_THAN', 'LESS_THAN'),
    ('left', 'ADD', 'SUBTRACT'),
    ('left', 'MULTIPLY', 'DIVIDE', 'REMAINDER'),
)

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
        print('Error en la sintaxis: el programa termina antes de tiempo. '
              'Puede faltar un punto y coma (;), una expresion o ENDIF.')
    else:
        if p.type == 'COLON':
            explicacion = 'Puede faltar una expresion antes de los dos puntos (:).'
        elif p.type == 'SEMICOLON':
            explicacion = 'Puede faltar una expresion antes del punto y coma (;).'
        elif p.type in ('ELSE', 'ENDIF'):
            explicacion = 'Revisa las instrucciones del IF y sus separadores.'
        else:
            explicacion = 'Puede faltar algun simbolo o haber una instruccion mal escrita.'
        print('Error en la sintaxis, linea %d: token %s, valor %r. %s' %
              (p.lineno, p.type, p.value, explicacion))


analizador_sintactico = yacc.yacc(debug=False, write_tables=False)


def analizar(codigo):
    global hubo_error
    hubo_error = False
    lexer.lineno = 1
    resultado = analizador_sintactico.parse(codigo, lexer=lexer)
    if hubo_error or resultado is None:
        print('No se ha podido crear el arbol por un error de sintaxis.')
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
        ('Arbol de la asignacion total', 'total = precio * unidades - 3;'),
        ('Precedencia: suma y multiplicacion', 'x = 2 + 3 * 4;'),
        ('Precedencia: resta por la izquierda', 'x = 10 - 3 - 2;'),
        ('Comparacion encadenada: debe fallar', 'x = a < b < c;'),
        ('Construccion nueva: modulo', 'x = 10 % 3;'),
        ('IF sin ELSE', 'IF x > 0 : PRINT x; ENDIF;'),
        ('Error: falta punto y coma', 'x = 5'),
        ('Error: condicion incompleta', 'IF x > : PRINT x; ENDIF;'),
    ]
    for nombre, codigo in pruebas:
        print()
        print(nombre)
        print('Codigo:')
        print(codigo)
        print('Resultado:')
        analizar(codigo)
