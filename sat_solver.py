# Alunos: Julia Retore e Lucas Thomas
import sys

# Leitura do arquivo no formato DIMACS CNF
def leitura_arquivo_cnf(nome_arquivo):
  clausulas = set() # utilização de set pra eliminar cláusulas duplicadas
  with open(nome_arquivo, 'r') as arquivo:
    for linha in arquivo:
        # preâmbulo
        if linha.startswith('c'): continue # ignorar comentários
        if linha.startswith('p'):
            _, _, num_literais, num_clausulas = linha.split()
        # cláusulas
        else:
            literais = list(map(int, linha.split()))
            literais = tuple(set(literais[:-1])) #retira o 0 do final;
            clausulas.add(literais)

  return [list(t) for t in clausulas], int(num_literais), int(num_clausulas)

# Simplifica o conjunto de cláusulas, por propagação unitária
def simplifica_clausula_unitaria(F, valoracao):
    clausulas_unitarias = [clausula for clausula in F if len(clausula) == 1] 
    while clausulas_unitarias: 
        L = clausulas_unitarias[0][0]
        F = propagacao(F, L)
        valoracao += [L]
        if(F == -1): return -1, []
        if(len(F) == 0):return F, valoracao 

        clausulas_unitarias = [clausula for clausula in F if len(clausula) == 1]
    return F, valoracao 

# Simplifica o conjunto de cláusulas, por propagação da valoração do átomo correspondente
def propagacao(F, L):
    nova_F = []
    for clausula in F:
        if  L in clausula: continue
        if -L in clausula:  # Se ∼L estiver na cláusula, removemos ∼L
            nova_clausula = [x for x in clausula if x != -L]
            if len(nova_clausula) == 0:  
                return -1  # A fórmula é insatisfatível (⊥)
            nova_F.append(nova_clausula) 
        else:
            nova_F.append(clausula)
    return nova_F

# Heurística de Seleção do Literal: MOM
def Heuristica_MOM(F):
    moms = {}
    maior_ocorrencia = 0
    literal_maior_ocorrencia = 0
    tamanho_minimo = len(F[0])

    for clausula in F:
       tamanho_minimo = min(tamanho_minimo, len(clausula))
    
    for clausula in F:
      if len(clausula) == tamanho_minimo:
        for L in clausula:
          if L in moms: moms[L] += 1
          else:  moms[L] = 1
          if moms[L] > maior_ocorrencia:
            maior_ocorrencia = moms[L]
            literal_maior_ocorrencia = L
    return literal_maior_ocorrencia

# Algoritmo de DPLL
def dpll(F, valoracao):
    if(F != -1): F, valoracao = simplifica_clausula_unitaria(F, valoracao)
    if(F == -1): return [] 
    if(len(F) == 0): return valoracao 
    

    # Seleção do literal de forma sequencial:
    # for L in range(1, num_literais + 1):
    #     if L not in valoracao and -L not in valoracao:            
    #         nova_valoracao = dpll(propagacao(F, L), valoracao + [L])
    #         if(nova_valoracao == -1):
    #             nova_valoracao = dpll(propagacao(F, -L), valoracao + [-L])
    #         if(nova_valoracao != -1): return nova_valoracao


    # Seleção do literal pela Heurística MOM:
    L = Heuristica_MOM(F)

    nova_valoracao = dpll(propagacao(F, L), valoracao + [L])
    if not nova_valoracao:
        nova_valoracao =  dpll(propagacao(F, -L), valoracao + [-L])
    return nova_valoracao

# Formata a saída esperada e salva no arquivo de resposta
def escreve_saida(nome_arquivo_origem, valoracao):
    nome_arquivo_saida = nome_arquivo_origem.rsplit('.', 1)[0] + '.res'
    with open(nome_arquivo_saida, 'w') as arquivo:
        if valoracao:
            arquivo.write("SAT\n")
            if(valoracao): valoracao.extend([i for i in range(1, num_literais + 1) if i not in valoracao and -i not in valoracao])
            valoracao = sorted(valoracao, key=abs)
            valoracao_str = ' '.join(map(str, valoracao)) + ' 0\n'
            arquivo.write(valoracao_str)
        else:
            arquivo.write("UNSAT\n")

# Calcula a frequencia de cada literal em um conjunto de cláusulas
def frequencia_literais(F):
    frequencia = {}
    for clausula in F:
        for literal in clausula:
            if literal in frequencia: frequencia[literal] += 1
            else: frequencia[literal] = 1
    return frequencia

# Eliminação de literais puros
def remove_literais_puros(F, frequencia, valoracao):
    literais_puros = {L for L in frequencia if -L not in frequencia}
    for L in literais_puros:
        F = propagacao(F, L)  # Propagação para eliminar cláusulas
        valoracao += [L]
    return F, valoracao

# Resolução de Literais Simples
def resolucao_literais_simples(F, frequencia, valoracao):
    literais_simples = [L for L, cont in frequencia.items() if cont == 1]
    for L in literais_simples:
        F = propagacao(F, L)  # Propagação para eliminar cláusulas que contêm o literal
        valoracao += [L]
    return F, valoracao

# Eliminação de Literais Opostos
def elimina_literais_opostos(F):
    nova_F = []

    for clausula in F:
        literais_presentes = set()
        tem_oposto = False
        for literal in clausula:
            if -literal in literais_presentes:
                tem_oposto = True
                break
            literais_presentes.add(literal)
        if not tem_oposto:
            nova_F.append(clausula)  # Adiciona a cláusula se não contém literais opostos

    return nova_F

# Aplica simplificações
def aplica_simplificacoes(F):
    frequencia = frequencia_literais(F)
    F = elimina_literais_opostos(F)
    if F == -1: return []
    frequencia = frequencia_literais(F)
    F, valoracao = remove_literais_puros(F, frequencia, [])
    if F == -1: return []
    frequencia = frequencia_literais(F)
    F, valoracao = resolucao_literais_simples(F, frequencia, valoracao)
    if F == -1: return []

    return F, valoracao

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python seu_script.py nome_do_arquivo")
        sys.exit(1)
    nome_arquivo_origem = sys.argv[1]
    
    clausulas, num_literais, num_clausulas = leitura_arquivo_cnf(nome_arquivo_origem)
    clausulas, valoracao = aplica_simplificacoes(clausulas)
    valoracao = dpll(clausulas, valoracao)
    escreve_saida(nome_arquivo_origem, valoracao)


#Como escolher o literal:
# 1- Sequencialmente
# 2- MOM: Máximo número de Ocorrências de Mínimo comprimento. 

#Simplificações: 
# 1- Eliminação cláusulas duplicadas
# 2- Eliminação de literais puros 
# 3- Resolução de literais simples 
# 4- Eliminação de literais opostos



