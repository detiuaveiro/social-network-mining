// User DB

create table tweets(
    timestamp,
    tweet_id,
    user_id,
    likes,
    retweets
)

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
    API_type choice("Twitter","Instagram"),
    filter choice("Keywords","Username"),
    name string,
    tags String[],
    bots Integer[],
    active boolean
)


