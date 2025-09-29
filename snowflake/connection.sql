create warehouse pickleball_wh
with
    warehouse_size = 'xsmall'
    auto_suspend = 300
    auto_resume = true
    initially_suspended = true;

--creating the db
create database games_db;

create table games_data (
    game_id string,
    match_id string,
    game_nbr int,
    score_w int,
    score_l int,
    w_team_id string,
    l_team_id string,
    skill_lvl string,
    scoring_type string,
    ball_type string,
    dt_played date,
    skill_lvl_clean float,
    winner string,
    score_diff int   
)

--create new stage connecting to s3
create or replace stage my_s3_stage
URL=removed
CREDENTIALS=(AWS_KEY_ID=Removed AWS_SECRET_KEY=removed)

copy into games_data
from @my_s3_stage
FILE_FORMAT = (TYPE ='CSV' SKIP_HEADER = 1);
