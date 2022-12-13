import argparse, time, sys
from logging import INFO, DEBUG
from random import randint
from datetime import datetime, timedelta
from globals import *
from payment_system.bank import Bank
from payment_system.payment_processor import PaymentProcessor
from payment_system.transaction_generator import TransactionGenerator
from utils.currency import Currency
from utils.logger import CH, LOGGER
import threading


if __name__ == "__main__":
    # Verificação de compatibilidade da versão do python:
    if sys.version_info < (3, 5):
        sys.stdout.write('Utilize o Python 3.5 ou mais recente para desenvolver este trabalho.\n')
        sys.exit(1)

    # Captura de argumentos da linha de comando:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_unit", "-u", help="Valor da unidade de tempo de simulação")
    parser.add_argument("--total_time", "-t", help="Tempo total de simulação")
    parser.add_argument("--debug", "-d", help="Printar logs em nível DEBUG")
    args = parser.parse_args()
    if args.time_unit:
        time_unit = float(args.time_unit)
    if args.total_time:
        total_time = int(args.total_time)
    if args.debug:
        debug = True

    # Configura logger
    if debug:
        LOGGER.setLevel(DEBUG)
        CH.setLevel(DEBUG)
    else:
        LOGGER.setLevel(INFO)
        CH.setLevel(INFO)

    # Printa argumentos capturados da simulação
    LOGGER.info(f"Iniciando simulação com os seguintes parâmetros:\n\ttotal_time = {total_time}\n\tdebug = {debug}\n")
    time.sleep(3)

    # Inicializa variável `tempo`:
    t = 0
    
    # Cria os Bancos Nacionais e popula a lista global `banks`:
    for i, currency in enumerate(Currency):
        
        # Cria Banco Nacional
        bank = Bank(_id=i, currency=currency)
        
        # Deposita valores aleatórios nas contas internas (reserves) do banco
        bank.reserves.BRL.deposit(10)
        bank.reserves.CHF.deposit(10)
        bank.reserves.EUR.deposit(10)
        bank.reserves.GBP.deposit(10)
        bank.reserves.JPY.deposit(10)
        bank.reserves.USD.deposit(10)

        for i in range(0, 10):
            bank.new_account(100, 200)
        
        # Adiciona banco na lista global de bancos
        banks.append(bank)

    # Inicializa gerador de transações e processadores de pagamentos para os Bancos Nacionais:
    for i, bank in enumerate(banks):
        # Inicializa um TransactionGenerator thread por banco:
        TransactionGenerator(_id=i, bank=bank).start()
        # Inicializa um PaymentProcessor thread por banco.
        # Sua solução completa deverá funcionar corretamente com múltiplos PaymentProcessor threads para cada banco.
        PaymentProcessor(_id=i, bank=bank).start()
        
    # Enquanto o tempo total de simuação não for atingido:
    while t < total_time:
        # Aguarda um tempo aleatório antes de criar o próximo cliente:
        dt = randint(0, 3)
        time.sleep(dt * time_unit)

        # Atualiza a variável tempo considerando o intervalo de criação dos clientes:
        t += dt

    for bank in banks:
        bank.operating = False
    
    ending_time = datetime.now()

    # @TODO: Finalizar todas as threads        

    # Termina simulação. Após esse print somente dados devem ser printados no console.
    LOGGER.info(f"A simulação chegou ao fim!\n")
     # status do banco
    for bank in banks:
        bank.info()

    transações_não_processadas = 0
    total_wait_time_seconds = 0

    for bank in banks:
        transações_não_processadas += len(bank.transaction_queue)
        for transaction in bank.transaction_queue:
            total_wait_time_seconds += ((ending_time - transaction.created_at).seconds - 1) #parece que ele arredonda pra cima
            
    average_wait_time = total_wait_time_seconds / transações_não_processadas
    LOGGER.info(f"Tempo médio de espera: {average_wait_time} segundos")
    LOGGER.info(f"Número total de transações não processadas: {transações_não_processadas}\n")
