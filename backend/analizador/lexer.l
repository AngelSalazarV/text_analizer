%{
#include <stdio.h>
%}

%option noyywrap

%%

"if"|"else"|"while"|"return" { printf("KEYWORD: %s\n", yytext); }
[\xC2-\xF4][\x80-\xBF]*      { printf("UTF8_CHAR: %s\n", yytext); } // Simplificación para caracteres UTF-8
[a-zA-Z_][a-zA-Z0-9_]*       { printf("IDENTIFIER: %s\n", yytext); }
"+"|"-"|"*"|"/"              { printf("OPERATOR: %s\n", yytext); }
[0-9]+                       { printf("NUMBER: %s\n", yytext); }
\n                           
.                            { printf("UNKNOWN: %s\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}