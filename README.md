## **Projeto de obtenção de dados TEC:**
### *Andres Benoit - andres.benoit7@gmail.com*
=============================================

### Bibliotecas utilizadas
- PyMysql - Para fazer a comunicação com o banco de dados
- JSON - Para retornar Json files na API
- Flask - Framework para a API

=============================================

### Informações importantes
Todos os dados selecionados e colocados em um banco de dados são providenciados pela IGS(International GNSS Service) e podem ser encontrados
no repositório da NASA em: ftp://cddis.nasa.gov/gnss/products/ionex/

### Guia para utilizar a API:

1 - Para listar os dados TEC de todo o ano: 

=============================================

### Classes desenvolvidas
#### class criaBD():
Encontrada em criarbd.py - Utilizada para criar um banco de dados para dado intervalo de tempo em anos
#### class importtec():
Encontrada em importarz.py - Utilizada para importar os arquivos .Z do repositório da NASA, estes dados são armazenados localmente para futuro tratamento
