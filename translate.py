from antlr4 import *
from cpp.CppLexer import CppLexer
from cpp.CppParser import CppParser
import sys

class ScopeInfo:
    def __init__(self):
        self.variable_types = {}

imports = set()
scope_infos: list[ScopeInfo] = [ScopeInfo()]

def get_variable_type(name: str) -> str:
    for i in range(len(scope_infos) - 1, -1, -1):
        if name in scope_infos[i].variable_types:
            return scope_infos[i].variable_types[name]
    return None

def program_to_python(ctx: CppParser.ProgramContext) -> str:
    out = ""
    for child in ctx.getChildren():
        out += to_python(child)
    return out + "exit(main())\n"

def executable_scope_to_python(ctx: CppParser.ExecutableScopeContext) -> str:
    # Create a new scope info
    scope_infos.append(ScopeInfo())

    out = ""
    for child in ctx.getChildren():
        lines = to_python(child)
        if len(lines.strip()) > 0:
            for line in lines.split('\n'):
                if len(line.strip()) > 0:
                    out += "  " + line + "\n"

    # Remove the scope info
    scope_infos.pop()

    if len(out) == 0:
        out = "  pass\n"
    return out

def function_definition_to_python(ctx: CppParser.FunctionDefinitionContext) -> str:
    return_type = to_python(ctx.typeSpecifier())
    name = ctx.identifier().getText()
    args_str = to_python(ctx.argumentListDefinition()) if ctx.argumentListDefinition() is not None else ""
    body_str = to_python(ctx.executableScope())

    return f"def {name}({args_str}) -> {return_type}:\n{body_str}\n"

def argument_list_definition_to_python(ctx: CppParser.ArgumentListDefinitionContext) -> str:
    args = []
    for child in ctx.getChildren():
        if isinstance(child, CppParser.ArgumentDefinitionContext):
            args.append(to_python(child))
    return ", ".join(args)

def argument_definition_to_python(ctx: CppParser.ArgumentDefinitionContext) -> str:
    type_name = to_python(ctx.typeSpecifier())
    identifier = ctx.identifier().getText()
    return f"{identifier}: {type_name}"

def cout_statement_to_python(ctx: CppParser.CoutStatementContext) -> str:
    phrases = []
    for child in ctx.getChildren():
        if isinstance(child, CppParser.ExpressionContext):
            phrases.append(to_python(child))
        elif isinstance(child, CppParser.CoutEndlContext):
            phrases.append("'\\n'")
    return f"print({', '.join(phrases)}, sep='', end='')\n"

def cin_statement_to_python(ctx: CppParser.CinStatementContext) -> str:
    identifier = ctx.identifier().getText()
    var_type = get_variable_type(identifier)
    return f"{identifier} = {var_type}(input())\n"

def return_statement_to_python(ctx: CppParser.ReturnStatementContext) -> str:
    expression = to_python(ctx.expression())
    return f"return {expression}\n"

def expression_statement_to_python(ctx: CppParser.ExpressionStatementContext) -> str:
    return to_python(ctx.expression()) + "\n"

def binary_operation_sequence_to_python(ctx: CppParser.BinaryOperationSequenceContext) -> str:
    out = ""
    for child in ctx.getChildren():
        if isinstance(child, CppParser.AtomicExpressionContext):
            out += to_python(child)
        elif isinstance(child, CppParser.BinaryOperatorContext):
            out += f" {child.getText()} "
    return out

def unary_operation_to_python(ctx: CppParser.UnaryOperationContext) -> str:
    value = to_python(ctx.atomicExpression())
    prefix = ctx.unaryPrefixOperator().getText() if ctx.unaryPrefixOperator() is not None else ""
    postfix = ctx.unaryPostfixOperator().getText() if ctx.unaryPostfixOperator() is not None else ""
    
    # NOTE: Increment/decrement operators should not be used as expressions in source C++ code.
    if postfix == "++":
        return f"{value} += 1"
    elif postfix == "--":
        return f"{value} -= 1"
    elif prefix == "++":
        return f"{value} += 1"
    elif prefix == "--":
        return f"{value} -= 1"
    elif prefix == "-":
        return f"-{value}"
    elif prefix == "!":
        return f"not {value}"
    else:
        raise Exception(f"Unknown unary operator: {prefix}{postfix}")

