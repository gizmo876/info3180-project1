DROP TABLE IF EXISTS profiles;
CREATE TABLE profiles (
 userid varchar PRIMARY KEY,
 firstname VARCHAR(255) not null,
 lastname VARCHAR(255) not null,
 email VARCHAR(255) not null,
 location varchar(255)  not null,
 biography VARCHAR(255) not null,
 gender VARCHAR(255) not null,
 photo VARCHAR(255) not null,
 created_on VARCHAR(255) not null
);


create user "project1";
create database "formdatabase";
\password project1      testpass
 alter database formdatabase owner to project1;