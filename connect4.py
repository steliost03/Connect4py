#	 Connect4py - A Connect 4 implementation for 1 or 2 players
#    Copyright (C) 2011  Argiris Dramountanis, Nikos Kerastas, Vasilis Paloglou,
#	 Sotiris Papatheodorou, Stelios Tsiakalos
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This exception is raised when a column is full
class FullColumnError(Exception):
    def __init__(self):
        pass

# Create the board
def initboard():
    global board
    title("Connect 4")
    print "----------Connect4----------"
    print
    print "Please wait..."
    print
    board=[[],[],[],[],[],[],[]]
	# Board elements: 1(human-yellow), 2(cpu-red)
    # Draw the board with turtle
    ht()
    bgcolor("#4f4f4f")
    speed(0)

    color("#000060") # Shadow color
    up()
    goto(-300,-300)
    down()
    fill(True)
    goto(-312,-288)
    left(90)
    fd(600)
    right(90)
    fd(600)
    goto(300,300)
    goto(-300,-300)
    fill(False)
    color("#000090")
    fill(True)
    up()
    goto(-300,-300)
    down()
    for i in range(2):
        fd(600)
        left(90)
        fd(600)
        left(90)
    fill(False)
    # Draw circles
    for i in range(1,7):
        for j in range(7):
            color("#000060")
            up()
            goto(j*80-250+7+1,i*80-300-7+1)
            down()
            begin_fill()
            circle(30)
            end_fill()
            color("#4f4f4f")
            up()
            goto(j*80-250,i*80-300)
            down()
            begin_fill()
            circle(30)
            end_fill()
    # Draw numbers
    for i in range(7):
        up()
        goto(i*80-250,-80-200)
        down()
        color("white")
        write(str(i+1),False,align="center",font=("Arial",20,"normal"))

# Reset the board
def emptyboard():
    global board
    print "----------------------------"
    print
    print "Please wait..."
    print
    print "----------------------------"
    board[:]=[[],[],[],[],[],[],[]]
    # Draw over the colored disks in turtle
    color("#4f4f4f")
    for i in range(1,7):
        for j in range(7):
            up()
            goto(j*80-250,i*80-300)
            down()
            begin_fill()
            circle(30)
            end_fill()

# Draw the disc added
def disc(col,pl,h):
    """column,player,column height"""
    up()
    goto(col*80-250,h*80-300)
    down()
    if pl==1:
        color("yellow")
    else:
        color("red")
    begin_fill()
    circle(30)
    end_fill()

# The player adds a disc
def add(pl):
    """player"""
    global nextturn,col
    # Check if the board is full
    for j in range(7):
        if len(board[j])<6:
            break
    else:
        nextturn=0

    # The player plays if the board is not full
    while nextturn==1:
        # Check for valid input
        try:
            col=int(raw_input("Column: "))-1
            if col<0:
				# Negative index
                raise ValueError
            elif len(board[col])==6:
				# The chosen column is full
                raise FullColumnError
            else:
				# Add the disc to the board
                board[col].append(pl)
				# Draw the disc
                disc(col,pl,len(board[col]))
            break
		# Messages for invalid input
        except IndexError:
            print "Please enter a number in the range 1-7"
        except ValueError:
            print "Please enter a number in the range 1-7"
        except FullColumnError:
            print "This column is full,please choose another"

	# Check if the current player won with the last move
    if win(board,col)==pl:
            nextturn=0

