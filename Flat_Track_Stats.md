#Flat Track Stats Difference over Sum#
As shown at: http://flattrackstats.com/about/algorithm/detailed

*It is an ELO ranking

*Key element is Difference over Sum. 
*Compared to expected "difference over sum"
*change in team ranking is given 

*bonus: computationally feasible
*adjusts to large changes in skill with suitable factors
*another rating method would be nice given how broken SRS is

*expected DoS given by:

-1+2/(1+exp(Rb-Ra-đ))

where đ is a home factor or home playoff factor or what have you

