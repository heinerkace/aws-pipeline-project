
select * from games_data

select count(*) as total_rows, 
    avg(score_diff) as average_margin
from games_data;

select * from games_data limit 5;
    
select winner as winning_team, count(winner) as num_wins, skill_lvl_clean as skill_level
from games_data
where skill_lvl_clean > 4.5
group by winner, skill_lvl_clean
order by count(winner) desc;



--Rank teams by skill level
select
    w_team_id as team_id,
    skill_lvl_clean,
    dt_played,
    rank() over (partition by skill_lvl_clean order by dt_played) as skill_rank
from games_data