# The computer adds a disc
def addcpu(pl):
    """player"""
    global nextturn,col
    # Check if the board is full
    for j in range(7):
        if len(board[j])<6:
            break
    else:
        nextturn=0
	# The cpu plays if the board is not full
    if nextturn==1:
        # Rate the possible moves

        # Check if this is the cpus fisrt move
        lengths=[len(board[i]) for i in range(7)]
        if (lengths.count(1)==1 and lengths.count(0)==6) or lengths.count(0)==7:
            if len(board[3])==0:
				# Play on the middle column if possible
                col=3
            else:
				# Else play next to it
                col=choice([2,4])
        else:
            # Initialize the rating lists
            ratings1=[[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],\
			[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],[],[],[],[],[]],[[],[],\
			[],[],[],[],[]],[[],[],[],[],[],[],[]]]
            ratings2=[[],[],[],[],[],[],[]]
            ratings3=[]
            for i in range(7):
                ratings3.append(-1)
                for j in range(7):
                    ratings2[i].append(-1)
                    for k in range(7):
                        ratings1[i][j].append(-1)

			# Check if the cpu can win in one move - high priority
            flag=True
            for i in range(7):
                if ratewin(board,i,pl)>0:
                    col=i
                    flag=False
                    break
            # Check if the player can win in one move - medium priority
            if flag:
                for i in range(7):
                    if ratewin(board,i,pl%2+1)>0:
                        col=i
                        flag=False
                        break
            # Rate the rest of the moves - low priority
            if flag:
                # Check three moves ahead
                for i in range(7):
                    if len(board[i])<6:
                        board[i].append(pl)
                        for j in range(7):
                            if len(board[j])<6:
                                board[j].append(pl%2+1)
                                for k in range(7):
                                    ratings1[i][j][k]=rate(board,k,pl)
                                board[j].pop()
                        board[i].pop()
                # Two moves ahead - max
                for i in range(7):
                    for j in range(7):
                        ratings2[i][j]=max(ratings1[i][j])
                # One move ahead max
                for i in range(7):
                    ratings3[i]=max(ratings2[i])

                # Check for full columns
                for i in range(7):
                    if len(board[i])==6:
                        ratings3[i]=-4
                # Check if one of the cpu moves makes the player win - avoid it
                for i in range(7):
                    if len(board[i])<5:
                        board[i].append(pl)
                        if ratewin(board,i,pl%2+1)>0:
                            ratings3[i]=-3
                        board[i].pop()
                # Choose the move with the highest rating
                if ratings3.count(max(ratings3))>1:
					# Choose randomly if needed
                    indexlist=[i for i in range(7) if ratings3[i]==max(ratings3)]
                    col=choice(indexlist)
                else:
                    col=ratings3.index(max(ratings3))
        # Perform the chosen move
        board[col].append(pl)
        disc(col,pl,len(board[col]))
	# Check if the cpu won with its last move
    if win(board,col)==pl:
        nextturn=0

# Check which player won
def paikths(board,col):
    """board,column"""
    if board[col][len(board[col])-1]==1:
        return 1
    else:
        return 2

# Check if one of the players won
def win(board,col):
    """board,column"""
	# Returns the number of the player that won or zero if nobody won
	# Only need to check around the disk that was added last

    # Check columns
    if len(board[col])>=4:
		# If the column has 4 or more disks
        i,cons=len(board[col])-1,1
        while (i>=1) and (cons<4):
			# Count consequtive disks with the same color
            if board[col][i]==board[col][i-1]:
                i,cons=i-1,cons+1
            else:
                break
        if cons==4:
			# If 4 consequtive disks were found, check which player won
            return paikths(board,col)

    # Check rows - no need to check if there is no disk in the middle column
    if len(board[3])>=len(board[col]):
        i,j,cons=len(board[col])-1,col,1
        while (j<=5) and (cons<4):
			# Count consequtive disks with the same colot on the right of col
            try:
                if board[j][i]==board[j+1][i]:
                    j,cons=j+1,cons+1
                else:
                    break
            except IndexError:
				# Raised when an empty cell is encountered
                break
        if cons==4:
			# If 4 consequtive disks were found, check which player won
            return paikths(board,col)
        j=col
        while (j>=1) and (cons<4):
			# Count consequtive disks with the same colot on the left of col
            try:
                if board[j][i]==board[j-1][i]:
                    j,cons=j-1,cons+1
                else:
                    break
            except IndexError:
				# Raised when an empty cell is encountered
                break
        if cons==4:
			# If 4 consequtive disks were found, check which player won
            return paikths(board,col)

    # Check giagonals
    # Count consequtive disks on the top right
    i,j,cons=len(board[col])-1,col,1
    while i<5 and j<6 and cons<4:
        try:
            if board[j][i]==board[j+1][i+1]:
                cons=cons+1
                i,j=i+1,j+1
            else:
                break
        except IndexError:
            break
    if cons==4:
            return paikths(board,col)
    # Count consequtive disks on the bottom left
    i,j=len(board[col])-1,col
    while i>0 and j>0 and cons<4:
        try:
            if board[j][i]==board[j-1][i-1]:
                cons=cons+1
                i,j=i-1,j-1
            else:
                break
        except IndexError:
            break
    if cons==4:
            return paikths(board,col)
    # Count consequtive disks on the top left
    i,j,cons=len(board[col])-1,col,1
    while i<5 and j>0 and cons<4:
        try:
            if board[j][i]==board[j-1][i+1]:
                cons=cons+1
                i,j=i+1,j-1
            else:
                break
        except IndexError:
            break
    if cons==4:
            return paikths(board,col)
    # Count consequtive disks on the bottom right
    i,j=len(board[col])-1,col
    while i>0 and j<6 and cons<4:
        try:
            if board[j][i]==board[j+1][i-1]:
                cons=cons+1
                i,j=i-1,j+1
            else:
                break
        except IndexError:
            break
    if cons==4:
            return paikths(board,col)
	# Return zero if nobody won
    return 0

