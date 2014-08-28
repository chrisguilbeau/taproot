use taproot;
drop table if exists strongs;
create table strongs (strongs varchar(25), word varchar(255), primary key (strongs)) character set=utf8;

insert into strongs
select distinct concat('G', strongs) as strongs, base_word as word
from bf.lexicon_greek
union all
select distinct concat('H', strongs) as strongs, base_word as word
from bf.lexicon_hebrew
where id not in (6501);

drop table if exists strongs_json;
create table strongs_json (strongs varchar(25), json text) character set=utf8;
alter table strongs_json add index strongs (strongs);

insert into strongs_json
select distinct concat('G', strongs) as strongs, data
from bf.lexicon_greek
union all
select distinct concat('H', strongs) as strongs, data
from bf.lexicon_hebrew
where id not in (6501);
