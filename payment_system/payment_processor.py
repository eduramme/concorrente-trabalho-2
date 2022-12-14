import time
from threading import Thread

from globals import *
from payment_system.bank import Bank
from utils.transaction import Transaction, TransactionStatus
from utils.currency import get_exchange_rate, Currency
from utils.logger import LOGGER


class PaymentProcessor(Thread):
    """
    Uma classe para representar um processador de pagamentos de um banco.
    Se você adicionar novos atributos ou métodos, lembre-se de atualizar essa docstring.

    ...

    Atributos
    ---------
    _id : int
        Identificador do processador de pagamentos.
    bank: Bank
        Banco sob o qual o processador de pagamentos operará.

    Métodos
    -------
    run():
        Inicia thread to PaymentProcessor
    process_transaction(transaction: Transaction) -> TransactionStatus:
        Processa uma transação bancária.
    """

    def __init__(self, _id: int, bank: Bank):
        Thread.__init__(self)
        self._id  = _id
        self.bank = bank


    def run(self):
        """
        Esse método deve buscar Transactions na fila de transações do banco e processá-las 
        utilizando o método self.process_transaction(self, transaction: Transaction).
        Ele não deve ser finalizado prematuramente (antes do banco realmente fechar).
        """

        LOGGER.info(f"Inicializado o PaymentProcessor {self._id} do Banco {self.bank._id}!")
        queue = self.bank.transaction_queue
        lock = self.bank.lock
        transacao_na_fila = self.bank.transacao_na_fila

        while self.bank.operating:
            transaction = None
            try:
                with lock:
                    if (queue == []):
                        print("Fila vazia")
                        transacao_na_fila.wait()
                    transaction = queue.pop(-1)
                LOGGER.info(f"Transaction_queue do Banco {self.bank._id}: {len(queue)}")
            except Exception as err:
                LOGGER.error(f"Falha em PaymentProcessor.run(): {err}")
            else:
                self.process_transaction(transaction)

        LOGGER.info(f"O PaymentProcessor {self._id} do banco {self.bank._id} foi finalizado.")


    def process_transaction(self, transaction: Transaction) -> TransactionStatus:
        """
        Esse método deverá processar as transações bancárias do banco ao qual foi designado.
        Caso a transferência seja realizada para um banco diferente (em moeda diferente), a 
        lógica para transações internacionais detalhada no enunciado (README.md) deverá ser
        aplicada.
        Ela deve retornar o status da transacão processada.
        """
        
        # TODO: Proteger cada conta com Lock / checkar a ordem desses locks para evitar condição de corrida
        conta_origem = banks[transaction.origin[0]].accounts[transaction.origin[1]]
        banco_origem = banks[transaction.origin[0]]
        conta_destino = banks[transaction.destination[0]].accounts[transaction.destination[1]]

        if (conta_origem.currency == conta_destino.currency):
            conta_origem.withdraw(transaction.amount)
            conta_destino.deposit(transaction.amount)
            with banco_origem.lock_transferencias_nac:
                banco_origem.transferencias_nac += 1
        else:
            # exchange_rate = get_exchange_rate(conta_origem.currency, conta_destino.currency)

            conta_origem.withdraw(transaction.amount)
            
            # if conta_origem.currency == Currency.USD:
            #     origem_curr = self.bank.reserves.USD
            # elif conta_origem.currency == Currency.EUR:
            #     origem_curr = self.bank.reserves.EUR
            # elif conta_origem.currency == Currency.GBP:
            #     origem_curr = self.bank.reserves.GBP
            # elif conta_origem.currency == Currency.JPY:
            #     origem_curr = self.bank.reserves.JPY
            # elif conta_origem.currency == Currency.CHF:
            #     origem_curr = self.bank.reserves.CHF
                
            # origem_curr.deposit(transaction.amount * exchange_rate)

            # if conta_destino.currency == Currency.USD:
            #     destino_curr = self.bank.reserves.USD
            # elif conta_destino.currency == Currency.EUR:
            #     destino_curr = self.bank.reserves.EUR
            # elif conta_destino.currency == Currency.GBP:
            #     destino_curr = self.bank.reserves.GBP
            # elif conta_destino.currency == Currency.JPY:
            #     destino_curr = self.bank.reserves.JPY
            # elif conta_destino.currency == Currency.CHF:
            #     destino_curr = self.bank.reserves.CHF

            # destino_curr.withdraw(transaction.amount)

            conta_destino.deposit(transaction.amount)

            with banco_origem.lock_transferencias_int:
                banco_origem.transferencias_int += 1
           

        LOGGER.info(f"PaymentProcessor {self._id} do Banco {self.bank._id} iniciando processamento da Transaction {transaction._id}!")
        
        # NÃO REMOVA ESSE SLEEP!
        # Ele simula uma latência de processamento para a transação.
        time.sleep(3 * time_unit)

        transaction.set_status(TransactionStatus.SUCCESSFUL)
        return transaction.status
