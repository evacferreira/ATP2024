#Trabalho de casa 2

Para desenvolver o jogo comecei por criar um menu com as duas opções de modo de jogo.
Para o primeiro modo de jogo (modo 0), o programa vai escolher um número aleatório entre 0 e 100 através da função random.randrange que o utilizador irá tentar adivinhar.  A cada tentativa, o programa fornece dicas, informando o jogador se o número escolhido por este é maior ou menor que o número correto até este acertar. No final, o jogo revela o número de tentativas que o utilizador precisou até acertar o número.
No segundo modo de jogo (modo 1) o jogador escolhe um número entre 0 e 100 que o programa tenta adivinhá-lo. O computador faz palpites (usando a lógica de busca binária) e, com base nas orientações do jogador, se o número correto é maior ou menor, ajusta as suas tentativas até chegar à solução, seguindo uma estratégia de eliminação progressiva.

