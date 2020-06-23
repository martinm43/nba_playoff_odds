# NBA Playoff Odds




## Summary 
A set of scripts to calculate ratings for teams, based on point differential and strength of schedule, and then use those ratings to determine playoff odds over a given season. 

## Examples

**info_table** - generates a snapshot of a season (pythagorean wins, Strength-of-Schedule adjusted net rating, away record, home record, and overall record)

	Pythagorean Win Expectations, Est. SRS, and Records 
	Based on Games Played Between: Oct 01 2018 and May 01 2019
	======  ==============  ==========  =============  =============  ================
	Team    Pythag. Wins    Est. SRS    Away Record    Home Record    Overall Record
	======  ==============  ==========  =============  =============  ================
	MIL     64              4.409       27-14          33-8           60-22
	GSW     60              3.61        27-14          30-11          57-25
	TOR     58              3.461       26-15          32-9           58-24
	HOU     55              2.744       22-19          31-10          53-29
	POR     53              2.674       21-20          32-9           53-29
	DEN     53              2.536       20-21          34-7           54-28
	UTA     56              2.498       21-20          29-12          50-32
	OKC     51              1.904       22-19          27-14          49-33
	PHI     49              1.55        20-21          31-10          51-31
	BOS     54              1.486       21-20          28-13          49-33
	LAC     44              1.413       22-19          26-15          48-34
	IND     51              1.255       19-22          29-12          48-34
	SAS     45              1.174       16-25          31-10          47-35
	ORL     43              -0.085      17-24          25-16          42-40
	SAC     38              -0.152      15-26          24-17          39-43
	CHA     38              -0.307      14-27          25-16          39-43
	DET     40              -0.31       15-26          26-15          41-41
	BKN     41              -0.436      19-22          23-18          42-40
	MIA     40              -0.541      20-21          19-22          39-43
	LAL     37              -0.582      16-25          22-19          38-44
	MIN     37              -0.726      11-30          25-16          36-46
	MEM     33              -1.064      12-29          21-20          33-49
	NOP     37              -1.202      14-27          19-22          33-49
	DAL     37              -1.433      9-32           24-17          33-49
	WAS     33              -2.012      10-31          22-19          32-50
	ATL     24              -3.192      11-30          17-24          28-54
	CHI     18              -3.992      13-28          9-32           22-60
	PHX     17              -4.462      7-34           12-29          19-63
	CLE     16              -5.046      6-35           13-28          19-63
	NYK     16              -5.174      8-33           9-32           17-65
	======  ==============  ==========  =============  =============  ================

**prediction_table** - generates a table of playoff odds
	
	Playoff odds for the 2019 season as of Jan 01 2019
	============  =============  ===========  ===========
	Conference    Team           Avg. Wins    Playoff %
	============  =============  ===========  ===========
	E             Bucks          63.9         100.0%
	E             Raptors        58.9         100.0%
	E             Pacers         56.4         100.0%
	E             Celtics        54           100.0%
	E             76ers          47.7         100.0%
	E             Hornets        42           98.4%
	E             Heat           39.3         95.6%
	E             Nets           34.5         48.1%
	E             Pistons        34.1         46.7%
	E             Magic          31.1         10.1%
	E             Wizards        27.4         1.1%
	E             Bulls          19.6         0.0%
	E             Hawks          19.4         0.0%
	E             Knicks         18.4         0.0%
	E             Cavaliers      15.9         0.0%
	W             Nuggets        57.3         100.0%
	W             Thunder        54.1         99.7%
	W             Warriors       53.9         99.8%
	W             Jazz           48.4         84.4%
	W             Clippers       47.7         79.5%
	W             Lakers         47.7         83.8%
	W             Rockets        47.3         78.4%
	W             Trail Blazers  46.5         71.1%
	W             Spurs          45.9         61.3%
	W             Kings          41.3         11.6%
	W             Pelicans       41.2         13.4%
	W             Grizzlies      41           11.1%
	W             Mavericks      39           3.7%
	W             Timberwolves   38.1         2.2%
	W             Suns           18           0.0%
	============  =============  ===========  ===========

**plot_season_odds** - creates a graph of playoff odds for teams in one division in one season

![Playoff odds for Pacific Division, 2019](https://raw.githubusercontent.com/martinm43/nba_playoff_odds/master/src/README_example.png) 

**update_nba_api** - obtains data (for now, just end scores) from the undocumented stats.nba.com api.

## Installation

Use "git clone..." or download a zip.

Monte Carlo simulation extension written in C++ requires g++ compilation using the build script (python/cython_mcss/ext_build.sh) and associated dependencies, see below.

## Requirements

Python requirements:  
the nba_py library (only for update_nba_api)  
peewee (version 3.11+)
numpy, scipy, and cython (obtained from the Anaconda scientific distribution)  

C++ requirements for compiling Monte Carlo cython extension:  
libarmadillo-dev   
libsqlite3-dev  

## To Do
Improve markdown formatting of README (e.g., link to all mentioned libraries)  
Rearrange structure of library (move code one level down into "src"  
Write manual test descriptions  
Write all scripts in "function" form   
Write automated tests/unit tests  

*A whole lot of else - this project is very much still in development!*
