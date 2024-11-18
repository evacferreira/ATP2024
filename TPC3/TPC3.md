###Trabalho de casa 3

O Jogo dos 21 Fósforos é um jogo com dois modos dependendo de quem inicia o jogo, se o usuário ou o computador. O objetivo do jogo é não retirar o último fósforo, que tirar perde.
O jogo começa com 21 fósforos, e cada jogador, na sua vez, pode retirar entre 1 e 4 fósforos. O programa permite que o utilizador escolha o modo de jogo que prefere, se deseja começar ou se prefere que o computador inicie a partida, sendo que durante o jogo os turnos vão alternando (se começa o utilizador, depois joga o computador e vice-versa).

No turno do usuário, o programa solicita que ele insira o número de fósforos de 1 a 4 que deseja retirar. A entrada é validada para garantir que o número seja válido e menor do que os fósforos restantes. Após uma jogada válida, o número de fósforos é atualizado, e o jogo verifica se restam fósforos. Caso já não existam, o jogador que retirou o último fósforo perde, e o outro é declarado vencedor.

No turno do computador, o programa utiliza uma estratégia inteligente implementada na função jogada_computador. Essa estratégia procura deixar múltiplos de 5 fósforos para o próximo jogador, garantindo vantagem ao computador. Caso não seja possível, o computador faz uma jogada aleatória dentro dos limites permitidos (entre 1 e o número de fósforos restantes). Após a jogada do computador, o numero de fosforos é atualizado e o programa verifica novamente se o jogo terminou.

O jogo é controlado pela função principal, main, que apresenta o menu inicial e solicita ao jogador que escolha o modo de jogo. Em seguida, chama a função jogar para executar o fluxo do jogo, alternando entre os turnos do usuário e do computador até que o vencedor seja determinado.






