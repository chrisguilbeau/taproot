from pymysql import connect
bible = connect(host='localhost', port=3306,
    user='root', passwd='', db='bible2', charset='utf8')

class Rows(tuple):
    pass

def get_rows(sql, params=[]):
    cursor = bible.cursor()
    cursor.execute(sql, params)
    result = Rows(cursor.fetchall())
    result.fields = [meta[0] for meta in cursor.description]
    cursor.close()
    return result

def get_distinct_words():
    sql = '''
        select *
        from WordDistinctLower
        '''
    return [word for word, in get_rows(sql)]

def get_ref_words(book, chap):
    sql = '''
        select BookName, Chapter, VerseNum, Word, Punc, Italic,
            cParen, oParen, StrongsID
        from MainIndex mi
        join Books b
        on b.bookId = mi.bookId
        join BookAliases ba
        on ba.bookId = b.bookId
        left join StrongsIndex si
        on si.wordId = mi.wordId
        where Alias = %s
        and chapter = %s
        '''
    params = [book, chap]
    return get_rows(sql, params)

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
        select word, count(*)
        from MainIndex m
        join StrongsIndex si
        on m.WordID = si.WordID
        where si.StrongsID = %s
        group by word
        order by count(*) desc
        '''
    params = [number]
    return get_rows(sql, params)

def get_strongs_usage(number):
    sql = '''
        select Word, BookName, v.Chapter, v.VerseNum, VerseText
        from MainIndex m
        join StrongsIndex si
        on m.WordID = si.WordID
        join Verses v
        on v.VerseId = m.VerseId
        join Books b
        on b.BookId = v.BookId
        where si.StrongsID = %s
        '''
    params = [number]
    return get_rows(sql, params)

def get_word_meta(word):
    sql = '''
        select lemma, xlit, pronounce, language, s.strongsId, count(*)
        from MainIndex m
        join StrongsIndex si
        on si.wordId = m.wordId
        join Strongs s
        on s.strongsId = si.strongsId
        where word = %s
        group by word, lemma, xlit, pronounce, language, s.strongsId
        order by count(*) desc
        '''
    params = [word]
    return get_rows(sql, params)

def is_word(word):
    sql = '''
        select count(*)
        from WordDistinctLower
        where word = %s
        '''
    params = [word]
    return bool(get_rows(sql, params)[0][0])
