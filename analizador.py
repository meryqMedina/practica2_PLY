"""Analizador lexico de la Practica 1, adaptado a los nuevos enunciados de P2."""
import ply.lex as lex

# Palabras reservadas de la Practica 1 y las necesarias en Practica 2.
palabras_reservadas = {
    'break': 'BREAK', 'do': 'DO', 'else': 'ELSE',
    'float': 'FLOAT', 'for': 'FOR', 'if': 'IF',
    'int': 'INT', 'while': 'WHILE', 'repeat': 'KW_REPEAT',
    'IF': 'IF', 'ELSE': 'ELSE', 'ENDIF': 'ENDIF', 'PRINT': 'PRINT',
}

tokens = tuple(set(palabras_reservadas.values())) + (
    'ID', 'LIT_INT', 'LIT_FLOAT',
    'GREATER_THAN', 'GREATER_EQUALS', 'LESS_THAN', 'LESS_EQUALS',
    'EQUALS', 'NOT_EQUALS', 'ASSIGNMENT',
    'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'REMAINDER',
    'AND', 'OR', 'NOT', 'BITWISE_AND', 'BITWISE_OR',
    'SEMICOLON', 'OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS',
    'OPEN_SQUARE_BRACKET', 'CLOSED_SQUARE_BRACKET',
    'OPEN_BRACKET', 'CLOSED_BRACKET', 'END_PROGRAM', 'COLON',
)

t_ignore = ' \t'


def t_LIT_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_LIT_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t


def t_newline(t):
    r'(\r\n|\r|\n)'
    t.lexer.lineno += 1


t_GREATER_EQUALS = r'>='
t_LESS_EQUALS = r'<='
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'
t_ASSIGNMENT = r'='
t_ADD = r'\+'
t_SUBTRACT = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_REMAINDER = r'%'
t_NOT = r'!'
t_BITWISE_AND = r'&'
t_BITWISE_OR = r'\|'
t_SEMICOLON = r';'
t_OPEN_PARENTHESIS = r'\('
t_CLOSED_PARENTHESIS = r'\)'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSED_SQUARE_BRACKET = r'\]'
t_OPEN_BRACKET = r'\{'
t_CLOSED_BRACKET = r'\}'
t_END_PROGRAM = r'\#'
t_COLON = r':'


def t_error(t):
    ultimo_salto = max(t.lexer.lexdata.rfind('\n', 0, t.lexpos),
                       t.lexer.lexdata.rfind('\r', 0, t.lexpos))
    columna = t.lexpos - ultimo_salto
    print('Error lexico: caracter no valido %r en linea %d, columna %d' %
          (t.value[0], t.lexer.lineno, columna))
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':
    entrada = 'total = precio * 4;\nIF total > 3 : PRINT total; ENDIF;'
    lexer.input(entrada)
    for tok in lexer:
        print(tok)
