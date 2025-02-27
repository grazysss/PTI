# Planejamento de Treinos Inteligente com IA (PTI)
from rich.console import Console
from rich.table import Table
import key
from google import genai
import os

client = genai.Client(api_key= key.API_KEY)
console = Console()

ficha = []

def inicio(ficha):
    console.print('[bold red]Seja bem vindo ao sistema de armazenamento de treinos![/bold red]')
    verificar_conta(ficha)

def verificar_conta(ficha):
    exist = input('Já possui conta aqui? (S/N): ').strip().upper()

    if exist == 'S':
        entrar_conta(ficha)
    else:
        cadastrar_conta(ficha)
            
def cadastrar_conta(ficha):
    pergunta = input('Deseja criar sua conta? (S/N): ')
    if pergunta == 'S':
        nome = input('Nome: ')
        sobrenome = input('Sobrenome: ')
        social = input('Como deseja ser chamado? ')
        validado = False
        while not validado:
            print('')
            email = input('Insira seu EMAIL:\n')
            if '@gmail.com' in email or '@hotmail.com' in email or '@outlook.com' in email:
                print('Email válido!')
                validado = True
            else:
                print('Email inválido!')
                validado = False
        if validado:
            senha = input('Insira sua senha:\n')
            with open ('usuarios.csv', 'a') as arquivo:
                arquivo.write(f'{nome};{sobrenome};{social};{email};{senha}\n')
            with open ('usuarios.csv', 'r') as arquivo:
                usuarios = arquivo.readlines()

            while True:
                confirmar_senha = input('Confirme sua senha:\n')
                for linha in usuarios:
                    dados = linha.strip().split(';')
                if confirmar_senha in dados[4]:
                    print('Conta criada com sucesso!')
                    print('')
                    break
                else:
                    print('Senha inválida!')
            menu(ficha)

def entrar_conta(ficha):
    while True:
        email = input('Insira seu EMAIL: ')
        
        if not ('@gmail.com' in email or '@hotmail.com' in email or '@outlook.com' in email):
            print('Email inválido!')
            continue
        
        try:
            with open('usuarios.csv', 'r') as arquivo:
                usuarios = arquivo.readlines()
        except FileNotFoundError:
            print('Nenhum usuário cadastrado ainda.')
            cadastrar_conta(ficha)
            return
        
        usuario_encontrado = None
        
        for linha in usuarios:
            dados = linha.strip().split(';')
            if dados[3] == email:
                usuario_encontrado = dados
                break
        
        if usuario_encontrado:
            while True:
                senha = input('Insira sua senha: ')
                if usuario_encontrado[4] == senha:
                    print('Você fez seu login com sucesso!')
                    print('')
                    menu(ficha)
                    return
                else:
                    print('Senha incorreta. Tente novamente.')
        else:
            print('Email não cadastrado.')
        menu(ficha)

