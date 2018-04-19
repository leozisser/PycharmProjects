# -*- coding: utf-8 -*-
from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, dictionary, type, custom,normalized
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline
from natasha.markup import show_markup, show_json, format_json

with open('test/test.txt', encoding='utf-8') as text:
    a = text.readlines()

MULTIPLE_NUMBERS = rule(
type('INT'),
rule(type('PUNCT'),
    type('INT')
).repeatable().optional())


CODE_LONG = rule(
        gram('ADJF'),
    gram('ADJF').optional().repeatable(),
    dictionary({'кодекс'})
)

CODE_SHORT = rule(
morph_pipeline({'АПК','УК','НК','ГК','КОАП', 'АПРК', 'Кодекс Российской Федерации об административных правонарушениях', 'Кодекс об административных правонарушениях Российской Федерации', 'Кодекс РФ об административных правонарушениях'})
)

CODE = rule(
    or_(CODE_SHORT,
        CODE_LONG)
)

ARTICLE = rule(rule(dictionary({'статья', 'ст'}),
                    rule(type('PUNCT')).optional()).repeatable(),
                    # MULTIPLE_NUMBERS
                    )


PUNKT = rule(rule(dictionary({'п'}), rule(type('PUNCT')).optional()).repeatable(), MULTIPLE_NUMBERS)



PODPUNKT = rule(dictionary(['подп', 'пп']), rule(type('PUNCT')).optional(), MULTIPLE_NUMBERS) #insert or_ (п.п.)

PART = rule(rule(dictionary('ч'), rule(type('PUNCT')).optional()).repeatable(), MULTIPLE_NUMBERS)      # также берет "часов"

Match = fact('', ['podpunkt', 'punkt', 'part', 'article', 'source'])
Source = fact(
    'source',
    ['type', 'name'])

Statya = fact('',['article'])

Article = rule(
    ARTICLE,
    MULTIPLE_NUMBERS.interpretation(Statya.article)).interpretation(Statya)

#may I NOT interpret 1st rule ('statya')?

parser = Parser(Article)

for number, line in enumerate(a):
    for match in parser.findall(line):
        start, stop = match.span
        # print(match)
        print(start, stop, [t.value for t in match.tokens], number)
        print(match.fact)



#normalize names of codes and then map them onto tags
#частью первой статьи 29 Устава железнодорожного транспорта Российской Федерации
