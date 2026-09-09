drop schema if exists world_demographics cascade;
create schema world_demographics;
set search_path to world_demographics;

create table country (
	country_id serial primary key,
	country_code char(2) not null,
    country_name varchar(100) not null,
    area_km2 int null
);

create table age (
	age_id serial primary key,
	age_range varchar(25) not null
);

create table demographics (
	demo_id serial primary key,
	year int not null,
	growth_rate numeric(10,2) null,
	population int null,
	yearly_births int null,
	yearly_deaths int null,
	natural_increase int null,
	net_migrants int null,
	net_migration_rate numeric(10,2) null,
	rate_natural_increase numeric(10,2) null,
	le_at_birth numeric(10,2) null,
	female_le_at_birth numeric(10,2) null,
	male_le_at_birth numeric(10,2) null,
	country_id int not null
		references country(country_id)
);

create table age_demographic (
	demographic_age_id serial primary key,
	demo_id int not null
		references demographics(demo_id),
	age_id int not null
		references age(age_id),
	births int null,
	fertility_rate numeric(10,2) null,
	unique (demo_id, age_id)
);