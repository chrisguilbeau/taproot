use taproot;

drop table if exists usage_words;
create table usage_words (strongs varchar(25), word varchar(25)) character set=utf8;
alter table usage_words add index pk (strongs, word);

LOAD DATA LOCAL INFILE 'usage_words.csv' INTO TABLE usage_words
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

