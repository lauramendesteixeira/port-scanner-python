# PORT SCANNER - SENAI (FASE 1)

**Autores:** Laura Mendes Teixeira e Joy Gabriella Sanchez da Silva

---

## O QUE FAZ

Scanner de porta única com interface gráfica. Verifica se uma porta específica está aberta ou fechada em um host.

---

## FUNCIONALIDADES

- Interface gráfica azul marinho
- Campo para host, porta e timeout
- Timeout configurável (padrão 2 segundos)
- Thread para não travar a tela
- Mensagens coloridas: verde para aberta, vermelho para fechada/erro
- Tratamento de erros (host inválido, porta inválida)

---

## COMO USAR

1. Execute o programa
2. Digite o host/IP (ex: 192.168.56.101)
3. Digite a porta (ex: 80)
4. Clique em "INICIAR SCAN"
5. Aguarde o resultado

---

## TESTES REALIZADOS

**VM Metasploitable (192.168.56.101)**
- Porta 21 (FTP): ABERTA
- Porta 22 (SSH): ABERTA
- Porta 23 (Telnet): ABERTA
- Porta 80 (HTTP): ABERTA
- Porta 443 (HTTPS): FECHADA

**IPs Externos**
- 8.8.8.8 porta 443: ABERTA
- 8.8.8.8 porta 53: ABERTA
- scanme.nmap.org porta 80: ABERTA

**Tratamento de Erros**
- Host inexistente: mensagem de erro
- Porta inválida (70000): mensagem de erro
- Argumentos faltando: mensagem de uso correto

---

## PRINCIPAIS FUNÇÕES DO CÓDIGO

**check_port()** - Cria um socket TCP e tenta conectar. Retorna True se a conexão for bem sucedida (connect_ex retorna 0).

**start_scan()** - Valida os dados do usuário e cria uma thread para executar o scan sem travar a interface.

**run_scan()** - Executa o scan de fato, exibe cabeçalho e resultados.

**log_message()** - Insere mensagens coloridas no painel de resultados.

---

## PRÉ-REQUISITOS

Python 3.6 ou superior
