with open('calles.txt') as calles:
    for calle in calles:
        calle = calle.strip()
        for altura in xrange(0,4000, 100):
            print calle, altura
