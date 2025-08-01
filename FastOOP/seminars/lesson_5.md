# 5. В одной строке кода не более одной "точки" (префикса вызова метода).

Это формальная синтаксическая реализация известного закона Деметры (Law of Demeter, LoD), хорошо снижающего связанность модулей/классов.

LoD гласит: каждый программный модуль (класс) должен обращаться только к непосредственным друзьям -- знакомым ему модулям, при этом знать ему надо максимально возможный минимум о чём угодно во внешнем мире (в том числе и об используемых модулях), кроме своего прямого кода.

Речь тут не просто о конкретной строке кода, а о том, что мы вообще отказываемся от любых цепочек вызовов методов вроде

obj.get_obj2().method2().get_obj3().method3();

LoD активно применяется в ООП, подразумевая в частности отказ от цепочек вызовов методов, но есть важный нюанс.

Существует концепция [текучего интерфейса (Fluent interface)](https://ru.wikipedia.org/wiki/Fluent_interface), которая удобна для реализации объектно-ориентированного API, чтобы записывать код не в виде

```python
obj.method1();
obj.method2();
obj.method3();
...
а в виде

obj.method1()
   .method2()
   .method3();
```

...
Каждый метод возвращает вызывающий его объект, поэтому такая цепочка возможна для записи в одной инструкции, а не в наборе команд (паттерн Method Chaining, на основе которого часто строятся сложные запросы и фильтры).

В данном случае LoD допускает подобную схему, так как мы используем в цепочке один и тот же объект, не обращаясь ни к каким сторонним сущностям.

Однако и в этом случае, **в каждой строке кода всё равно должно быть записано не более одного вызова метода.**

В чём сермяга данного правила? Дело в том, что **в цепочках вызовов обычно трудно определить, какой именно объект берёт на себя ответственность за ту или иную операцию** (за исключением случая Fluent interface). Практически всегда в цепочках вызовов, где несколько "точек" в одной инструкции, находится много неправильно распределенных обязанностей между разными классами.

Если в какой-то инструкции записано более одной точки, значит, объект становится посредником в цепочке вызовов, а это означает в свою очередь, что он знает слишком много о других объектах. Подумайте, чтобы перенести его некоторые активности в один из объектов, с которым он оказался связан в этой цепочке.

Несколько точек означают, **что ваш объект слишком глубоко копается в другом объекте.** Многочисленные точки указывают также, что **вы нарушаете инкапсуляцию**.

Думайте об этом так: **вы можете играть со своими игрушками, игрушками, которые вы сделали сами, и игрушками, которые вам кто-то явно подарил и которые теперь ваши. Но вы никогда, никогда не можете играть с чужими игрушками.**
