# В Python поддерживаются только 2 варианта скрытия методов: 1 и 4 

class Animal:
    
    # публичный метод в родителе, публичный и в потомке
    def voice(self):
        self._voice_impl()

    # защищенный метод в родителе, защищенный и в потомке. В питоне это все на уровне договоренности
    def _voice_impl(self):
        print("basic animal voice")

    # приватный метод в родителе, приватный и в потомке. Тут уже используется манглинг
    def __scream(self):
        print("basic animal scream")


class Cat(Animal):
    # защищенный в потомке метод родительского класса
    def _voice_impl(self):
        print("Meow")

    def __scream(self):
        print("MEEEEEEEEEOW")

animal = Animal()
cat = Cat()


# вызов публичных методов 
animal.voice()
cat.voice()

# вызов защищенных методов, по сути мы можем так написать, но на уровне соглашения нельзя так делать
animal._voice_impl()
cat._voice_impl()

# интерпритатор выведет ошибку
# cat.__scream()
# но мы то знаем, что используется манглинг
cat._Cat__scream()
# кстати, через потомка мы можем вызвать приватные метод родителя
cat._Animal__scream()
