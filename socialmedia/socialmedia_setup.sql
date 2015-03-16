/*
 *   The script file is used to create the list of all tables
 *   for the socialmedia information system.
 *
 *   We shall first drop all the tables just in case if they were created.
 *
 */

DROP TABLE main_authors;
DROP TABLE main_posts;
DROP TABLE main_comments;
DROP TABLE main_friends;
DROP TABLE main_follows;

CREATE TABLE main_authors (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    host varchar(32) NOT NULL,
    displayname varchar(32) UNIQUE NOT NULL,
    password varchar(32) NOT NULL,
    github varchar(40),
    url varchar(257),
    approved_flag int,
    guid varchar(32) UNIQUE
);

CREATE TABLE main_comments (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    author varchar(32) NOT NULL,
    comments varchar(512),
    pubDate Date,
    guid varchar(32) UNIQUE
);

CREATE TABLE main_posts (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    title varchar(100),
    source varchar(256),
    origin varchar(256),
    description varchar(256),
    content_type varchar(256),
    content varchar(512),
    author main_authors,
    categories varchar(32),
    comments main_comments,
    pubDate Date,
    visibility varchar(16),
    guid varchar(32) UNIQUE
);

CREATE TABLE main_friends (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    authorguid1 varchar(32) NOT NULL,
    authorguid2 varchar(32) NOT NULL,
    accepted varchar(8) NOT NULL
);

   
CREATE TABLE main_follows (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    authorguid1 varchar(32) NOT NULL,
    authorguid2 varchar(32) NOT NULL
);

