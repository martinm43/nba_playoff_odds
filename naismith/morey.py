#Selection of mathematical models for NBA win predictions

def SRS_regress(dSRS):
  import math
  return 1/(1+math.exp(-1*(0.15+dSRS*0.35)))

def burke_regress(dBurke):
	import math
	return 1/(1+math.exp(-1*(0.15+dBurke*0.3)))
  
if __name__=='__main__':
  print(SRS_regress(2))