# Rate a possible move of the given player
def rate(board,col,pl):
    """board,column,player"""

    score=0
    if len(board[col])<6:
        # Columns
        cons=0
        for i in range(len(board[col])-1,-1,-1):
            if board[col][i]==pl:
                cons=cons+1
            else:
                break
        # Check if there is enough space
        if 6-len(board[col])+cons>=4:
			# Add the rating
            if cons>=3:
                score=score+1337 # Arbitrary large number for high priority
            else:
                score=score+cons

		# Rows
        # Copy the line in a list
        line=[]
        i=len(board[col])
        for j in range(7):
            try:
                if board[j][i]==1:
                    line.append(1)
                else:
                    line.append(2)
            except IndexError:
                line.append(0)
                continue
        # On the right of col
        consr=0
        j=col+1
        counterr=0
        while j<=6 and counterr<3:
            if line[j]==pl:
                consr=consr+1
                counterr=counterr+1
                j=j+1
            elif line[j]==pl%2+1:
                break
            else:
                counterr=counterr+1
                j=j+1
        # On the left of col
        consl=0
        j=col-1
        counterl=0
        while j>=0 and counterl<3:
            if line[j]==pl:
                consl=consl+1
                counterl=counterl+1
                j=j-1
            elif line[j]==pl%2+1:
                break
            else:
                counterl=counterl+1
                j=j-1
        # Add the rating
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337
            else:
                score=score+consr+consl

		# Diagonal
        # bottom right upper left
        # Copy the diagonal in a list
        line[:]=[]
        i=len(board[col])
        k=i
        l=col
        while k>0 and l<6 and l>0:
            k=k-1
            l=l+1
        for m in range(6):
            try:
                if l>=0:
                    if k==i and l==col:
                        deikths=m
                    if board[l][k]==1:
                        line.append(1)
                    else:
                        line.append(2)
                    k=k+1
                    l=l-1
                else:
                    raise IndexError
            except IndexError:
                line.append(0)
                k=k+1
                l=l-1
                continue
        # On the right of deikths
        consr=0
        j=deikths+1
        counterr=0
        while j<7 and counterr<3:
            try:
                if line[j]==pl:
                    consr=consr+1
                    counterr=counterr+1
                    j=j+1
                elif line[j]==pl%2+1:
                    break
                else:
                    counterr=counterr+1
                    j=j+1
            except IndexError:
                break
        # On the left of deikths
        consl=0
        j=deikths-1
        counterl=0
        while j>=0 and counterl<3:
            try:
                if line[j]==pl:
                    consl=consl+1
                    counterl=counterl+1
                    j=j-1
                elif line[j]==pl%2+1:
                    break
                else:
                    counterl=counterl+1
                    j=j-1
            except IndexError:
                break
        # Add the rating
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337
            else:
                score=score+consr+consl
        # bottom left upper right
        # Copy the diagonal in a list
        line[:]=[]
        i=len(board[col])
        k=i
        l=col
        while k>0 and l>0:
            k=k-1
            l=l-1
        for m in range(6):
            try:
                if k==i and l==col:
                    deikths=m
                if board[l][k]==1:
                    line.append(1)
                else:
                    line.append(2)
                k=k+1
                l=l+1
            except IndexError:
                line.append(0)
                k=k+1
                l=l+1
                continue
        # On the left of deikths
        consr=0
        j=deikths+1
        counterr=0
        while j<7 and counterr<3:
            try:
                if line[j]==pl:
                    consr=consr+1
                    counterr=counterr+1
                    j=j+1
                elif line[j]==pl%2+1:
                    break
                else:
                    counterr=counterr+1
                    j=j+1
            except IndexError:
                break
        # On the right of deikths
        consl=0
        j=deikths-1
        counterl=0
        while j>=0 and counterl<3:
            try:
                if line[j]==pl:
                    consl=consl+1
                    counterl=counterl+1
                    j=j-1
                elif line[j]==pl%2+1:
                    break
                else:
                    counterl=counterl+1
                    j=j-1
            except IndexError:
                break
        # Add the rating
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337
            else:
                score=score+consr+consl
        return score
    else:
        return -2

