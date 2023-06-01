import msvcrt
import os
import sys
import random
import time
from dataclasses import dataclass, asdict


def clear():
    os.system('cls')


@dataclass
class Player:
    symbol: str
    x: int
    y: int
    healthPoints: int
    scorePoints: int


@dataclass
class Meteor:
    symbol: str
    x: int
    y: int
    direction: int
    damagePoints: int
    speedPoints: int


class PlayerHandle:
    def __init__(self, sym, x, y, hp, sp):
        self.player = Player(sym, x, y, hp, sp)

    def get_dataclass(self):
        return asdict(self.player)

    def edit(self, key, value):
        self.player.__dict__[key] = value


class MeteorHandle:
    def __init__(self, sym, x, y, direct, dp, sp):
        self.meteor = Meteor(sym, x, y, direct, dp, sp)

    def get_dataclass(self):
        return asdict(self.meteor)

    def edit(self, key, value):
        self.meteor.__dict__[key] = value


def generateMeteor(n, m):
    chance = random.randint(0, 3)
    return MeteorHandle("*",
                        random.randint(0, n - 1) if chance == 0 else (
                            0 if chance == 1 else (random.randint(0, n - 1) if chance == 2 else n - 1)),
                        0 if chance == 0 else (random.randint(0, m - 1) if chance == 1 else (
                            m - 1 if chance == 2 else random.randint(0, m - 1))),
                        chance,
                        random.randint(25, 75),
                        random.randint(1, 5))


def loadLevel(n, m):
    return [[" " for j in range(n)] for i in range(m)]


def updateLevel(mapObj, entityList):
    for entity in entityList:
        mapObj[entity.get_dataclass()["y"]][entity.get_dataclass()["x"]] = entity.get_dataclass()["symbol"]


def printLevel(mapObj):
    print(" _" * (len(mapObj[0]) + 1))
    for i in range(len(mapObj)):
        print(end="| ")
        for j in range(len(mapObj[0])):
            print(mapObj[i][j], end=" ")
        print(end="|\n")
    print(" ‾" * (len(mapObj[0]) + 1))


def printPlayerInfo(playerObj):
    print(
        f"Жизни: {playerObj.get_dataclass()['healthPoints'] if playerObj.get_dataclass()['healthPoints'] > 0 else 'ВЫ ПОГИБЛИ'}\tОчки: {playerObj.get_dataclass()['scorePoints']}")


def printRules():
    print(
        "\nУправление:\n\tW: ↑\tS: ↓\n\tA: ←\tD: →\t\nПравила:\n\t* - метеориты\tP - игрок\n\nНаберите 100 очков, избегайте метеоритов\t")


def damageTaken(mapObj, entity):
    for i in range(2):
        clear()
        print("\033[41m")
        clear()
        printInterface(mapObj, entity)
        time.sleep(0.005)

        clear()
        print("\033[40m")
        clear()
        printInterface(mapObj, entity)
        time.sleep(0.005)

    entity[-1].edit("symbol", "P")


def printInterface(mapObj, entity):
    clear()
    printPlayerInfo(entity[-1])
    printLevel(mapObj)
    printRules()


def collisionCheck(obj, playerObj):
    if obj.get_dataclass()["x"] == playerObj.get_dataclass()["x"] and \
            obj.get_dataclass()["y"] == playerObj.get_dataclass()["y"]:
        playerObj.edit("symbol", "#")
        playerObj.edit("healthPoints",
                       playerObj.get_dataclass()["healthPoints"] - obj.get_dataclass()[
                           "damagePoints"])


def changeComplexity():
    clear()
    print("Meteors SUCK --- by Finik Aka Moxem\t\n")
    print("\tВыбор сложности.\t\n")
    print("1.\tЛегкая.\t")
    print("2.\tНормальная.\t")
    print("3.\tСложная.\t")


def mainMenu(complex):
    clear()
    print("Meteors SUCK --- by Finik Aka Moxem\t\n")
    print("\tГлавное меню.\t\n")
    print("1.\tНачать игру.\t")
    print(f"2.\tИзменить сложность.\t({complex})")
    print("3.\tВыход.\t")


