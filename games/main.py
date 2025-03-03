'''Programa principal de games'''
from Athlete import Athlete
from Sport import Sport
from Game import Game
from Team import Team
import game_logic as gl
import json

def main(archivo_torneo:str):
    '''Función principal de games'''
    if archivo_torneo != "":
        with (open(archivo_torneo, "r", encoding="utf8")) as f:
            torneo = json.load(f)
    else:
        players_mexico=['Chicharito', 'Chucky', 'Ochoa', 'Tecatito', 'Guardado','Herrera','Layua','Moreno','Araujo','Gallardo','Jimenez','Oribe','Jimenez']
        players_espania=['Casillas', 'Ramos', 'Pique', 'Iniesta', 'Silva', 'Isco', 'Busquets','Costa','Moreta','Asensio']
        players_brasil=['Neymar', 'Coutinho', 'Alisson', 'Marcelo', 'Casemiro', 'Jesus', 'Firmino', 'Fred', 'Fagner', 'Thiago', 'Ederson']
        players_argentina=['Messi', 'Aguero', 'Di Maria', 'Otamendi', 'Perez', 'Rojo', 'Banega', 'Higuain', 'Mascherano', 'Mercado', 'Pavon']
        lista_mexico=[Athlete(x) for x in players_mexico]
        lista_espania=[Athlete(x) for x in players_espania]
        lista_brasil=[Athlete(x) for x in players_brasil]
        lista_argentina=[Athlete(x) for x in players_argentina]
        soccer=Sport("Soccer", 11, "FIFA")
        mexico=Team("Mexico", soccer, lista_mexico)
        espania=Team("España", soccer, lista_espania)
        brasil=Team("Brasil", soccer, lista_brasil)
        argentina=Team("Argentina", soccer, lista_argentina)
        equipos=[mexico, espania, brasil, argentina]

        d={}
        for local in equipos:
            for visitante in equipos:
                if local != visitante:
                    juego=Game(local, visitante)
                    partido=f'{local} - {visitante}'
                    partido_2=f'{visitante} - {local}'
                    if partido_2 not in d:
                        d[partido]=juego.to_json()

        #print(d.keys())
        torneo=list(d.values())
        #juego=Game(mexico, espania)
        #torneo=[juego.to_json()]
        archivo="torneo.json"
        with open(archivo, "w", encoding="utf8") as f:
            json.dump(torneo, f, ensure_ascii=False, indent=4)
        print(f"Se escribió archivo '{archivo}' satisfactoriamente")
    # Jugar todos los juegos del torneo
    for juego in torneo:
        A = Team(juego['A']['name'], Sport(juego['A']['sport']['name'], juego['A']['sport']['players'], juego['A']['sport']['league']), [Athlete(x['name']) for x in juego['A']['players']])
        B = Team(juego['B']['name'], Sport(juego['B']['sport']['name'], juego['B']['sport']['players'], juego['B']['sport']['league']), [Athlete(x['name']) for x in juego['B']['players']])
        game = Game(A, B)
        game.play()
        #print(game)
        juego['score'] = game.score
        print("-----------------")
    #Calcular el tablero de puntuación
    print(torneo)
    #torneo=gl.json_to_tournament()
    tablero = gl.scoring(torneo)
    gl.display_tablero(tablero)

if __name__ == "__main__":
    archivo_torneo = "torneo.json"
    main(archivo_torneo)
 