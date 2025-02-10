'''
tablero.py: Dibuja el tablero del juego de el gato
'''
import random

def dibuja_tablero(simbolos:dict):
    print(f'''
    {simbolos['1']} | {simbolos['2']} | {simbolos['3']}
    ---------
    {simbolos['4']} | {simbolos['5']} | {simbolos['6']}
    ---------
    {simbolos['7']} | {simbolos['8']} | {simbolos['9']}
    ''')

def ia(simbolos:dict, lista_combinaciones:list):
    '''Juega la maquina'''
    for combinaciones in lista_combinaciones:
        casillas=[simbolos[c] for c in combinaciones]
        casilla_libre_combinacion=[c for c in combinaciones if simbolos[c]==c]
        #Si la IA ve una combinación con 2 casillas 'O' y la otra vacía, la elige para ganar
        if (casillas.count('O') == 2 and casilla_libre_combinacion):
            simbolos[casilla_libre_combinacion[0]]='O'
            return
        #Si la IA ve una combinación con 2 casillas 'X' y la otra vacía, la elige para bloquear
        if (casillas.count('X') == 2 and casilla_libre_combinacion):
            simbolos[casilla_libre_combinacion[0]]='O'
            return
    #Si el centro está libre, lo elige
    if '5' in casillas:
        simbolos['5']='O'
        return
    esquina = [e for e in ['1', '3', '7', '9'] if simbolos[e] == e]
    if esquina:
        simbolos[random.choice(esquina)]='O'
        return
    casilla_desocupada=[c for c in simbolos if simbolos[c] == c]
    if casilla_desocupada:
        simbolos[random.choice(casilla_desocupada)]='O'

    '''ocupado= True
    while ocupado==True:
        x=random.choice(list(simbolos.keys()))
        if simbolos[x] not in ['X','O']:
            simbolos[x]='O'
            ocupado=False'''

def usuario(simbolos:dict):
    '''Juega el usuario'''
    lista_numeros=[str(i) for i in range(1,10)] # del 1 al 9
    ocupado = True
    while ocupado==True:
        x=input('ᓚ₍ ^. ̫ .^₎ 𖹭 Ingresa el número de la casilla: ')
        if x in lista_numeros:
            if simbolos[x] not in ['X','O']:
                simbolos[x]='X'
                ocupado=False
            else:
                print('- ˕ •マ ¡Esa casilla está ocupada!')
        else:
            print('ฅ ฅ Por favor, elige un número del 1 al 9')

def juego(simbolos:dict):
    '''Juego del gato'''
    lista_combinaciones=[
        ['1','2','3'],
        ['4','5','6'],
        ['7','8','9'],
        ['1','4','7'],
        ['2','5','8'],
        ['3','6','9'],
        ['1','5','9'],
        ['3','5','7']
        ]
    en_juego=True
    dibuja_tablero(simbolos)
    movimientos=0
    gana= None
    while en_juego:
        usuario(simbolos)
        dibuja_tablero(simbolos)
        movimientos += 1
        gana=checa_winner(simbolos,lista_combinaciones)
        if gana is not None:
            en_juego=False
            continue
        if movimientos >=9:
            en_juego=False
            continue
        ia(simbolos,lista_combinaciones)
        dibuja_tablero(simbolos)
        movimientos +=1
        gana=checa_winner(simbolos,lista_combinaciones)
        if gana is not None:
            en_juego=False
            continue
        if movimientos >=9:
            en_juego=False
            continue
    return gana

def checa_winner(simbolos:dict, combinaciones:list):
    '''Checa si hay un ganador'''
    for c in combinaciones:
        if simbolos[c[0]] == simbolos[c[1]] == simbolos[c[2]]:
            return simbolos[c[0]]
    return None 

def actualiza_score(score:dict,ganador:str, u:str):
    '''Actualiza el score'''
    X=score["X"]
    O=score["O"]
    
    if ganador=='X':
        nombre_ganador=u
    elif ganador=='O':
        nombre_ganador="Computadora"
    else:
        nombre_ganador=None

    if ganador is not None:
        print(f'¡Ha ganado {nombre_ganador}!')
        if ganador=='X':
            X["G"] += 1
            O["P"] += 1
        elif ganador=='O':
            O["G"] +=1
            X["P"] +=1
        else:
            X["E"] +=1
            O["E"] +=1
    else:
        print('¡Tenemos un empate! ^- ﻌ -^')
        X["E"] += 1
        O["E"] += 1

def despliega_tablero(score:dict, u:str):
    '''Despliega el tablero de score'''
    print(f'''
    {u} | G: {score["X"]["G"]} | P: {score["X"]["P"]} | E: {score["X"]["E"]}
    Computadora | G: {score["O"]["G"]} | P: {score["O"]["P"]} | E: {score["O"]["E"]}
    ''')

if __name__=='__main__':
    numeros=[str(i) for i in range(1,10)]
    dsimbolos={x:x for x in numeros}
    g = juego(dsimbolos)
    if g is not None:
        print(f'¡Ha ganado {g}!')
    else:
        print('Empate')
    '''dibuja_tablero(dsimbolos)
    ia(dsimbolos)
    dibuja_tablero(dsimbolos)
    usuario(dsimbolos)
    dibuja_tablero(dsimbolos)
    x=random.choice(numeros)
    numeros.remove(x)
    dsimbolos[x]='X'
    dibuja_tablero(dsimbolos)
    o = random.choice(numeros)
    numeros.remove(o)
    dsimbolos[o]='O'
    dibuja_tablero(dsimbolos)
    print(numeros)
    '''