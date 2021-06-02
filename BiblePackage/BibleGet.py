def bibleVerse(book_name: str, chapter: int, verse: int, last_verse=0) :
    location = 'Bible/' + book_name + '/' + book_name + '_' + str(chapter) + '.txt'
    with open(location, 'r') as bible:
        bible_read = bible.readlines()

        if last_verse == 0:
            range_verse = f'{book_name} {chapter}:{verse}'
            verse_line = 2 * (verse - 1)
            msg = bible_read[verse_line]
            msg = [
                range_verse,
                msg,
                0xffff00
            ]
            return msg

        else:
            i = verse
            i_i = last_verse + 1
            bible_verse = ''
            range_verse = f'{book_name} {chapter}:{verse}-{last_verse}'
            while i < i_i:
                verse_line = 2 * (i - 1)
                bible_verse += bible_read[verse_line] + '\n'
                i += 1
            length = len(bible_verse)

            if length < 2001:
                msg = [
                    range_verse,
                    bible_verse,
                    0xffb300
                ]
                return msg
            else:
                msg = [
                    "ERROR",
                    "Error: You have requested too many Bible verses ""and have exceeded the discord limit of 2000 "
                    "characters ""please shorten your request and try again.",
                    0xff0000
                ]
                return msg