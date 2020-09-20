DROP TABLE IF EXISTS songs;
CREATE TABLE songs (songid integer PRIMARY KEY, song_public_id varchar(100) UNIQUE, title VARCHAR(100), artist VARCHAR(100), album VARCHAR(100), filename varchar(100) UNIQUE);