# Check if the given player can win in a single move
def ratewin(board,col,pl):
    """board,column,player"""
	# This follows a similar procedure to rate()
    score=0
    if len(board[col])<6:
        # Columns
        cons=0
        for i in range(len(board[col])-1,-1,-1):
            if board[col][i]==pl:
                cons=cons+1
            else:
                break
        if 6-len(board[col])+cons>=4:
            if cons>=3:
                score=score+1337

		# Rows
        line=[]
        i=len(board[col])
        for j in range(7):
            try:
                if board[j][i]==1:
                    line.append(1)
                else:
                    line.append(2)
            except IndexError:
                line.append(0)
                continue
        consr=0
        j=col+1
        counterr=0
        while j<=6 and counterr<3:
            if line[j]==pl:
                consr=consr+1
                counterr=counterr+1
                j=j+1
            else:
                break
        consl=0
        j=col-1
        counterl=0
        while j>=0 and counterl<3:
            if line[j]==pl:
                consl=consl+1
                counterl=counterl+1
                j=j-1
            else:
                break
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337

		# Diagonal
        line[:]=[]
        i=len(board[col])
        k=i
        l=col
        while k>0 and l<6 and l>0:
            k=k-1
            l=l+1
        for m in range(6):
            try:
                if l>=0:
                    if k==i and l==col:
                        deikths=m
                    if board[l][k]==1:
                        line.append(1)
                    else:
                        line.append(2)
                    k=k+1
                    l=l-1
                else:
                    raise IndexError
            except IndexError:
                line.append(0)
                k=k+1
                l=l-1
                continue
        consr=0
        j=deikths+1
        counterr=0
        while j<7 and counterr<3:
            try:
                if line[j]==pl:
                    consr=consr+1
                    counterr=counterr+1
                    j=j+1
                else:
                    break
            except IndexError:
                break
        consl=0
        j=deikths-1
        counterl=0
        while j>=0 and counterl<3:
            try:
                if line[j]==pl:
                    consl=consl+1
                    counterl=counterl+1
                    j=j-1
                else:
                    break
            except IndexError:
                break
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337
        line[:]=[]
        i=len(board[col])
        k=i
        l=col
        while k>0 and l>0:
            k=k-1
            l=l-1
        for m in range(6):
            try:
                if k==i and l==col:
                    deikths=m
                if board[l][k]==1:
                    line.append(1)
                else:
                    line.append(2)
                k=k+1
                l=l+1
            except IndexError:
                line.append(0)
                k=k+1
                l=l+1
                continue
        consr=0
        j=deikths+1
        counterr=0
        while j<7 and counterr<3:
            try:
                if line[j]==pl:
                    consr=consr+1
                    counterr=counterr+1
                    j=j+1
                else:
                    break
            except IndexError:
                break
        consl=0
        j=deikths-1
        counterl=0
        while j>=0 and counterl<3:
            try:
                if line[j]==pl:
                    consl=consl+1
                    counterl=counterl+1
                    j=j-1
                else:
                    break
            except IndexError:
                break
        if counterr+counterl+1>=4:
            if (consr>=3) or (consl>=3) or (consr+consl>=3):
                score=score+1337
        return score
    else:
        return -2


################################################################################
############################# Main program #####################################
################################################################################

from turtle import *
from random import choice
synexeia='y'
games=1 # Number of games played
initboard()
plnum=raw_input('Enter the number of players(1/2): ')
while plnum not in ['1','2']:
    plnum=raw_input('Please 1 or 2: ')
print
print "----------------------------"
if plnum=='1':
	# One player vs cpu
    humanscore,computerscore=0,0
    while synexeia=='y': # Game loop
        nextturn=1 # The current game continues while this is true
        if games%2==1: # Change who plays first on each game
            player=1
        else:
            player=2
        while nextturn==1: # Round loop
            if player==1:
                print 'Human is playing'
                add(player)
            else:
                addcpu(player)
                print 'Computer played in column',col+1
            print
            player=player%2+1 # Change the current player
        print "----------------------------"
        print
        if win(board,col)==1:
            print 'Human won!'
            humanscore=humanscore+1
        elif win(board,col)==2:
            print 'Computer won!'
            computerscore=computerscore+1
        else:
            print 'Draw'
        games=games+1
        print
        print "Human - Computer"
        print
        print "    "+str(humanscore)+" - "+str(computerscore)
        print
        synexeia=raw_input('Do you want to play again?(y/n): ')
        while synexeia!='y' and synexeia!='n':
            synexeia=raw_input('Please y or n: ')
        if synexeia=='y':
            emptyboard()
else:
	# Two players
    yellowscore,redscore=0,0
    while synexeia=='y':
        nextturn=1
        if games%2==1:
            player=1
        else:
            player=2
        while nextturn==1:
            if player==1:
                print 'Yellow is playing'
            else:
                print 'Red is playing'
            add(player)
            print
            player=player%2+1
        print "----------------------------"
        print
        if win(board,col)==1:
            print 'Yellow won!'
            yellowscore=yellowscore+1
        elif win(board,col)==2:
            print 'Red won!'
            redscore=redscore+1
        else:
            print 'Draw'
        games=games+1
        print
        print "Yellow - Red"
        print
        print "      "+str(yellowscore)+" - "+str(redscore)
        print
        synexeia=raw_input('Do you want to play again?(y/n): ')
        while synexeia!='y' and synexeia!='n':
            synexeia=raw_input('Please y or n: ')
        if synexeia=='y':
            emptyboard()
