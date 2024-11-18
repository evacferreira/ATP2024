###Trabalho de casa 6

Este programa é uma aplicação destinada à gestão de alunos em turmas escolares que possibilita a criação de turmas, a inserção de novos alunos, a consulta de informações específicas de alunos, o armazenamento de turmas em arquivos, a recuperação de dados armazenados e a listagem dos alunos de uma turma. 
Cada turma é representada como uma lista que contém as informações dos alunos matriculados. Cada aluno é representado por um tuplo com três elementos: o nome do aluno, um ID único e uma lista de três notas referentes a diferentes avaliações (trabalho de casa, projeto e teste). As turmas são agrupadas em uma lista maior, que representa a escola como um todo.

As funcionalidades do programa são:
Menu: O programa apresenta um menu principal com opções que o utilizador irá escolher, tais como: criar turmas, inserir alunos, listar turmas, consultar alunos, salvar dados em arquivos, recuperar informações e encerrar a aplicação.

Criação de Turmas: Permite criar novas turmas fornecendo um nome. Caso a turma já exista, o programa informa o utilizador e impede essa inserção.

Adicionar Alunos: Insere alunos numa turma em específico. O utilizador fornece o nome do aluno, um identificador único (ID) e suas notas em três categorias (trabalho de casa, projeto e teste). Caso o Id já exista, a função não permite que o aluno seja adicionado à turma.

Listagem de Alunos: Exibe todos os alunos de uma turma, mostrando o nome, ID e as respetivas notas. Caso a turma não exista, retornará uma mensagem de erro.

Consulta de Alunos: Permite procurar informações detalhadas de um aluno pelo seu ID numa turma específica. Exibe os dados completos do aluno. Caso o id não seja encontrado, informa o utilizador.

Guardar e Carregar Dados: Os dados de uma turma podem ser guardados num arquivo de texto, armazenando informações como nome, ID e notas. Posteriormente, esses dados podem ser recuperados do arquivo e reintegrados no programa.

Encerramento: O programa encerra quando o utilizador escolher a opção correspondente, exibindo uma mensagem de despedida.