# dotpycSGE
Sistema de registro de entrega para condominio


Bem-Vindo a sua API DotPycSGE

 Developer: Michael de Mattos

1° Instalação e configuração do banco de dados: https://youtu.be/3PbM0_FIiWc

2° Aplique o Schema do banco de dados: dotpycSGE/model/query.sql

3° Configure o arquivo de conexao com o banco dedados: dotpycSGE/.config

4° Configure o arquivo de configuração do servidor de E-mail: dotpycSGE/font/engineers/.password

5° Aplique as informações de acesso ao banco de dados:

INSERT INTO EMPRESA (RAZAO_SOCIAL, CPF_CNPJ, DATA_CONTRACAO, SITUACAO, CHAVE)
            VALUES (
                    'MICHAEL.ORTIZ', 
                    'XX.XXX.XXX-XX', 
                    'current_timestrap', 
                    'A', 
                    'K2#KSF*G$w@#$'
                    );
            
            INSERT INTO LOGIN (USUARIO, SENHA, COD_EMPRESA)
            VALUES (
                    'DOTPYC', 
                    'semsenha', 
                    '1'
                    );

6° Realize o login na aplicação conforme os dados informados:
img src="https://i.imgur.com/CXAon89.png" class="img-fluid" alt="...">

7° Agora é só navegar nas opções da sua API
<img src="https://i.imgur.com/cN32c4e.png" class="img-fluid" alt="...">

Contate o desenvolvedor:
Telegram: +55 017 99174-0025
Whatsapp: +55 017 99174-0025
E-mail: chelmto3000@gmail.com
