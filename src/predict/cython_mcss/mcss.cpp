
/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <iomanip>
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <armadillo>
#include "mcss.hpp"

#define MAX_ITER 10000

using namespace std;
using namespace arma;

//Matrix Printing Tools

template<class Matrix>
void print_matrix(Matrix matrix) {
    matrix.print(std::cout);
}

//Converting vectors from python into appropriate matrices
//and vice versa.

stdvecvec mat_to_std_vec(arma::mat &A) {
    stdvecvec V(A.n_rows);
    for (size_t i = 0; i < A.n_rows; ++i) {
        V[i] = arma::conv_to< stdvec >::from(A.row(i));
    };
    return V;
}

mat std_vec_to_HH_mat(vector< vector<double> > std_vec_array){

    vector<double> std_vec_array_flat;
    for (size_t i = 0; i < std_vec_array.size(); i++) 
        {
        vector<double> el = std_vec_array[i];
        for (size_t j=0; j < el.size(); j++) {
            std_vec_array_flat.push_back(el[j]);
        }
    }
    mat col_vec(std_vec_array_flat);
    mat mat_from_vec_t = reshape(col_vec,30,30);
    mat mat_from_vec = mat_from_vec_t.t();
    return mat_from_vec;
}

mat std_vec_to_future_mat(vector< vector<double> > std_vec_array){

    vector<double> std_vec_array_flat;
    for (size_t i = 0; i < std_vec_array.size(); i++) 
        {
        vector<double> el = std_vec_array[i];
        for (size_t j=0; j < el.size(); j++) {
            std_vec_array_flat.push_back(el[j]);
        }
    }
    mat col_vec(std_vec_array_flat);
    mat mat_from_vec_t = reshape(col_vec,3,std_vec_array.size());
    mat mat_from_vec = mat_from_vec_t.t();
    return mat_from_vec;
}

//Crude statistical model, implemented locally.

double uniformRandom() {
  return ( (double)(rand()) + 1. )/( (double)(RAND_MAX));
}

//The Monte Carlo "muscle." All SQL based functions are abstracted outside this loop
//so other more "user friendly" languages can transmit information to this loop.
mat mcss_function(mat mat_head_to_head, mat future_games, stdteamvec list_of_teams){

    //Random info
    srand(time(NULL));

    //Two vectors for holding key information to be used later
    vector<Team> teams;

    // Matrix examples.
    mat MCSS_Head_To_Head = zeros<mat>(30,30);
    mat Sim_Total = zeros<mat>(30,30);
    mat debug_total = zeros<mat>(30,30);
    mat sim_playoff_total = zeros<mat>(30,4); // [Top 8, Wins, Top 6, PIT]  For the 2021 season, a third column of "Play in odds" will be added.
    mat error_matrix = ones<mat>(1,1);

    mat Head_To_Head = mat_head_to_head;
    //Debug Print - cout << Head_To_Head << endl;

    teams = list_of_teams;
    size_t const half_size=teams.size()/2;

    //Debug Print - cout << future_games << endl;
    int num_future_games = future_games.n_rows;
    for(int x_iter=0;x_iter<MAX_ITER;x_iter++){
    /* S5 - Monte Carlo Simulation */
        //set mcss head to head matrix to zero
        MCSS_Head_To_Head.zeros();
        for(int i=0;i<num_future_games;i++)
        {
            int away_team_id = future_games.row(i)[0]-1;
            int home_team_id = future_games.row(i)[1]-1;

            if (uniformRandom()<future_games.row(i)[2])
                MCSS_Head_To_Head.row(home_team_id)[away_team_id]++;
            else
                MCSS_Head_To_Head.row(away_team_id)[home_team_id]++;
        }

        debug_total.zeros();
        debug_total = MCSS_Head_To_Head+Head_To_Head;

        /*
        cout << "Head to Head" << endl;
        cout << Head_To_Head << endl;
        cout << "MCSS Head to Head" << endl;
        cout << MCSS_Head_To_Head << endl;
        */

        //Calculate raw wins - only concerned with that now (can implement tie breaking functionality later)
        mat total_wins = sum(debug_total.t());

        for(int i=0;i<30;i++){
            sim_playoff_total.row(i)[1] = sim_playoff_total.row(i)[1] +  total_wins[i];
            //cout << sim_playoff_total.row(i)[2] << endl;
        }
        //Create a copy of the teams list, only defined in the scope of this loop
        vector<Team> sim_teams = teams;

        //Round all wins
        for(int i=0;i<30;i++){
            sim_teams[i].set_total_wins(round(total_wins[i]));
        }

        random_shuffle(sim_teams.begin(),sim_teams.end());
	sort(sim_teams.begin(),sim_teams.end(),teams_sort());

        //Create conference based vectors. 
        vector<Team>::const_iterator first = sim_teams.begin();
        vector<Team>::const_iterator mid = sim_teams.begin() + half_size;
        vector<Team>::const_iterator last = sim_teams.end();
        vector<Team> east_conf(first,mid);
        vector<Team> west_conf(mid+1,last); //When you split, you need to start one more entry over.

       //iterate through list of teams to determine division winners.
        for(int i=0;i<30;i++){
            string team_name = sim_teams[i].get_full_team_name();
            string team_division = sim_teams[i].get_division();
            int team_id = sim_teams[i].get_team_id();
            //cout << team_name << ":" << team_division << ":" << total_wins << "\n" << endl;
	    //Play-in is now a new designation, for the teams finishing 7-10 in each conf.
            if( ((i >= 0) && (i <= 7)) || ((i >= 15) && (i <= 22))){
                sim_playoff_total.row(team_id-1)[0]++; //top 8 (legacy format)
            }
            if( ((i >= 0) && (i <= 5)) || ((i >= 15) && (i <= 20))){
            		sim_playoff_total.row(team_id-1)[2]++; //top 6
    	    }
    	    if( ((i >= 6) && (i <= 9)) || ((i >= 21) && (i <= 24))){
            		sim_playoff_total.row(team_id-1)[3]++; //play in tournament
    	    }
        }
    }

    for(int i=0;i<30;i++){
        sim_playoff_total.row(i)[0] = sim_playoff_total.row(i)[0]/MAX_ITER;
        sim_playoff_total.row(i)[1] = sim_playoff_total.row(i)[1]/MAX_ITER;
        sim_playoff_total.row(i)[2] = sim_playoff_total.row(i)[2]/MAX_ITER;
        sim_playoff_total.row(i)[3] = sim_playoff_total.row(i)[3]/MAX_ITER;
    }

    cout << MAX_ITER << " simulations complete." << endl; //--not necessary.
    return sim_playoff_total;
}

//only require this instantiation as we are only using the vanilla analysis tool
template void print_matrix<arma::mat>(arma::mat matrix);

stdvecvec simulations_result_vectorized(stdvecvec head_to_head_list_python, stdvecvec future_games_list_python, stdteamvec teams_list_python){
    mat head_to_head_mat = std_vec_to_HH_mat(head_to_head_list_python);
    mat future_mat = std_vec_to_future_mat(future_games_list_python);
    stdteamvec teams = teams_list_python; 
    //cout << future_mat << endl;
    mat sim_results = mcss_function(head_to_head_mat,future_mat,teams);
    return mat_to_std_vec(sim_results);
}


//C++ Printing and processing function.
int main()
{

return 0;
}