def menu(ficha):
    verificar = input('Já possui uma ficha? (S/N): ').strip().upper()
    if verificar != 'S':
        console.print("[bold yellow]A ficha de treino está vazia![/bold yellow]")
        print('Cadastre a sua!')

    def info(ficha):
        console.print('[bold red]Planejamento de Treinos Inteligente[/bold red]')
        print('1. Exibir Ficha de Treino')
        print('2. Cadastrar Dados')
        print('3. Editar Dados')
        print('4. Remover Exercício')
        print('5. Pesquisar Dados')
        print('6. Salvar a Ficha do Treino')
        print('7. Consultar IA')
        print('8. Limpar Terminal')
        print('9. Sair')
        print('')
    info(ficha)

    def exibir(ficha):
        if not ficha:
            console.print("[bold yellow]A ficha de treino está vazia![/bold yellow]")
            return
        
        tabela = Table(title="Ficha de Treino")

        tabela.add_column("Exercício", style="magenta")
        tabela.add_column("Séries", style="blue", justify="center")
        tabela.add_column("Repetições", style="green", justify="center")
        tabela.add_column("Carga", style="yellow", justify="center")
        tabela.add_column("Observações", style="cyan")

        for linha in ficha:
            tabela.add_row(*linha)

        console.print(tabela)
    
    def cadastrar(ficha):
        print('Cadastrar Dados')
        exercicio = input('Nome do Exercício: ')

        pergunta = input('Deseja adicionar Séries e Repetições? (S/N) ')
        if pergunta == 'S':
            series = input('Número de Séries: ')
            repeticoes = input('Número de Repetições: ')

            pergunta = input('Deseja adicionar Carga e Observações? (S/N) ')
            if pergunta == 'S':
                carga = input('Carga: ')
                observacoes = input('Observações: ')

                ficha.append([exercicio, series, repeticoes, carga, observacoes])
                print('Exercício cadastrado com sucesso!')

            else:
                ficha.append([exercicio, series, repeticoes, 'x', 'x'])
                print('Exercício cadastrado com sucesso!')
    
        else:
            pergunta = input('Deseja adicionar Carga e Observações? (S/N) ')
            if pergunta == 'S':
                carga = input('Carga: ')
                observacoes = input('Observações: ')
                ficha.append([exercicio, 'x','x', carga, observacoes])
                print('Exercício cadastrado com sucesso!')
    
            else:
                ficha.append([exercicio, 'x','x', 'x', 'x'])
                print('Exercício cadastrado com sucesso!')

    def editar(ficha):
        print('Editar Dados')
        pergunta = input('Qual deseja editar? (Exercício, Séries, Repetições, Carga ou Observação): ').strip().capitalize()

        if pergunta not in ['Exercício', 'Séries', 'Repetições', 'Carga', 'Observação']:
            print('Opção inválida!')
            return

        for i in range(len(ficha)):
            if pergunta == 'Exercício':
                novo_valor = input('Novo nome do Exercício: ').strip()
                ficha[i][0] = novo_valor
            elif pergunta == 'Séries':
                novo_valor = input('Novo número de Séries: ').strip()
                ficha[i][1] = novo_valor
            elif pergunta == 'Repetições':
                novo_valor = input('Novo número de Repetições: ').strip()
                ficha[i][2] = novo_valor
            elif pergunta == 'Carga':
                novo_valor = input('Nova Carga: ').strip()
                ficha[i][3] = novo_valor
            elif pergunta == 'Observação':
                novo_valor = input('Nova Observação: ').strip()
                ficha[i][4] = novo_valor

            print(f'{pergunta} editado(a) com sucesso!')
            return

        print('Exercício não encontrado!')

    def remover(ficha):
        print('Remover Exercício')
        exercicio = input('Nome do Exercício: ')
        for i in range(len(ficha)):
            if ficha[i][0] == exercicio:
                del ficha[i]
                print('Exercício removido com sucesso!')
                return
        print('Exercício não encontrado!')

    def pesquisar(ficha):
        print('Pesquisar Dados')
        exercicio = input('Nome do Exercício: ')
        for i in range(len(ficha)):
            if ficha[i][0] == exercicio:
                print(ficha[i])
                return
        print('Exercício não encontrado!')

    def limpar(ficha):
        os.system('cls')
        info(ficha)

    def salvar(ficha):
        print('Salvar a Ficha do Treino')
        with open ('ficha_treino.csv', 'a') as arquivo_ft:
            with open ('usuarios.csv', 'r') as arquivo_d:
                usuarios = arquivo_d.readlines()
            for linha in usuarios:
                dados = linha.strip().split(';')
                for exercicio in ficha:
                    arquivo_ft.write(f'{dados[2]};{exercicio[0]};{exercicio[1]};{exercicio[2]};{exercicio[3]};{exercicio[4]}\n')
        print('Ficha de treino salva com sucesso!')

        with open ('ficha_treino.csv', 'r') as arquivo_t:
            treino = arquivo_t.readlines()
            print(f'{treino[len(treino) - 1]}')
            print('')

    def consultarIA(ficha):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="""
            Gere uma tabela em formato CSV de 5 dias de treinamento.
            A tabela deve conter colunas: Dia (segunda/terça/quarta), Exercício, Repetições, Séries, Carga (moderada).
            Formato estritamente CSV, sem explicações ou textos adicionais.
            """,
        )

        tabela = Table(title='Plano de Treino - Força e Resistência')

        tabela.add_column('Dia', style='white', justify='center')
        tabela.add_column('Exercício', style='red')
        tabela.add_column('Repetições', style='white', justify='center')
        tabela.add_column('Séries', style='white', justify='center')
        tabela.add_column('Carga', style='white', justify='center')

        csv_ia = response.text

        linhas = csv_ia.split('\n')[1:]

        for linha in linhas:
            colunas = linha.split(',')
            tabela.add_row(*colunas)

        console.print(tabela)

        with open ("treinoIA.csv", "a", encoding="utf-8") as arquivo:
            with open ('usuarios.csv', 'r') as arquivo_d:
                usuarios = arquivo_d.readlines()
            for linha in usuarios:
                dados = linha.strip().split(';')
            arquivo.write(f'{dados[2]}')
            arquivo.write("Dia,Exercício,Repetições,Séries,Carga\n") 

            for linha in linhas:
                arquivo.write(linha + "\n")

            arquivo.write('')
        print("Plano de treino salvo em treinoIA.csv com sucesso!")

    while True:
        option = int(input('Insira uma opção: '))
        if option == 1:
            exibir(ficha)
            print('')
        elif option == 2:
            cadastrar(ficha)
            print('')
        elif option == 3:
            editar(ficha)
            print('')
        elif option == 4:
            remover(ficha)
            print('')
        elif option == 5:
            pesquisar(ficha)
            print('')
        elif option == 6:
            salvar(ficha)
            print('')
        elif option == 7:
            consultarIA(ficha)
            print('')
        elif option == 8:
            limpar(ficha)
            print('')
        elif option == 9:
            console.print('[bold red]Você saiu do sistema![/bold red]')
            break
        
inicio(ficha)