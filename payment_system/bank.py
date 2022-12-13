from typing import Tuple
from threading import Thread, Condition, Lock

from payment_system.account import Account, CurrencyReserves
from utils.transaction import Transaction
from utils.currency import Currency
from utils.logger import LOGGER


class Bank():
    """
    Uma classe para representar um Banco.
    Se você adicionar novos atributos ou métodos, lembre-se de atualizar essa docstring.

    ...

    Atributos
    ---------
    _id : int
        Identificador do banco.
    currency : Currency
        Moeda corrente das contas bancárias do banco.
    reserves : CurrencyReserves
        Dataclass de contas bancárias contendo as reservas internas do banco.
    operating : bool
        Booleano que indica se o banco está em funcionamento ou não.
    accounts : List[Account]
        Lista contendo as contas bancárias dos clientes do banco.
    transaction_queue : Queue[Transaction]
        Fila FIFO contendo as transações bancárias pendentes que ainda serão processadas.

    Métodos
    -------
    new_account(balance: int = 0, overdraft_limit: int = 0) -> None:
        Cria uma nova conta bancária (Account) no banco.
    new_transfer(origin: Tuple[int, int], destination: Tuple[int, int], amount: int, currency: Currency) -> None:
        Cria uma nova transação bancária.
    info() -> None:
        Printa informações e estatísticas sobre o funcionamento do banco.
    
    """

    def __init__(self, _id: int, currency: Currency):
        self._id                = _id
        self.currency           = currency
        self.reserves           = CurrencyReserves()
        self.operating          = True
        self.accounts           = []
        self.transaction_queue  = []

        # lock for queues
        self.lock               = Lock()
        self.transacao_na_fila  = Condition(self.lock)

        # bank info
        self.lock_transferencias_nac = Lock()
        self.lock_transferencias_int = Lock()

        self.transferencias_nac = 0 #proteger essas áreas do código na hora de incrementar
        self.transferencias_int = 0


    def new_account(self, balance: int = 0, overdraft_limit: int = 0) -> None:
        """
        Esse método deverá criar uma nova conta bancária (Account) no banco com determinado 
        saldo (balance) e limite de cheque especial (overdraft_limit).
        """
        # TODO: IMPLEMENTE AS MODIFICAÇÕES, SE NECESSÁRIAS, NESTE MÉTODO!

        # Gera _id para a nova Account
        acc_id = len(self.accounts) + 1

        # Cria instância da classe Account
        acc = Account(_id=acc_id, _bank_id=self._id, currency=self.currency, balance=balance, overdraft_limit=overdraft_limit)
  
        # Adiciona a Account criada na lista de contas do banco
        self.accounts.append(acc)


    def info(self) -> None:
        """
        Essa função deverá printar os seguintes dados utilizando o LOGGER fornecido:
        1. Saldo de cada moeda nas reservas internas do banco
        2. Número de transferências nacionais e internacionais realizadas
        3. Número de contas bancárias registradas no banco
        4. Saldo total de todas as contas bancárias (dos clientes) registradas no banco
        5. Lucro do banco: taxas de câmbio acumuladas + juros de cheque especial acumulados
        """
        # TODO: IMPLEMENTE AS MODIFICAÇÕES, SE NECESSÁRIAS, NESTE MÉTODO!

        saldo_clientes = []

        LOGGER.info(f"===========================================")
        LOGGER.info(f"Estatísticas do Banco Nacional {self._id}:")
        LOGGER.info(f"Saldo das moedas no Bancos: USD:{self.reserves.USD.balance}, BRL: {self.reserves.BRL.balance}, EUR: {self.reserves.EUR.balance}, CHB: {self.reserves.CHF.balance}, JPY: {self.reserves.JPY.balance}, GBP: {self.reserves.GBP.balance}")
        LOGGER.info(f"{self.transferencias_nac} e {self.transferencias_int} transferências nacionais e internacionas foram realizadas, respectivamente")
        LOGGER.info(f"O banco tem {len(self.accounts)} contas bancárias abertas")     
        for account in self.accounts:
            saldo_clientes.append(account.balance)
        LOGGER.info(f"saldo dos clientes: {saldo_clientes}")
        LOGGER.info(f"o Banco teve {11111111} de lucro")
        LOGGER.info(f"===========================================")

