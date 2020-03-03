// User DB

CREATE TABLE "tweets"(
    "tweet_id" integer NOT NULL PRIMARY KEY, 
    "user_id" integer NOT NULL, 
    "likes" integer NOT NULL, 
    "retweets" integer NOT NULL, 
    "timestamp" timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);


create table user(
    timestamp,
    user_id,
    followers,
    following
)

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