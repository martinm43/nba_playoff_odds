# distutils: language = c++
# distutils: sources = mcss.cpp

# Cython interface file for wrapping the object
#
#


from libcpp.vector cimport vector
from libcpp.string cimport string

# c++ interface to cython
cdef extern from "mcss.hpp":

    cdef cppclass Team:

        Team(int,string,string,string,string,float) except +

        int get_team_id()
        string get_mlbgames_name()
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

cdef extern from "mcss.hpp":
    vector[vector[double]] simulations_result_vectorized(vector[vector[double]], vector[vector[double]], vector[Team])

