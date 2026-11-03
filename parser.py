# parser.py - Analizador sintáctico y traductor a AST
from analizador import tokens, lexer
from ast_nodes import *

# Tabla de precedencia y asociatividad con los tokens reales de la Práctica 1
precedence = (
    ('nonassoc', 'EQUALS', 'GREATER_THAN', 'LESS_THAN'),
    ('left', 'ADD', 'SUBTRACT'),
    ('left', 'MULTIPLY', 'DIVIDE', 'REMAINDER'),
    ('right', 'UMINUS'), # Menos unario para la ampliación
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
    '''sentencia : ID ASSIGNMENT expresion SEMICOLON'''
    p[0] = AssignNode(p[1], p[3])

def p_sentencia_print(p):
    '''sentencia : PRINT expresion SEMICOLON'''
    p[0] = PrintNode(p[2])

def p_sentencia_if(p):
    '''sentencia : IF expresion COLON lista_sentencias ELSE COLON lista_sentencias ENDIF SEMICOLON
                 | IF expresion COLON lista_sentencias ENDIF SEMICOLON'''
    if len(p) == 10:
        p[0] = IfNode(p[2], p[4], p[7])
    else:
        p[0] = IfNode(p[2], p[4])

def p_expresion_binaria(p):
    '''expresion : expresion ADD expresion
                 | expresion SUBTRACT expresion
                 | expresion MULTIPLY expresion
                 | expresion DIVIDE expresion
                 | expresion REMAINDER expresion
                 | expresion EQUALS expresion
                 | expresion GREATER_THAN expresion
                 | expresion LESS_THAN expresion'''
    p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_expresion_unaria(p):
    '''expresion : SUBTRACT expresion %prec UMINUS'''
    p[0] = UnaryOpNode(p[1], p[2])

def p_expresion_grupo(p):
    '''expresion : OPEN_PARENTHESIS expresion CLOSED_PARENTHESIS'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : LIT_INT
                 | LIT_FLOAT'''
    p[0] = NumberNode(p[1])

def p_expresion_variable(p):
    '''expresion : ID'''
    p[0] = VarNode(p[1])

def p_error(p):
    if p:
        print(f"Error sintáctico: Token '{p.type}' inesperado (valor: '{p.value}') en la línea {p.lineno}")
    else:
        print("Error sintáctico: Fin de fichero inesperado (falta cerrar un bloque como ENDIF o un punto y coma).")

import ply.yacc as yacc
parser = yacc.yacc()


# --- BLOQUE DE PRUEBAS ---
if __name__ == '__main__':
    print("==========================================")
    print(" 1. PRUEBA DEL PROGRAMA PRINCIPAL")
    print("==========================================")
    codigo_principal = """
    precio = 12.5;
    unidades = 4;
    total = precio * unidades - 3;
    IF total > (unidades + 30):
        PRINT total;
        total = total - 10;
    ELSE:
        PRINT 0;
    ENDIF;
    """
    lexer.input(codigo_principal)
    ast = parser.parse(lexer=lexer)
    if ast:
        muestra(ast)

    print("\n==========================================")
    print(" 2. PRUEBAS DE PRECEDENCIA")
    print("==========================================")
    print("Prueba: x = 2 + 3 * 4;")
    lexer.input("x = 2 + 3 * 4;")
    muestra(parser.parse(lexer=lexer))

    print("\n==========================================")
    print(" 3. PRUEBA DE AMPLIACIÓN (Menos unario y Módulo)")
    print("==========================================")
    print("Prueba: x = -5 + 10 % 3;")
    lexer.input("x = -5 + 10 % 3;")
    muestra(parser.parse(lexer=lexer))

    print("\n==========================================")
    print(" 4. PRUEBAS DE ERRORES SINTÁCTICOS")
    print("==========================================")
    print("Caso A (Falta punto y coma): x = 15")
    parser.parse("x = 15", lexer=lexer)

    print("\nCaso B (Condición incompleta): IF x > :")
    parser.parse("IF x > :", lexer=lexer)