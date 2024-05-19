grammar Cpp;
import CppTokens;

// Parser rules
program: globalDefinition*;
globalDefinition: variableDeclaration | functionDefinition | classDefinition;
variableDeclaration: typeSpecifier variableDeclarationItem (COMMA variableDeclarationItem)* SEMICOLON;
variableDeclarationItem: identifier (ASSIGN expression)?;
functionDefinition: typeSpecifier identifier LEFT_PAREN argumentListDefinition? RIGHT_PAREN LEFT_BRACKET executableScope RIGHT_BRACKET;
argumentListDefinition: argumentDefinition (COMMA argumentDefinition)*;
argumentDefinition: typeSpecifier identifier;
classDefinition: CLASS identifier baseClassSpecifier? LEFT_BRACKET classDefinitionItem* RIGHT_BRACKET SEMICOLON;
baseClassSpecifier: COLON (PUBLIC | PROTECTED | PRIVATE) identifier;
classDefinitionItem: variableDeclaration | functionDefinition | ctorDefinition | accessSpecifier;
ctorDefinition: identifier LEFT_PAREN argumentListDefinition? RIGHT_PAREN LEFT_BRACKET executableScope RIGHT_BRACKET;
accessSpecifier: (PUBLIC | PRIVATE | PROTECTED) COLON;
executableScope: statement*;
statement: variableDeclaration | coutStatement | cinStatement | returnStatement | ifStatement | whileStatement | forStatement | switchStatement | breakStatement | continueStatement | assignmentStatement | expressionStatement;
coutStatement: (STD SCOPE_RES)? COUT (SHIFT_LEFT (expression | coutEndl))+ SEMICOLON;
coutEndl: (STD SCOPE_RES)? ENDL;
cinStatement: (STD SCOPE_RES)? CIN SHIFT_RIGHT useIdentifier SEMICOLON;
returnStatement: RETURN expression SEMICOLON;
ifStatement: IF LEFT_PAREN expression RIGHT_PAREN executableScopeOrStatement ifStatementElseIf* ifStatementElse?;
ifStatementElseIf: ELSE IF LEFT_PAREN expression RIGHT_PAREN executableScopeOrStatement;
ifStatementElse: ELSE executableScopeOrStatement;
whileStatement: WHILE LEFT_PAREN expression RIGHT_PAREN executableScopeOrStatement;
forStatement: FOR LEFT_PAREN forStatementInit forStatementCondition forStatementUpdate RIGHT_PAREN executableScopeOrStatement;
forStatementInit: variableDeclaration | expression SEMICOLON | SEMICOLON;
forStatementCondition: expression SEMICOLON | SEMICOLON;
forStatementUpdate: expression?;
switchStatement: SWITCH LEFT_PAREN expression RIGHT_PAREN LEFT_BRACKET switchCase* switchDefault? RIGHT_BRACKET;
switchCase: CASE expression COLON executableScope BREAK SEMICOLON;
switchDefault: DEFAULT COLON executableScope (BREAK SEMICOLON)?;
breakStatement: BREAK SEMICOLON;
continueStatement: CONTINUE SEMICOLON;
executableScopeOrStatement: LEFT_BRACKET executableScope RIGHT_BRACKET | statement;
assignmentStatement: useIdentifier assignmentOperator expression SEMICOLON;
expressionStatement: expression SEMICOLON;
expression: atomicExpression | binaryOperationSequence | unaryOperation;
atomicExpression: ANY_LITERAL | useIdentifier | LEFT_PAREN expression RIGHT_PAREN | functionCall | stdToString;
binaryOperationSequence: atomicExpression (binaryOperator atomicExpression)+;
unaryOperation: unaryPrefixOperator atomicExpression | atomicExpression unaryPostfixOperator;
functionCall: useIdentifier LEFT_PAREN argumentList? RIGHT_PAREN;
stdToString: STD_TO_STRING LEFT_PAREN expression RIGHT_PAREN;
argumentList: expression (COMMA expression)*;
typeSpecifier: integerType | stringType | floatType | voidType | identifier;
useIdentifier: (thisPrefix | baseClassPrefix)? identifier ((DOT | ARROW) identifier)*;
thisPrefix: THIS ARROW;
baseClassPrefix: identifier SCOPE_RES;
assignmentOperator: ASSIGN | ASSIGN_ADD | ASSIGN_SUB | ASSIGN_MUL | ASSIGN_DIV;
unaryPrefixOperator: INCR | DECR | ADD | SUB;
unaryPostfixOperator: INCR | DECR;
binaryOperator: MUL | DIV | ADD | SUB | EQUAL | NEQUAL | GREATER | GREATER_EQUAL | LESS | LESS_EQUAL;
integerType: INT | LONG | SHORT;
stringType: (STD SCOPE_RES)? STRING;
floatType: FLOAT | DOUBLE;
voidType: VOID;
identifier: ID;