def gameOver(arg, m):
    if arg:
        clear()
        print("\n" * (m // 2) + "\tВЫ ПРОИГРАЛИ!\t" + "\n" * (m // 2) + "Нажмите любую клавишу...")
        msvcrt.getwch()
    else:
        clear()
        print("\n" * (m // 2) + "\tВЫ ПОБЕДИЛИ!\t" + "\n" * (m // 2) + "Нажмите любую клавишу...")
        msvcrt.getwch()
    mainMenu("Легкая")


def main(n):
    m = n
    player = PlayerHandle("P", n // 2, m // 2, 100, 0)
    entity = [player]

    while player.get_dataclass()["healthPoints"] > 0 and player.get_dataclass()["scorePoints"] < 100:
        level = loadLevel(n, m)
        updateLevel(level, entity)
        printInterface(level, entity)

        movePlayer = msvcrt.getwch()
        while movePlayer not in "WASDwasdЦФЫВцфыв":
            movePlayer = msvcrt.getwch()

        if (movePlayer.lower() == "w" or movePlayer.lower() == "ц") and player.get_dataclass()["y"] > 0:
            player.edit("y", player.get_dataclass()["y"] - 1)
            for obj in entity:
                if isinstance(obj, MeteorHandle):
                    collisionCheck(obj, player)
        elif (movePlayer.lower() == "s" or movePlayer.lower() == "ы") and player.get_dataclass()["y"] < m - 1:
            player.edit("y", player.get_dataclass()["y"] + 1)
            for obj in entity:
                if isinstance(obj, MeteorHandle):
                    collisionCheck(obj, player)
        elif (movePlayer.lower() == "a" or movePlayer.lower() == "ф") and player.get_dataclass()["x"] > 0:
            player.edit("x", player.get_dataclass()["x"] - 1)
            for obj in entity:
                if isinstance(obj, MeteorHandle):
                    collisionCheck(obj, player)
        elif (movePlayer.lower() == "d" or movePlayer.lower() == "в") and player.get_dataclass()["x"] < n - 1:
            player.edit("x", player.get_dataclass()["x"] + 1)
            for obj in entity:
                if isinstance(obj, MeteorHandle):
                    collisionCheck(obj, player)

        for step in range(1, 6):
            for obj in entity:
                if isinstance(obj, MeteorHandle):
                    if obj.get_dataclass()["direction"] == 0:
                        if obj.get_dataclass()["y"] < m - 1:
                            if obj.get_dataclass()["speedPoints"] >= step:
                                obj.edit("y", obj.get_dataclass()["y"] + 1)
                        else:
                            entity.pop(entity.index(obj))
                    elif obj.get_dataclass()["direction"] == 1:
                        if obj.get_dataclass()["x"] < n - 1:
                            if obj.get_dataclass()["speedPoints"] >= step:
                                obj.edit("x", obj.get_dataclass()["x"] + 1)
                        else:
                            entity.pop(entity.index(obj))
                    elif obj.get_dataclass()["direction"] == 2:
                        if obj.get_dataclass()["y"] > 0:
                            if obj.get_dataclass()["speedPoints"] >= step:
                                obj.edit("y", obj.get_dataclass()["y"] - 1)
                        else:
                            entity.pop(entity.index(obj))
                    elif obj.get_dataclass()["direction"] == 3:
                        if obj.get_dataclass()["x"] > 0:
                            if obj.get_dataclass()["speedPoints"] >= step:
                                obj.edit("x", obj.get_dataclass()["x"] - 1)
                        else:
                            entity.pop(entity.index(obj))
                    collisionCheck(obj, player)

            level = loadLevel(n, m)
            updateLevel(level, entity)
            printInterface(level, entity)
            time.sleep(0.01)

            if player.get_dataclass()["symbol"] == "#":
                damageTaken(level, entity)

        if random.randint(0, 5) != 0:
            meteor = generateMeteor(n, m)
            entity = [meteor] + entity

        player.edit("scorePoints", player.get_dataclass()["scorePoints"] + 1)

    if player.get_dataclass()["healthPoints"] <= 0:
        gameOver(1, m)
    else:
        gameOver(0, m)


if __name__ == "__main__":
    complexity = "Легкая"

    mainMenu(complexity)

    while 1:
        choice = msvcrt.getwch()
        while choice not in "123":
            choice = msvcrt.getwch()

        if choice == "1":
            main(21 if complexity == "Легкая" else (11 if complexity == "Нормальная" else 5))
        elif choice == "2":
            changeComplexity()

            choice = msvcrt.getwch()
            while choice not in "123":
                choice = msvcrt.getwch()

            if choice == "1":
                complexity = "Легкая"
            elif choice == "2":
                complexity = "Нормальная"
            else:
                complexity = "Сложная"
        else:
            sys.exit()

        mainMenu(complexity)
