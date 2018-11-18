SET SQL_SAFE_UPDATES = 0;
create database c3swebcom;

use c3swebcom;

drop table cs_users;

create table cs_users(
	id int not null auto_increment primary key,
	ccid int not null,
    name varchar(100) not null,
    password varchar(100),
    address varchar(500),
    ip_count int,
    expiry_date varchar(10),
    package varchar(100),
    phone varchar(100),
    mobile varchar(100),
    domain varchar(100),
    unique key(ccid,domain))engine=innoDb;

create table c3s_plans(
	id int not null auto_increment primary key,
    name varchar(30) not null,
    price float(6,2) not null default 0.00)engine=innoDb;
    
create table admin_users(
	id int not null auto_increment primary key,
    name varchar(50) not null unique,
    password varchar(100) not null,
    role enum("admin","operator") default "operator")engine=innoDb;
    
create table ip_table(
	id int not null auto_increment primary key,
    user_id int not null references cs_users(id),
    ip varchar(15) default "0.0.0.0",
    status enum('enabled','disabled') default "enabled")engine=innoDb;
    
drop table ip_table;

insert into admin_users(name,password,role) values("admin",sha1("admin1234"),"admin");
select * from ip_table;
select ccid,count(*) as cnt from ip_table group by ccid,domain having cnt>1;
select count(*) from ip_table where status="disabled";


insert into c3s_plans(name,price) values("unlimited_250",250.00);
insert into c3s_plans(name,price) values("unlimited_350",350.00),("unlimited_500",500.00);
select * from c3s_plans;
select name,address from cs_users;
select * from cs_users where name="";
update cs_users set password=sha1(concat(ccid,"1111"));

update cs_users set name="default" where name="";
show tables;
select * from django_session;
delete from django_session;
truncate cs_users;
select * from cs_users where ccid=19990;
select distinct domain from cs_users;
