# 22. Добавим ещё больше строгости

Добавим к этой пессимистичной практике ещё больше формальной строгости. Проблема в том, что ковариантность ("автоматическая" параметризация кода типами по мере спуска по иерархии наследования без необходимости модификации логики) и полиморфизм могут вступать в конфликт друг с другом, поэтому в популярных языках программирования на ковариантность накладываются весьма сильные ограничения. В C# например она допускается только для интерфейсов и делегатов. В Java ковариантность поддерживается относительно типа результата переопределяемого метода.

В частности, ООП допускает две потенциально конфликтные операции: полиморфное присваивание
x = y
и ковариантный вызов
x.foo(z)
(который следует отличать, конечно, от динамического связывания с аналогичным синтаксисом). Классический конфликт возникает, когда мы начинаем использовать x одновременно и как полиморфный объект, и как объект, вызывающий ковариантный метод foo(). Эффект от такой комбинации может быть далеко не всегда предсказуемым: программист может, сам того не желая, "перехитрить" систему типов, и получить совсем другой результат.

Ковариантность -- это в некотором смысле тоже полиморфизм, только с другим механизмом.
Классический полиморфизм подразумевает в частности вызов foo(T z), где в качестве z может использоваться полиморфный параметр (в реальных вызовах можно задавать потомки класса T).
Ковариантность в частности подразумевает вызов foo<T>(T z), где уже сам тип T выступает параметром метода, и сама логика, обработка объекта z параметризуется типом T. На практике это реализуется передачей в качестве аргумента не просто типа T, а обобщённого типа, например List<T>, когда включается ковариантная типизация.
В таких случаях, когда параметр метода -- обобщённый тип, а вызывается этот метод полиморфным объектом, нередко и возникают неоднозначности.

**Строгое решение запрещает использовать некую сущность в программе одновременно и как полиморфную, и как ковариантную.**

Простое синтаксическое правило выявления полиморфных сущностей в программе таково:

Сущность x полиморфна, если

1. она участвует в полиморфном присваивании

x = y

или

2. x -- формальный параметр любого метода.

_В потенциально подозрительных случаях рекомендуется выполнять полиморфное присваивание не напрямую, а с помощью упоминавшейся ранее попытки присваивания._

В таком случае применять ковариантный вызов метода к переменной x не разрешается.

Задание 16.

Если используемый вами язык программирования это допускает, напишите примеры полиморфного и ковариантного вызовов метода.
