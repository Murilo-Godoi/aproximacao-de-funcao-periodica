import csv
import math


# realizar produtos escalares
def produto_escalar(v1, v2):
    resultado = 0
    for i in range(len(v1)):
        resultado += (v1[i] * v2[i])
    return resultado


# importar os dados do arquivo fornecido, retorna uma lista de pares (x,y)
def data(arquivo):
    file = open(f'{arquivo}', 'r')
    csv_reader = csv.reader(file)

    lists_from_csv = []
    for row in csv_reader:
        lists_from_csv.append(row)
    lists_from_csv.pop(0)
    return lists_from_csv


# transforma os valores de x em um intervalo [0, 2π]
def transforma_em_pi(list):
    x = []
    for i in range(len(list)):
        x.append(2 * int(list[i][0]) * math.pi / tamanho_amostra)
    return x


# cria um vetor com os valores de f(x) fornecidos
def vetor_y(list):
    y = []
    for i in range(len(list)):
        y.append(float(list[i][1]))
    return y


# criam os vetores com os cossenos e senos a partir dos valors de x e alfa
def vetor_c(x, alfa):
    c = []
    for i in range(len(x)):
        c.append(math.cos(alfa * x[i]))
    return c


def vetor_s(x, alfa):
    s = []
    for i in range(len(x)):
        s.append(math.sin(alfa * x[i]))
    return s

#função que realiza o método dos mínimos quadrados - trigonométrico - caso discreto
def MMQ_trig_discreto(y,N):
    a = []
    b = []
    for i in range(ordem + 1):
        if i == 0:
            a_k = produto_escalar(y, vetor_c(x, i)) / (N)
            b_k = produto_escalar(y, vetor_s(x, i)) / (N)
            a.append(a_k)
            b.append(b_k)
        else:
            a_k = produto_escalar(y, vetor_c(x, i)) / (N / 2)
            b_k = produto_escalar(y, vetor_s(x, i)) / (N / 2)
            a.append(a_k)
            b.append(b_k)
    return a,b

#Função de aproximação definida a partir dos coeficientes a,b encontrados no MMQ-trigonométrico
def F(x):
    resultado = 0
    for i in range(len(a)):
        resultado += a[i] * math.cos(i * x) + b[i] * math.sin(i * x)
    return resultado

#como os valores fornecidos foram convertidos para um intervalo[0,2π], para aproximar valores fora do intervalo, é necessário converte-los proporcinalmente a esse intervalo
#essa função adiciona valores inteiros de x até o valor stop na lista de valores de x definida anteriormente
#cabe ressaltar que essa conversão poderia ser feita dentro na função de aproximação F(x), mas optei por essa forma para facilitar o entendimento da função de aproximação
def mais_valores_x(stop):
    for i in range(len(x)+1,stop+1):
        x.append(2 * i * math.pi / tamanho_amostra)
    return x

#converte um valor específico de x proporcionalmente ao intervalo [0,2π]
def valor_especifico_x(valor):
    return valor*2*math.pi/tamanho_amostra

#retorna uma string com a função de aproximação encontrada
def escreve_funcao():
    funcao = 'F(x) = %.2f' % (a[0])
    for i in range(1, len(a)):
        if a[i] >= 0:
            a_k = ' + %.2fcos(%ix)' % (a[i], i)
        else:
            a_k = ' - %.2fcos(%ix)' % (abs(a[i]), i)
        if b[i] >= 0:
            b_k = ' + %.2fsen(%ix)' % (b[i], i)
        else:
            b_k = ' - %.2fsen(%ix)' % (abs(b[i]), i)
        funcao += a_k + b_k
    return funcao

#escreve 2 arquivos de saida para a ordem de aproximação escolhida, um contendo as aproximações até o valor de 132 e outro contendo um resumo dos resultados obtidos
def arquivo_saida():
    dados_aproximados = []
    for i in range(len(x)):
        par_ordenado = []
        par_ordenado.append(i+1)
        par_ordenado.append(F(x[i]))
        dados_aproximados.append(par_ordenado)
    arquivo_saida = open('aproximações-%i.csv' % (ordem), 'w', newline='')
    writer = csv.writer(arquivo_saida, delimiter=',')
    for i in range(len(dados_aproximados)):
        writer.writerow(dados_aproximados[i])
    saida = open("resultados-%i.txt" % (ordem), "w")
    saida.write('Resultados para uma aproximação de ordem %i com o método dos mínimos quadrados trigonométrico - caso discreto\n\ncoeficientes a: \n %s \n\ncoeficientes b:\n%s\n\nFunção de aproximação\n%s' % (ordem, a, b, funcao))


dados = data('dados_temperatura_minima.csv')
tamanho_amostra = len(dados)
x = transforma_em_pi(dados)
y = vetor_y(dados)
N = len(dados)
ordem = int(input('ordem de aproximação:'))

while ordem >= (tamanho_amostra/2):
    print('A ordem de aproximação deve ser menor que metade do tamanho da amostra, escolha outro valor')
    ordem = int(input('ordem de aproximação:'))

a,b = MMQ_trig_discreto(y,N)
funcao = escreve_funcao()

mais_valores_x(132)
print(len(x))
arquivo_saida()
print(funcao)
print("A aproximação para o valor de 132 é %.6f"%(F(valor_especifico_x(132))))




