## **Projeto de obtenção de dados TEC:**
### *Andres Benoit - andres.benoit7@gmail.com*
=============================================

### Bibliotecas utilizadas
- PyMysql - Para fazer a comunicação com o banco de dados
- JSON - Para retornar Json files na API
- Flask - Framework para a API
- Os - para algumas funções recorrentes como criar um diretório
- Time - Para contabilizar o tempo que leva o código em operar

=============================================

### Informações importantes
- Todos os dados selecionados e colocados em um banco de dados são providenciados pela IGS(International GNSS Service) e podem ser encontrados
no repositório da NASA em: ftp://cddis.nasa.gov/gnss/products/ionex/
- O deploy da API foi feita no Heroku

=============================================

### Arquivos
- main.py contém o coração do projeto, nele foi desenvolvido a interface para filtar o arquivo IONEX e armazenar no BD, assim como chamar as classes de outros arquivos
- api.py contém o cógido desenvolvido para a construção da API.
- tecdata/criarbd.py - contém o código para criar o banco de dados no servidor dada uma data em ano, a nomeclatura criada é ano_latitude_longitude
- tecdata/importarz.py - contém o código para importar os dados do repositório da NASA, criar a posta separada em anos e armazenar nela os arquivos compactados

=============================================

### Estrutura do Banco de dados
Existem 71 tabelas contendo dados TEC por ano. Para cada tabela é atribuida a seguinte nomeclatura ano_latitude.

Em cada banco de dados existem 76 colunas, a primeira é o identificador de cada linha, segue a hora do dia e o índice F10.7 (ainda não está com o valor correto), *futuramente serão adicionados outros índices para desenvolver uma análise mais aprimorada*. A colunas que seguem são as latitudes variando de -180 a 180 com passo de 5. Note que cada tabela possui 4745, isso se a que são 365 dias onde cada dia possui 13 intervalos, ou seja, começa na hora 0 e vai até a hora 24 com passo de 2, assim 365x13=4745.

=============================================

### Guia para utilizar a API:

1 - Para listar os dados TEC de um intervalo de dias: https://tecdatas.herokuapp.com/tec?ano=&lat=&dia_i=&dia_f=

=============================================

### Classes desenvolvidas
#### class criaBD():
Encontrada em criarbd.py - Utilizada para criar um banco de dados para dado intervalo de tempo em anos
#### class importtec():
Encontrada em importarz.py - Utilizada para importar os arquivos .Z do repositório da NASA, estes dados são armazenados localmente para futuro tratamento
