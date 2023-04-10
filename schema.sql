create table if not exists codes (
    id varchar primary key,
    title varchar,
    code_type varchar,
    valid_from integer,
    valid_to integer
);

create table if not exists history (
    email varchar,
    code varchar,
    date timestamp default current_timestamp,
    primary key (email, code)
);