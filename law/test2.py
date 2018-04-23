# -*- coding: utf-8 -*-
from yargy import Parser, rule, and_, or_, not_, forward
from yargy.predicates import gram, dictionary, type, custom,normalized, eq, gte, lte
from yargy.interpretation import fact, attribute

NAME = and_(gte(1000), lte(2100))


Source = fact(
    '',
    ['name', attribute('type', 'codex')]
)




SOURCE = rule(NAME.interpretation(Source.name))\
    .interpretation(Source)

Match = fact(
    'Match',
    ['article', 'source']
)
ARTICLE = dictionary(['статья']).interpretation(Match.article)

MATCH = forward().interpretation(Match)

MATCH.define(or_(
    ARTICLE,
    # rule(MATCH, ARTICLE),
    rule(
        MATCH,
        SOURCE.interpretation(
            Match.source
        )
    )
))
parser = Parser(MATCH)
text = ' статья 1004'
for match in parser.findall(text):
    print(match)
    print(match.fact)
