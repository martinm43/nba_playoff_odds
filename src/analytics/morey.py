#Selection of mathematical models for NBA win predictions

def Elo_regress(dElo):
  return 1/(1+10**((-1*(dElo-93.5)/325)))

def SRS_regress(dSRS):
  import math
  return 1/(1+math.exp(-1*(0.15+dSRS*.095))) #.3
  
if __name__=='__main__':
  print((Elo_regress(500)))
