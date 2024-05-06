%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
int yyerror(const char *s);
%}


%token SE SENAO ENQUANTO EXECUTE OBSTACULO CORRIMAO RAMPA ESCADA EQ NEQ OLLIE KICKFLIP GRIND HEELFLIP SEMICOLON LBRACE RBRACE IDENTIFIER

%left EQ NEQ

%union {
    char *str;
}

%%

program: statement
       ;

statement: if_statement
         | loop_statement
         | action_statement
         ;

if_statement: SE '(' condition ')' '{' statement '}' 
            | SE '(' condition ')' '{' statement '}' SENAO '{' statement '}'
            ;

loop_statement: ENQUANTO '(' condition ')' '{' statement '}'
               ;

action_statement: EXECUTE action SEMICOLON
                ;

condition: OBSTACULO relation tipo_obstaculo
         ;

relation: EQ
        | NEQ
        ;

tipo_obstaculo: CORRIMAO
              | RAMPA
              | ESCADA
              ;

action: OLLIE
      | KICKFLIP
      | GRIND
      | HEELFLIP
      ;

%%

int yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
    return 0;
}

int main() {
    yyparse();
    return 0;
}

