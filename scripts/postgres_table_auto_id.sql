alter table logs add column id SERIAL;
alter table logs add PRIMARY KEY (id);
alter table policies add column id SERIAL;
alter table policies add PRIMARY KEY (id);
alter table tweets drop constraint tweets_pkey;
alter table tweets add column id SERIAL;
alter table tweets add PRIMARY KEY (id);
alter table users drop constraint users_pkey;
alter table users add column id SERIAL;
alter table users add PRIMARY KEY (id);