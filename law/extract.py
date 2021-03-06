# -*- coding: utf-8 -*-
import json
from yargy import Parser, rule, or_, forward
from yargy.predicates import dictionary, type
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline
from natasha.markup import show_json, format_json
import postprocessing

MULTIPLE_NUMBERS = rule(
type('INT'),
    rule(
    or_(
        dictionary({'и'}),
        type('PUNCT')
    ),
    type('INT')
).repeatable().optional(),
)

Match = fact('match', ['podpunkt', 'punkt', 'part', 'article','paragraph', 'chapter', 'name', 'source'])

APK = rule(morph_pipeline(['АПК','арбитражный процессуальный кодекс', 'АПРК'])).interpretation(Match.name.const('АПК')) #АПРК - нашел опечатку, решил ее включить.
UK = rule(morph_pipeline(['УК', 'Уголовный кодекс',])).interpretation(Match.name.const('УК'))
GK = rule(morph_pipeline(['ГК', 'Гражданский кодекс'])).interpretation(Match.name.const('ГК'))
NK = rule(morph_pipeline(['НК', 'Налоговый кодекс'])).interpretation(Match.name.const('НК'))
KOAP = rule(morph_pipeline(['КоАП', 'Кодекс Российской Федерации об административных правонарушениях',
    'Кодекс об административных правонарушениях Российской Федерации',
    'Кодекс РФ об административных правонарушениях',
    'Кодекса Российской Федерации «Об административных правонарушениях»'])).interpretation(Match.name.const('КоАП'))
ZK = rule(morph_pipeline(['ЗК', 'Земельный кодекс'])).interpretation(Match.name.const('ЗК'))
JK = rule(morph_pipeline(['ЖК', 'жилищный кодекс'])).interpretation(Match.name.const('ЖК'))
RF = rule(morph_pipeline({'РФ', 'Российская Федерация', 'Россия'}))

CODE = rule(or_(
        GK,
        UK,
        JK,
        ZK,
        KOAP,
        NK,
        APK
        ),
    RF.optional()
)

Source = fact(
    'source',
    [attribute('name', 'not_defined'), attribute('type', 'codex')]
)

SOURCE = rule(CODE.interpretation(Source.name))\
    .interpretation(Source)

Match = fact('match', ['podpunkt', 'punkt', 'part', 'article', 'source', 'paragraph', 'chapter', 'name'])

ARTICLE = rule(rule(dictionary({'статья', 'ст'}),
                rule(type('PUNCT')).optional()).repeatable(),
                MULTIPLE_NUMBERS.interpretation(Match.article),
                rule(type('PUNCT')).optional()
               )
PUNKT = rule(rule(dictionary({'пункт'}), rule(type('PUNCT')).optional()).repeatable(),
             MULTIPLE_NUMBERS.interpretation(Match.punkt),
             rule(type('PUNCT')).optional()
             )

PODPUNKT = rule(rule(dictionary({'подпункт', 'пп', 'п'}), rule(type('PUNCT')).optional()).repeatable(),
                MULTIPLE_NUMBERS.interpretation(Match.podpunkt),
                rule(type('PUNCT')).optional()
                ) #insert or_ (п.п.)

PART = rule(rule(dictionary({'часть'}), rule(type('PUNCT')).optional()).repeatable(),
            MULTIPLE_NUMBERS.interpretation(Match.part),
            rule(type('PUNCT')).optional()
            )

PARAGRAPH = rule(rule(dictionary({'параграф','§'}),
                      rule(type('PUNCT')).optional()).repeatable(),
                 MULTIPLE_NUMBERS.interpretation(Match.paragraph),
                 rule(type('PUNCT')).optional()
                 )

CHAPTER = rule(rule(dictionary({'глава','гл'}),
                    rule(type('PUNCT')).optional()).repeatable(),
                MULTIPLE_NUMBERS.interpretation(Match.chapter),
                rule(type('PUNCT')).optional()
                )


NO_CODE = rule(or_(
    rule(
        PODPUNKT.optional(),
            PUNKT.optional(),
        ARTICLE),
    rule(
        PUNKT.optional(),
        PART,
        ARTICLE),
    rule(
        PARAGRAPH.optional(),
        CHAPTER

    ),
    rule(PARAGRAPH)
),
)

MATCH = forward().interpretation(Match)

MATCH.define(or_(
    NO_CODE,
    rule(
        MATCH,
        SOURCE.interpretation(
            Match.source
        ), RF.optional()
    )
)
)
parser = Parser(MATCH)

with open('test.txt', 'r', encoding='utf-8') as text:
    a = text.readlines()

result = open('test.jsonl','w', encoding='utf-8')

for number, line in enumerate(a):
    linebox = []
    matches = []
    spans = []
    w = parser.findall(line)
    d = [m.fact.as_json for m in w]

    for match in parser.findall(line):
        start, stop = match.span
        spans.append(start)
        spans.append(stop)
        strt = min(spans)
        stp = max(spans)
        spans = [strt, stp]  # самое простое решение. Можно еще объединять спаны, если они соседствуют,
                             # и разъединять, если нет, но в test.txt мэтчи всегда идут подряд

    print('line, spans: ', number+1, spans)
    print(line.strip('\n'))
    rawr = json.loads(format_json(d))
    mf = [i for i in rawr]
    # print('mf',mf)
    fin = postprocessing.pretty(mf)
    print(spans, fin)
    linebox.append(line.strip('\n'))
    linebox.append(spans)
    linebox.append(fin)
    result.write(str(linebox))
    result.write('\n')
result.close()
