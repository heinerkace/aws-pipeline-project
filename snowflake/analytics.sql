--Split matches by team and show game history for each team
create temporary table win_loss_by_date as
with split_games as (
    select game_id, match_id, dt_played, score_diff, winner, w_team_id as team_id
    from games_data
    union all
    select game_id, match_id, dt_played, score_diff, winner, l_team_id as team_id
    from games_data
)
select
    team_id,
    dt_played,
    score_diff,
    case 
        when team_id = winner then 'win'
        else 'loss'
    end as match_outcome,
    row_number() over (partition by team_id order by dt_played) as game_history
from split_games
order by team_id, game_history;

------------------------------------------------------------------------------------

--Teams average point differentials win/loss counts
select
    team_id,
    sum(case when match_outcome = 'win' then 1 else 0 end) as total_wins,
    sum(case when match_outcome = 'loss' then 1 else 0 end) as total_losses,
    avg(score_diff)
from win_loss_by_date
group by team_id
order by total_wins desc;
