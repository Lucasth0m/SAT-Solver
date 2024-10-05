# Alunos: Julia Retore e Lucas Thomas
import sys

# leitura do arquivo no formato DIMACS CNF
def leitura_arquivo_cnf(nome_arquivo):
  clausulas = []
  with open(nome_arquivo, 'r') as arquivo:
    for linha in arquivo:
        # preâmbulo
        if linha.startswith('c'): continue # ignorar comentários
        if linha.startswith('p'):
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

def escrever_saida(nome_arquivo_origem, valoracao):
    nome_arquivo_saida = nome_arquivo_origem.rsplit('.', 1)[0] + '.res'
    
    with open(nome_arquivo_saida, 'w') as arquivo:
        if valoracao:
            arquivo.write("SAT\n")
            valoracao_str = ' '.join(map(str, valoracao)) + ' 0\n'
            arquivo.write(valoracao_str)
        else:
            arquivo.write("UNSAT\n")



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python seu_script.py nome_do_arquivo")
        sys.exit(1)
    nome_arquivo_origem = sys.argv[1]

    clausulas, num_literais, num_clausulas = leitura_arquivo_cnf(nome_arquivo_origem)
    valoracao = dpll(simplifica(clausulas), [])
    if(valoracao): valoracao.extend([i for i in range(1, num_literais + 1) if i not in valoracao and -i not in valoracao])
    escrever_saida(nome_arquivo_origem, valoracao)

        
