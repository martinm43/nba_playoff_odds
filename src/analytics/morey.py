#Selection of mathematical models for NBA win predictions


def Elo_regress(dElo):
  max_elo_diff = 400
  f = max_elo_diff/1.10266
  h = 0.17609*f
  return 1/(1+10**((-1*(dElo+h)/f)))

def SRS_regress(dSRS):
  import math
  return 1/(1+math.exp(-1*(0.15+dSRS*.095))) #.3

if __name__=='__main__':
  print((Elo_regress(0)))
