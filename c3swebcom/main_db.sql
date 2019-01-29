SET SQL_SAFE_UPDATES = 0;
create database c3swebcom;

use c3swebcom;

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
alter table cs_orders add column paid enum('1','0') default '0' after completed_at;
alter table cs_orders add column payment_date datetime default null after paid;


drop table ip_table;

update cs_users set password=sha1(concat(ccid,"1111"));

update cs_users set name="default" where name="";
delete from django_session;

alter table admin_users add column password_string varchar(100) not null default "1111";


create table cs_localities(
	id int not null auto_increment primary key,
    `name` varchar(100) not null,
    `code` varchar(100) not null)ENGINE=InnoDB;
INSERT INTO `cs_localities` VALUES (1,'default','default');

alter table cs_users add column locality int default 1 after address;
alter table cs_users add foreign key(locality) references cs_localities(id);

CREATE TABLE `cs_price_mappings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package` int(11) DEFAULT NULL,
  `locality` int(11) DEFAULT NULL,
  `price` float(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

alter table cs_price_mappings add foreign key(package) references cs_packages(id);
alter table cs_price_mappings add foreign key(locality) references cs_localities(id);
