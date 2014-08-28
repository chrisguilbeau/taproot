use taproot;
drop table if exists verses;
create table verses (book_id int, chapter int, verse int, text text, primary key (book_id, chapter, verse)) character set=utf8;

insert into verses
select book, chapter, verse, words
from bf.bible_en_verses;

