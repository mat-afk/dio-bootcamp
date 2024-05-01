columns = 65
dotted_line = "".center(columns, "-")

menu = f'''
{dotted_line}
{"BEM-VINDO AO SISTEMA BANCÁRIO".center(columns, " ")}
{dotted_line}

Selecione uma opção para continuar:'''

options = {
    "0": "Sacar",
    "1": "Depositar",
    "2": "Extrato",
    "3": "Sair"
}

extract = 0.0
selected_option = "0"
withdraws = []
WITHDRAW_VALUE_LIMIT = 500.0
DIARY_WITHDRAW_LIMIT = 3

print(menu)

while True:
    print()

    for key in options.keys():
        print(f"[{key}] {options[key]}")

    print()
    selected_option = input("=> ")

    if selected_option not in options:
        print("Selecione uma opção válida")

    elif options[selected_option] == "Sacar":
        print(options[selected_option].upper().center(columns, "-"))

        if len(withdraws) >= DIARY_WITHDRAW_LIMIT:
            print(f"Você só pode realizar no máximo {DIARY_WITHDRAW_LIMIT} operações de saque por dia")
            print(dotted_line)
            continue

        value = float(input("Digite o valor a ser sacado: R$ "))

        errors = []

        if value <= 0:
            errors.append("Você pode sacar apenas valores maiores do que zero em sua conta")

        if value > extract:
            errors.append("Você não pode sacar valores maiores que o seu extrato")

        if value > WITHDRAW_VALUE_LIMIT:
            errors.append(f"O seu limite de saque é de R$ {WITHDRAW_VALUE_LIMIT:.2f}")

        status = "sucesso" if not errors else "erro"
        print(f"Houve {status} na operação de saque")

        if errors:
            for err in errors:
                print(err)
            print("Tente novamente")
            continue
        else:
            extract -= value
            withdraws.append(value)

        print(dotted_line)

    elif options[selected_option] == "Depositar":
        print(options[selected_option].upper().center(columns, "-"))

        value = float(input("Digite o valor a ser depositado: R$ "))

        errors = []

        if value <= 0:
            errors.append("Você pode depositar apenas valores maiores do que zero em sua conta")

        status = "sucesso" if not errors else "erro"
        print(f"Houve {status} na operação de depósito")

        if errors:
            for err in errors:
                print(err)
            print("Tente novamente")
            continue
        else:
            extract += value

        print(dotted_line)

    elif options[selected_option] == "Extrato":
        print(options[selected_option].upper().center(columns, "-"))

        print(f"O seu extrato é de R$ {extract:.2f}")
        if withdraws:
            print(f"Os saques realizados na sua conta hoje foram de: {withdraws}")

        print(dotted_line)
    
    elif options[selected_option] == "Sair":
        print("Obrigado por usar o nosso sistema!!! :)")
        break