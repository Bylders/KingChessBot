from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse

def ab(x):
	if x < 0:
		return -1 * x
	else:
		return x

def printgrid(size, grid):
	for i in range(size, 0, -1):
		for j in range(1, size + 1):
			print grid[i*(size + 1) + j],
		print "\n"

def ping(request):
	val = {}
	val["ok"] = "true"
	return JsonResponse(val, safe=False)

def start(request):
	size = int(request.GET["g"])

	mearr = request.GET["y"].split("|")
	mex = int(mearr[0])
	mey = int(mearr[1])

	oparr = request.GET["o"].split("|")
	opx = int(oparr[0])
	opy = int(oparr[1])

	grid = []

	for i in range(0, size + 1):
		grid.append([0 for j in range(0, size + 1)])

	grid[mey][mex] = 2
	grid[opy][opx] = 3

	f = open("grid.txt", "w")

	myloc = str(size) + "\n" + str(mex) + " " + str(mey) + "\n"
	oploc = str(opx) + " " + str(opy) + "\n"
	f.write(myloc)
	f.write(oploc)

	gridstr = ""
	for i in range(0, size + 1):
		for j in range(0, size + 1):
			gridstr += str(grid[i][j])

	f.write(gridstr)
	f.close()

	printgrid(size, gridstr)

	val = {}
	val["ok"] = "true"
	return JsonResponse(val, safe=False)


mov = [[-1,0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
WALL = 1

def gethur(x, y, opp,grid, n):
    if [x,  y] == opp:
        return 0
    elif ab(opp[0] - x) <= 1 and ab(opp[1] - y) <= 1:
    	return 999
    else:
    	s=0
    	for m in mov:
    		a,b=m
    		if (not (x + a< 1 or x + a > n)) and (not(y + b < 1 or y + b >n )) and (not (grid[y+b][x+a] == 1)):
    			if grid[y+b][x+a]==0 or grid[y+b][x+a]==3:
    				s+=1
    	if s<3:
    		return 5
    	else:
    		return 1

def getnext(n, me, grid, opp):
	x, y = me
	mini = 999999999999
	j,k = opp
	if j>x:
		if k>y:
			mov = [[1,1], [0,1], [1,0], [-1,1], [1,-1], [-1,0], [0,-1], [-1,-1]]
		elif k==y:
			mov = [[1,0], [1,1], [1,-1], [0,1], [0,-1], [-1,1], [-1,-1], [-1,0]]
		else:
			mov = [[1,-1], [1,0], [0,-1], [1,1], [-1,-1], [0,1], [-1,0], [-1,1]]
	elif j==x:
		if k>y:
			mov = [[0,1], [-1,1], [1,1], [-1,0], [1,0], [-1,-1], [1,-1], [0,-1]]
		else:
			mov = [[0,-1], [-1,-1], [1,-1], [-1,0], [1,0], [-1,1], [1,1], [0,1]]
	else:
		if k>y:
			mov = [[-1,1], [0,1], [-1,0], [1,1], [-1,-1], [1,0], [0,-1], [1,-1]]
		elif k==y:
			mov = [[-1,0], [-1,1], [-1,-1], [0,1], [0,-1], [1,1], [1,-1], [1,0]]
		else:
			mov = [[-1,-1], [-1,0], [0,-1], [-1,1], [1,-1], [0,1], [1,0], [1,1]]

	for m in mov:
		a, b = m
		if (not (x + a< 1 or x + a > n)) and (not(y + b < 1 or y + b >n )) and (not (grid[y+b][x+a] == 1)):
			h = gethur(x + a, y + b, opp,grid, n)
			if h < mini:
				mini = h
				minim = m

	return me[0]+minim[0], me[1]+minim[1]

def play(request):
	f = open("grid.txt", 'r')
	oldgridstr = f.readlines()
	f.close()

	size = int(oldgridstr[0].strip("\n"))

	movearr = request.GET["m"].split("|")
	movx = int(movearr[0])
	movy = int(movearr[1])

	oldme = oldgridstr[1].strip("\n").split(" ")
	oldmex = int(oldme[0])
	oldmey = int(oldme[1])

	oldop = oldgridstr[2].strip("\n").split(" ")
	oldopx = int(oldop[0])
	oldopy = int(oldop[1])

	grid = [[0 for i in range(size + 1)] for j in range(size + 1)]

	for i in range(size + 1):
		for j in range(size + 1):
			grid[i][j] = int(oldgridstr[3][i * (size + 1) + j])

	grid[oldmey][oldmex] = 1
	grid[oldopy][oldopx] = 1


	################################################################

	me = [oldmex, oldmey]
	opp = [movx, movy]

	newmex, newmey = getnext(size, me, grid, opp)
	print newmex, newmey
		# code our move #


	################################################################

	grid[movy][movx] = 3
	grid[newmey][newmex] = 2		# (6, 5)

	f = open("grid.txt", "w")

	myloc = str(size) + "\n" + str(newmex) + " " + str(newmey) + "\n"
	oploc = str(movx) + " " + str(movy) + "\n"
	f.write(myloc)
	f.write(oploc)

	gridstr = ""
	for i in range(0, size + 1):
		for j in range(0, size + 1):
			gridstr += str(grid[i][j])

	f.write(gridstr)
	f.close()

	printgrid(size, gridstr)

	val = {}
	val["m"] = str(newmex) + "|" + str(newmey)
	print val
	return JsonResponse(val, safe=False)
