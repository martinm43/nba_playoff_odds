
/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <iomanip>
#include <iostream>
#include <vector>
#include "sqlite3.h"
#include <string>
#include <math.h>
#include <armadillo>
#include "mcss.hpp"

#define MAX_ITER 50000

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

double SRS_regress(double rating_away, double rating_home)
{
    float m=0.15;
    float b=-0.15;
    return (double) 1.0/(1.0 + exp(-1*(m*(rating_home-rating_away)+b)));
}

//Functions accepting void (using raw SQL written by author)
//and returning matrices for mcss_function (the monte carlo simulation)

mat return_future_games(){

    sqlite3 *db;
    int rc;
    string DatabaseName("mlb_data.sqlite");
    mat error_matrix = ones<mat>(1,1);
    mat Head_To_Head = zeros<mat>(30,30);


    /* S1 - GETTING LIST OF KNOWN WINS */
    string SQLStatement;

    SQLStatement =  "select count(*) from "
                    "games as g inner join srs_ratings as ra on "
                    "ra.team_id=g.away_team inner join srs_ratings as rh on "
                    "rh.team_id=g.home_team where g.scheduled_date >= datetime('now') "
                    "and ra.rating_date = (select max(rating_date) from srs_ratings) "
                    "and rh.rating_date = (select max(rating_date) from srs_ratings);";

    sqlite3_stmt *stmt;

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return error_matrix;
    }
    
    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return error_matrix;
    }

    static int num_future_games;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

        num_future_games = sqlite3_column_int(stmt,0);
    }

    cout << "Number of games to predict: " << num_future_games << endl;

    mat future_games = zeros<mat>(num_future_games,3);


    SQLStatement =  "select g.away_team, ra.rating, g.home_team, rh.rating from "
                    "games as g inner join srs_ratings as ra on "
                    "ra.team_id=g.away_team inner join srs_ratings as rh on "
                    "rh.team_id=g.home_team where g.scheduled_date >= datetime('now') "
                    "and ra.rating_date = (select max(rating_date) from srs_ratings) "
                    "and rh.rating_date = (select max(rating_date) from srs_ratings) "
                    "order by g.id asc";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return error_matrix;
    }

    int future_games_row = 0;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

         //Debug print to screen - example (away team, away rtg, home team, home rtg)
         future_games.row(future_games_row)[0] = sqlite3_column_int(stmt,0);
         future_games.row(future_games_row)[1] = sqlite3_column_int(stmt,2);

         double away_team_rtg = sqlite3_column_double(stmt,1);
         double home_team_rtg = sqlite3_column_double(stmt,3);

         future_games.row(future_games_row)[2] = SRS_regress(away_team_rtg,home_team_rtg);
         /*
            TO DO: Add the actual calculation of the binomial win odds to the array. It may not be 
            possible within ihis loop, in order to allow for debugging against its Python counterpart.
            Be careful! Also you'll have to expand the array/perform additional downstream calculations - MAM
         */
         future_games_row++;
         //cout << future_games_row << endl;
    }

    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Processing of future games' binomial win probabilities is complete." << endl;
    }
    
    //cout << future_games << endl;
    return future_games;
}

stdteamvec return_league_teams(){

    stdteamvec list_of_teams;

    stdteamvec error_team_list;
    Team error_team(-1,"ERROR","ERROR","ERROR","ERROR",-99);
    error_team_list.push_back(error_team);

    sqlite3 *db;
    int rc;
    string DatabaseName("mlb_data.sqlite");

    /* S1 - GETTING LIST OF KNOWN WINS */
    string SQLStatement;

    SQLStatement = "select t.id,t.mlbgames_name,t.abbreviation,t.division,t.league,s.rating "
                    "from teams as t "
                    "inner join SRS_Ratings as s "
                    "on s.team_id=t.id "
                    "where s.rating <> 0 "
                    "and s.rating_date = (select rating_date from SRS_ratings "
                    "order by rating_date desc limit 1) "
                    "order by t.id asc ";

    sqlite3_stmt *stmt;

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return error_team_list;
    }
    
    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return error_team_list;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {

        int team_id = sqlite3_column_int(stmt,0);
        string mlbgames_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,1)));
        string abbreviation = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,2)));
        string division = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,3)));
        string league = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,4)));
        float rating = sqlite3_column_double(stmt,5);
        list_of_teams.push_back(Team(team_id,mlbgames_name,abbreviation,division,league,rating));
   
    }

    cout << "Games successfully entered" << endl;
    return list_of_teams;
}

//The Monte Carlo "muscle." All SQL based functions are abstracted outside this loop
//so other more "user friendly" languages can transmit information to this loop.
mat mcss_function(mat mat_head_to_head, mat future_games, stdteamvec list_of_teams){

    sqlite3 *db;
    int rc;

    //Random info
    srand(time(NULL));

    //Two vectors for holding key information to be used later
    vector<Team> teams;

    // Matrix examples.
    mat MCSS_Head_To_Head = zeros<mat>(30,30);
    mat Sim_Total = zeros<mat>(30,30);
    mat debug_total = zeros<mat>(30,30);
    mat sim_playoff_total = zeros<mat>(30,2); // [Wins, Playoff Odds], other columns can be added later.
    mat error_matrix = ones<mat>(1,1);

    mat Head_To_Head = mat_head_to_head;
    //cout << Head_To_Head << endl;

    //Name of the database
    string DatabaseName("mlb_data.sqlite");


    /* S1 - GETTING LIST OF KNOWN WINS*/

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return error_matrix;
    }

    teams = list_of_teams;
    size_t const half_size=teams.size()/2;

    


    //cout << future_games << endl;
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

        sort(sim_teams.begin(),sim_teams.end(),teams_sort());

        //Create american league and national league vectors.
        vector<Team>::const_iterator first = sim_teams.begin();
        vector<Team>::const_iterator mid = sim_teams.begin() + half_size;
        vector<Team>::const_iterator last = sim_teams.end();
        vector<Team> east_conf(first,mid);
        vector<Team> west_conf(mid+1,last); //When you split, you need to start one more entry over.

       //iterate through list of teams to determine division winners.
        for(int i=0;i<30;i++){
            string team_name = sim_teams[i].get_mlbgames_name();
            string team_division = sim_teams[i].get_division();
            int team_id = sim_teams[i].get_team_id();
            int total_wins = sim_teams[i].get_total_wins();
            //cout << team_name << ":" << team_division << ":" << total_wins << endl;
            if( ((i >= 0) && (i <= 7)) || ((i >= 15) && (i <= 22))){
                sim_playoff_total.row(team_id-1)[0]++;
            }
            /* need to sort the teams that aren't leaders in each league
                so 1-4,6-9,11-14 */

        }
    }

    for(int i=0;i<30;i++){
        sim_playoff_total.row(i)[0] = sim_playoff_total.row(i)[0]/MAX_ITER;
        sim_playoff_total.row(i)[1] = sim_playoff_total.row(i)[1]/MAX_ITER;
    }

    cout << MAX_ITER << " simulations complete." << endl;
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
