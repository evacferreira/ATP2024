###Trabalho de casa 7

Este programa consiste numa aplicação que permite analisar dados meteorológicos diários tendo várias funcionalidades, tais como:cálculo de estatísticas meteorológicas, armazenamento e recuperação de dados a partir de arquivos,  a visualização de gráficos relacionados a temperaturas e precipitação. Cada registro meteorológico é composto pela data, temperatura mínima, temperatura máxima e o índice de precipitação do dia.

O programa apresenta um menu interativo que permite ao usuário escolher a funcionalidade que quiser. As opções são exibidas de forma clara num menu para que seja mais prático ao utilizador.

1. Cálculo da Temperatura Média Diária
Esta funcionalidade calcula a temperatura média de cada dia, fazendo a média aritmética entre as temperaturas mínima e máxima do respectivo dia.

2. Guardar Tabela de Dados num Ficheiro
Permite armazenar os dados meteorológicos num ficheiro de texto. O ficheiro é guardado em formato legível, com os dados organizados por linhas e separados por símbolos específicos.

3. Carregar Tabela de Dados a Partir de um Ficheiro
Esta opção lê os dados meteorológicos de um ficheiro previamente guardado e carrega-os para uso na aplicação. Os dados são convertidos para o formato utilizado pelo programa.

4. Determinação da Temperatura Mínima Mais Baixa
Identifica a menor temperatura mínima registrada na tabela de dados meteorológicos, permitindo ao usuário saber qual foi o dia mais frio.

5. Cálculo da Amplitude Térmica Diária
Calcula a diferença entre a temperatura máxima e a temperatura mínima de cada dia.

6. Identificação da Precipitação Máxima
Encontra o maior índice de precipitação registrado e retorna esse valor juntamente com a data em que ocorreu. 

7. Identificação de Dias com Precipitação Superior a um Valor Específico
Permite ao usuário especificar um valor de referência para precipitação. O programa retorna todos os dias em que a precipitação foi maior do que o valor de precipitação recebido.

8. Cálculo do Maior Período de Dias com Precipitação Abaixo de um Valor Específico
Determina a maior sequência de dias consecutivos em que a precipitação foi inferior a um valor dado pelo usuário.

9. Geração de Gráficos para Visualização
Cria gráficos que mostram as temperaturas mínima e máxima, além do índice de precipitação ao longo do período analisado. Esses gráficos são exibidos utilizando a biblioteca matplotlib.



Ao iniciar o programa, o menu é exibido para que o usuário escolha uma funcionalidade.
O usuário insere o número da opção desejada e o programa executa a funcionalidade correspondente.Após a execução, o menu é exibido novamente para que o usuário possa realizar outra operação ou encerrar o programa.
A aplicação é encerrada ao selecionar a opção de sair (opção "0").
