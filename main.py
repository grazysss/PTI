# Planejamento de Treinos Inteligente com IA (PTI)

import streamlit as st
from rich.console import Console
import key
from google import genai
import time

client = genai.Client(api_key= key.API_KEY)
console = Console()

ficha = []

def inicio(ficha):
    console.print('[bold blue]Seja bem vindo ao sistema de armazenamento de treinos![/bold blue]')
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
    email = input('Insira seu EMAIL:\n')

    try:
        if '@gmail.com' in email or '@hotmail.com' in email or '@outlook.com' in email:
            with open('usuarios.csv', 'r') as arquivo:
                usuarios = arquivo.readlines()
        else:
            print('Email inválido!')
    except FileNotFoundError:
        print('Nenhum usuário cadastrado ainda.')
        cadastrar_conta(ficha)
        return
    
    for linha in usuarios:
        dados = linha.strip().split(';')
        if dados[3] == email:
            senha = input('Insira sua senha:\n')
            if dados[4] == senha:
                print('Você fez seu login com sucesso!')
                menu(ficha)
                return
            else:
                print('Senha incorreta. Tente novamente.')
                return 
    print('Email inválido! Insira novamente.')

def menu(ficha):
    console.print('[bold red]Planejamento de Treinos Inteligente[/bold red]')
    print('1. Exibir Ficha de Treino')
    print('2. Cadastrar Dados')
    print('3. Editar Dados')
    print('4. Remover Exercício')
    print('5. Pesquisar Dados')
    print('6. Salvar a Ficha do Treino')
    print('7. Consultar IA')
    print('8. Sair')
    print('')

    def exibir(ficha):
        print('Ficha de Treino:')
        print(ficha)
    
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
        print('Editar Dados:')
        exercicio = input('Nome do Exercício: ')
        for i in range(len(ficha)):
            if ficha[i][0] == exercicio:
                series = input('Número de Séries: ')
                repeticoes = input('Número de Repetições: ')
                carga = input('Carga: ')
                observacoes = input('Observações: ')
                ficha[i] = [exercicio, series, repeticoes, carga, observacoes]
                print('Exercício editado com sucesso!')
                return
        print('Exercício não encontrado!')

    def remover(ficha):
        print('Remover Exercício:')
        exercicio = input('Nome do Exercício: ')
        for i in range(len(ficha)):
            if ficha[i][0] == exercicio:
                del ficha[i]
                print('Exercício removido com sucesso!')
                return
        print('Exercício não encontrado!')

    def pesquisar(ficha):
        print('Pesquisar Dados:')
        exercicio = input('Nome do Exercício: ')
        for i in range(len(ficha)):
            if ficha[i][0] == exercicio:
                print(ficha[i])
                return
        print('Exercício não encontrado!')

    def salvar(ficha):
        print('Salvar a Ficha do Treino:')
        arquivo = open('ficha_treino.csv', 'w')
        for exercicio in ficha:
            arquivo.write(f'{exercicio[0]};{exercicio[1]};{exercicio[2]};{exercicio[3]};{exercicio[4]}\n')
        arquivo.close()
        print('Ficha de treino salva com sucesso!')

    def consultarIA(ficha):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="""
            Gere uma tabela em formato CSV de 5 dias de treinamento.
            Gere uma tabela CSV com um programa de treinamento de força e resistência para 5 dias, incluindo exercícios, repetições, séries e instruções detalhadas.
            Somente a tabela, sem comentários ou instruções adicionais.
            """,
        )
        print(response.text)

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
            break
        elif option == 8:
            console.print('[bold red]Você saiu do sistema![/bold red]')
            break

inicio(ficha)