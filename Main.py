import keyboard
import pygame
from time import sleep
from random import randrange
turn = 1


class piece:
    def __init__(self, color=None, value=None, moved=False):
        self.color = color
        # 0=Black
        # 1=White
        self.value = value
        self.moved = moved


yes = ['rook', 'bishop', 'pawn', 'king', 'horse', 'queen']
tableu = ['r', 'b', 'p', 'k', 'h', 'q']
arounds = [0, -1, 1, -8, 8, 9, -9, -7, 7]
images = []
win = pygame.display.set_mode((600, 600))
clicked = None
for i in yes:
    for j in range(2):
        images.append(pygame.image.load(i+'_'+str(j+1)+'.png'))


def make_board(wid, hei):
    run = True
    for y in range(0, hei, hei//8):
        for x in range(0, wid, wid//8):
            rank = (y/75)*8+(x/75)
            if (x/75+y/75) % 2 == 0:
                color = (255, 228, 156)
            else:
                color = (106, 77, 15)
            pygame.draw.rect(win, color, pygame.Rect(x, y, 80, 80))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            if run == False:
                break
        if run == False:
            break


class board():
    def __init__(self):
        self.pieces = [piece() for i in range(64)]


def make_pieces(fen, board):
    rank = 0
    table = {"r": 1, "b": 2, "p": 3, "k": 4, "h": 5, "q": 6}
    yye = board.pieces
    for i in fen:
        if i == '/':
            rank += 15
            continue
        if i.lower() not in table:
            rank += int(i)
        else:
            if i.lower() == i:
                col = 0
            else:
                col = 1
            pie = table[i.lower()]-1
            yye[rank] = piece(col, pie)
            rank += 1
    return board


def show_pieces(board):
    x = 0
    y = 0
    num = 0
    for i in board.pieces:
        if i.color != None:
            if clicked == None:
                win.blit(images[i.value*2+i.color], (x, y))
        x += 75
        num += 1
        if x % 600 == 0:
            x = 0
            y += 75


make_board(600, 600)
game = board()
boardy = 'pppppppprhbqkbhr'
game = make_pieces('rhbqkbhrpppppppp//2' +
                   'rhbkqbhrpppppppp'.upper()[::-1], game)
show_pieces(game)
pygame.display.update()
clicked = None
oth = pygame.mouse.get_pos()
c = 0
run = True
while not keyboard.is_pressed('ctrl') and run:
    if clicked != None:
        mousy = pygame.mouse.get_pos()
        xmark = mousy[0]//75
        ymark = mousy[1]//75
        sew = xmark+ymark*8
        for i in arounds:
            try:
                indexy = sew-i
                if indexy in valids:
                    if game.pieces[indexy].value == None:
                        color = (255, 0, 0)
                    else:
                        color = (34, 177, 76)
                elif indexy == clicked:
                    color = (255, 242, 255)
                elif (indexy % 8+indexy//8) % 2 == 0:
                    color = (255, 228, 156)
                else:
                    color = (106, 77, 15)
                pygame.draw.rect(win, color, pygame.Rect(
                    indexy % 8*75, indexy//8*75, 75, 75))
                win.blit(images[game.pieces[indexy].value*2 +
                         game.pieces[indexy].color], (indexy % 8*75, indexy//8*75))
            except:
                pass
        color = (255, 242, 0)
        pygame.draw.rect(win, color, pygame.Rect(
            clicked % 8*75, clicked//8*75, 75, 75))
        win.blit(images[game.pieces[clicked].value*2 +
                 game.pieces[clicked].color], (mousy[0]-25, mousy[1]-25))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clone = pos
            xmark = pos[0]//75
            ymark = pos[1]//75
            if clicked == None:
                clicked = xmark+ymark*8
                if game.pieces[clicked].value == None or (game.pieces[clicked].color) % 2 != turn % 2:
                    clicked = None
                else:
                    secd = clicked
                    valids = []
                    for other in range(64):
                        le = True
                        x1 = clicked % 8
                        y1 = clicked//8
                        x2 = other % 8
                        y2 = other//8
                        # rook
                        if game.pieces[other].color == game.pieces[clicked].color:
                            le = False
                        if game.pieces[clicked].value == 0 and le:
                            if (y1 == y2) and le:
                                le = True
                                if x1 > x2:
                                    vali = -1
                                else:
                                    vali = 1
                            elif x1 == x2 and le:
                                le = True
                                if y1 > y2:
                                    vali = -8
                                else:
                                    vali = 8
                            else:
                                le = False
                            if le:
                                for i in range(clicked, other, vali):
                                    if i == clicked:
                                        continue
                                    if game.pieces[i].value != None:
                                        le = False
                                        break
                        # bishop
                        if game.pieces[clicked].value == 1 and le:
                            left = x1-x2
                            up = y1-y2
                            if left < 0:
                                left = left*(-1)
                            if up < 0:
                                up = up*(-1)
                            if up == left:
                                pass
                            else:
                                le = False
                            if le:
                                if y1 > y2:
                                    if x1 > x2:
                                        vali = -9
                                    else:
                                        vali = -7
                                else:
                                    if x1 > x2:
                                        vali = 7
                                    else:
                                        vali = 9
                                for i in range(clicked, other, vali):
                                    if i == clicked:
                                        continue
                                    if game.pieces[i].value != None:
                                        le = False
                                        break
                        # queen
                        if game.pieces[clicked].value == 5 and le:
                            if (y1 == y2):
                                if x1 > x2:
                                    vali = -1
                                else:
                                    vali = 1
                            elif x1 == x2:
                                if y1 > y2:
                                    vali = -8
                                else:
                                    vali = 8
                            else:
                                le = False
                            if le:
                                for i in range(clicked, other, vali):
                                    if i == clicked:
                                        continue
                                    if game.pieces[i].value != None:
                                        le = False
                                        break
                            if le == False:
                                left = x1-x2
                                up = y1-y2
                                if left < 0:
                                    left = left*(-1)
                                if up < 0:
                                    up = up*(-1)
                                if up == left:
                                    le = True
                                else:
                                    le = False
                                if le:
                                    if y1 > y2:
                                        if x1 > x2:
                                            vali = -9
                                        else:
                                            vali = -7
                                    else:
                                        if x1 > x2:
                                            vali = 7
                                        else:
                                            vali = 9
                                    for i in range(clicked, other, vali):
                                        if i == clicked:
                                            continue
                                        if game.pieces[i].value != None:
                                            le = False
                                            break
                        # king
                        if game.pieces[clicked].value == 3 and le:
                            xchange = x1-x2
                            ychange = y1-y2
                            if xchange < -1 or xchange > 1 or ychange < -1 or ychange > 1:
                                le = False
                        # horse
                        if game.pieces[clicked].value == 4 and le:
                            xchange = x1-x2
                            ychange = y1-y2
                            if xchange == 0:
                                le = False
                            if xchange == 2 or xchange == -2:
                                if ychange == 1 or ychange == -1:
                                    pass
                                else:
                                    le = False
                            elif xchange == 1 or xchange == -1:
                                if ychange == -2 or ychange == 2:
                                    pass
                                else:
                                    le = False
                            else:
                                le = False
                        # pawn
                        if game.pieces[clicked].value == 2 and le:
                            if game.pieces[other].value != None:
                                le = False
                            xchange = x1-x2
                            ychange = y1-y2
                            nuuu = -8
                            if game.pieces[clicked].color == 0:
                                ychange *= -1
                                nuuu *= -1
                            if ychange < 0:
                                le = False
                            if xchange != 0:
                                if game.pieces[other].value != None and ychange == 1 and (xchange == 1 or xchange == -1):
                                    le = True
                                else:
                                    le = False
                            numm = 1
                            if not game.pieces[clicked].moved:
                                numm = 2
                            if ychange > numm:
                                le = False
                            if numm == 2 and ychange == 2 and game.pieces[clicked+nuuu].value != None:
                                le = False
                        if le:
                            valids.append(other)
                    for i in valids:
                        xposs = (i % 8)*75
                        yposs = (i//8)*75
                        if game.pieces[i].value == None:
                            color = (255, 0, 0)
                        else:
                            color = (34, 177, 76)
                        pygame.draw.rect(
                            win, color, pygame.Rect(xposs, yposs, 75, 75))
                        if game.pieces[i].value != None:
                            win.blit(
                                images[game.pieces[i].value*2+game.pieces[i].color], (i % 8*75, i//8*75))

            else:
                do = True
                icecream = game.pieces[clicked]
                other = xmark+ymark*8
                le = True
                if clicked == other:
                    do = False
                elif other in valids:
                    pass
                else:
                    le = False
                if (clicked % 8+clicked//8) % 2 == 0:
                    color = (255, 228, 156)
                else:
                    color = (106, 77, 15)
                pygame.draw.rect(win, color, pygame.Rect(
                    clicked % 8*75, clicked//8*75, 75, 75))
                win.blit(images[game.pieces[clicked].value*2 +
                         game.pieces[clicked].color], (mousy[0]-25, mousy[1]-25))
                if (clicked % 8+clicked//8) % 2 == 0:
                    color = (255, 228, 156)
                else:
                    color = (106, 77, 15)
                if (other % 8+other//8) % 2 == 0:
                    color = (255, 228, 156)
                else:
                    color = (106, 77, 15)
                if le and do:
                    thingies = board()
                    thingies.pieces = game.pieces
                    mom = board()
                    mom.pieces = [i for i in game.pieces]
                    if game.pieces[other].value == 3:
                        run = False
                        break
                    pygame.draw.rect(win, color, pygame.Rect(
                        (other % 8)*75, (other//8)*75, 75, 75))
                    thingies.pieces[clicked].moved = True
                    thingies.pieces[other] = thingies.pieces[clicked]
                    for i in range(64):
                        if thingies.pieces[i].value == 3 and thingies.pieces[i].color == 1:
                            king = i
                            break
                    secd = clicked
                    validsy = []
                    icecream = thingies.pieces[clicked]
                    thingies.pieces[clicked] = piece()
                    e = other
                    place = game.pieces[clicked]
                    for clicked in range(64):
                        if game.pieces[clicked].value == None:
                            continue
                        for other in range(64):
                            le = True
                            x1 = clicked % 8
                            y1 = clicked//8
                            x2 = other % 8
                            y2 = other//8
                            # rook
                            if thingies.pieces[other].color == game.pieces[clicked].color:
                                le = False
                            if thingies.pieces[clicked].value == 0 and le:
                                if (y1 == y2) and le:
                                    le = True
                                    if x1 > x2:
                                        vali = -1
                                    else:
                                        vali = 1
                                elif x1 == x2 and le:
                                    le = True
                                    if y1 > y2:
                                        vali = -8
                                    else:
                                        vali = 8
                                else:
                                    le = False
                                if le:
                                    for i in range(clicked, other, vali):
                                        if i == clicked:
                                            continue
                                        if thingies.pieces[i].value != None:
                                            le = False
                                            break
                            # bishop
                            if thingies.pieces[clicked].value == 1 and le:
                                left = x1-x2
                                up = y1-y2
                                if left < 0:
                                    left = left*(-1)
                                if up < 0:
                                    up = up*(-1)
                                if up == left:
                                    pass
                                else:
                                    le = False
                                if le:
                                    if y1 > y2:
                                        if x1 > x2:
                                            vali = -9
                                        else:
                                            vali = -7
                                    else:
                                        if x1 > x2:
                                            vali = 7
                                        else:
                                            vali = 9
                                    for i in range(clicked, other, vali):
                                        if i == clicked:
                                            continue
                                        if thingies.pieces[i].value != None:
                                            le = False
                                            break
                            # queen
                            if thingies.pieces[clicked].value == 5 and le:
                                if (y1 == y2):
                                    if x1 > x2:
                                        vali = -1
                                    else:
                                        vali = 1
                                elif x1 == x2:
                                    if y1 > y2:
                                        vali = -8
                                    else:
                                        vali = 8
                                else:
                                    le = False
                                if le:
                                    for i in range(clicked, other, vali):
                                        if i == clicked:
                                            continue
                                        if thingies.pieces[i].value != None:
                                            le = False
                                            break
                                if le == False:
                                    left = x1-x2
                                    up = y1-y2
                                    if left < 0:
                                        left = left*(-1)
                                    if up < 0:
                                        up = up*(-1)
                                    if up == left:
                                        le = True
                                    else:
                                        le = False
                                    if le:
                                        if y1 > y2:
                                            if x1 > x2:
                                                vali = -9
                                            else:
                                                vali = -7
                                        else:
                                            if x1 > x2:
                                                vali = 7
                                            else:
                                                vali = 9
                                        for i in range(clicked, other, vali):
                                            if i == clicked:
                                                continue
                                            if thingies.pieces[i].value != None:
                                                le = False
                                                break
                            # king
                            if thingies.pieces[clicked].value == 3 and le:
                                xchange = x1-x2
                                ychange = y1-y2
                                if xchange < -1 or xchange > 1 or ychange < -1 or ychange > 1:
                                    le = False
                            # horse
                            if thingies.pieces[clicked].value == 4 and le:
                                xchange = x1-x2
                                ychange = y1-y2
                                if xchange == 0:
                                    le = False
                                if xchange == 2 or xchange == -2:
                                    if ychange == 1 or ychange == -1:
                                        pass
                                    else:
                                        le = False
                                elif xchange == 1 or xchange == -1:
                                    if ychange == -2 or ychange == 2:
                                        pass
                                    else:
                                        le = False
                                else:
                                    le = False
                            # pawn
                            if thingies.pieces[clicked].value == 2 and le:
                                if thingies.pieces[other].value != None:
                                    le = False
                                xchange = x1-x2
                                ychange = y1-y2
                                nuuu = -8
                                if thingies.pieces[clicked].color == 0:
                                    ychange *= -1
                                    nuuu *= -1
                                if ychange < 0:
                                    le = False
                                if xchange != 0:
                                    if thingies.pieces[other].value != None and ychange == 1 and (xchange == 1 or xchange == -1):
                                        le = True
                                    else:
                                        le = False
                                numm = 1
                                if not thingies.pieces[clicked].moved:
                                    numm = 2
                                if ychange > numm:
                                    le = False
                                if numm == 2 and ychange == 2 and thingies.pieces[clicked+nuuu].value != None:
                                    le = False
                            if le:
                                validsy.append(other)
                    clicked = secd
                    other = e
                    if king in validsy:
                        if turn % 2 == 1:
                            game.pieces = mom.pieces
                            turn -= 1
                    else:
                        le = True
                    if game.pieces[other].value != None:
                        win.blit(images[game.pieces[other].value*2 +
                                        game.pieces[other].color], (xmark*75, ymark*75))
                    pygame.display.update()
                    if game.pieces[other].value == 2:
                        if game.pieces[other].color == 1:
                            if other >= 0 and other <= 7:
                                while game.pieces[other].value == 2:
                                    for i in tableu:
                                        if keyboard.is_pressed(i):
                                            game.pieces[other].value = tableu.index(
                                                i)
                        else:
                            if other >= 56 and other <= 63:
                                while game.pieces[other].value == 2:
                                    for i in tableu:
                                        if keyboard.is_pressed(i):
                                            game.pieces[other].value = tableu.index(
                                                i)
                    turn += 1
                for i in valids:
                    xposs = (i % 8)*75
                    yposs = (i//8)*75
                    pygame.draw.rect(win, (255, 0, 0),
                                     pygame.Rect(xposs, yposs, 75, 75))
                    # if game.pieces[i].value!=None:
                    #     win.blit(images[game.pieces[i].value*2+game.pieces[i].color],(i%8*75,i//8*75))
                    if (xposs/75+yposs/75) % 2 == 0:
                        color = (255, 228, 156)
                    else:
                        color = (106, 77, 15)
                    pygame.draw.rect(win, color, pygame.Rect(
                        i % 8*75, i//8*75, 75, 75))
                    if game.pieces[i].value != None:
                        win.blit(
                            images[game.pieces[i].value*2+game.pieces[i].color], (i % 8*75, i//8*75))
                pygame.display.update()
                xmark = mousy[0]//75
                ymark = mousy[1]//75
                clicked = None
                for i in arounds:
                    try:
                        indexy = other-i
                        if (indexy % 8+indexy//8) % 2 == 0:
                            color = (255, 228, 156)
                        else:
                            color = (106, 77, 15)
                        pygame.draw.rect(win, color, pygame.Rect(
                            indexy % 8*75, indexy//8*75, 75, 75))
                        if game.pieces[indexy].value != None:
                            win.blit(
                                images[game.pieces[indexy].value*2+game.pieces[indexy].color], (indexy % 8*75, indexy//8*75))
                    except:
                        pass
    pygame.display.update()
