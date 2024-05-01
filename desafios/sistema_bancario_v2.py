import re

def sacar(*, 
    saldo: float, 
    valor: float, 
    extrato: str, 
    limite: float, 
    numero_saques: int, 
    limite_saques: int
):
    if valor <= 0:
        print(erro("Operação falhou! O valor de saque é inválido"))
    elif valor > saldo:
        print(erro("Operação falhou! Sua conta não tem saldo suficiente"))
    elif valor > limite:
        print(erro(f"Operação falhou! O valor do saque excede o limite"))
    elif numero_saques >= limite_saques:
        print(erro(f"Operação falhou! Você não pode realizar mais de {limite_saques} por dia"))
    else:
        saldo -= valor
        extrato += format_operacao("Saque", valor)
        numero_saques += 1

        print(sucesso("Saque realizado com sucesso!"))

    return saldo, extrato


def format_operacao(operacao: str, valor: float) -> str:
    formatted = "".center(60, " ")
    formatted = list(formatted)
    start = 0
    end = len(formatted) - 1
    formatted_valor = f"R$ {valor:.2f}"
    formatted_valor = list(formatted_valor)

    while start < end:
        formatted[start] = operacao[start] if start < len(operacao) else "."
        formatted[end] = formatted_valor[len(formatted_valor) - 1 - start] if len(formatted_valor) - 1 - start >= 0 else "."
        start += 1
        end -= 1

    return "".join(formatted) + "\n"

def depositar(saldo: float, valor: float, extrato: str, /):
    if valor <= 0:
        print(erro("Operação falhou! O valor de depósito é inválido"))
    else:
        saldo += valor
        extrato += format_operacao("Depósito", valor)
        print(sucesso("Depósito realizado com sucesso!"))

    return saldo, extrato


def exibir_extrato(saldo: float, /, *, extrato: str):
    print(boilerplate_line("=", "EXTRATO"))
    print(extrato if extrato else "Não foram realizadas operações")
    print(format_operacao("Saldo", saldo), end="")
    print(boilerplate_line("="))


def criar_usuario(usuarios):
    cpf = get_cpf()
    usuario = get_usuario_from_list(cpf, usuarios)

    if usuario:
        print(erro("Já existe um usuário com esse CPF"))
        return usuario

    nome = input("Informe seu nome: ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
    bairro, logradouro, numero = input("Informe seu endereço (bairro, logradouro, 000): ").split(", ")
    cidade, uf = input("Informe sua cidade e seu estado (cidade/UF): ").split("/")

    novo_usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": f"{logradouro}, {numero} - {bairro}, {cidade}/{uf}"
    }

    usuarios.append(novo_usuario)

    print(sucesso(f"Usuário {novo_usuario["nome"]} criado com sucesso!"))

    return novo_usuario


def criar_conta(contas, agencia, numero):
    cpf = get_cpf()
    usuario = get_usuario_from_list(cpf, usuarios)

    if not usuario:
        return print(erro("Não foi encontrado um usuário com esse CPF"))
    
    contas_existentes = get_contas_from_usuario(usuario, contas)
    if contas_existentes:
        print("Você tem as seguintes contas cadastradas: ")
        listar_contas(contas_existentes, usuario)

        numero_conta_selecionada = input("Digite o número da conta que você quer usar ou 0 para criar uma nova: ")

        if numero_conta_selecionada != "0":
            print(sucesso("Nova conta selecionada!"))
            return get_conta_from_list(numero_conta_selecionada, contas)
    
    nova_conta = {
        "agencia": agencia,
        "numero": numero,
        "cpf_usuario": usuario["cpf"],
        "saldo": 0.0,
        "extrato": [],
    }

    contas.append(nova_conta)
    
    print(sucesso(f"Conta {nova_conta["numero"]} criada com sucesso!"))

    return nova_conta


def get_usuario_from_list(cpf: str, usuarios: list):
    usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario.pop() if usuario else None

def get_conta_from_list(numero, contas: list):
    conta = [conta for conta in contas if conta["numero"] == numero]
    return conta.pop() if conta else None

