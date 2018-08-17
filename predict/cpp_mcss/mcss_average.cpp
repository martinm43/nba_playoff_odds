
/* Testing out SO code for CPP */
/* Reading values from the sqlite api into an array*/

#include <iomanip>
#include <fstream>
#include <iostream>
#include <vector>
#include <sqlite3.h>
#include <string>
#include <math.h>
#include <armadillo>
#include <mcss.h>
#include <ctime>

#define MAX_ITER 100000

using namespace std;
using namespace arma;

int main()
{
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    //Random info
    srand(time(NULL));

    //Two vectors for holding key information to be used later
    vector<Game> games;
    vector<Team> teams;

    // Matrix examples.
    mat Head_To_Head = zeros<mat>(30,30);
    mat MCSS_Head_To_Head = zeros<mat>(30,30);
    mat Sim_Total = zeros<mat>(30,30);
    mat debug_total = zeros<mat>(30,30);

    //Name of the database
    string DatabaseName("mlb_data.sqlite");

    /* S1 - GETTING LIST OF KNOWN WINS */
    string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE scheduled_date <= datetime('now','-1 day');");

    sqlite3_stmt *stmt;

    rc = sqlite3_open(DatabaseName.c_str(), &db);
    if( rc ){
     fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
     sqlite3_close(db);
     return(1);
    }
    
    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        //Writing out the games to the screen (temporary for now, just for error checking)
        //cout << "Away team id: " << sqlite3_column_int(stmt,0) << endl;
        //cout << "Away team runs scored: " << sqlite3_column_int(stmt,1) << endl;

        //Store in our vector
        int away_team_id = sqlite3_column_int(stmt,0);
        int away_runs = sqlite3_column_int(stmt,1);
        int home_team_id = sqlite3_column_int(stmt,2);
        int home_runs = sqlite3_column_int(stmt,3);
        games.push_back(Game(away_team_id,away_runs,home_team_id,home_runs));

        if (home_runs > away_runs)
            Head_To_Head.row(home_team_id-1)[away_team_id-1]++;
        else
            Head_To_Head.row(away_team_id-1)[home_team_id-1]++;
    }

    cout << "Games successfully entered" << endl;
    //cout << "Head to Head Matrix:" << endl;
    //cout << Head_To_Head << endl;

    /* S2 - GETTING THE TEAMS AND THEIR MOST RECENT RATINGS */

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

    while (sqlite3_step(stmt) == SQLITE_ROW) {

        //Write information into the vectors.
        int team_id = sqlite3_column_int(stmt,0);
        string mlbgames_name = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,1)));
        string abbreviation = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,2)));
        string division = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,3)));
        string league = string(reinterpret_cast<const char *>(sqlite3_column_text(stmt,4))); //does not capture whole division!!
        float rating = sqlite3_column_double(stmt,5);
        teams.push_back(Team(team_id,mlbgames_name,abbreviation,division,league,rating));
    }

    /* S3 - GETTING THE NUMBER OF FUTURE GAMES FOR S4 */

    SQLStatement =  "select count(*) from "
                    "games as g inner join srs_ratings as ra on "
                    "ra.team_id=g.away_team inner join srs_ratings as rh on "
                    "rh.team_id=g.home_team where g.scheduled_date >= datetime('now') "
                    "and ra.rating_date = (select max(rating_date) from srs_ratings) "
                    "and rh.rating_date = (select max(rating_date) from srs_ratings);";

    rc = sqlite3_prepare_v2(db, SQLStatement.c_str(),
                            -1, &stmt, NULL);

    if (rc != SQLITE_OK) {
        cerr << "SELECT failed: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return 1;
    }

    int num_future_games;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

        num_future_games = sqlite3_column_int(stmt,0);
    }

    cout << "Number of games to predict: " << num_future_games << endl;

    mat future_games = zeros<mat>(num_future_games,4);

    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Game processing is complete." << endl;
    }
    /* S3 - GETTING FUTURE GAMES AND THEIR ASSOCIATED RATINGS */

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
        return 1;
    }

    int future_games_row = 0;

    while (sqlite3_step(stmt) == SQLITE_ROW) {

         //Debug print to screen - example (away team, away rtg, home team, home rtg)
         future_games.row(future_games_row)[0] = sqlite3_column_int(stmt,0);
         future_games.row(future_games_row)[1] = sqlite3_column_double(stmt,1);
         future_games.row(future_games_row)[2] = sqlite3_column_int(stmt,2);
         future_games.row(future_games_row)[3] = sqlite3_column_double(stmt,3);
         future_games_row++;
         //cout << future_games_row << endl;
    }

    sqlite3_finalize(stmt);

    if (rc == SQLITE_OK) {
        cerr << "Processing of future games' binomial win probabilities is complete." << endl;
    }
    

    for(int x_iter=0;x_iter<MAX_ITER;x_iter++){
    /* S5 - Monte Carlo Simulation */
        //set mcss head to head matrix to zero
        MCSS_Head_To_Head.zeros();
        for(int i=0;i<num_future_games;i++)
        {
            int away_team_id = future_games.row(i)[0]-1;
            float away_team_rtg = future_games.row(i)[1];
            int home_team_id = future_games.row(i)[2]-1;
            float home_team_rtg = future_games.row(i)[3];

            //cout << away_team_id << endl;
            //cout << away_team_rtg << endl;
            //cout << home_team_id << endl;
            //cout << home_team_rtg << endl;

            if (uniformRandom()<SRS_regress(away_team_rtg,home_team_rtg))
                MCSS_Head_To_Head.row(home_team_id)[away_team_id]++;
            else
                MCSS_Head_To_Head.row(away_team_id)[home_team_id]++;
        }

        debug_total.zeros();
        debug_total = MCSS_Head_To_Head+Head_To_Head;
        Sim_Total += debug_total;
    }
        mat total_wins = sum(Sim_Total.t()/MAX_ITER);
        //cout << total_wins << endl;

    for(int i=0;i<30;i++){
        teams[i].set_total_wins(round(total_wins[i]));
    }

    /* S6 - Sorting and Printing */
    sort(teams.begin(),teams.end(),teams_sort());

    cout << "Printing a sorted list of teams, by average wins over " 
            << MAX_ITER << " simulations." << endl;

    //Heading printing
    cout << left << setw(14) << "Division" << "|" 
         << left << setw(12) << " Team" << "|" 
         << left << setw(3) << " Wins" << endl;

    cout<<"***********************************"<<endl;

    for(int i=0;i<30;i++){
        string team_name = teams[i].get_mlbgames_name();
        //cout << teams[i].get_division() << endl;
        string team_division = teams[i].get_division();
        int team_wins = teams[i].get_total_wins();
        cout << left << setw(13) << team_division << " | " 
             << left << setw(10) << team_name << " | " 
             << left << setw(3) << team_wins << endl;
    }

return 0;
}
