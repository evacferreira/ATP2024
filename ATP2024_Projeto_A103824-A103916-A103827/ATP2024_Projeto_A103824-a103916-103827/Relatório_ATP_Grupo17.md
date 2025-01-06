# Relatório de Algoritmos E Técnicas de Programação Grupo 17
Trabalho realizado por:
- Beatriz Coelho, A103824
- Eva Ferreira, A103916
- Lara Alves, A103827

Docentes:
- José Carlos Leite Ramalho
- Luís Filipe Costa Cunha

Ano letivo: 2024/25

## Índice
- [Introdução](#introdução)
- [Base de dados](#base-de-dados)
- [Funções](#funções)
  - [Funções Requisitadas](#funções-requisitadas)
  - [Funções Auxiliares](#funções-auxiliares)
- [Command Line Interface (CLI)](#command-line-interface-cli)
- [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Conclusão](#conclusão)
- [Bibliografia](#bibliografia)

## Introdução
No âmbito da UC de Algoritmos e Técnicas de Programação, foi proposto o desenvolvimento de um sistema de gestão de publicações de artigos ciêntificos em Python, que permite aos utilizadores criar, eliminar, atualizar, organizar e consultar as mesmas. Este sistema também fornece funcionalidades de análise e estatisticas sobre estas funções.

Para a elaboração deste trabalho foram essenciais os conhecimentos adquiridos ao longo das aulas, pois com estes conseguimos realizar todas as etapas consistentes do trabalho, como manipulação de datasets e criação de interfaces gráficas. Esta aplicação tem como objetivo facilitar o acesso à informação contida no dataset (com as publicações), exibindo-a de forma clara, sendo a sua operação fácil e prática para que o seu uso por parte do utilizador seja simples e intuitivo.

## Base de dados
Para a criação deste sistema de gestão de publicações de artigos ciêntificos, foi disponibilizada uma base de dados em json com várias artigos e as suas respetivas informações. Esta base de dados trata-se de uma lista de dicionários, tendo estes, por sua vez, 8 chaves:
- abstract
- keywords
- authors
- doi
- pdf
- publish_date
- title
- url

## Funções
### Funções Requisitadas
Esta aplicação foi criada com base em certos requisitos. Assim, foram definidas as seguintes funções, de modo a atingir todos os requisitos propostos para o sistema:
- Carregar a base de dados: o programa carrega para a memória a base de dados (dataset)
- Criar Publicações: o programa permite criar um artigo especificando um título, resumo, palavras-chave, DOI, uma lista de autores e sua afiliação correspondente, url para o ficheiro PDF do artigo, data de publicação e url do artigo
- Eliminar Publicações: o programa permite eliminar um artigo com um doi especifico
- Atualizar Publicações: o programa permitie a atualização de informações de uma publicação
- Consultar Publicações: o programa permite filtrar a informação do dataset. Para isto foram criadas diversas variantes desta função (filtrar por título, autor, afiliação, data de publicação e palavras-chave)
- Organizar Publicações: o programa deve permitir ordenar as publicações pelos títulos e pela data de publicação
- Listar Autores: para isto foram criadas 2 funções, que permitem ao programa listar os autores quer por frequência de publicação, quer por ordem alfabética
- Analisar Publicações por Autor: recorrendo às funções especificadas anteriormente, o programa permite aceder aos artigos de cada autor da lista
- Listar Palavras-Chave: para isto foram criadas 2 funções, que permitem ao programa listar as palavras-chave quer por frequência de publicação, quer por ordem alfabética
- Analisar Publicações por Palavras-Chave: recorrendo às funções especificadas anteriormente, o programa permite aceder aos artigos associadas a cada palavra-chave
- Estatísticas de Publicações: para isto foram criadas várias funções analisar gráficos e estatísticas como números de publicações por ano, mês, autores por frequência de publicação (top 20), autores por ano, palavras-chave por frequência e também palavra-chave mais frequente por ano
- Importar a base de dados: o programa importa para o ficheiro previamente carregado a informação nele contida
- Exportar a base de dados: o programa exporta para um novo ficheiro as alterações realizadas na base de dados durante a sua utilização

### Funções Auxiliares
Para assegurar o funcionamento das restantes funções, no momento em que estas são utilizadas para a criação da interface, foram desenvolvidas diversas funções auxiliares:
- Ler a base de dados: esta função lê a informação de uma base de dados
- Confirmar DOI: esta função confirma que o DOI introduzido existe na base de dados
- DOI existentes: esta função lista todos os DOI existentes
- DOI eliminados: esta função lista todos os DOI que foram eliminados
- Criar DOI: esta função gera um link para o DOI de um novo artigo
- Gerar URL: esta função gera um link para o URL de um novo artigo
- Gerar PDF: esta função gera um link para o PDF de um novo artigo
- Obter Publicação por DOI: esta função recebe o DOI de um artigo e retorna toda a informação sobre o mesmo (artigo completo)
- Obter Publicação por Título: esta função recebe o título de um artigo e retorna toda a informação sobre o mesmo (artigo completo)
- Lista dos anos: esta funçãonlista os anos presentes nas datas de publicação da base de dados
- Litar autores: esta função lista os autores das publicações presentes na base de dados por ordem alfabética

## Command Line Interface (CLI)
O CLI corresponde à Interface de Linha de Comando. Esta consiste na criação de programas, no nosso caso a criação de um sistema de gestão de publicações de artigos ciêntificos, que permitam a interação com o utilizador através de uma linha de comando. Assim, pela inserção dos comandos definidos nas funções acima definidas, o utilizador interage diretamente na linha de comando.

Para a interface de Linha de Comando criamos um menu cuja resposta é um input com as opções Carregar BD, Criar Publicação, Eliminar Publicação, Consultar Publicações, Analisar Publicações, Estatísticas, Importar BD e Exportar BD para além de uma opção Ajuda que explica o que faz cada uma das opções anteriores. Ao inicializar a aplicação, esta permite mexer na opção Carregar BD ( obrigando a carregar uma base de dados para ser possível trabalhar com as outras opções) e o Ajuda. Assim como na interface principal, o utilizador irá ser capaz de criar uma nova publicação. O utilizador terá de escrever manualmente no local indicado os dados referentes à nova publicação sendo esta depois inserida na base de dados. Para Eliminar publicação, o utilizador terá de escrever o DOI da publicação e esta será eliminada da base de dados. Para Consultar Publicações, é necessário escolher uma das opções que irão surgir no menu (consultar uma publicação completa, consultar por data, por keyword, por afiliação, por título ou por autor). A opção Analisar publicações irá permitir ao utilizador listar todos os autores existentes no sistema (por ordem de frequência de publicações ou por ordem alfabética), bem como as publicações associadas a cada autor. Relativamente ao Estatísticas, este gera gráficos sobre a frequência de palavras-chave, número de publicações por autor, e número de publicações por ano. No que diz respeito ao Importar e Exportar BD, o primeiro pega num ficheiro existente e junta à base de dados em que o utilizador está a trabalhar a informação nova (não acrescenta a repetida) e o Exportar permite exportar a informação da base de dados atual para um ficheiro existente ou não (pode gerar um novo).


## Graphical User Interface (GUI)
O GUI corresponde à Interface Gráfica do Utilizador. Esta permite uma interação entre os utilizadores e os computadores através de elemento visuais, como botões, menus e janelas, de forma a facilitar a comunicação e a execuçãoo de tarefas.

### Janela principal
Deste modo, optamos por criar uma interface principal dividida por duas colunas, do lado esquerdo com onze botões ("Carregar BD", "Nova Publicação", "Eliminar Publicação", "Atualizar Publicação", "Consultar Publicação", "Organizar Publicação", "Analise de Publicação", "Estatística", "Importar BD", "Exportar BD" e "Sair") e do lado direito uma caixa de texto onde serão impressas todas as informações que o utilizador escolher visualizar.

Criamos também um menu para aceder ao "Ajuda" no canto superior esquerdo, sendo que dentro deste existem dez submenus que se destinam a ajuda específica para cada uma das funções referidas acima (com exceção do "Sair").

[janelaprincipal-relat-rio.png](https://postimg.cc/Lg6fK6St)

### Botão Carregar BD

O botão "carregar Bd" permite ao utilizador carregar dos arquivos do computador a base de dados com que deseja trabalhar. Como podemos perceber pela imagem, ao carregar neste botão é aberta uma nova janela que conta com dois botões: "Browse", "Carregar". O primeiro permite ao utilizador pesquisar no seu computador que arquivo, em formato json, pretende carregar para a aplicação. Já o segundo, só é ativado quando um ficheiro é escolhido. Ao selecionar o mesmo, os dados contidos no arquivo são lidos pela aplicação.

Ao iniciar a aplicação apenas o botão "Carregar" e o "Sair" estão funcionais. Até que o utilizador carregue para a aplicação uma base de dados válida, esta situação mantém-se.

[carregar-Bd-relat-rio.png](https://postimg.cc/jLgfmkXG)

### Botão Nova Publicação

O botão "Nova Publicação" possibilita a criação de uma nova publicação. Ao carregar neste surge uma nova janela, onde devem ser introduzidos os dados acerca desta nova publicação (abstrato, palavras-chave, autores, doi, pdf, data de publicação, titlo, url). Para que a publicação seja criada é necessário que os campos do abstrato, titulo e pelo menos 1 autor estejam preenchidos. Os campos doi, url, pdf são gerados automaticamente pela aplicação. Os restantes campos não têm cariz obrigatório.

Para a data de publicação foi utilizado um calendário para ser mais prático para o utilizador selecionar a data. 

Por fim, tal como podemos ver na imagem, essa janela apresenta também os botões "Submeter", para guardar a nova tarefa e "Sair", para fechar a janela.

[novapublica-ao-relatorio.png](https://postimg.cc/SYyXtHvY)

### Botão Eliminar Publicação

O botão "Eliminar Publicação" permite ao utilizar eliminar uma publicação existente. Ao carregar neste surge uma nova janela onde o utilizador terá de escrever o doi da publicação que pretende eliminar e, seguidamente, clicar no botão "Submeter" para que esta seja eliminada da base de dados devidamente. 

Para que esta função funcione devidamente foi necessário criar uma função de confirmarDOI que verifica se o identificador introduzid existe realmente na base de dados e, caso não exista, irá surgir uma janela a anunciar que o DOI é inválido. 

[eliminarbd-relat-rio.png](https://postimg.cc/jwZbh90j)

### Botão Atualizar Publicação

O botão "Atualizar Publicação" possibilita ao utilizador atualizar a informação contida dentro de uma publicação, com a exceção dos campos pdf, url e doi que não se podem alterar. Para isso o utilizador terá que introduzir o doi da publicação que pretende alterar, a semelhança do botão anterior, tal como demonstra a figura seguinte. 

[atualizarbd-1-relatorio.png](https://postimg.cc/JsfZ16Ft)

Após estes passos será aberta outra janela com toda a informação relativa à publicação escolhida e, para proceder à atualização, será necessário que o utilizador apague os dados dos parâmetros que quer alterar e escreva a nova informação. Por fim, as alterações só são submetidas quando o botão "Submeter" é carregado. Se o utilizador clicar no botão "Sair", a janela é fechada e as alterações não são guardadas.

[atualizarbd2-relatorio.png](https://postimg.cc/vDZgdwm3)

### Botão Consultar Publicações

O botão "Consultar Publicações" permite ao utilizador consultar publicações de várias maneiras: consultar todas as aplicações, consultar publicação completa, consultar publicações por titulo, por autor, por afiliação, por data e por palavras-chave. Ao carregar abre uma janela que permite selecionar uma das opções anteriormente referidas, tal como mostrado na figura seguinte.

[consultarbd-1-relatorio.png](https://postimg.cc/1g8XTYNC)

Se for selecionada a opção de "Consultar todas as publicações" é aberta uma nova janela com os titulos de todas as publicações da base de dados. Se o utilizador selecionar um titulo, é mostrado na caixa de texto da janela principal os detalhes dessa publicação, ou seja, o restante da informação contida na mesma.

[consultarbd-2-relatorio.png](https://postimg.cc/YjmJ4YJm)
[consultarbd-3-relatorio.png](https://postimg.cc/ts9fmf7h)

Se for selecionada a opção de "Consultar publicação completa", é aberta uma nova janela em que é pedido o doi(identificador) da publicação que o utilizador pretende consultar. Ao ser inserido um doi válido, a informação é mostrada na caixa de texto da janela principal.

As restantes das opções funcionam de forma semelhante. Dependendo de por que informação queremos consultar a publicação, é aberta uma nova janela a pedir essa mesma informação, ou seja, se quisermos consultar por palavra-chave, é aberta uma nova janela a pedir ao utilizador qual a palavra chave pela qual pretende procurar pela publicação.


### Botão Organizar Publicações

O botão "Organizar" permite ao utilizador organizar as publicações ou por ordem alfabética (de A a Z) ou pela data de publicação. Ao carregar neste botão vai ser aberta uma janela que permite ao utilizador selecionar de que maneira quer organizar as publicações. Após o fazer, irá aparecer na janela principal os titulos de todas as publicações da base de dados ordenadas da maneira selecionada.

[organizarbd-relatorio.png](https://postimg.cc/nsdVRBk1)


### Botão Análise de Publicação

O botão "Análise de Publicação" permite ao utilizador analisar as publicações pelos autores ou pelas palavras-chave. Esta analise pode em ambos os casos ser feita quer por ordem alfabética quer por ordem de frequência. Ao carregar neste botão é aberta uma janela que permite ao utilizador selcionar por que opção quer analisar as publicações: autor por ordem alfabética, autor por frequência de publicação, palavras-chave por ordem alfabética e palavras-chave por frequência. Tal como nas outras janelas se o botão "Submeter" for selecionado, realiza-se a opção. Caso contrário, se o botão "Sair" for selecionado cancela-se a opção.

[analisarbd-1-relatorio.png](https://postimg.cc/Q9SbMp7w)
 
Todas as opções funcionam de forma semelhante. Após o utilizador selecionar porque opção quer analisar as publicações, é aberta uma nova janela com todos os autores / palavras-chave organizados da maneira escolhida. O utilizador pode escolher então um autor / palavra-chave e visualizar todas as publicações em que sua opção está contida. 

[analisarbd-2-relatorio.png](https://postimg.cc/hzCLnKWq)

### Botão Estatística

O botão "Estatística" permite ao utilizador visualizar a informação contida na base de dados de formas distintas, com recurso a vários gráficos. Ao carregar neste botão é aberta uma janela para que o utilizador consiga selecionar qual o gráfico que pretende visualizar. Os gráficos que podem ser desenhados são: publicações por ano, publicações por mês por ano, top 20 autores, publicações por ano de um autor e top 20 palavras-chave.Dependendo da opção que for selecionada, são pedidas ao utilizador as restantes informações necessárias para desenhar o gráfico.

[estatisticabd-relat-rio.jpg](https://postimg.cc/qNdK61TY)

### Botão Importar BD

O botão "Importar BD" permite ao utilizador carregar mais informação, desde que seja no mesmo formato, para a aplicação. Ao carregar neste botão é aberta uma nova janela com três botões: "Browse", "Ok" e "Cancelar". O botão "Browse", permite ao utilizador procurar nos ficheiros armazenados no seu computador qual pretende carregar. O botão "Ok", importa o ficheiro e juntas os dados contidos neste aos dados já carregados para aplicação sem repetir informação. Já o "Cancelar", cancela a ação.

[importar-bd-relatorio.png](https://postimg.cc/PvmhTVpb)

### Botão Exportar BD

O botão "Exportar BD" permite ao utilizador guardar as alterações feitas na base de dados num novo ficheiro. Ao carregar neste botão surge uma nova janela com três botões: "Procurar", "Exportar" e "Cancelar". O botão procurar permite selecionar um ficheiro guardado no armazenamento do computador e substitui-lo pelo ficheiro que queremos guardar. Caso o utilizador não pretenda selecionar um ficheiro já existente, poderá apenas defenir o nome que quer dar ao novo ficheiro e este será criado.

Tal como nas restantes janelas, o botão "Sair" permite realizar a operação e o botão "Sair" cancela a mesma.

[exportarbd-relatorio.png](https://postimg.cc/dkT80JVM)


### Botão Sair
Na interface principal exite um botão "Sair"que permite ao utilizador fechar a aplicação. Ao ser pressionado esse botão, abre-se uma nova janela onde pergunta se o utilizador pretende mesmo encerrar a app ou não.

[sairbd-relatorio.png](https://postimg.cc/zLKBGLFC)


### Botão Ajuda

O botão "Ajuda" foi desenvolvido para auxiliar o utilizador a perceber quais os passos que terá que seguir para conseguir operar de forma correta a apalicação. Este está dividido em dez submenus, que explicam todos os botões da janela principal com a excessão do botão "Sair". Dentro de cada um destes submenus é possível aceder às instruções respetivas a cada funcionalidade.

Deste modo, ao clicar em "Ajuda" e, seguidamente, em "Nova Publicação", por exemplo, irá surgir uma nova janela com uma imagem da janela dessa função e as intruções correspondentes sobre como funcionar com esta. Além disto, existe ainda o botão "Voltar" para fechar a janela.

[ajudabd-relat-rio.png](https://postimg.cc/f3ppg72x)

## Conclusão

Este projeto permitiu consolidar a UC de Algoritmos e Técnicas de Programação, explorando a potencialidade da linguagem Python e adquirindo melhores práticas de desenvolvimento de software.
  
Gostaríamos de conseguir ter aprimorado algumas funcionalidades da interface e da linha de comandos bem como o aspeto gráfico da aplicação.
Concluindo, a aplicação cumpriu os requisitos propostos para o projeto, mas também aqueles que fomos acrescentando ao longo da realização do trabalho, nomeadamente o menu Ajuda na interface.

## Bibliografia
FreeSimpleGUI
https://epl.di.uminho.pt/~jcr/AULAS/ATP2024/aulas2024.html