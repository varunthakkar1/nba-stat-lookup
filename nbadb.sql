DROP DATABASE IF EXISTS nbadb;

CREATE DATABASE nbadb;
USE nbadb;

CREATE TABLE stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player_name VARCHAR(75),
    team VARCHAR(3),
    age INT,
    height FLOAT,
    weight FLOAT,
    college VARCHAR(75),
    country VARCHAR(30),
    draft_year INT,
    draft_round INT,
    draft_number INT,
    games_played INT,
    avg_pts FLOAT,
    avg_reb FLOAT,
    avg_asts FLOAT,
    net_rating FLOAT,
    oreb_pct FLOAT,
    dreb_pct FLOAT,
    true_shooting FLOAT,
    ast_pct FLOAT,
    season VARCHAR(10)
);