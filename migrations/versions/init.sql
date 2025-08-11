BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- Running upgrade  -> 08f82a01da19

CREATE TABLE players (
    id UUID NOT NULL, 
    username VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (username)
);

CREATE TABLE matches (
    id UUID NOT NULL, 
    completed BOOLEAN NOT NULL, 
    winner_id UUID, 
    PRIMARY KEY (id), 
    FOREIGN KEY(winner_id) REFERENCES players (id)
);

CREATE TYPE choice AS ENUM ('UNKNOWN', 'ROCK', 'PAPER', 'SCISSORS', 'LIZARD', 'SPOCK');

CREATE TABLE player_matches (
    player_id UUID NOT NULL, 
    match_id UUID NOT NULL, 
    move choice NOT NULL, 
    PRIMARY KEY (player_id, match_id), 
    FOREIGN KEY(match_id) REFERENCES matches (id), 
    FOREIGN KEY(player_id) REFERENCES players (id)
);

INSERT INTO alembic_version (version_num) VALUES ('08f82a01da19') RETURNING alembic_version.version_num;

COMMIT;