CREATE OR REPLACE FUNCTION usp_parse_race_detail(
	i_race_id BIGINT
)
RETURNS TABLE(
	status_id INT,
	status_text TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
	_arr TEXT;
	_col TEXT;
	_odds NUMERIC(10,2);
	_col_count INT;
	_col_start INT;
	_race_number INT;
	_race_line BOOLEAN;
	_result_line BOOLEAN;
BEGIN

	_col_count = 0;
	SELECT COALESCE(MAX(race_number), 1)
	  INTO _race_number
	  FROM race_details
	 WHERE race_id = i_race_id;

	FOR _arr IN 
		SELECT regexp_split_to_table(details, E'\n')
		  FROM race 
		 WHERE id = COALESCE(i_race_id, id)
	LOOP

		RAISE NOTICE 'race_id: %, race_number: %',i_race_id, _race_number;
    	IF _arr LIKE '%Temperature: %' THEN
    		_race_line = FALSE;
    		_result_line = TRUE;
    		_race_number = _race_number + 1;
    	END IF;
    	IF _race_line THEN
			INSERT INTO race_details (race_id, race_number, 
				horse_number, horse,hv, pp, quarter, half,
				thirdq, stretch, finish, finish_parsed, time, lastq, driver,
				odds, trainer)
			SELECT i_race_id, _race_number, 
				TRIM(substring(_arr FROM 0 FOR 3))::INT,
				substring(_arr FROM 4 FOR 23),
				substring(_arr FROM 26 FOR 4),
				substring(_arr FROM 30 FOR 5),
				substring(_arr FROM 37 FOR 7),
				substring(_arr FROM 45 FOR 7),
				substring(_arr FROM 53 FOR 7),
				substring(_arr FROM 61 FOR 7),
				substring(_arr FROM 70 FOR 8),
				substring(split_part(substring(_arr FROM 70 FOR 8), '/', 1) FROM '[0-9]+')::INT,
				substring(_arr FROM 81 FOR 8),
				substring(_arr FROM 89 FOR 5),
				substring(_arr FROM 94 FOR 15),
				CASE WHEN 
				REPLACE(REPLACE(REPLACE(TRIM(substring(
					_arr FROM 109 FOR 8)), '*',''), 'N', ''), 'R', '') = '' THEN NULL
				ELSE 
				REPLACE(REPLACE(REPLACE(TRIM(substring(
					_arr FROM 109 FOR 8)), '*',''), 'N', ''), 'R', '')::NUMERIC(10,2)
				END,
				substring(_arr FROM 118 FOR 12);

    	END IF;

    	IF _arr LIKE '%Trainer%' THEN
    		_race_line = TRUE;
    	END IF;

	END LOOP;

	RETURN QUERY
	SELECT 200, 'OK'::TEXT;
END;
$$;