def atomic_expression_to_python(ctx: CppParser.AtomicExpressionContext) -> str:
    if ctx.expression() is not None:
        return f"({to_python(ctx.expression())})"
    else:
        return ctx.getText()
    
def function_call_to_python(ctx: CppParser.FunctionCallContext) -> str:
    name = ctx.identifier().getText()
    args_str = to_python(ctx.argumentList()) if ctx.argumentList() is not None else ""
    return f"{name}({args_str})"

def argument_list_to_python(ctx: CppParser.ArgumentListContext) -> str:
    args = []
    for child in ctx.getChildren():
        if isinstance(child, CppParser.ExpressionContext):
            args.append(to_python(child))
    return ", ".join(args)

def type_specifier_to_python(ctx: CppParser.TypeSpecifierContext) -> str:
    if ctx.integerType() is not None:
        return "int"
    elif ctx.stringType() is not None:
        return "str"
    elif ctx.floatType() is not None:
        return "float"
    elif ctx.voidType() is not None:
        return "None"
    else:
        imports.add("from typing import Any")
        return "Any"
    
def variable_declaration_to_python(ctx: CppParser.VariableDeclarationContext) -> str:
    type_name = to_python(ctx.typeSpecifier())

    lines = []
    for child in ctx.getChildren():
        if isinstance(child, CppParser.VariableDeclarationItemContext):
            identifier = child.identifier().getText()
            if child.expression() is not None:
                value = to_python(child.expression())
                lines.append(f"{identifier}: {type_name} = {value}")
            
            scope_infos[-1].variable_types[identifier] = type_name

    return "\n".join(lines) + "\n"

def executable_scope_or_statement_to_python(ctx: CppParser.ExecutableScopeOrStatementContext) -> str:
    if ctx.executableScope() is not None:
        return to_python(ctx.executableScope())
    else:
        statement = to_python(ctx.statement())
        if len(statement.strip()) == 0:
            statement = "pass"
        return f"  {statement}\n"

def if_statement_to_python(ctx: CppParser.IfStatementContext) -> str:
    condition = to_python(ctx.expression())
    body = to_python(ctx.executableScopeOrStatement())
    out = f"if {condition}:\n{body}"

    for child in ctx.getChildren():
        if isinstance(child, CppParser.IfStatementElseIfContext):
            condition = to_python(child.expression())
            body = to_python(child.executableScopeOrStatement())
            out += f"elif {condition}:\n{body}"
        elif isinstance(child, CppParser.IfStatementElseContext):
            body = to_python(child.executableScopeOrStatement())
            out += f"else:\n{body}"
    
    return out

def while_statement_to_python(ctx: CppParser.WhileStatementContext) -> str:
    condition = to_python(ctx.expression())
    body = to_python(ctx.executableScopeOrStatement())
    return f"while {condition}:\n{body}"

def for_statement_to_python(ctx: CppParser.ForStatementContext) -> str:
    out = ""

    init_var_decl = ctx.forStatementInit().variableDeclaration()
    if init_var_decl is not None:
        out += to_python(init_var_decl)
    
    init_expr = ctx.forStatementInit().expression()
    if init_expr is not None:
        out += to_python(init_expr) + '\n'

    condition = ctx.forStatementCondition().expression()
    if condition is not None:
        out += f"while {to_python(condition)}:\n"
    else:
        out += "while True:\n"

    body = to_python(ctx.executableScopeOrStatement())
    out += body

    update = ctx.forStatementUpdate().expression()
    if update is not None:
        out += "  " + to_python(update) + '\n'
    
    return out

