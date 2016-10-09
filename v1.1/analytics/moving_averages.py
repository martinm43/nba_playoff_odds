#-*-coding:utf8;-*-
#qpy:2
#qpy:console


#StackOverflow: manual methods are 20x slower
#See http://stackoverflow.com/questions/13728392/moving-average-or-running-mean  
def runningMeanFast(x, N): 
  import numpy as np
  conv_array=np.convolve(x, np.ones((N,))/N)[(N-1):]
  #original program - return conv_array
  #multiply by factors to correct for end of array
  #for i in range(1,N):
  #  conv_array[-i]=conv_array[-i]*N/i
  return conv_array
  

if __name__=='__main__':
  import numpy as np
  x=[1,3,6,7,9,10]
  N=2
  x=np.asarray(x)
  print(x)
  print(runningMeanFast(x,N))
  
