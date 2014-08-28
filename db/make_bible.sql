use taproot;
drop table if exists bible;
/* drop table if exists book_name; */
/* drop table if exists book_alias; */
/* drop table if exists bible_author; */

create table bible (book_id int, chapter int, verse int, phrase_order int, phrase text, strongs varchar(25), word_usage varchar(25)) character set=utf8;
alter table bible add index pk (book_id, chapter, verse, phrase_order);
alter table bible add index strongs_phrase (strongs);
/* create table book_name (book_id int, name varchar(25)) character set=utf8; */
/* create table book_alias (book_id int, alias varchar(25)) character set=utf8; */
/* create table book_author (book_id int, author varchar(25)) character set=utf8; */

insert into bible
select distinct book, chapter, verse, cluster, phrase, uw.strongs, uw.word
from (
    select
        book,
        chapter,
        verse,
        cluster,
        group_concat(word order by word_order asc separator ' ') as phrase,
        strongs
    from (
        select
            be.id as word_order,
            be.book as book,
            be.chapter as chapter,
            be.verse as verse,
            be.clusterId as cluster,
            be.word as word,
            concat(
            case when be.book < 40 then 'H' else 'G' end,
            bo.strongs
            ) as strongs
        from bf.bible_en be
        left join bf.bible_original bo
        on bo.id = be.orig_id
        ) t
    group by book, chapter, verse, cluster, strongs
    ) t2
left join usage_words uw
on uw.strongs = t2.strongs
and lower(phrase) like concat('%', lower(uw.word), '%');

create table bible2 like bible;
insert into bible2
select book_id, chapter, verse, phrase_order, phrase, strongs, max(word_usage)
from bible
group by book_id, chapter, verse, phrase_order, phrase, strongs;

truncate table bible;
insert into bible
select * from bible2;

drop table bible2;

/* insert into bible */
/* select */
/*     book, */
/*     chapter, */
/*     verse, */
/*     cluster, */
/*     group_concat(word order by word_order asc separator ' ') as phrase, */
/*     strongs */
/* from ( */
/*     select */
/*         be.id as word_order, */
/*         be.book as book, */
/*         be.chapter as chapter, */
/*         be.verse as verse, */
/*         be.clusterId as cluster, */
/*         be.word as word, */
/*         concat( */
/*             case when be.book < 40 then 'H' else 'G' end, */
/*             bo.strongs */
/*             ) as strongs */
/*     from bf.bible_en be */
/*     join bf.bible_original bo */
/*     on bo.id = be.orig_id */
/*     ) t */
/* group by book, chapter, verse, cluster, strongs */
