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
        "endereco": {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "UF": uf
        }
    }

    usuarios.append(novo_usuario)

    print(sucesso(f"Usuário {novo_usuario["nome"]} criado com sucesso!"))

    return novo_usuario


def criar_conta(contas, agencia, numero):
    cpf = get_cpf()
    usuario = get_usuario_from_list(cpf, usuarios)

    if not usuario:
        return print(erro("Não foi encontrado um usuário com esse CPF"))
    
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
    return [usuario for usuario in usuarios if usuario["cpf"] == cpf].pop() if usuarios else None


def get_cpf() -> str:
    cpf = str(input("Digite seu CPF: ")).strip()

    if not (re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) or re.match(r"\d{11}", cpf)):
        return print(erro("CPF inválido"))

    return cpf.replace(".", "").replace("-", "")


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

Selecione uma opção para continuar:'''

options = {
    "1": "novo usuário",
    "2": "nova conta",
    "3": "sacar",
    "4": "depositar",
    "5": "extrato",
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

    for num, operation in options.items():
        print(f"[{num}] {operation.title()}")

    selected_option = input("=> ")

    if selected_option not in options.keys():
        print(erro("Selecione uma opção válida!"))

    elif options[selected_option] == "sacar":
        valor = float(input("Digite o valor que você quer sacar: R$ "))
        saldos, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=LIMITE,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES
        )

    elif options[selected_option] == "depositar":
        valor = float(input("Digite o valor que você quer depositar: R$ "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif options[selected_option] == "extrato":
        exibir_extrato(saldo, extrato=extrato)

    elif options[selected_option] == "novo usuário":
        usuario_atual = criar_usuario(usuarios)

    elif options[selected_option] == "nova conta":
        numero = len(contas) + 1
        criar_conta(contas, AGENCIA, numero)

    elif options[selected_option] == "sair":
        print("Obrigado por usar o nosso sistema!!! :)")
        break