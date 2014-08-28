
use taproot;
drop table if exists book_name;
create table book_name (book_id int, name varchar(25), primary key (book_id)) character set=utf8;

LOAD DATA LOCAL INFILE 'book_name.csv' INTO TABLE book_name
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

