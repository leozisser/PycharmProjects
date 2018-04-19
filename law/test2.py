from yargy.predicates import eq, type, dictionary
from yargy import Parser, rule, and_, or_
from yargy.interpretation import fact, attribute
from yargy.predicates import dictionary, gte, lte
ARTICLE = rule(
        type('INT')
)
MULTIPLE_NUMBERS = rule(type('INT'))

Statya = fact('', ['article']
)
Article = rule(
    ARTICLE,
    MULTIPLE_NUMBERS.interpretation(
        Statya.article
    )
).interpretation(Statya)

parser = Parser(Article)
match = parser.match('5  650')
print(match.fact)