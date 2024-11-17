import ply.lex as lex
import ply.yacc as yacc
import math
print("Введите название файла: ")
filename = input()
# Определение лексера
tokens = (
    'ID',
    'ASSIGN',
    'INT',
    'PRINT',
    'SEMICOLON',
    'STR',
    'PLUS',
    'MINUS',
    'LET',
    'LPAREN',
    'RPAREN',
    'MULT',
    'DIVIDE',
    'DEGREE',
    'STRS',
    'SQRT',
    'WHILE',
    'MORE',
    'NOTMORE',
    'LFPAREN',
    'RFPAREN',
    'IF',
)
t_MINUS = r'-'
t_PLUS = r'\+'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MULT = r'\*'
t_DIVIDE = r'\/'
t_DEGREE = r'\*\*'
t_MORE = r'\>'
t_NOTMORE = r'\<'
t_LFPAREN = r'\{'
t_RFPAREN = r'\}'

def t_IF(t):
    r'if'
    t.type = 'IF'
    return t

def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    return t

def t_SQRT(t):
    r'sqrt'
    t.type = 'SQRT'
    return t

def t_STRS(t):
    r'str'
    t.type = 'STRS'
    return t

def t_PRINT(t):
    r'print'
    t.type = 'PRINT'
    return t

def t_LET(t):
    r'let'
    t.type = 'LET'
    return t

def t_ID(t):
    r'[a-zA-Z_а-яА-Я][a-zA-Z0-9_а-яА-Я]*'
    t.type = 'ID'
    return t

def t_STR(t):
    r'\"[^\"]*\"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'
#! Не менять! {
def t_error(t):
    print(f"Неверный символ: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
variables = {}
#! }

def p_expression(p):
    '''
    expression : STR
               | INT
               | ID
               | comparison
    '''
    p[0] = p[1]


def p_comparison_more(p):
    'comparison : expression MORE expression'
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 > operand2
# Функции сравнения (выражение >||< выражение)
def p_comparison_notmore(p):
    'comparison : expression NOTMORE expression'
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 < operand2



# Функция корня (sqrt())
def p_expression_sqrt(p):
    'expression : SQRT LPAREN expression RPAREN'
    operand1 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = math.sqrt(operand1)
# Функция перевода числа в строку (str())
def p_expression_strs(p):
    '''expression : STRS LPAREN INT RPAREN
       expression : STRS LPAREN ID RPAREN
       '''
    p[0] = str(p[3])
# Функция возведения в степень (x ** y)
def p_expression_degree(p):
    'expression : expression DEGREE expression'
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 ** operand2

# Функция умножения (x * y)
def p_expression_multiply(p):
    '''
    expression : expression MULT expression
    '''
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 * operand2

# Функция деления (x / y)
def p_expression_divide(p):
    '''
    expression : expression DIVIDE expression
    '''
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 / operand2

# Функция сложения (x + y)
def p_expression_plus(p):
    '''
    expression : expression PLUS expression
    '''
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 + operand2

# Функция вычитания (x - y)
def p_expression_minus(p):
    '''
    expression : expression MINUS expression
    '''
    operand1 = variables[p[1]] if isinstance(p[1], str) else p[1]
    operand2 = variables[p[3]] if isinstance(p[3], str) else p[3]
    p[0] = operand1 - operand2

# Функция задачи переменной (x = y)
def p_statement_assign(p):
    'statement : LET ID ASSIGN expression SEMICOLON'
    variables[p[2]] = p[4]
    return

# Функция вывода (print('x'))
def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON
    '''
    print(p[3])
    return

# Функция вывода переменной (print(x))
def p_statement_printid(p):
    'statement : PRINT LPAREN ID RPAREN SEMICOLON'
    print(variables[p[3]])
    return

def p_program(p):
    '''
    program : statement
            | program statement
    '''
    pass

def p_error(p):
    print("Синтаксическая ошибка")


#! Не менять! {
start = 'program'
precedence = (
   ('left', 'PLUS', 'MINUS'),
   ('left', 'MULT', 'DIVIDE'),
   ('right', 'DEGREE', 'SQRT'),
)
parser = yacc.yacc()
#! }

#* Интерпретатор

with open(filename, encoding = 'utf-8') as file:
    code = file.read()
    parser.parse(code)
        