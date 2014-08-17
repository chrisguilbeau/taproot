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

def get_word_meta(word):
    sql = '''
        select lemma, xlit, pronounce, language, count(*)
        from MainIndex m
        join strongsindex si
        on si.wordId = m.wordId
        join strongs s
        on s.strongsId = si.strongsId
        where word = %s
        group by word, lemma, xlit, pronounce, language
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
