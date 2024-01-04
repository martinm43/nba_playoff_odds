# distutils: language = c++
# distutils: sources = mcss.cpp

"""
Cython interface file for wrapping the objects in the pxd file

"""

cimport mcss_ext
from libcpp.string cimport string
from libcpp.vector cimport vector
from cython.operator import dereference

cdef extern from "mcss.hpp":

    cdef cppclass Team:

        Team(int,string,string,string,string,float) except +
        Team() except +

        int get_team_id()
        string get_full_team_name()
        string get_abbreviation()
        string get_division()
        string get_league()
        float get_rating()
        int get_total_wins()


        void set_total_wins(int val)
        void set_wild_card_odds(float val)
        void set_division_odds(float val)
        void set_playoff_odds(float val)
        float get_wild_card_odds()
        float get_division_odds()
        float get_playoff_odds()

cdef class PyTeam:
    cdef Team *thisptr # hold a C++ instance of a team object

    def __cinit__(self,int id, string full_team_name, string abbreviation, string division, string league, float rating):
        self.thisptr = new Team(id,full_team_name,abbreviation,division,league,rating)

    def __dealloc__(self):
        del self.thisptr

    def get_team_id(self):
        return self.thisptr.get_team_id()

    def get_full_team_name(self):
        return self.thisptr.get_full_team_name()

    def get_abbreviation(self):
        return self.thisptr.get_abbreviation()

    def get_division(self):
        return self.thisptr.get_division()

    def get_league(self):
        return self.thisptr.get_league()

    def get_rating(self):
        return self.thisptr.get_rating()

    def get_total_wins(self):
        return self.thisptr.get_total_wins()

    def set_total_wins(self,val):
        self.thisptr.set_total_wins(val)

    def set_wild_card_odds(self,val):
        self.thisptr.set_wild_card_odds(val)

    def set_division_odds(self,val):
        self.thisptr.set_division_odds(val)

    def set_playoff_odds(self,val):
        self.thisptr.set_playoff_odds(val)

    def get_wild_card_odds(self):
        return self.thisptr.get_wild_card_odds()

    def get_division_odds(self):
        return self.thisptr.get_division_odds()

    def get_playoff_odds(self):
        return self.thisptr.get_playoff_odds()

def simulations_result_vectorized(head_to_head, future_games, list_of_teams, int year):
    """
    
    Wrapper to the C++ main function simulations_result_vectorized
    which leads to the Monte Carlo simulation muscle, the C++ function
    mcss_function.

    Parameters
    ----------
    head_to_head : matrix of each team's record against each other team
    future_games : list of pending games in format 
                    [away_team,home_team,home_team win probability]
    list_of_teams : A list of list in the format:
        [team_id,team short name,team abbreviation,
         team division,team conference,team_rating]
        [1, b'Hawks', b'ATL', b'Southeast', b'E', 998.7491657887414]

    Returns
    -------
    A list of lists in the format:
        [team_odds_of_making_playoffs,team_average_wins]

    """
    #Convert Python list of teams to a list of C++ team objects
    
    cdef vector[Team] cpp_list_of_teams

    for t in list_of_teams:
        team_id = int(t[0])
        full_team_name = t[1]
        abbreviation = t[2]
        division = t[3]
        league = t[4]
        rating = t[5]
        st = PyTeam(team_id,full_team_name,abbreviation,division,league,rating)
        st_cpp =dereference(st.thisptr)
        cpp_list_of_teams.push_back(st_cpp)

    return mcss_ext.simulations_result_vectorized(head_to_head, future_games,cpp_list_of_teams,year)
