import time


def tally():
    score = 0

    while True:
        increment = yield score
        if increment is None:
            continue
        score += increment


white_sox = tally()
blue_jays = tally()

print('white_sox', next(white_sox))
print('blue_jays', next(blue_jays))

print('white_sox', white_sox.send(3))
print('blue_jays', blue_jays.send(2))

print('white_sox', white_sox.send(2))
print('blue_jays', blue_jays.send(4))

while True:
    print()
    print('white_sox', next(white_sox))
    print('blue_jays', next(blue_jays))
    time.sleep(1)

