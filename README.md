### Naismith ###
This is a little project I made to get NBA data using an API that 
scrapes data from official sources, stores it in a database, 
and predicst the likelihood of various NBA teams making the playoffs.
It (the folder) can run on any platform with a Python installation. 
Uses Monte Carlo simulations (a regular loop based simulation,
and a much faster, though more memory intensive, vector based 
simulation)

Done for fun and wanting to learn some Python, Git, iPython, Eclipse...

MAM - June 2017.

MAM - Now about to implement folder functionality in order to better organize work. "Folders/module" version will be new branch 
      until all files can be confirmed as working.

MAM, Oct 1 2017: the new files have been updated as required. Folder (aka module) functionality has been added.
It is known, however, that srscalc is a bit more complex of a problem than first though. A working (?) project exists in GitHub
but it is written for Python 3. 

Now dropping unused/unverified "intermediate calculation" tables (e.g. advanced stats moving average, or ASMA) as the fundamental 
calculations behind them are unverified. 

To do/considering:
*DONE: removing unused legacy calculation tables as above (anything related to our srs calculations)
*DONE: Pythagorean wins expectation function
*Reviewing and reperforming rest calculations
 *DONE: if rest=0 at beginning of season set to 72
 *DONE: proper ids based on year, game number, and home/away? (optional)
 *investigate the negative rest occurences in the new year.
*storing playoff odds in a table/figuring out how to automate them in order to produce "odds of making the playoffs" guides
*tiebreaker logic for playoffs
*implementing the above "Python 3" library for srscalc
*removing superfluous print-to-screen statements
*refining the output files - correcting formating in final output file
*Making output file optional
*Laptop: perform regression using Burke odds
*figuring out how to email them/playoff predictions/expected outcomes of games to personal account

Configured cron job on pi (be sure to change to required directory first)
