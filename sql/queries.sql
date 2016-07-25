select round(odds), count(*) 
from race_details 
where finish_parsed=1 
group by round(odds) 
order by round(odds);

select t.name, round(odds) odds, count(*)
from race_details d
join race r on r.id = d.race_id
join track t on t.id = r.track_id
where finish_parsed=1 
group by t.name, round(odds) 
order by t.name, round(odds);


select t.name, count(*)
from race_details d
join race r on r.id = d.race_id
join track t on t.id = r.track_id
where finish_parsed=1 and odds > 3
group by t.name
order by t.name;


select round(odds), count(*) , ((count(*) * 1.0)/209.0) * 100
from race_details 
where finish_parsed=1 
group by round(odds) 
order by round(odds);