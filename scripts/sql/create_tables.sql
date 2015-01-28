set search_path to "banyan";

drop table local_apps;
create table if not exists local_apps (
        id serial primary key,
        app_name varchar(100) not null,
        app_path TEXT not null,
        created_at timestamp default current_timestamp,
        updated_at timestamp default current_timestamp
);

drop table local_files;
create table if not exists local_files (
        id serial primary key,
        file_name varchar(100) not null,
        file_path TEXT not null,
        created_at timestamp default current_timestamp,
        updated_at timestamp default current_timestamp
);

drop table daily_forecasts;
create table if not exists daily_forecasts (
        id serial primary key,
        forecast_date DATE,
        forecast TEXT,
        latitude float,
        longitude float,
        timezone varchar(100),
        created_at timestamp default current_timestamp,
        updated_at timestamp default current_timestamp
);

select * from local_apps;