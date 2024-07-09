%{
#include <stdio.h>
#include <string.h>

int palabras = 0;
int palabras_con_tilde = 0;
int caracteres = 0;
int vocales = 0;
int consonantes = 0;
int puntuaciones = 0;

%}

%option noyywrap

letter           [a-zA-ZñÑ]
number            [0-9]
tilde_lower      (\xC3[\xA1\xA9\xAD\xB3\xBA])
tilde_upper      (\xC3[\x81\x89\x8D\x93\x9A])
utf8_letter      ({letter}|{tilde_lower}|{tilde_upper})
punctuation      [,.;]

%%

{utf8_letter}+ {
    // Incrementa el conteo de palabras
    palabras++;
    printf("PALABRA: %s\n", yytext);
    // Verifica si la palabra contiene alguna tilde
    int contiene_tilde = 0;
    if (strstr(yytext, "\xC3\xA1") || strstr(yytext, "\xC3\xA9") || strstr(yytext, "\xC3\xAD") || 
        strstr(yytext, "\xC3\xB3") || strstr(yytext, "\xC3\xBA") || strstr(yytext, "\xC3\x81") || 
        strstr(yytext, "\xC3\x89") || strstr(yytext, "\xC3\x8D") || strstr(yytext, "\xC3\x93") || 
        strstr(yytext, "\xC3\x9A")) {
        contiene_tilde = 1;
        palabras_con_tilde++;
    }
    // Contar caracteres, vocales y consonantes
    for (int i = 0; yytext[i] != '\0'; i++) {
        caracteres++;
        if (strchr("aeiouAEIOUáéíóúÁÉÍÓÚ", yytext[i]) != NULL) {
            vocales++;
        } else if ((yytext[i] >= 'a' && yytext[i] <= 'z') || (yytext[i] >= 'A' && yytext[i] <= 'Z') || yytext[i] == 241 || yytext[i] == 209) {
            consonantes++;
        }
    }
    if (contiene_tilde) {
        printf("PALABRA CON TILDE: %s\n", yytext);
    }
    
}
"+"|"-"|"*"|"/"               { printf("OPERADOR: %s\n", yytext); }
{number}+                     { printf("NUMERO: %s\n", yytext); }
{punctuation}                 { puntuaciones++; caracteres++; printf("PUNTUACION: %s\n", yytext); }
.                             

%%

int main() {
    yylex();
    // Imprimir las estadísticas al final del análisis
    printf("PALABRAS: %d\n", palabras);
    printf("PALABRAS CON TILDE: %d\n", palabras_con_tilde);
    printf("CARACTERES: %d\n", caracteres);
    printf("VOCALES: %d\n", vocales);
    printf("CONSONANTES: %d\n", consonantes);
    printf("PUNTUACIONES: %d\n", puntuaciones);
    return 0;
}