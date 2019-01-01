SET SQL_SAFE_UPDATES = 0;
create database c3swebcom;

use c3swebcom;

drop table cs_users;

create table cs_domains(
id int not null auto_increment primary key,
name varchar(100) not null,
url varchar(100) not null unique,
auth_user varchar(100),
auth_pass varchar(100),
created_on datetime default current_timestamp,
status enum('up','down') default 'up'
)engine=innoDb;

create table cs_users(
	id int not null auto_increment primary key,
	ccid int not null,
    name varchar(100) not null,
    password varchar(100),
    address varchar(500),
    ip_count int,
    expiry_date date,
    package varchar(100),
    phone varchar(100),
    mobile varchar(100),
    domain varchar(100),
    unique key(ccid,domain))engine=innoDb;

drop table cs_users;

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
    user_id int not null references cs_users(id) on delete cascade,
    ip varchar(15) default "0.0.0.0",
    status enum('enabled','disabled') default "enabled")engine=innoDb;

create table cs_orders(
			id int auto_increment not null primary key,
		    user_id int references cs_users(id),
		    initiator_id int default 0,
		    initiator_type enum('admin','user') default "admin",
		    plan varchar(100),
		    value float(10,2) default 0.00,
		    amount float(10,2) default 0.00,
		    initiated_at datetime default current_timestamp,
		    completed_at datetime,
		    status enum('1','0') default '0',
		    response varchar(100) default null
		)ENGINE=InnoDB;
create table `cs_packages`(
`id` int auto_increment not null primary key,
`remote_id` int not null,
`name` varchar(100) not null,
`value` float(10,2) not null default 0,
`domain_id` int references cs_domains(id) on delete cascade
)ENGINE=InnoDB;

alter table cs_orders add foreign key(initiator_id) references admin_users(id);

select cs.ccid,name,address,expiry_date,package,phone,mobile,domain,group_concat(ip.ip) from cs_users cs inner join ip_table ip on cs.id=ip.user_id where cs.id=74 group by cs.ccid,cs.domain limit 10;
select user_id,count(*) as cnt from ip_table group by user_id having cnt>1;

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
