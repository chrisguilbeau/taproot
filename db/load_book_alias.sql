use taproot;
drop table if exists book_alias;
create table book_alias (book_id int, alias varchar(25), primary key (book_id, alias)) character set=utf8;
alter table book_alias add index alias (alias);

LOAD DATA LOCAL INFILE 'book_alias.csv' INTO TABLE book_alias
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

