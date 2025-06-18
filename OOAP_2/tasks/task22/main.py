class Material:
    pass


class Newsprint(Material):
    pass


class ThickPaper(Material):
    pass


class ContentType:
    content: str


class ScienseContent(ContentType):
    content: str = "science"


class NewspaperContent(ContentType):
    content: str = "newspaper"


class YellowPressContent(ContentType):
    content: str = "yellow-press"

# Наследуются способы классификация предков - книга, газета, и желтая пресса
class Book(ThickPaper, ScienseContent):
    pass


class Newspaper(Newsprint, NewspaperContent):
    pass


class YellowPressMagazine(ThickPaper, YellowPressContent):
    pass
