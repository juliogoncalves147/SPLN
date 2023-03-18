import ply.yacc as yacc


def p_1(p): 
    "dic : Es"; 
    pass


def p_2(p): "Es : E Linha_B Es"; pass


def p_3(p): "Es : E"; pass


def p_4(p): "E : Itens"; pass


def p_5(p): "Itens : Item '\n' Itens"; pass


def p_6(p): "Itens : Item"; pass


def p_7(p): "Item : AtrC"; pass


def p_8(p): "Item : Ling"; pass


def p_9(p): "AtrC : id ':' Valor"; pass


def p_10(p): "Ling : idL ':' '\n' Ts"; pass


def p_11(p): "Ts : Ts '\n' T"; pass


def p_12(p): "Ts : T"; pass


def p_13(p): "T : '-' Termo AtrTs"; pass


def p_14(p): "AtrTs : AtrTs AtrT"; pass


def p_15(p): "AtrTs : AtrT"; pass


def p_16(p): "AtrT : '\n' '+' id ':' VAL"; pass
