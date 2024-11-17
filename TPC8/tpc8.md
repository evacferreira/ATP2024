#Trabalho de casa 8

Nos três primeiros exercícios do teste de aferição, foram utilizadas listas em compreensão. 
No primeiro exercício foi feita uma lista com os elementos que não estão presentes em ambas as listas dadas.
No segundo exercício o código divide um texto em palavras e filtra aquelas que possuem mais de 3 caracteres.
No terceiro exercício é criada uma lista de tuplos onde cada tuplo enumera a posição da palavra (a partir de 1) e a respetiva palavra. 

No quarto exercício foi criada uma função que a string s e verifica quantas vezes a substring subs aparece. Cada vez que encontra a substring, soma mais 1 ao contador.
No quinto exercício com o objetivo de devolver o menor produto que for possível calcular multiplicando os 3 menores inteiros de uma lista, foi criada uma função que ordena a lista  através do sort e calcula o produto dos três menores números (números que ocuparem o indíce 0, 1 e 2).
Já o sexto exercício, foi resolvido criando uma função que reduz um número inteiro para um único dígito somando repetidamente os seus dígitos até ser apenas 1. 
Finalmente, o sétimo exercício verifica se uma substring está contida noutra string:
se estiver, retorna o índice inicial da substring; caso contrário, retorna -1.

O último exercício consiste na criação de uma série de funções que permitem a manipulação de uma rede social tais como: quantidade de posts, posts por autor, todos os autores de posts, inserir e remover um novo post, posts de um autor em específico e posts comentados por um dado autor.

Na primeira alínea, por cada post na rede social soma mais 1 ao contador, retornando esse número no final.
Na segunda alínea, dada a rede social e um autor, por cada post na rede social, se o autor desse post for o mesmo autor recebido na função, irá somar ao contador mais um e for fim, retornar esse número.
Na terceira alínea, é devolvida uma lista com todos os autores de posts e utiliza a função sort para a ordenar alfabeticamente.
Na quarta alínea, a fução vai inserir um novo post na rede social e para tal, vai receber de parâmetros: redeSocial, conteudo, autor, dataCriacao,comentarios. No fim, retorna a rede social já com o novo post inserido.
Já na quinta alínea, dado um id de um post, se este id tiver correspondencia de um id da rede social, este será removido e a função vai retornar a nova rede social sem esse post.
Por fim, a sexta alínea devolve uma distribuição de posts por autor e a sétima alínea devolve uma lista com os posts comentados por um autor(recebido na função).


