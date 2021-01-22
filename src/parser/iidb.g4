grammar iidb;

options {
    language=Python3;
}

parse
 : ( isql_stmt_list | error )* EOF
 ;

error
 : UNEXPECTED_CHAR 
 ;

isql_stmt_list
 : ';'* isql_stmt ( ';'+ isql_stmt )* ';'*
 ;

isql_stmt
 : ( add_condition_stmt )
 ;

add_condition_stmt
 : ADD any_name TO ( database_name '.' )? table_name '.' column_name CONDITION 
   '(' expr (AND expr)* ')' WHERE column_name '=' expr
 ;

table_name
 : any_name
 ;

database_name
 : any_name
 ;

column_name
 : any_name
 ;

any_name
 : IDENTIFIER
 | STRING_LITERAL
 ;

expr
 : any_name
 | date_function
 | expr ( '=' | '!=' | '<' | '>' ) expr
 | NUMERIC_LITERAL
 ;

date_function
 : DATE '(' STRING_LITERAL ')'
 ;

////////

ADD : A D D;
AND : A N D;
CONDITION : C O N D I T I O N;
DATE : D A T E;
TO : T O;
WHERE : W H E R E;

IDENTIFIER
 : '"' (~'"' | '""')* '"'
 | '`' (~'`' | '``')* '`'
 | '[' ~']'* ']'
 | [a-zA-Z_] [a-zA-Z_0-9]* // TODO check: needs more chars in set
 ;

NUMERIC_LITERAL
 : DIGIT+ ( '.' DIGIT* )? ( E [-+]? DIGIT+ )?
 | '.' DIGIT+ ( E [-+]? DIGIT+ )?
 ;

STRING_LITERAL
 : '\'' ( ~'\'' | '\'\'' )* '\''
 ;

SPACES
 : [ \u000B\t\r\n] -> channel(HIDDEN)
 ;

UNEXPECTED_CHAR
 : .
 ;

fragment DIGIT : [0-9];

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];

