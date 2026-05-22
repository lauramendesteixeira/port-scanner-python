# PORT SCANNER - SENAI (FASE 2)

**Autores:** Laura Mendes Teixeira e Joy Gabriella Sanchez da Silva

---

## O QUE FAZ

Scanner de range de portas com medição de tempo e identificação de serviços. Diferente da Fase 1, testa várias portas de uma só vez.

---

## DIFERENÇA DA FASE 1

- Fase 1: testava apenas uma porta por vez
- Fase 2: testa um intervalo inteiro (ex: da porta 1 até 100)

---

## FUNCIONALIDADES

- Interface gráfica azul marinho
- Campos para host, porta inicial e porta final
- Dicionário de serviços (ex: porta 21 = FTP, porta 22 = SSH)
- Identifica e exibe o nome do serviço ao lado da porta
- Barra de progresso com percentual
- Medição de tempo total da varredura
- Botão "PARAR SCAN" para interromper
- Botão "LIMPAR RESULTADOS"

---

## COMO USAR

1. Execute o programa
2. Digite o host/IP (ex: 192.168.56.101)
3. Digite a porta inicial (ex: 1)
4. Digite a porta final (ex: 100)
5. Clique em "INICIAR SCAN"
6. Acompanhe a barra de progresso e os resultados

---

## TESTES REALIZADOS

**VM Metasploitable (192.168.56.101)**

Range 1 a 100:
- Porta 21: FTP (ABERTA)
- Porta 22: SSH (ABERTA)
- Porta 23: Telnet (ABERTA)
- Porta 25: SMTP (ABERTA)
- Porta 53: DNS (ABERTA)
- Porta 80: HTTP (ABERTA)

Range 101 a 200:
- Porta 111: RPC (ABERTA)
- Porta 139: NetBIOS (ABERTA)

**Tempo total:** aproximadamente 188 segundos para 100 portas

---

## PRINCIPAIS FUNÇÕES DO CÓDIGO

**Dicionário servicos** - Mapeia portas para nomes de serviços.

**get_service_name()** - Recebe a porta e retorna o nome do serviço.

**scan_port_range()** - Loop que percorre todas as portas do range, atualiza a barra de progresso e exibe as portas abertas com seus serviços.

**run_scan()** - Marca o tempo de início com time.time(), executa o scan e calcula o tempo total no final.

**stop_scan()** - Muda a variável is_scanning para False, interrompendo o loop.

---

## PARTE MAIS DESAFIADORA

A barra de progresso e a medição de tempo. Foi necessário atualizar a interface a cada porta escaneada sem travar o programa.

---

## PRÉ-REQUISITOS

Python 3.6 ou superior
