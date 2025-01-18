class ReadableMixin:
    def read(self) -> None:
        print(f"Read {self.__class__.__name__} as {self.format}.")

class Journal:
    format = "paper journal"

class Book:
    format = "paper book"


class EBook:
    format = "ebook"


class ReadableEBook(EBook, ReadableMixin):
    ...

class ReadableBook(Book, ReadableMixin):
    ...


class ReadableJournal(Journal, ReadableMixin):
    ...


ReadableJournal().read()
ReadableBook().read()
ReadableEBook().read()
