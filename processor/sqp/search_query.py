import ply.lex as lex
import ply.yacc as yacc


class Parser:
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data)


class SearchQuery(Parser):

    # Lexer
    reserved = {
            "AND": "AND",
            "OR": "OR",
            "NOT": "NOT"
    }

    tokens = ["TERM", "LPAREN", "RPAREN"] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_TERM(self, t):
        r'([a-zA-Z_0-9]|\*)+'
        t.type = self.reserved.get(t.value, "TERM")
        return t

    t_ignore = " \t\n\r"

    def t_error(self, t):
        print(f"[error] processor: illegal character: '{t.value[0]}'")
        t.lexer.skip(1)

    # Parser
    precedence = (
            ('left', 'AND', 'OR'),
            ('left', 'NOT')
    )

    def p_phrase_single(self, p):
        'phrase : TERM'
        p[0] = ('TERM', p[1])

    def p_phrase_mulitple(self, p):
        'phrase : TERM phrase'
        p[0] = ('AND', ('TERM', p[1]), p[2])

    def p_query_phrase(self, p):
        'query : phrase'
        p[0] = p[1]

    def p_query_binary(self, p):
        '''query : query AND query
                 | query OR query'''
        if p[2] == 'AND':
            p[0] = ('AND', p[1], p[3])
        elif p[2] == 'OR':
            p[0] = ('OR', p[1], p[3])

    def p_query_unary(self, p):
        'query : NOT query'
        p[0] = ('NOT', p[2])

    def p_query_group(self, p):
        'query : LPAREN query RPAREN'
        p[0] = p[2]

    def p_error(self, p):
        if p:
            print(f"[error] processor: syntax error at '{p.value}'")
        else:
            print("[error] processor: syntax error at EOF")
