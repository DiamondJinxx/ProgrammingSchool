Пример с неистинным наследованием
```python
import abc

class Animal(abc.ABC):

	def __init__(self, name: str) -> None:
		self._name = name
	
	@abstractmethod
	def voice(self) -> None:
		...

class Dog(Animal):
	def voice(self) -> None:
		print(f"{self._name}: Gav!")

class Cat(Animal):
	def voice(self) -> None:
		print(f"{self._name}: Myau!")

class AngryDog(Dog):
	def voice(self) -> None:
		print(f"{self._name}: zloe gav!")

class LazyCat(Cat):
	def voice(self) -> None:
		print(f"{self._name}: Lenivoe myau :3")
```

С использованием паттерна Посетитель

```python
import abc

class Visitor:
	...

class Animal(abc.ABC):

	def __init__(self, name: str) -> None:
		self._name = name
	
	@abstractmethod
	def voice(self) -> None:
		...

	@abstractmethod	
	def accept(self, visitor: Visitor) -> None:
		...

class Dog(Animal):
	def voice(self) -> None:
		print(f"{self._name}: Gav!")

	def accept(self, visitor: Visitor) -> None:
		visitor.do_for_dog(self)

class Cat(Animal):
	def voice(self) -> None:
		print(f"{self._name}: Myau!")

	def accept(self, visitor: Visitor) -> None:
		visitor.do_for_cat(self)

class AnimalVisitor(Visitor):
	def do_for_cat(self, cat: Cat) -> None:
		print("* lazily *")
		cat.voice()
				   
	def do_for_dog(self, dog: Dog) -> None:
		print("* actively * ")	
		dog.voice()
```

Более серьезное примера не нашел, прошу простить :)

Мне если честно не очень понравился вариант реализации шаблона Посетитель с использованием двойной диспетчеризации, если не использовать преимущество динамических ЯП с добавлением полей налету, то я тут вижу проблему циклических импортов: визитеру нужно знать про типы объектов, которые он посещает, а объектам нужно знать про методы визитера. 

Как будто бы, если добавить функций в классы, можно добиться переопределения поведения с использованием истинного наседования, например:
```python
class Animal(abc.ABC):

	def __init__(self, name: str) -> None:
		self._name = name

	@abstractmethod
	def _get_voice(self) -> str:
		...
	
	@abstractmethod
	def voice(self) -> None:
		...

class Dog(Animal):

	def _get_voice(self) -> str:
		return "gav"
		
	def voice(self) -> None:
		voice = self._get_voice()
		print(f"{self._name}: {voice}!")

class AngryDog(Dog):
	def _get_voice(self) -> str:
		return "zloe " + super()._get_voice()

```

