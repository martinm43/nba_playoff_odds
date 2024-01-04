#include <cmath>
#include <ctime>
#include <iostream>
#include <sqlite3.h>
#include <vector>
#include <Eigen/Dense> //NOLINT
#include <Eigen/Sparse>
#include <Eigen/SparseQR>
#include <Eigen/OrderingMethods>


//ORM
struct Game {
    int id;
    int home_team_id;
    int home_team_runs;
    int away_team_id;
    int away_team_runs;
    int year;
    double epochtime;
};

int selectDataCallback(void* data, int argc, char** argv, char** /*azColName*/) {
    std::vector<Game>* games = static_cast<std::vector<Game>*>(data);

    Game game;
    game.id = std::stoi(argv[0]);
    game.home_team_id = std::stoi(argv[1]);
    game.home_team_runs = std::stoi(argv[2]);
    game.away_team_id = std::stoi(argv[3]);
    game.away_team_runs = std::stoi(argv[4]);
    game.year = std::stoi(argv[5]);
    game.epochtime = std::stod(argv[6]);
    games->push_back(game);

    return 0;
}

struct Rating {
    int team_id;
    float srs_rating;
    int year;
    double epochtime;
};


int main() {
    sqlite3* db;
    char* errorMsg = nullptr;

    // Open a connection to the database
    int rc = sqlite3_open("nba_data.sqlite", &db);
    if (rc != SQLITE_OK) {
        std::cout << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return rc;
    }
    
    std::vector<Rating> ratings_history;

    int start_year = 1999;
    int end_year = 2024;

    // Set up times - start time.
    std::tm timeinfo = {}; // Initialize to all zeros
    for(int year = start_year;year<=end_year;year++){
        std::cout<<"Processing year "<<std::to_string(year)<<std::endl;
        timeinfo.tm_year = year - 1 - 1900; // Year since 1900 (2023)
        timeinfo.tm_mon = 9;           // Month (0-based index)
        timeinfo.tm_mday = 1;         // Day of the month
        std::time_t epochTime = std::mktime(&timeinfo); // Convert to epoch time

        // Set up times - end time for calculation.
        std::tm endtimeinfo = {}; // Initialize to all zeros
        endtimeinfo.tm_year = year - 1 - 1900; // Year since 1900 (2023)
        endtimeinfo.tm_mon = 10;           // Month (0-based index)
        endtimeinfo.tm_mday = 1;         // Day of the month
        std::time_t endepochTime = std::mktime(&endtimeinfo); // Convert to epoch time

        // Set up times - end time of year.
        std::tm yearendtimeinfo = {}; // Initialize to all zeros
        yearendtimeinfo.tm_year = year - 1900; // Year since 1900 (2023)
        yearendtimeinfo.tm_mon = 4;           // Month (August, 0-based index)
        yearendtimeinfo.tm_mday = 1;         // Day of the month
        std::time_t yearendepochTime = std::mktime(&yearendtimeinfo); // Convert to epoch time

        //moving necessary type declarations out of loop
        std::string selectquery;
        const char* selectDataQuery;
        std::vector<Game> games;
        const int numTeams = 30;
        int numDays=4;


        while(endepochTime < yearendepochTime) {
            // Alternatively use the current end time.
            //std::time_t endepochTime = std::time(nullptr); // Get the current epoch time
            
            //Debug print script for datetimes.
            //std::cout << "Epoch Time for "+std::to_string(year)+"-"+std::to_string(timeinfo.tm_mon)+"-"+std::to_string(timeinfo.tm_mday) <<": " << epochTime << std::endl;
            

            // Query the table
            selectquery = "SELECT id, home_team_id, home_pts, away_team_id, away_pts,"
            " season_year , datetime FROM bballref_scores where (datetime > "+std::to_string(epochTime)+" and datetime < "+std::to_string(endepochTime)+") and (home_pts > 0 or away_pts> 0)"; 
            selectDataQuery = selectquery.c_str(); 
    
            rc = sqlite3_exec(db, selectDataQuery, selectDataCallback, &games, &errorMsg);
            if (rc != SQLITE_OK) {
                std::cout << "SQL error: " << errorMsg << std::endl;
                sqlite3_free(errorMsg);
                sqlite3_close(db);
                return rc;
            }


            // Process the data
            
            // Multi year functionality
            // int processing_year = games[0].year;




            //const int numTeams = 30;


            //Dealing with seasons that started late
            int game_size_tol = 1; //originally 1 quarter of season
            if(games.size() < game_size_tol){
                endepochTime = endepochTime + 60*60*24*numDays;
                continue;
            }



            std::vector<std::vector<double> > M(numTeams, std::vector<double>(games.size(), 0.0));
            std::vector<double> S(games.size(),0.0);

            for (unsigned long col=0;col<games.size();col++) {
        
                double home, away, homescore, awayscore;
                home = games[col].home_team_id;
                away = games[col].away_team_id;
                homescore = games[col].home_team_runs;
                awayscore = games[col].away_team_runs;

                // In the csv data, teams are numbered starting at 1
                // So we let home-team advantage be 'team 0' in our matrix
                M[int(home) - 1][col] = 1.0;
                M[int(away) - 1][col] = -1.0;

                int diff_score = static_cast<int>(homescore) - static_cast<int>(awayscore);
                /* POTENTIAL FUTURE ADJUSTMENTS - MORE USEFUL IN BASKETBALL
                int max_MOV = 100;
                int win_floor = 0;

                if (diff_score > max_MOV) {
                    diff_score = static_cast<int>(max_MOV);
                } else if (diff_score < -max_MOV) {
                    diff_score = static_cast<int>(-max_MOV);
                }

                Granting a bonus based on "actually winning the game".
                This is intended to account for teams that can "win games when it counts".
                A crude adjustment for teams with significantly different talent levels from other teams.
                if (diff_score > 0) {  // bonuses for a win
                    diff_score = std::max(static_cast<int>(win_floor), diff_score);
                } else {  // demerits for a loss
                    diff_score = std::min(static_cast<int>(-win_floor), diff_score);
                }*/

                S[col] = diff_score;
            }

            //the matrix with all the game results is sparse
            //the matrix with all the actual point differentials is dense

            typedef Eigen::SparseMatrix<double> SparseMatrix;
            typedef Eigen::VectorXd DenseVector;
            
            SparseMatrix Mmatrix(numTeams, games.size()); // Convert 2D vector to Eigen matrix
            DenseVector Svector(games.size());     // Convert 1D vector to Eigen vector

            // Fill Eigen matrix and vector with data
            for (int i = 0; i < numTeams; ++i) {
                for (int j = 0; j < games.size(); ++j) {
                    if(M[i][j] != 0) {
                        Mmatrix.insert(i, j) = M[i][j];
                        }
                }
            }
            for (int j = 0; j < games.size(); ++j) {
                Svector(j) = S[j];
            }

            SparseMatrix MmatrixT = Mmatrix.transpose();
            Eigen::RowVectorXd SvectorT = Svector.transpose();
            

            //Debug print dimensions of matrices
            //std::cout << "MT is " << MmatrixT.rows() << " by " << MmatrixT.cols() << std::endl;
            //std::cout << "S is " << Svector.rows() << " by " << Svector.cols() << std::endl;

            Eigen::LeastSquaresConjugateGradient<SparseMatrix> solver1;
            int maxIterations = 25; //Accurate enough and doesn't give blow up solutions
            solver1.setMaxIterations(maxIterations); //known stable value
            solver1.compute(MmatrixT);
            if (solver1.info() != Eigen::Success) {
                // decomposition failed
                return -1;
            }

            DenseVector x1 = solver1.solve(Svector);
            //std::cout << "SRS results on epochtime: " << endepochTime << std::endl;
            //std::cout << "Solution using LeastSquaresConjugateGradient:\n";
            
            for (int i=0; i<x1.size(); i++){
            Rating rating;
            rating.team_id = i+1;
            rating.year = year;
            rating.epochtime = endepochTime;
            rating.srs_rating = x1[i];
            ratings_history.push_back(rating);
            //std::cout << rating.team_id << ": " << rating.srs_rating << "\n";
            }

            //std::cout<<"Completion. "<<std::endl;
        
            endepochTime = endepochTime + 60*60*24*numDays;
            //std::cout<<std::to_string(endepochTime)<<std::endl;
            //std::cout<<std::to_string(yearendepochTime)<<std::endl;
        }
    }
    std::cout << "total values calculated: " << ratings_history.size() << "\nBeginning insert now" << std::endl;

    //Delete existing table
    std::string deleteQuery = "DROP TABLE IF EXISTS SRS;";
    rc = sqlite3_exec(db, deleteQuery.c_str(), nullptr, nullptr, &errorMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "Error deleting table: " << errorMsg << std::endl;
        sqlite3_free(errorMsg);
        sqlite3_close(db);
        return 1;
    } else {
        std::cout << "Original SRS ratings table deleted successfully." << std::endl;
    }

    // Create the table again
    std::string createQuery = "CREATE TABLE SRS ("
                              "id INTEGER PRIMARY KEY, "
                              "team_id INTEGER, "
                              "srs_rating FLOATs, "
                              "epochtime REAL, "
                              "team_abbreviation STRING, "
                              "current_abbreviation STRING, "
                              "year INTEGER);";
    rc = sqlite3_exec(db, createQuery.c_str(), nullptr, nullptr, &errorMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "Error creating table: " << errorMsg << std::endl;
        sqlite3_free(errorMsg);
        sqlite3_close(db);
        return 1;
    } else {
        std::cout << "New blank ratings table created. Populating." << std::endl;
    }

    // Prepare the INSERT statement using INSERT INTO VALUES 
    std::string insertQuery = "INSERT INTO SRS (team_id, srs_rating, epochtime, year) VALUES (?, ?, ?, ?);";
    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, insertQuery.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Error preparing statement: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }


     rc = sqlite3_exec(db, "BEGIN TRANSACTION;", nullptr, nullptr, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Error beginning transaction: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // Bind and execute the INSERT statement for each Rating object in the ratings_history collection
    for (unsigned long i=0;i<ratings_history.size();i++) {
        Rating rating = ratings_history[i];
        sqlite3_bind_int(stmt, 1, rating.team_id);
        sqlite3_bind_double(stmt, 2, rating.srs_rating);
        sqlite3_bind_double(stmt, 3, rating.epochtime);
        sqlite3_bind_int(stmt, 4, rating.year);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Error executing statement: " << sqlite3_errmsg(db) << std::endl;
            sqlite3_close(db);
            return 1;
        }
        //std::cout<<i<<std::endl;
        sqlite3_reset(stmt);
    }

    // Commit the transaction
    rc = sqlite3_exec(db, "COMMIT;", nullptr, nullptr, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Error committing transaction: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // Finalize the statement and close the database connection
    sqlite3_finalize(stmt);

    //SQL statement for updating all team abbreviations
    std::string abbrev_update = "UPDATE SRS as r SET team_abbreviation = (SELECT abbreviation FROM pro_api_teams AS t WHERE r.team_id = t.bball_ref_id)";
    // Commit the transaction
    rc = sqlite3_exec(db, abbrev_update.c_str(), nullptr, nullptr, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Error updating associated abbreviations: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }


    // Close the database connection
    sqlite3_close(db);
    std::cout<<"Operations completed succesfully"<<std::endl;
    return 0;
}

