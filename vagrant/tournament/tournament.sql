-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- connect to tournament
\c tournament

-- used for removing warnings/errors when testing.
-- DROP VIEW IF EXISTS playerstandings;
-- DROP VIEW IF EXISTS playerwins;
-- DROP VIEW IF EXISTS playerlosses;
-- DROP TABLE IF EXISTS winners;
-- DROP TABLE IF EXISTS losers;
-- DROP TABLE IF EXISTS players;

CREATE TABLE IF NOT EXISTS players (
	id serial primary key,
	name text
);

CREATE TABLE IF NOT EXISTS winners (
	id serial primary key,
	winner serial references players(id)
);

CREATE TABLE IF NOT EXISTS losers (
	id serial primary key,
	loser serial references players(id)
);

CREATE VIEW playerwins AS
SELECT
	players.id as id,
	count(winners.winner) as wins
FROM
	players
LEFT JOIN
	winners
ON
	players.id = winners.winner
GROUP BY
	players.id
;
	
CREATE VIEW playerlosses AS
SELECT
	players.id as id,
	count(losers.loser) as losses
FROM
	players
LEFT JOIN
	losers
ON
	players.id = losers.loser
GROUP BY
	players.id
;

CREATE VIEW playerstandings AS
SELECT 
	*,
	playerwins.wins + playerlosses.losses as matches
FROM players
NATURAL JOIN playerwins
NATURAL JOIN playerlosses
ORDER BY wins DESC;

-- Quit
\q
