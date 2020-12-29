#!/usr/bin/env python3
import os
import time
import torch
from state import State
import chess

class Valuator():
  def __init__(self):
    from train import Net
    vals = torch.load("nets/value.pth")
    self.model = Net()
    self.model.load_state_dict(vals)
    self.reset()

  def __call__(self, s):
    self.count+=1
    b = s.serialize()[None]
    out = self.model(torch.tensor(b).float())
    return float(out.data[0][0])

  def reset(self):
    self.count = 0

MAXVAL = 10000
def minimax(s, v, depth, a, b, big=False):
  if depth>=3 or s.board.is_game_over():
    return v(s)

  #White is maxing
  turn = s.board.turn
  if turn == chess.WHITE:
    ret = -MAXVAL
  else:
    ret = MAXVAL
  if big: 
    bret = []

	# Prune with beam search
  isort = []
  for e in s.board.legal_moves:
    s.board.push(e)
    isort.append((v(s), e))
    s.board.pop()
  move = sorted(isort, key=lambda x: x[0], reverse=s.board.turn)

  if depth >= 2:
    move = move[:10]

  for e in [x[1] for x in move]:
    s.board.push(e)
    tval = minimax(s, v, depth+1, a, b)
    s.board.pop()
    if big:
      bret.append((tval, e))
    if turn == chess.WHITE:
      ret = max(ret, tval)
      a = max(a, ret)
      if a>=b:
        break   # b cut-off
    else:
      ret = min(b, tval)
      b = min(b, ret)
      if a>=b:
        break

  if big:
    return ret, bret
  else:
    return ret

def explore_leaves(s, v):
  ret = []
  start = time.time()
  v.reset()
  bval = v(s)
  cval, ret = minimax(s, v, 0, a=-MAXVAL, b=MAXVAL, big=True)
  eta = time.time() - start
  print("%.2f -> %.2f: explored %d nodes in %.3f seconds %d/sec" % (bval, cval, v.count, eta, int(v.count/eta)))
  return ret

    
if __name__=="__main__":
  v = Valuator()
  s = State()
  print(v(s))
  for e in s.edges():
    s.board.push(e)
    print(v(s))
    s.board.pop()

  print("With explore leaves")
  ret = explore_leaves(s,v)
  print([x[0] for x in ret])
