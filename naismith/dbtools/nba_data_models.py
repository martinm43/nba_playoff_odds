from peewee import *

database = SqliteDatabase('nba_data.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class BballrefAvgPtsDiff(BaseModel):
    game = IntegerField(db_column='game_id', null=True)
    p_diff = FloatField(null=True)
    season = IntegerField(null=True)
    team = IntegerField(db_column='team_id', null=True)

    class Meta:
        db_table = 'bballref_avg_pts_diff'

class BballrefRest(BaseModel):
    away_streak = FloatField(null=True)
    datetime = FloatField(null=True)
    game = IntegerField(db_column='game_id', null=True)
    is_away = IntegerField(null=True)
    resttime = FloatField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    season_year = IntegerField(null=True)

    class Meta:
        db_table = 'bballref_rest'

class BballrefScores(BaseModel):
    notes = TextField(db_column='Notes', null=True)
    ot = TextField(db_column='OT', null=True)
    away_pts = IntegerField(null=True)
    away_team = TextField(null=True)
    away_team_id = IntegerField(null=True)
    box_score = TextField(null=True)
    date = TextField(null=True)
    datetime = FloatField(null=True)
    home_pts = IntegerField(null=True)
    home_team = TextField(null=True)
    home_team_id = IntegerField(null=True)
    season_year = IntegerField(null=True)
    start_time = TextField(null=True)

    class Meta:
        db_table = 'bballref_scores'

class NbaPyApiData(BaseModel):
    game_date_est = TextField(db_column='GAME_DATE_EST', null=True)
    away_ast = IntegerField(db_column='away_AST', null=True)
    away_fg3_pct = FloatField(db_column='away_FG3_PCT', null=True)
    away_fg_pct = FloatField(db_column='away_FG_PCT', null=True)
    away_ft_pct = FloatField(db_column='away_FT_PCT', null=True)
    away_game_sequence = IntegerField(db_column='away_GAME_SEQUENCE', null=True)
    away_pts = IntegerField(db_column='away_PTS', null=True)
    away_pts_ot1 = IntegerField(db_column='away_PTS_OT1', null=True)
    away_pts_ot10 = IntegerField(db_column='away_PTS_OT10', null=True)
    away_pts_ot2 = IntegerField(db_column='away_PTS_OT2', null=True)
    away_pts_ot3 = IntegerField(db_column='away_PTS_OT3', null=True)
    away_pts_ot4 = IntegerField(db_column='away_PTS_OT4', null=True)
    away_pts_ot5 = IntegerField(db_column='away_PTS_OT5', null=True)
    away_pts_ot6 = IntegerField(db_column='away_PTS_OT6', null=True)
    away_pts_ot7 = IntegerField(db_column='away_PTS_OT7', null=True)
    away_pts_ot8 = IntegerField(db_column='away_PTS_OT8', null=True)
    away_pts_ot9 = IntegerField(db_column='away_PTS_OT9', null=True)
    away_pts_qtr1 = IntegerField(db_column='away_PTS_QTR1', null=True)
    away_pts_qtr2 = IntegerField(db_column='away_PTS_QTR2', null=True)
    away_pts_qtr3 = IntegerField(db_column='away_PTS_QTR3', null=True)
    away_pts_qtr4 = IntegerField(db_column='away_PTS_QTR4', null=True)
    away_reb = IntegerField(db_column='away_REB', null=True)
    away_team_abbreviation = TextField(db_column='away_TEAM_ABBREVIATION', null=True)
    away_team_city_name = TextField(db_column='away_TEAM_CITY_NAME', null=True)
    away_team = IntegerField(db_column='away_TEAM_ID', null=True)
    away_team_wins_losses = TextField(db_column='away_TEAM_WINS_LOSSES', null=True)
    away_tov = IntegerField(db_column='away_TOV', null=True)
    away_standard = IntegerField(db_column='away_standard_id', null=True)
    day_datetime = FloatField(null=True)
    full_date = TextField(null=True)
    home_ast = IntegerField(db_column='home_AST', null=True)
    home_fg3_pct = FloatField(db_column='home_FG3_PCT', null=True)
    home_fg_pct = FloatField(db_column='home_FG_PCT', null=True)
    home_ft_pct = FloatField(db_column='home_FT_PCT', null=True)
    home_game_sequence = IntegerField(db_column='home_GAME_SEQUENCE', null=True)
    home_pts = IntegerField(db_column='home_PTS', null=True)
    home_pts_ot1 = IntegerField(db_column='home_PTS_OT1', null=True)
    home_pts_ot10 = IntegerField(db_column='home_PTS_OT10', null=True)
    home_pts_ot2 = IntegerField(db_column='home_PTS_OT2', null=True)
    home_pts_ot3 = IntegerField(db_column='home_PTS_OT3', null=True)
    home_pts_ot4 = IntegerField(db_column='home_PTS_OT4', null=True)
    home_pts_ot5 = IntegerField(db_column='home_PTS_OT5', null=True)
    home_pts_ot6 = IntegerField(db_column='home_PTS_OT6', null=True)
    home_pts_ot7 = IntegerField(db_column='home_PTS_OT7', null=True)
    home_pts_ot8 = IntegerField(db_column='home_PTS_OT8', null=True)
    home_pts_ot9 = IntegerField(db_column='home_PTS_OT9', null=True)
    home_pts_qtr1 = IntegerField(db_column='home_PTS_QTR1', null=True)
    home_pts_qtr2 = IntegerField(db_column='home_PTS_QTR2', null=True)
    home_pts_qtr3 = IntegerField(db_column='home_PTS_QTR3', null=True)
    home_pts_qtr4 = IntegerField(db_column='home_PTS_QTR4', null=True)
    home_reb = IntegerField(db_column='home_REB', null=True)
    home_team_abbreviation = TextField(db_column='home_TEAM_ABBREVIATION', null=True)
    home_team_city_name = TextField(db_column='home_TEAM_CITY_NAME', null=True)
    home_team = IntegerField(db_column='home_TEAM_ID', null=True)
    home_team_wins_losses = TextField(db_column='home_TEAM_WINS_LOSSES', null=True)
    home_tov = IntegerField(db_column='home_TOV', null=True)
    home_standard = IntegerField(db_column='home_standard_id', null=True)

    class Meta:
        db_table = 'nba_py_api_data'

class ProApiGames(BaseModel):
    away = IntegerField(db_column='away_id', null=True)
    away_score = IntegerField(null=True)
    bballref_away = IntegerField(db_column='bballref_away_id', null=True)
    bballref_home = IntegerField(db_column='bballref_home_id', null=True)
    bbr = IntegerField(db_column='bbr_id', null=True)
    date = IntegerField(null=True)
    game = IntegerField(db_column='game_id', null=True)
    home = IntegerField(db_column='home_id', null=True)
    home_score = IntegerField(null=True)
    pld = IntegerField(db_column='pld_id', null=True)
    season = TextField(null=True)

    class Meta:
        db_table = 'pro_api_games'

class ProApiTeams(BaseModel):
    abbreviation = TextField(null=True)
    bball_ref = IntegerField(db_column='bball_ref_id', null=True)  # 
    city = TextField(null=True)
    conf_or_league = TextField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    team_name = TextField(null=True)

    class Meta:
        db_table = 'pro_api_teams'

class ProTeamAdvStats(BaseModel):
    ast_pct = FloatField(null=True)
    ast_ratio = FloatField(null=True)
    ast_tov = FloatField(null=True)
    def_rating = FloatField(null=True)
    dreb_pct = FloatField(null=True)
    efg_pct = FloatField(null=True)
    game = IntegerField(db_column='game_id', null=True)
    min = TextField(null=True)
    off_rating = FloatField(null=True)
    opponent = IntegerField(db_column='opponent_id', null=True)
    oreb_pct = FloatField(null=True)
    pace = FloatField(null=True)
    period = TextField(null=True)
    pie = FloatField(null=True)
    season = IntegerField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    tm_tov_pct = FloatField(null=True)
    treb_pct = FloatField(null=True)
    ts_pct = FloatField(null=True)
    usg_pct = FloatField(null=True)

    class Meta:
        db_table = 'pro_team_adv_stats'

class ProlineData(BaseModel):
    away_1st = IntegerField(null=True)
    away_2nd = IntegerField(null=True)
    away_3rd = IntegerField(null=True)
    away_4th = IntegerField(null=True)
    away_ot_pts = IntegerField(db_column='away_OT_pts', null=True)
    away_pts = IntegerField(null=True)
    away_team = TextField(null=True)
    away_team_id = IntegerField(null=True)
    away_v_money_line = FloatField(null=True)
    away_v_ou = FloatField(null=True)
    away_v_pts_money = FloatField(null=True)
    away_v_pts_sprd = FloatField(null=True)
    date = TextField(null=True)
    home_1st = IntegerField(null=True)
    home_2nd = IntegerField(null=True)
    home_3rd = IntegerField(null=True)
    home_4th = IntegerField(null=True)
    home_ot_pts = IntegerField(db_column='home_OT_pts', null=True)
    home_pts = IntegerField(null=True)
    home_team = TextField(null=True)
    home_team_id = IntegerField(null=True)
    home_v_money_line = FloatField(null=True)
    home_v_ou = FloatField(null=True)
    home_v_pts_money = FloatField(null=True)
    home_v_pts_sprd = FloatField(null=True)
    home_v_total = FloatField(null=True)
    season = IntegerField(null=True)
    time_of_day = TextField(null=True)
    unix_date = FloatField(null=True)

    class Meta:
        db_table = 'proline_data'

