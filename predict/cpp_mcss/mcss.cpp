
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

mat return_head_to_head(){

    sqlite3 *db;
    int rc;
    string DatabaseName("mlb_data.sqlite");
    mat error_matrix = ones<mat>(1,1);
    mat Head_To_Head = zeros<mat>(30,30);


    /* S1 - GETTING LIST OF KNOWN WINS */
    string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE scheduled_date <= datetime('now','-1 day');");

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

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        int away_team_id = sqlite3_column_int(stmt,0);
        int away_runs = sqlite3_column_int(stmt,1);
        int home_team_id = sqlite3_column_int(stmt,2);
        int home_runs = sqlite3_column_int(stmt,3);
        if (home_runs > away_runs)
            Head_To_Head.row(home_team_id-1)[away_team_id-1]++;
        else
            Head_To_Head.row(away_team_id-1)[home_team_id-1]++;
    }

    cout << "Games successfully entered" << endl;

    return Head_To_Head;
}

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
    mat sim_playoff_total = zeros<mat>(30,3);
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
            sim_playoff_total.row(i)[2] = sim_playoff_total.row(i)[2] +  total_wins[i];
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
        vector<Team> amer_league(first,mid);
        vector<Team> nat_league(mid+1,last); //When you split, you need to start one more entry over.

        //American League Wildcard Teams
        vector<Team>::const_iterator amer_league_ac_first = amer_league.begin()+1;
        vector<Team>::const_iterator amer_league_ac_end = amer_league.begin()+4;
        vector<Team> amer_league_wc(amer_league_ac_first,amer_league_ac_end);
        amer_league_wc.insert(amer_league_wc.end(),amer_league.begin()+6,amer_league.begin()+9);
        amer_league_wc.insert(amer_league_wc.end(),amer_league.begin()+11,amer_league.begin()+14);

        //Sort then print - TO DO: convert to a generic struct don't use the name struct
        sort(amer_league_wc.begin(),amer_league_wc.end(),wins_sort());
        for(vector<Team>::iterator it = amer_league_wc.begin(); it != amer_league_wc.end(); ++it){
                string team_name = (*it).get_mlbgames_name();
        }

        //National League Wildcard Teams
        vector<Team>::const_iterator nat_league_ac_first = nat_league.begin()+1;
        vector<Team>::const_iterator nat_league_ac_end = nat_league.begin()+4;
        vector<Team> nat_league_wc(nat_league_ac_first,nat_league_ac_end);
        nat_league_wc.insert(nat_league_wc.end(),nat_league.begin()+6,nat_league.begin()+9);
        nat_league_wc.insert(nat_league_wc.end(),nat_league.begin()+11,nat_league.begin()+14);

        //Sort then print - TO DO: convert to a generic struct don't use the name struct
        sort(nat_league_wc.begin(),nat_league_wc.end(),wins_sort());
        for(vector<Team>::iterator it = nat_league_wc.begin(); it != nat_league_wc.end(); ++it){
                string team_name = (*it).get_mlbgames_name();
        }

        for(int i=0;i<2;i++){
                int al_wc_team_id = amer_league_wc[i].get_team_id();
                int nl_wc_team_id = nat_league_wc[i].get_team_id();
                sim_playoff_total.row(al_wc_team_id-1)[1]++;
                sim_playoff_total.row(nl_wc_team_id-1)[1]++;
        }


       //iterate through list of teams to determine division winners.
        for(int i=0;i<30;i++){
            string team_name = sim_teams[i].get_mlbgames_name();
            string team_division = sim_teams[i].get_division();
            int team_id = sim_teams[i].get_team_id();

            if( (i == 0) || (i == 5) || (i == 10) || (i == 15) | (i == 20) | (i == 25)){
                sim_playoff_total.row(team_id-1)[0]++;
            }
            /* need to sort the teams that aren't leaders in each league
                so 1-4,6-9,11-14 */

        }
    }

    for(int i=0;i<30;i++){
        sim_playoff_total.row(i)[0] = sim_playoff_total.row(i)[0]/MAX_ITER;
        sim_playoff_total.row(i)[1] = sim_playoff_total.row(i)[1]/MAX_ITER;
        sim_playoff_total.row(i)[2] = sim_playoff_total.row(i)[2]/MAX_ITER;
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

    sqlite3 *db;
    int rc;
    string SQLStatement;
    string DatabaseName("mlb_data.sqlite");
    sqlite3_stmt *stmt;

    cout << "running main" << endl;
    stdteamvec teams;

    mat head_to_head_results;
    head_to_head_results = return_head_to_head();
    mat future_games;
    future_games = return_future_games();
    mat simulation_results;
    teams = return_league_teams();
    simulation_results = mcss_function(head_to_head_results,future_games,teams);
    
    /* S2 - GETTING THE TEAMS AND THEIR MOST RECENT RATINGS */

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return 1;
    }
    
    SQLStatement =  "select t.id,t.mlbgames_name,t.abbreviation,t.division,t.league,s.rating "
                    "from teams as t "
                    "inner join SRS_Ratings as s "
                    "on s.team_id=t.id "
                    "where s.rating <> 0 "
                    "and s.rating_date = (select rating_date from SRS_ratings "
                    "order by rating_date desc limit 1) "
                    "order by t.id asc ";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    for(int i=0;i<30;i++){
        float wild_card_odds = simulation_results.row(i)[1];
        float division_odds = simulation_results.row(i)[0];
        float playoff_odds = simulation_results.row(i)[0] + simulation_results.row(i)[1];
        teams[i].set_wild_card_odds(wild_card_odds);
        teams[i].set_division_odds(division_odds);
        teams[i].set_playoff_odds(playoff_odds);
        teams[i].set_total_wins(simulation_results.row(i)[2]);
    }


    sort(teams.begin(),teams.end(),teams_sort());


    //Heading printing.
    cout << left << setw(14) << "Division " << "|" 
         << left << setw(13) << " Team " << "|" 
         << left << setw(10) << " Average Wins " << "|"
         << left << setw(10) << " Wild Card Odds " << "|"
         << left << setw(10) << " Division Odds " << "|"
         << left << setw(10) << " Playoff Odds " << endl;

    int header_length = 90; //trial and error

    //Enumerating teams.
    for(int i=0;i<30;i++){
            if( (i == 0) || (i == 5) || (i == 10) || (i == 15) | (i == 20) | (i == 25)){
                for(int i=0;i<header_length;i++){
                cout<<"*";
                }
            cout<<endl;
            }
        //cout << teams[i].get_division() << endl;
        string team_division = teams[i].get_division();
        string team_name = teams[i].get_mlbgames_name();
        int team_wins = teams[i].get_total_wins();
        float wild_card_odds = teams[i].get_wild_card_odds();
        float division_odds = teams[i].get_division_odds();
        float playoff_odds = teams[i].get_playoff_odds();
        cout << left << setw(13) << team_division << " | " 
             << left << setw(11) << team_name << " | " 
             << right << setw(12) << team_wins << " | " 
             << fixed << setprecision(1) << right << setw(13) << wild_card_odds*100.0 << "%" << " | " 
             << fixed << setprecision(1) << right << setw(12) << division_odds*100.0 << "%" << " | " 
             << fixed << setprecision(1) << right << setw(11) << playoff_odds*100.0 << "%" << endl;
    }
    cout << endl;
    cout << "Total number of simulations: " << MAX_ITER << endl;

return 0;
}
