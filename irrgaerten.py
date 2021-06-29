import queue
import time
import os


# -------------------------Funktionen-------------------------
def irrgarten1():
    irrgarten = \
    [["*", "*", "*", "*", "*", "S", "*"],
     ["*", " ", "*", " ", " ", " ", "*"],
     ["*", " ", "*", " ", "*", " ", "*"],
     ["E", " ", " ", " ", "*", " ", "*"],
     ["*", " ", "*", "*", "*", " ", "*"],
     ["*", " ", " ", " ", " ", " ", "*"],
     ["*", "*", "*", "*", "*", "*", "*"]]

    return irrgarten


def irrgarten2():
    irrgarten = \
    [["*", "*", "*", "*", "*", "*", "*", "S", "*"],
     ["*", " ", " ", " ", " ", " ", " ", " ", "*"],
     ["*", " ", "*", " ", "*", "*", "*", " ", "*"],
     ["E", " ", "*", " ", " ", " ", " ", " ", "*"],
     ["*", " ", "*", "*", "*", "*", "*", " ", "*"],
     ["*", " ", " ", " ", " ", " ", " ", " ", "*"],
     ["*", "*", "*", " ", "*", "*", "*", " ", "*"],
     ["*", " ", " ", " ", " ", " ", "*", " ", "*"],
     ["*", "*", "*", "*", "*", "*", "*", "*", "*"]]

    return irrgarten


def irrgarten3():
    irrgarten = \
    [["*", "*", "*", "S", "*"],
     ["*", " ", " ", " ", "*"],
     ["*", " ", "*", " ", "*"],
     ["*", " ", "*", " ", "*"],
     ["*", " ", " ", " ", "*"],
     ["*", "E", "*", "*", "*"]]

    return irrgarten


def findeStartEnde(irrgarten):
    """Durchläuft Irrgarten und gibt X-Koordinate von Start zurück, Y=0 ist hardkodiert, Irrgarten muss oben anfangen"""
    for i, pos in enumerate(irrgarten[0]):
        if pos == "S":
            startx = i
    return startx


def macheSchritte(x, y, weg):
    """Methode, die jeden Schritt in 'weg' macht und Koordinaten von weg zurückgibt"""
    wegXY = []
    for schritt in weg:
        if schritt == "L":
            x -= 1
        elif schritt == "R":
            x += 1
        elif schritt == "O":
            y -= 1
        elif schritt == "U":
            y += 1

        wegXY.append((x, y))
    return x, y, wegXY


def setzeWeg(irrgarten, wegXY):
    """Methode, die Lösungsweg entgegennimmt und Irrgarten ausgibt, Weg ist mit '-' markiert"""
    for y, _ in enumerate(irrgarten):
        for x, __ in enumerate(irrgarten[y]):
            if (x, y) in wegXY:
                print("- ", end="")  # end="", damit nach print-statement kein Zeilenumbruch wie sonst folgt
            else:
                print(irrgarten[y][x] + " ", end="")
        print()


def gebeIrrgartenAus(irrgarten, weg, startx):
    x = startx
    y = 0
    _, __, wegXY = macheSchritte(x, y, weg)
    setzeWeg(irrgarten, wegXY)


def checkeZug(irrgarten, weg, startx):
    """Kontrolliert, ob Schritte in 'weg' erlaubt sind; False wenn ein Schritt verboten ist, ansonsten True"""
    x = startx
    y = 0

    for schritt in weg:
        if schritt == "L":
            x -= 1
        elif schritt == "R":
            x += 1
        elif schritt == "O":
            y -= 1
        elif schritt == "U":
            y += 1

        if not (0 <= x < len(irrgarten[0]) and 0 <= y < len(irrgarten)):
            # return False, wenn Koordinaten nicht im Irrgartens sind
            return False

        elif irrgarten[y][x] == "*":
            # return False, wenn an der Position eine Wand ist
            return False

    return True


