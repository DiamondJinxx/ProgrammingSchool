# Как правильно и на основе каких абстракций проектировать классы

## Абстрактный тип данных
Это фундаментальный курс по ООП -- даже не столько по объектно-ориентированному проектированию, сколько по объектно-ориентированному программированию. Мы познакомимся в теории и на практике с самым базовым, самым главным в ООП понятием абстрактный тип данных (АТД), на основе которого следует разрабатывать любые объектно-ориентированные программы. Мы практически не будем затрагивать пока принципы наследования и полиморфизма, обойдёмся только одной инкапсуляцией. Парадигма АТД столь мощна, что на одной её основе можно успешно строить системы весьма и весьма высокой сложности.

По мере того, как мы начинаем решать всё более сложные задачи, сам код может стать слишком "перегруженным", если у нас не будет какой-нибудь техники для управления этой растущей сложностью. С помощью ООП мы можем применять идею построения чего-либо, используя детали низкого уровня, затем закрывая нашу "коробку" (класс) и рассматривая её как своего рода фиксированную, неизменяемую сущность, и основываясь на ней в дальнейшем. Мы закрываем её, представляя готовый способ работы с чем-то конкретным, и переходим к более крупной части проекта, забывая про скрытое под капотом наших "коробок" огромное облако мелких деталей реализации. Это очень мощная техника для решения больших задач.

**Абстрактный тип данных (АТД)** -- это неявное определение некоторого типа данных в нашей системе, которое формально задаёт некоторое множество объектов и набор допустимых операций над ними.

АТД -- определение неявное потому, что в коде программы оно отсутствует.

**Реализация конкретного АТД в коде происходит в виде класса.**

То есть АТД -- это более высокий уровень абстракции, нежели класс. Как объект в программе "реализует" некоторый класс -- создаётся на основе класса как некоторого шаблона, так и сам класс (тип данных в программе) "реализует" АТД.

АТД -- это некоторое абстрактное описание типа данных, существующее в голове разработчика и, желательно, в технической документации.

Программисту и проектировщику надо думать о проектировании и реализации программы не в терминах конкретных классов (системы типов конкретного приложения), а по возможности более абстрактно, в терминах абстрактных типов данных.

АТД задаёт допустимое множество объектов в том смысле, что оно формально определяет, по каким признакам различные значения относятся к этому множеству. Например, АТД Integer задаёт множество всех целых чисел, АТД String задаёт множество всех строк, АТД Cat задаёт множество всех котов с заданным набором характеристик.

АТД обязательно задаёт и набор допустимых операций над этим множеством. Для целых чисел это будет как минимум набор арифметических операций, для строк -- операции конкатенации, определения длины, выделения и поиска подстроки, для котов -- операции Бежать, Кушать, Спать, Мурлыкать, и т. д.

В качестве первого практического примера использования АТД мы разберём базовую структуру данных Stack (Стек), реализацией которой уже занимались на первом цикле по алгоритмам. Мы выясним, почему и в чём предложенный в задании класс, реализующий стек, был плохим, и создадим правильную версию.

"Что такое вычислительное мышление? Я представляю абстрактную машину с теми типами данных и операциями, которые мне наиболее подходят для решения задачи. Если бы такая машина существовала, я сразу бы могла легко написать нужную мне программу. Но такой машины нету. Поэтому я ввожу ряд подзадач -- типы данных и операции -- и мне нужно разобраться, как их реализовывать. Я выполняю такие итерации снова и снова, пока не доберусь до реальной вычислительной машины и существующего языка программирования.
Это и есть искусство проектирования". Барбара Лисков

[Интервью с Барбарой Лисков на Гейдельбергском форуме лауреатов](https://www.quantamagazine.org/barbara-liskov-is-the-architect-of-modern-algorithms-20191120/) (людей, получавших самые престижные премии в computer science и математике -- Филдса, Абеля, Тьюринга).
Основополагающие подходы Лисков, правильное использование абстракций и спецификаций, ставшие классикой ООАП, проходим на данном курсе.

