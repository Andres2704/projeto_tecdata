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
Existem 5183 tabelas contendo dados TEC por ano. Para cada tabela é atribuida a seguinte nomeclatura ano_latitude_longitude. 

Em cada banco de dados existem 15 colunas, começando com o dia, no qual este varia de 1 a 365, seguido de 13 tabelas contentdos os valores de TEC para cada hora do dia com um passo de 7200s, ou seja, a cada duas horas e por último o índice F10.7. Futuramente serão adicionadas outras fequências para a análise.

=============================================

### Guia para utilizar a API:

1 - Para listar os dados TEC de todo o ano: https://tecdatas.herokuapp.com/tec?dia=&lat=&lon

=============================================

### Classes desenvolvidas
#### class criaBD():
Encontrada em criarbd.py - Utilizada para criar um banco de dados para dado intervalo de tempo em anos
#### class importtec():
Encontrada em importarz.py - Utilizada para importar os arquivos .Z do repositório da NASA, estes dados são armazenados localmente para futuro tratamento
