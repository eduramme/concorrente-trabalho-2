from threading import Thread, Condition, Lock


# Lista de Bancos Nacionais
banks = []

# Printar Logs de DEBUG no console?
debug = False

# Tempo total de simulação
total_time = 1000

# Unidade de tempo (quanto menor, mais rápida a simulação)
time_unit = 0.1  # 0.1 = 100ms

# #locks
# lock = Lock()
# transacao_na_fila = Condition(lock)