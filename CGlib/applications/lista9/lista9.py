from math import floor

def dda(ponto1, ponto2):
    pontos_out = [ponto1]

    direction = ''
    steps = 0
    dy = ponto2[1] - ponto1[1]
    dx = ponto2[0] - ponto1[0]
    
    m = dy/dx
    yk = xk = 0
    ystep = xstep = 0
    
    if (abs(dy) > abs(dx)):
        #direction = 'y'
        steps = abs(ponto1[1] - ponto2[1])+1
        
        if (dy < 0):
            ystep = -1
            if (dx < 0):
                xstep = -1/m
            else:
                xstep = 1/m
        else:
            ystep = 1
            xstep = 1/m
    else:
        #direction = 'x'
        steps = abs(ponto1[0] - ponto2[0])+1
        
        if (dx < 0):
            xstep = -1
            if (dy < 0):
                ystep = -m
            else:
                ystep = m
        else:
            xstep = 1
            ystep = m

    yk = ponto1[1]
    xk = ponto1[0]
    
    for i in range(steps-1):
        yk += ystep
        xk += xstep
        pontos_out.append((floor(xk),floor(yk)))

    return pontos_out

def bresenhamX(ponto1, ponto2):
    pontos_out = []

    dy = ponto2[1] - ponto1[1]
    dx = ponto2[0] - ponto1[0]
    ystep = 1
    if (dy<0):
        dy = -dy
        ystep = -1

    pk = 2*dy - dx
    yk = ponto1[1]
    for x in range(ponto1[0],ponto2[0]+1):
        pontos_out.append((x,yk))
        if (pk >= 0):
            yk += ystep
            pk -= 2*dx
        pk += 2*dy
    return pontos_out

def bresenhamY(ponto1, ponto2):
    pontos_out = []

    dy = ponto2[1] - ponto1[1]
    dx = ponto2[0] - ponto1[0]
    xstep = 1
    if (dx<0):
        dx = -dx
        xstep = -1

    pk = 2*dx - dy
    xk = ponto1[0]
    for y in range(ponto1[1],ponto2[1]+1):
        pontos_out.append((xk,y))
        if (pk >= 0):
            xk += xstep
            pk -= 2*dy
        pk += 2*dx
    return pontos_out

def bresenham(ponto1, ponto2):
    if (abs(ponto1[1] - ponto2[1]) < abs(ponto1[0] - ponto2[0])):
        if (ponto1[0] > ponto2[0]):
            return bresenhamX(ponto2,ponto1)
        else:
            return bresenhamX(ponto1,ponto2)
    else:
        if (ponto1[1] > ponto2[1]):
            return bresenhamY(ponto2,ponto1)
        else:
            return bresenhamY(ponto1,ponto2)

pontos = [(0, 0),(6, 0),(10, 3),(8, 9),(0, 9),(5, 5)]

print("Pontos com DDA:")
for i in range(len(pontos)-1):
    print(dda(pontos[i], pontos[i+1]))
print(dda(pontos[len(pontos)-1], pontos[0]))

print("\nPontos com Bresenham:")
for i in range(len(pontos)-1):
    print(bresenham(pontos[i], pontos[i+1]))
print(bresenham(pontos[len(pontos)-1], pontos[0]))

