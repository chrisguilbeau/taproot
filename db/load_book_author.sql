use taproot;
drop table if exists book_author;
create table book_author (book_id int, author varchar(25), primary key (book_id, author)) character set=utf8;
alter table book_author add index author (author);

LOAD DATA LOCAL INFILE 'book_author.csv' INTO TABLE book_author
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

