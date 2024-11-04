create table
  public.users (
    user_id bigint generated by default as identity not null,
    created_at timestamp with time zone not null default now(),
    username text not null,
    email text not null,
    password text not null,
    constraint Users_pkey primary key (user_id),
    constraint Users_email_key unique (email),
    constraint Users_username_key unique (username)
  ) tablespace pg_default;


create table
  public.profile_info (
    user_id bigint generated by default as identity not null,
    level text not null default ''::text,
    about_me text not null default ''::text,
    logged_in boolean not null default false,
    constraint profile_info_pkey primary key (user_id)
  ) tablespace pg_default;
