// User DB

CREATE TABLE "tweets"(
    "tweet_id" numeric NOT NULL PRIMARY KEY, 
    "user_id" numeric NOT NULL, 
    "likes" integer NOT NULL, 
    "retweets" integer NOT NULL, 
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
insert into tweets values(831606548300517376, 6253282, 100, 2);


CREATE TABLE "users"(
    "user_id" numeric NOT NULL PRIMARY KEY, 
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    "followers" integer NOT NULL, 
    "following" integer NOT NULL
);

insert into users values(6253282, DEFAULT, 10000, 1234);



// Policies DB
create table logs(
    id_bot,
    timestamp,
    action
)

create table policies(
    id integer,
    API_type choice("Twitter", "Instagram"),
    filter choice("Keywords", "Username"),
    name string,
    tags String[],
    bots Integer[],
    active boolean
)