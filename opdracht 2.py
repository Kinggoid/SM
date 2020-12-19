import math
import numpy as np
import plotly.graph_objects as go


def middle_square(seed):
    """
    In deze definitie proberen we bij een bepaalde seed de 'middle-square root' methode toe te passen om een nieuw
    pseudorandom nummer te krijgen.
    """

    len_before = len(str(seed))
    new_seed = int(seed)

    # Vermenigvuldig de seed met zichzelf
    new_seed = new_seed ** 2
    new_seed = str(new_seed)

    # Kijk hoeveel groter het nieuwe nummer is en hoeveel we eraf moeten doen om een getal van dezelfde grote als de
    # origionele seed te krijgen.
    hoeveel_groter = len(new_seed) - len_before

    hoeveel_eraf_schaven = int(hoeveel_groter / 2)

    # Als het nieuwe nummer even is, schaven we evenveel van beide kanten af. Maar als hij oneven is, schaven we er
    # één minder van de linkerkant af.
    if hoeveel_groter % 2 == 0:
        new_seed = new_seed[hoeveel_eraf_schaven: -hoeveel_eraf_schaven]
    else:
        new_seed = new_seed[hoeveel_eraf_schaven: -(hoeveel_eraf_schaven + 1)]

    if len(str(int(new_seed))) == len_before - 1:
        # Het kan zijn dat de middelste nummers beginnen met een 0, wanneer je daar dan een int van maakt krijg je
        # een cijfer dat opeens kleiner is dan de bedoeling is. Daarom veranderen we het eerste cijfer van een nul naar
        # het eerste cijfer van de origionele seed ('random nummer').
        new_seed += str(seed)[0]
        new_seed = new_seed[1:]
    return new_seed


def wedstrijden_voorspellen(seed, aantal_competities, clubs, matches):
    """
    Hierin vind de Monte Carlo algoritme plaats. We weten hoeveel kans een club heeft om te winnen van een andere club.
    Vervolgens gebruiken we onze random number calculator om te kijken wat de uitslag van elke wedstrijd is. Wanneer we
    elke club tegen elkaar hebben laten spelen, kijken we op welke plaats deze zijn geland (eerste plaats, tweede plaats
    , etc). 'aantal_competities' geeft aan hoe vaak we deze simulatie gaan runnen. Uiteindelijk weten we hoe vaak elke
    club op elke plaats is beland.
    """
    new_number = seed
    voorspelde_uitslagen = np.zeros(25).reshape(5, 5)
    aantal_clubs = len(matches)
    aantal_matches = len(matches[0])

    for i in range(aantal_competities):
        scores = {"Ajax": 0, "Feyenoord": 0, "PSV": 0, "FC Utrecht": 0, "Willem II": 0}
        for x in range(aantal_clubs):
            for y in range(aantal_matches):
                # Random nummer
                new_number = middle_square(new_number)
                random_number = int(new_number[-2:])
                if not matches[x][y]:
                    # Wanneer een club tegen zichzelf speelt (dit kan niet dus slaan we het over)
                    continue
                else:
                    if random_number < matches[x][y][0]:
                        # Als een club wint, krijgen ze +3 punten
                        scores[clubs[x]] += 3
                    elif matches[x][y][0] < random_number < matches[x][y][0] + matches[x][y][1]:
                        # Wanneer twee clubs gelijk spelen, krijgen ze allebei +1 punt
                        scores[clubs[x]] += 1
                        scores[clubs[y]] += 1
                    else:
                        # Wanneer een club verliest, krijgt het andere team +3 punten
                        scores[clubs[y]] += 3

        # Nu je weet hoeveel elk team nu heeft gescoord, kunnen we kijken op welke plaats zij zijn beland. Dit werken
        # we bij op het scoreboard.
        voorspelde_uitslagen = leaderboard(scores, voorspelde_uitslagen, clubs)
    return voorspelde_uitslagen


def leaderboard(scores, leaderboard, clubs):
    """
    In deze definitie kijken we hoeveel punten elke club heeft gekregen, en dan kijken we op welke plaats elke club
    staat. Uiteindelijk werken we het leaderboard bij.
    """

    rankings = list(scores.values())
    val_list = list(scores.values())

    rankings.sort()
    rankings.reverse()

    vorige = 0
    plaats = 0

    for i in range(0, len(rankings)):
        if rankings[i] == vorige:
            # Waneer er twee clubs zijn met dezelfde score, delen ze beide dezelfde plaats.
            plaats -= 1
            val_list[val_list.index(rankings[i])] = 0

        club = clubs.index(clubs[val_list.index(rankings[i])])
        leaderboard[plaats][club] += 1
        plaats += 1
        vorige = rankings[i]
    return leaderboard


def kansen(uitslagen, repeat):
    """
    We weten nu hoe vaak elke club op elke plaats heeft gestaan, maar we willen weten hoeveel % kans ze hebben om hier
    te komen. Dat doen we hier.
    """
    for i in range(0, len(uitslagen[0])):
        for j in range(0, len(uitslagen)):
            uitslagen[j][i] = math.ceil(uitslagen[j][i] * 100 / repeat)
    return np.array(uitslagen)


def MonteCarlo():
    """
    Dit is de main module. Hierin definiëren we welke teams er zijn, wat hun kansen zijn om van elkaar te winnen en
    hoe groot hun kans is om op elke plaats te eindigen.
    """
    clubs = ["Ajax", "Feyenoord", "PSV", "FC Utrecht", "Willem II"]
    matches = [[[], [65, 17, 18], [54, 21, 25], [74, 14, 12], [78, 13, 9]],
               [[30, 21, 49], [], [37, 24, 39], [51, 22, 27], [60, 21, 19]],
               [[39, 22, 39], [54, 22, 24], [], [62, 20, 18], [62, 22, 16]],
               [[25, 14, 61], [37, 23, 40], [29, 24, 47], [], [52, 23, 25]],
               [[17, 18, 65], [20, 26, 54], [23, 24, 53], [37, 25, 38], []]]

    seed = 123456789
    repeat = 101

    uitslag = wedstrijden_voorspellen(seed, repeat, clubs, matches)
    voorspelde_kans_op_plaats = kansen(uitslag, repeat)

    # Maak een tabel om de resultaten goed te weergeven.
    fig = go.Figure(data=[go.Table(header=dict(values=clubs),
                                   cells=dict(values=voorspelde_kans_op_plaats))
                          ])
    fig.show()

MonteCarlo()