def switch_statement_to_python(ctx: CppParser.SwitchStatementContext) -> str:
    out = ""
    expression = to_python(ctx.expression())
    out += f"match {expression}:\n"

    switch_body = ""
    for child in ctx.getChildren():
        if isinstance(child, CppParser.SwitchCaseContext):
            case = to_python(child.expression())
            body = to_python(child.executableScope())
            switch_body += f"case {case}:\n{body}"
        elif isinstance(child, CppParser.SwitchDefaultContext):
            body = to_python(child.executableScope())
            switch_body += f"case _:\n{body}"

    if len(switch_body.strip()) == 0:
        out += "  case _:\n    pass\n"
    else:
        for line in switch_body.split('\n'):
            if len(line.strip()) > 0:
                out += "  " + line + "\n"
    
    return out

def break_statement_to_python(ctx: CppParser.BreakStatementContext) -> str:
    return "break"

def continue_statement_to_python(ctx: CppParser.ContinueStatementContext) -> str:
    return "continue"

def assignment_statement_to_python(ctx: CppParser.AssignmentStatementContext) -> str:
    identifier = ctx.identifier().getText()
    operator = ctx.assignmentOperator().getText()
    value = to_python(ctx.expression())
    return f"{identifier} {operator} {value}"

context_type_handlers = {
    CppParser.ProgramContext: program_to_python,
    CppParser.ExecutableScopeContext: executable_scope_to_python,
    CppParser.FunctionDefinitionContext: function_definition_to_python,
    CppParser.ArgumentListDefinitionContext: argument_list_definition_to_python,
    CppParser.ArgumentDefinitionContext: argument_definition_to_python,
    CppParser.CoutStatementContext: cout_statement_to_python,
    CppParser.CinStatementContext: cin_statement_to_python,
    CppParser.ReturnStatementContext: return_statement_to_python,
    CppParser.ExpressionStatementContext: expression_statement_to_python,
    CppParser.BinaryOperationSequenceContext: binary_operation_sequence_to_python,
    CppParser.UnaryOperationContext: unary_operation_to_python,
    CppParser.AtomicExpressionContext: atomic_expression_to_python,
    CppParser.FunctionCallContext: function_call_to_python,
    CppParser.ArgumentListContext: argument_list_to_python,
    CppParser.TypeSpecifierContext: type_specifier_to_python,
    CppParser.VariableDeclarationContext: variable_declaration_to_python,
    CppParser.ExecutableScopeOrStatementContext: executable_scope_or_statement_to_python,
    CppParser.IfStatementContext: if_statement_to_python,
    CppParser.WhileStatementContext: while_statement_to_python,
    CppParser.ForStatementContext: for_statement_to_python,
    CppParser.SwitchStatementContext: switch_statement_to_python,
    CppParser.BreakStatementContext: break_statement_to_python,
    CppParser.ContinueStatementContext: continue_statement_to_python,
    CppParser.AssignmentStatementContext: assignment_statement_to_python
}

def to_python(ctx: ParserRuleContext) -> str:
    global imports

    handler = context_type_handlers.get(type(ctx))
    if handler is not None:
        return handler(ctx)
    else:
        out = ""
        for child in ctx.getChildren():
            out += to_python(child)
        return out

def main():
    filepath = sys.argv[1]
    with open(filepath, 'r') as file:
        input_stream = InputStream(file.read())
    lexer = CppLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CppParser(token_stream)
    tree = parser.program()

    # Display the parse tree
    # print(tree.toStringTree(recog=parser))

    out = to_python(tree)

    # Add imports marked as used by to_python
    if len(imports) > 0:
        out = "\n".join(imports) + '\n\n' + out

    print(out)
    out_path = filepath.replace('.cpp', '.py')
    with open(out_path, 'w') as file:
        file.write(out)

if __name__ == '__main__':
    main()
