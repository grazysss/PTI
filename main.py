# Planejamento de Treinos Inteligente com IA (PTI)

import streamlit as st
from rich.console import Console
import time

console = Console()

ficha = []
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
        print('Cadastrar Dados:')
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
                ficha.append([exercicio, series, repeticoes, '', ''])
                print('Exercício cadastrado com sucesso!')
        else:
            print('')
            pergunta = input('Deseja adicionar Carga e Observações? (S/N) ')
            if pergunta == 'S':
                carga = input('Carga: ')
                observacoes = input('Observações: ')
                ficha.append([exercicio, '','', carga, observacoes])
                print('Exercício cadastrado com sucesso!')
            else:
                ficha.append([exercicio, '','', '', ''])
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
        # elif option == 7:
        #     consultarIA(ficha)
        #     print('')
        #     break
        elif option == 8:
            print('[bold red]Você saiu do sistema![/bold red]')
            break

menu(ficha)