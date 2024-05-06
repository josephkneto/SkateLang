%{
#include "parser.tab.h"
%}

%%
"se"                    { return SE; }
"senao"                 { return SENAO; }
"enquanto"              { return ENQUANTO; }
"execute"               { return EXECUTE; }
"obstaculo"             { return OBSTACULO; }
"corrimao"              { return CORRIMAO; }
"rampa"                 { return RAMPA; }
"escada"                { return ESCADA; }
"=="                    { return EQ; }
"!="                    { return NEQ; }
"ollie"                 { return OLLIE; }
"kickflip"              { return KICKFLIP; }
"grind"                 { return GRIND; }
"heelflip"              { return HEELFLIP; }
";"                     { return SEMICOLON; }
"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
[a-zA-Z][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }
[ \t\n]                 ; // Ignorar espaços em branco e quebras de linha
.                       { return *yytext; } // Retornar caracteres individuais como tokens
%%

int yywrap() { return 1; }
