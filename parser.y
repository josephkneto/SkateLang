%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
int yyerror(const char *s);
%}


%token SE SENAO ENQUANTO EXECUTE OBSTACULO CORRIMAO RAMPA ESCADA EQ NEQ OLLIE KICKFLIP GRIND HEELFLIP SEMICOLON LBRACE RBRACE IDENTIFIER LPAREN RPAREN

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

if_statement: SE LPAREN condition RPAREN LBRACE statement RBRACE 
            | SE LPAREN condition RPAREN LBRACE statement RBRACE SENAO LBRACE statement RBRACE
            ;

loop_statement: ENQUANTO LPAREN condition RPAREN LBRACE statement RBRACE
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

