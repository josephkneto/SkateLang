# SkateLang

# Código exemplo
```
enquanto (obstaculo != escada) {
    se (obstaculo == corrimao) {
        execute grind;
    } senao {
        se (obstaculo == rampa) {
            execute ollie;
        } senao {
            execute kickflip;
        }
    }
}
```
# EBNF
![image](https://github.com/josephkneto/SkateLang/assets/79852830/2f43bb61-0978-4511-87c6-bca126587135)

# Exemplo de entrada para o compilador

```
obstaculo = escada;
enquanto (obstaculo != corrimao) {
    se (obstaculo == escada) {
        execute ollie;
    }
}
```
Saida esperada:
OLLIE (em loop infinito)
