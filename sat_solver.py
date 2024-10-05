# leitura do arquivo no formato DIMACS CNF
def leitura_arquivo_cnf(nome_arquivo):
  clausulas = []
  with open(nome_arquivo, 'r') as arquivo:
    for linha in arquivo:
        # preâmbulo
        if linha.startswith('c'): continue # ignorar comentários
        if linha.startswith('p'): # precisa ????????
            _, _, num_literais, num_clausulas = linha.split()
        # cláusulas
        else:
            literais = list(map(int, linha.split()))
            literais = literais[:-1] #retira o 0 do final;
            clausulas.append(literais)
  return clausulas, int(num_literais), int(num_clausulas)


def simplifica(F):
    clausulas_unitarias = [clausula for clausula in F if len(clausula) == 1] 
    while clausulas_unitarias: 
        L = clausulas_unitarias[0][0]
        F = propagacao(F, L)
        clausulas_unitarias = [clausula for clausula in F if len(clausula) == 1]
    return F  

def propagacao(F, L):
    F = [clausula for clausula in F if L not in clausula]  # Remove as cláusulas que contêm L
    nova_F = []
    for clausula in F:
        if -L in clausula:  # Se ∼L estiver na cláusula, removemos ∼L
            nova_clausula = [x for x in clausula if x != -L]
            if len(nova_clausula) == 0:  # Se a cláusula se tornar vazia
                return -1  # A fórmula é insatisfatível (cláusula falsificada)
            nova_F.append(nova_clausula)  # Adiciona a nova cláusula à fórmula
        else:
            nova_F.append(clausula)  # Cláusula sem modificações
    return nova_F


def dpll(F, valoracao):
    if(F == -1): return [] 
    elif(len(F) == 0): return valoracao 

    for L in range(1, num_literais + 1):
        if L not in valoracao and -L not in valoracao:            
            nova_valoracao = dpll(propagacao(F, L), valoracao + [L])
            if not nova_valoracao:
                nova_valoracao = dpll(propagacao(F, -L), valoracao + [-L])
            
            return nova_valoracao
    return []


if __name__ == '__main__':
    clausulas, num_literais, num_clausulas = leitura_arquivo_cnf('teste.txt')
    F = simplifica(clausulas) 
    valoracao = dpll(clausulas, [])
    if(valoracao): 
        print('SAT')
        print(*valoracao, sep=" ", end=" ")
        print("0")
    else: 
        print('UNSAT')
        
