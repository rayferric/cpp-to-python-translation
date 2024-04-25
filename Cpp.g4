grammar Cpp;
import CppTokens;

// Parser rules
program: statement*;
statement: namespace | enum | variable | function |  using_directive ;
inside_func_statement: while_loop | switch_case | if_else | return_statement | throw_statement | for_loop | for_each_loop | try_catch_block | variable | function ;
inside_loop_statement:  while_loop | switch_case | if_else | break_statement | continue_statement | throw_statement | for_loop | for_each_loop | try_catch_block | variable | function ;
inside_if_statement: while_loop | switch_case | if_else | throw_statement | for_loop | for_each_loop | try_catch_block | variable;
namespace: NAMESPACE ID (scope | ASSIGN resolved_id SEMICOLON);
enum: ENUM CLASS? ID enum_scope SEMICOLON;
enum_scope: LEFT_BRACKET enum_item (COMMA enum_item)* RIGHT_BRACKET;
enum_item: ID (ASSIGN INT)?;
variable: some_type_without_pointer_suffix variable_decl_item (COMMA variable_decl_item)* SEMICOLON;
variable_decl_item: pointer_suffix? ID array_size_specifier? (ASSIGN expression | ctor_call_parens)?;
array_size_specifier: LEFT_SQ INT? RIGHT_SQ;
ctor_call_parens: (LEFT_PAREN | LEFT_BRACKET) expression_list? (RIGHT_PAREN | RIGHT_BRACKET);
function: some_type ID LEFT_PAREN parameter_list? RIGHT_PAREN func_scope;
parameter_list: parameter (COMMA parameter)*;
parameter: some_type ID array_size_specifier? (ASSIGN expression)?;
some_type: some_type_without_pointer_suffix pointer_suffix?;
pointer_suffix: (MUL | BIT_AND)+;
some_type_without_pointer_suffix: CONST? (simple_type | resolved_id) template_resolution? (LEFT_SQ INT RIGHT_SQ)*;
template_resolution: LESS some_type (COMMA some_type)* GREATER;
expression: resolved_id | ANY_LITERAL | expression bin_op expression | LEFT_PAREN expression RIGHT_PAREN | uno_prefix_op expression | expression uno_postfix_op | expression QUESTION expression COLON expression | LEFT_BRACKET expression_list RIGHT_BRACKET | function_call | array_access | lambda_expression | ctor_call;
bin_op: ADD | SUB | MUL | DIV | MOD | CARET | EQUAL | NEQUAL | GREATER | GREATER_EQUAL | LESS | LESS_EQUAL | LOG_AND | LOG_OR | LOG_NOT | ASSIGN | ASSIGN_ADD | ASSIGN_SUB | ASSIGN_MUL | ASSIGN_DIV | ASSIGN_MOD | ASSIGN_XOR | ASSIGN_AND | ASSIGN_OR | ASSIGN_LSH | ASSIGN_RSH | BIT_AND | BIT_OR | BIT_NOT | SHL | SHR | ARROW_STAR | ARROW | DOT_STAR | ELLIPSIS;
uno_prefix_op: INCR | DECR | ADD | SUB | BIT_NOT | LOG_NOT;
uno_postfix_op: INCR | DECR;
function_call: resolved_id LEFT_PAREN expression_list? RIGHT_PAREN;
expression_list: expression (COMMA expression)*;
while_loop: WHILE LEFT_PAREN expression RIGHT_PAREN loop_scope | WHILE LEFT_PAREN expression RIGHT_PAREN inside_loop_statement;
scope_or_statement: scope | statement;
if_scope_or_statement: if_scope | inside_if_statement;
loop_scope_or_statement: loop_scope | inside_loop_statement;
scope: LEFT_BRACKET statement* RIGHT_BRACKET;
func_scope: LEFT_BRACKET inside_func_statement* RIGHT_BRACKET;
loop_scope: LEFT_BRACKET inside_loop_statement* RIGHT_BRACKET;
if_scope: LEFT_BRACKET inside_if_statement* RIGHT_BRACKET;
resolved_id: ID ((SCOPE_RES | DOT) ID)*;
simple_type: CHAR | CHAR8_T | CHAR16_T | CHAR32_T | WCHAR_T | BOOL | SHORT | INT | LONG | FLOAT | DOUBLE | VOID | AUTO;
array_access: resolved_id LEFT_SQ expression RIGHT_SQ;
switch_case: SWITCH LEFT_PAREN expression RIGHT_PAREN LEFT_BRACKET switch_case_scope RIGHT_BRACKET;
switch_case_scope: (CASE expression COLON statement*)* (DEFAULT COLON statement*)*;
if_else: IF LEFT_PAREN expression RIGHT_PAREN if_scope_or_statement (ELSE IF LEFT_PAREN expression RIGHT_PAREN if_scope_or_statement)* (ELSE if_scope_or_statement)?;
lambda_expression: LEFT_SQ labda_captures? RIGHT_SQ LEFT_PAREN parameter_list? RIGHT_PAREN func_scope;
labda_captures: (lambda_capture_item (COMMA lambda_capture_item)*) | BIT_AND | ASSIGN;
lambda_capture_item: BIT_AND? ID;
return_statement: RETURN expression SEMICOLON;
break_statement: BREAK SEMICOLON;
continue_statement: CONTINUE SEMICOLON;
throw_statement: THROW expression SEMICOLON;
using_directive: USING NAMESPACE resolved_id SEMICOLON;
ctor_call: some_type ctor_call_parens;
for_loop: FOR LEFT_PAREN (variable | expression SEMICOLON | SEMICOLON) expression SEMICOLON expression RIGHT_PAREN loop_scope_or_statement;
for_each_loop: FOR LEFT_PAREN some_type ID COLON expression RIGHT_PAREN loop_scope_or_statement;
try_catch_block: TRY scope (CATCH LEFT_PAREN some_type ID? RIGHT_PAREN func_scope)*;
