from pymysql import connect

def getConnection():
    return connect(host='localhost', port=3306,
        user='root', passwd='', db='taproot', charset='utf8')

class Rows(tuple):
    pass

def get_rows(sql, params=[]):
    bible = getConnection()
    cursor = bible.cursor()
    cursor.execute(sql, params)
    result = Rows(cursor.fetchall())
    result.fields = [meta[0] for meta in cursor.description]
    cursor.close()
    bible.close()
    return result

def get_distinct_words():
    sql = '''
        select *
        from WordDistinctLower
        '''
    return [word for word, in get_rows(sql)]

def get_ref_data(book, chap):
    sql = '''
         select bn.name as book, chapter, verse, phrase, strongs
         from bible b
         join book_name bn
         on bn.book_id = b.book_id
         join book_alias ba
         on ba.book_id = b.book_id
         where ba.alias like %s
         and chapter = %s
         order by verse, phrase_order
        '''
    params = [book, chap]
    return get_rows(sql, params)

def get_strongs_word(strongs):
    sql = '''
        select word
        from strongs
        where strongs = %s
        '''
    params = [strongs]
    return get_rows(sql, params)[0][0]

def get_strongs_jsons(strongs):
    sql = '''
        select json
        from strongs_json
        where strongs = %s
        '''
    params = [strongs]
    return [json for json, in get_rows(sql, params)]

def get_strongs_record(number):
    sql = '''
        select lemma, xlit, pronounce, description, PartOfSpeech, Language
        from Strongs
        where StrongsID = %s
        '''
    params = [number]
    return get_rows(sql, params)[0]

def get_strongs_usage_counts(number):
    sql = '''
        select word_usage, count(*)
        from bible
        where strongs = %s
        group by word_usage
        order by count(*) desc
        '''
    params = [number]
    return get_rows(sql, params)

def get_strongs_usage(number):
    sql = '''
        select phrase, b.word_usage, bn.name, b.chapter, b.verse, v.text
        from bible b
        join book_name bn
        on bn.book_id = b.book_id
        join verses v
        on v.book_id = b.book_id
        and v.chapter = b.chapter
        and v.verse = b.verse
        where strongs = %s
        '''
    params = [number]
    return get_rows(sql, params)

def get_edit_strongs_data(strongsId):
    sql = '''
        select mi.Word, b.BookName, v.Chapter, v.VerseNum, v.VerseText
        from MainIndex mi
        join StrongsIndex si
        on si.WordID = mi.WordID
        join Books b
        on b.BookID = mi.BookID
        join Verses v
        on v.VerseID = mi.VerseID
        where StrongsID = %s
        '''
    params = [strongsId]
    return get_rows(sql, params)

def get_verse_edit_data(book, chap, verse):
    sql = '''
        select mi.WordId, Word, StrongsId
        from MainIndex mi
        left join StrongsIndex si
        on si.WordId = mi.WordId
        join Books b
        on b.bookid = mi.bookid
        where b.BookName = %s
        and chapter = %s
        and VerseNum = %s
        '''
    params = [book, chap, verse]
    return get_rows(sql, params)

def get_word_meta(word):
    sql = '''
        select s.strongs, s.word,
            count(*) as count, max(json) as json
        from bible b
        join strongs s
        on s.strongs = b.strongs
        join strongs_json sj
        on sj.strongs = s.strongs
        where word_usage = %s
        group by s.strongs, s.word
        order by count(*) desc
        '''
    params = [word]
    return get_rows(sql, params)

def make_edit(wordId, strongsId):
    bible = getConnection()
    cursor = bible.cursor()
    sql = '''
        delete from StrongsIndex
        where WordID = %s
        '''
    params = [wordId]
    cursor.execute(sql, params)
    if strongsId:
        sql = '''
            insert into StrongsIndex (WordID, StrongsID)
            values (%s, %s)
            '''
        params = [wordId, strongsId]
        cursor.execute(sql, params)
    bible.commit()
    cursor.close()
    bible.close()

def is_word(word):
    sql = '''
        select count(*)
        from bible
        where word_usage = %s
        limit 1
        '''
    params = [word]
    return bool(get_rows(sql, params)[0][0])