def get_contas_from_usuario(usuario: dict, contas: list):
    return [conta for conta in contas if conta["cpf_usuario"] == usuario["cpf"]]

def get_usuario_from_conta(conta, usuarios):
    return [usuario for usuario in usuarios if conta["cpf_usuario"] == usuario["cpf"]].pop() if usuarios and conta else None

def listar_contas(contas, usuario):
    if not contas:
        print(erro("Você não tem contas cadastradas"))

    for conta in contas:
        print(boilerplate_line("-"))
        print(f"Agência: {conta["agencia"]}")
        print(f"C/C: {conta["numero"]}")
        print(f"Titular: {usuario["nome"]}")
        print(boilerplate_line("-"))

def get_cpf() -> str:
    cpf = str(input("Digite seu CPF: ")).strip()

    if not (re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) or re.match(r"\d{11}", cpf)):
        return print(erro("CPF inválido"))

    return cpf.replace(".", "").replace("-", "")


def has_usuario_atual(usuario_atual):
    if not usuario_atual:
        print(erro("Crie ou selecione um usuário para continuar"))
        return False
    
    return True

def has_conta_atual(conta_atual):
    if not conta_atual:
        print(erro("Crie ou selecione uma conta para continuar"))
        return False
    
    return True

def can_do_operations(usuario_atual, conta_atual):
    return has_usuario_atual(usuario_atual) and has_conta_atual(conta_atual)

# aux design functions

def boilerplate_line(placeholder: str = "-", text: str = "") -> str:
    TERMINAL_COLUMNS = 60
    text = " " + text + " " if text else text
    return text.center(TERMINAL_COLUMNS, placeholder)

def erro(message: str = "Houve um erro"):
    return boilerplate_line("@", "ERRO") + "\n" + boilerplate_line("@", message)

def sucesso(message: str = "Sucesso!"):
    return boilerplate_line("=", "SUCESSO") + "\n" + boilerplate_line("=", message)


menu = f'''
{boilerplate_line("-")}
{boilerplate_line(" ", "BEM-VINDO AO SISTEMA BANCÁRIO")}
{boilerplate_line("-")}
'''

options = {
    "1": "novo usuário",
    "2": "nova conta",
    "3": "sacar",
    "4": "depositar",
    "5": "extrato",
    "6": "listar contas",
    "0": "sair"
}

AGENCIA = "0001"
LIMITE = 500.0
LIMITE_SAQUES = 3

saldo = 0.0
extrato = ""
numero_saques = 0

usuarios = []
contas = []
usuario_atual = {}
conta_atual = {}

selected_option = "0"

print(menu)

while True:

    print("Selecione uma opção para continuar: ")
    for num, operation in options.items():
        print(f"[{num}] {operation.title()}")

    selected_option = input("=> ")

    if selected_option not in options.keys():
        print(erro("Selecione uma opção válida!"))

    elif options[selected_option] == "sacar":
        if not can_do_operations(usuario_atual, conta_atual):
            continue

        valor = float(input("Digite o valor que você quer sacar: R$ "))
        saldo, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=LIMITE,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES
        )

    elif options[selected_option] == "depositar":
        if not can_do_operations(usuario_atual, conta_atual):
            continue

        valor = float(input("Digite o valor que você quer depositar: R$ "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif options[selected_option] == "extrato":
        if not can_do_operations(usuario_atual, conta_atual):
            continue

        exibir_extrato(saldo, extrato=extrato)

    elif options[selected_option] == "novo usuário":
        usuario_atual = criar_usuario(usuarios)

    elif options[selected_option] == "nova conta":
        numero = str(len(contas) + 1)
        conta_atual = criar_conta(contas, AGENCIA, numero)

    elif options[selected_option] == "listar contas":
        if not can_do_operations(usuario_atual, conta_atual):
            continue
        
        contas_usuario = get_contas_from_usuario(usuario_atual, contas)
        listar_contas(contas_usuario, usuario_atual)

    elif options[selected_option] == "sair":
        print("Obrigado por usar o nosso sistema!!! :)")
        break