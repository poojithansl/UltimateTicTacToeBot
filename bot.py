import sys
import random

class Bot:

    def __init__(self):
        self.block_corr = { 0:[1,3] , 1:[0,2] , 2:[1,5] , 3:[0,6] , 4:[4] , 5:[2,8] , 6:[3,7] , 7:[6,8] , 8:[5,7]}
        self.mine = ''
        self.bflags = ('x','o')


    def move(self, temp_board, temp_block, old_move, flag):
        if old_move == (-1, -1):
            return (3, 3)
        self.mine = flag
        blocks_valid = self.valid_block(temp_block,old_move)
        cells = self.empty_cells(temp_board, blocks_valid, temp_block)
        high = -100000
        maxi = (old_move[0], old_move[1])
        turn = []
        if flag == 'x':
            turn.append('x')
            turn.append('o')
        else:
            turn.append('o')
            turn.append('x')
        depth = 3
        if temp_block.count('x') > 2 and temp_block.count('o') > 2:
            depth = 5
        for j in range(1, depth + 1):
            for i in cells:
                temp2_board = [ row[:] for row in temp_board ]
                temp2_board[i[0]][i[1]] = flag
                value = self.alphabeta(temp2_board, turn[1], depth, i, temp_block[:], -100000, 100000, turn)
                if value > high:
                    high = value
                    maxi = i


        return (maxi[0], maxi[1])
    def valid_block(self, my_block, my_move):
        B = self.block_corr[(my_move[0]%3)*3 + (my_move[1]%3)]
        if len(B) == 1 :
            if my_block[4] == '-':
                return [4]
            else:
                return []
        else:
            if my_block[B[0]] == '-' and my_block[B[1]] == '-':
                return B
            elif my_block[B[0]] == '-':
                return [B[0]]
            elif my_block[B[1]] == '-':
                return [B[1]]
            else:
                return []




    def count(self,cnt_x,cnt_o,cnt_n):

        if (cnt_x == 2 and cnt_o == 1) or (cnt_x == 1 and cnt_o == 2) or (cnt_n == 3 ) or (cnt_x == cnt_o == cnt_n ==1):
            return  0
        elif cnt_x == 2 :
            return 10
        elif cnt_o == 2 :
            return -10
        elif cnt_x == 1:
            return 1
        elif cnt_o == 1:
            return -1
        elif cnt_o == 3:
            return -100
        elif cnt_x == 3:
            return 100

    def calc(self,val):
        if val <= -2:                           # val = [-3,-2]
            tmp = -10+(val+2)*90
            return tmp

        elif val <= -1:                         # val = (-2,-1]
            tmp = -1 + (val+1)*9
            return tmp

        elif val <= 1:                          # val = (-1,1]
            return val

        elif val <= 2:                          # val = (1,2]
            tmp = 1+(val-1)*9
            return tmp

        else:                          # val = (2,3]
            tmp = 10+(val-2)*90
            return tmp
    
    def utilit(self,boardmy,blockmy):
        t = []
        u_b = [0]*9
        vert={0:(0,0), 1:(0,3), 2:(0,6), 3:(3,0), 4:(3,3), 5:(3,6), 6:(6,0), 7:(6,3), 8:(6,6)}

        
        
        for i in range(9):
            if blockmy[i] == '-':
                t.append(i)
            
            elif blockmy[i] != self.mine:
                u_b[i] = -1
            elif blockmy[i] == self.mine:
                u_b[i] = 1
        
        for j in range(len(t)):
            x = vert[t[j]][0]
            y = vert[t[j]][1]
            u = 0
            for p in range(x,x+3):

                cnt_x,cnt_o,cnt_n = 0,0,0

                for q in range(y,y+3):
                    if boardmy[p][q] == self.mine:
                        cnt_x += 1
                    elif boardmy[p][q] == '-':
                        cnt_n += 1
                    elif boardmy[p][q] != self.mine:
                        cnt_o += 1
                    
                
                u += self.count(cnt_x,cnt_o,cnt_n)
            for q in range(y,y+3):

                cnt_x,cnt_o,cnt_n = 0,0,0

                for p in range(x,x+3):
                    if boardmy[p][q] == self.mine:
                        cnt_x += 1
                    elif boardmy[p][q] == '-':
                        cnt_n += 1
                    elif boardmy[p][q] != self.mine:
                        cnt_o += 1
                    
                u += self.count(cnt_x,cnt_o,cnt_n)
            cnt_x,cnt_o,cnt_n = 0,0,0   
            for p in range(3):

                if boardmy[x+p][y+p] == self.mine:
                    cnt_x += 1
                elif boardmy[x+p][y+p] == '-':
                    cnt_n += 1
                elif boardmy[x+p][y+p] != self.mine:
                    cnt_o += 1
                
            u += self.count(cnt_x,cnt_o,cnt_n)

            cnt_x,cnt_o,cnt_n = 0,0,0
            for p in range(3):

                if boardmy[x+p][y+2-p] == self.mine:
                    cnt_x += 1
                elif boardmy[x+p][y+2-p] == '-':
                    cnt_n += 1
                elif boardmy[x+p][y+2-p] != self.mine:
                    cnt_o += 1
                
            u += self.count(cnt_x,cnt_o,cnt_n)

            if u >= 100:
                u = 100
            elif u <= -100:
                u = -100
            u_b[t[j]] = u/100.0
            
        uti = 0
        r = 0
        while r <= 6:
            m = u_b[r]+u_b[r+1]+u_b[r+2]
            uti += self.calc(m)
            r += 3
        r = 0
        while r <= 2:
            m = u_b[r]+u_b[r+3]+u_b[r+6]
            uti += self.calc(m)
            r += 1
        m = u_b[0]+u_b[4]+u_b[8]
        uti += self.calc(m)

        m = u_b[2]+u_b[4]+u_b[6]
        uti += self.calc(m)

        return uti 


    def alphabeta(self, temp_board, flag, depth, old_move, block_stat, alpha, beta, turn):
        if depth == 0:
            return self.utilit(temp_board, block_stat)
        if flag == 'x':
            ind = 1
        else:
            ind = 0
        block_stat = self.bloup(temp_board, block_stat[:], old_move, self.bflags[ind])
        blocks_allowed = self.valid_block(block_stat, old_move)
        if len(blocks_allowed) == 0:
            for i in range(len(block_stat)):
                if block_stat[i] == '-':
                    blocks_allowed.append(i)

        cells = self.empty_cells(temp_board, blocks_allowed, block_stat)
        if len(cells) == 0:
            return self.utilit(temp_board, block_stat)
        if flag == turn[0]:
            for i in cells:
                temp2_board = [ row[:] for row in temp_board ]
                temp2_board[i[0]][i[1]] = flag
                score = self.alphabeta(temp2_board, turn[1], depth - 1, i, block_stat[:], alpha, beta, turn)
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break

            return alpha
        if flag == turn[1]:
            for i in cells:
                temp2_board = [ row[:] for row in temp_board ]
                temp2_board[i[0]][i[1]] = flag
                score = self.alphabeta(temp2_board, turn[0], depth - 1, i, block_stat[:], alpha, beta, turn)
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break

            return beta



   



    def empty_cells(self, gameb, blal, block_stat):
        cells = []
        for i in blal:
            x = i / 3
            y = i % 3
            for i in range(x * 3, x * 3 + 3):
                for j in range(y * 3, y * 3 + 3):
                    if gameb[i][j] == '-':
                        cells.append((i, j))



        if cells == []:
            bla = []
            
            for i in range(9):
                if block_stat[i] == '-':
                    bla.append(i)

            for i in bla:
                x = i / 3
                y = i % 3
                for i in range(x * 3, x * 3 + 3):
                    for j in range(y * 3, y * 3 + 3):
                        if gameb[i][j] == '-':
                            cells.append((i, j))



        return cells

    def bloup(self,boardm,blockm,bmove,flagm):
        bpos = bmove[0] / 3 * 3 + bmove[1] / 3
        x = int(bpos/3)*3
        y = (bpos%3)*3
 
        #print boardm
        #print
        #print blockm
        
        for i in range(x,x+3):
            count = 0
            for j in range(y,y+3):
                if boardm[i][j] == flagm:
                    count += 1
            if count == 3:
                blockm[bpos] = flagm
                return blockm
        
        for j in range(y,y+3):
            count = 0
            for i in range(x,x+3):
                if boardm[i][j] == flagm:
                    count += 1
            if count == 3:
                blockm[bpos] = flagm
                return blockm
        count = 0
        for i in range(3):
            if boardm[x+i][y+i] == flagm:
                count += 1
            if count == 3:
                blockm[bpos] = flagm
                return blockm
        count = 0
        for i in range(3):
            if boardm[x+i][y-i+2] == flagm:
                count += 1
            if count == 3:
                blockm[bpos] = flagm
                return blockm
        count = 0
        for i in range(x,x+3):
            for j in range(y,y+3):
                if boardm[i][j] != '-':
                    count += 1  

        if count == 0:
            blockm[bpos] = 'D'
            return blockm
        else:
            return blockm

    