def Ende(irrgarten, weg, startx):
    x = startx
    y = 0
    x, y, _ = macheSchritte(x, y, weg)

    # Koordinaten entsprechen nun der Position, die am Ende von "weg" erreicht wird
    if irrgarten[y][x] == "E":
        # Sollte Standort im Irrgarten "E" entsprechen (d.h. Ende), ist er gelöst; Ausdruck und Rückgabe von True
        print(f"Weg gefunden: {weg}")
        gebeIrrgartenAus(irrgarten, weg, startx)
        return True
    else:
        # Koordinaten entsprechen nicht "E", Ende nicht gefunden; Rückgabe von False
        return False


# -------------------------BreadthFirstSearch-------------------------
def BreadthFirstSearch(irrgarten, startx):
    mglSchritte = queue.Queue()  # Schlange, die mit allen möglichen Schritten gefüllt wird, bis Ziel gefunden ist
    mglSchritte.put("")

    bewegungen = ["L", "R", "O", "U"]  # "Links, Rechts, Oben, Unten
    weg = ""  # Schrittfolge, die geprüft wird

    while not Ende(irrgarten, weg, startx):
        weg = mglSchritte.get()  # Erstes Element aus Schlange wird in weg gespeichert
        for bewegung in bewegungen:
            # Bewegungen werden an weg angehangen und geprüft
            neuerWeg = weg + bewegung
            if checkeZug(irrgarten, neuerWeg, startx):
                mglSchritte.put(neuerWeg)


# -------------------------Linke-Hand-Methode-------------------------
def linkeHand(irrgarten, startx):
    x = startx
    y = 0
    richtung = "S"
    while irrgarten[y][x] != "E":

        if richtung == "S":
            if irrgarten[y][x + 1] != "*":
                # Ist links keine Wand, Drehung um 90° gegen den Uhrzeigersinn, dann einen Schritt nach vorne gehen
                richtung = "O"
                x += 1
            elif irrgarten[y + 1][x] != "*":
                # Ist vorne keine Wand, gehe einen Schritt nach vorne
                y += 1
            else:
                # Ansonsten um 90° drehen
                richtung = "W"

        elif richtung == "W":
            if irrgarten[y + 1][x] != "*":
                richtung = "S"
                y += 1
            elif irrgarten[y][x - 1] != "*":
                x -= 1
            else:
                richtung = "N"

        elif richtung == "N":
            if irrgarten[y][x - 1] != "*":
                richtung = "W"
                x -= 1
            elif irrgarten[y - 1][x] != "*":
                y -= 1
            else:
                richtung = "O"

        elif richtung == "O":
            if irrgarten[y - 1][x] != "*":
                richtung = "N"
                y -= 1
            elif irrgarten[y][x + 1] != "*":
                x += 1
            else:
                richtung = "S"

        druckeSchritt(irrgarten, x, y, richtung)
        time.sleep(1)

    print(f"Ziel gefunden x: {x}, y: {y}")


def druckeSchritt(irrgarten, x, y, richtung):
    """try:
        # Löscht den Output in der Konsole, damit der Irrgarten neu ausgegeben werden kann
        os.system("cls")
    except:
        pass"""

    # Der Irrgarten wird durchlaufen, entsprechen x und y der aktuellen Position in der Schleife, wird ein Pfeil mit
    # Blick in die aktuelle Richtung ausgedruckt, ansonsten wird gedruckt, was regulär im Irrgarten wäre (Wand oder " ")
    for iry, _ in enumerate(irrgarten):
        for irx, __ in enumerate(irrgarten[y]):
            if irx == x and iry == y:

                if richtung == "N":
                    print("↑ ", end="")
                elif richtung == "O":
                    print("→ ", end="")
                elif richtung == "S":
                    print("↓ ", end="")
                elif richtung == "W":
                    print("← ", end="")
            else:
                print(irrgarten[iry][irx] + " ", end="")
        print()
    print()


# -------------------------Main-------------------------
irrgarten = irrgarten2()
startx = findeStartEnde(irrgarten)

# Bitte ausgewählten Algorithmus auskommentieren
# BreadthFirstSearch(irrgarten, startx)
linkeHand(irrgarten, startx)
