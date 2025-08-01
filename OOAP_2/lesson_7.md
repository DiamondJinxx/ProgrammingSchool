# 7. Разбираемся с модульным противоречием

Выход из противоречивой модели модуля находится в парадигме ООП. Классические попытки совместить все пять принципов с помощью модулей, компонентов, пакетов, терпят неудачу.

Тема декомпозиции проекта на небольшие автономные сущности изучается в программной инженерии не менее полувека. Идея модулей строится вокруг набора функций, вокруг парадигмы так называемого структурного программирования, а ООП -- вокруг объекта. Это вечные попытки как-то более-менее эффективно разрешить конфликт между данными и функциями/методами их обработки. Подробно тему декомпозиции, построения модели предметной области, проектирования качественной иерархии классов, изучаем на следующем курсе. Пока мы приближаемся к идее, что класс (с использованием наследования и полиморфизма) представляется наиболее оптимальной формой модуля. Только надо всегда помнить, когда мы выполняем декомпозицию, то выделяем классы таким образом, что они представляют собой не просто наборы функций, а прежде всего некоторые структуры данных, которые хоть и описываются только операциями, однако все эти операции имеют семантическое отношение именно к своей структуре данных.

Основа объектно-ориентированного подхода -- это приоритет типов данных над описывающими их операциями. То есть в списке методов класса, который всегда задаёт некоторую структуру данных, не должно быть методов, не имеющих прямого отношения к этой структуре данных.

# ЭР

### Существуют ли ситуации, когда связи между модулями должны делаться публичными?

В общем случае это нарушение инкапсуляции и принципа единственной ответственности SRP (The Single Responsibility Principle, изучаем далее).
На практике допускаются технические исключения, когда проще и выразительнее сделать общедоступными некоторые связи модуля, которые используются во множестве других модулей. Например, это может быть модуль, содержащий инфраструктурный код (логирование, метрики, ...).
И надо также учитывать, что наличие множества неявных связей (зависимостей) приводит к трудноконтролируемому проекту. Большое количество таких связей -- признак плохого проектирования.

### Какие метрики вы бы предложили для количественной оценки принципов организации модулей?

Например, количество семантических единиц в программе, так называемых "сущностей". Хотя слепо минимизировать их тоже будет некорректным.

Формально, между модулями нужно выдерживать как можно меньшую связность, т.е. делать модули независимыми. Поэтому для количественной оценки можно использовать количество связей, исходящих из модуля (модули, от которых зависит данный модуль), и количество связей, входящих в модуль (модули, зависящие от этого модуля).

Соответственно, надо стремиться делать максимально автономные модули (минимизируя исходящие связи). Если у автономного модуля всего одна входящая стрелка, то, возможно, он используется всего один раз, и разбиение на модули было некорректным. Также будет плохим случай, когда связей слишком много, например "все зависят от всех", или когда задействуется слишком много контекста, а используется из него далеко не всё.

### Если вы разрабатывали программы, в которых было хотя бы 3-5 классов,как бы вы оценили их модульность по этим метрикам?

Пример 1.
Есть абстрактный класс Pizza и много-много классов, реализующих конкретные виды пицц.
Есть абстрактный класс Coffee и также много-много классов, реализующих конкретные виды кофе.
Есть абстрактный класс Restaurant и классы, реализующие конкретные рестораны, где продается пицца и кофе.
Добавим абстрактный класс Courier и классы, реализующие конкретные типы доставки.
Получаются три семантические единицы: еда, заведение, доставка, которые можно представить в виде разных модулей. Это вполне хороший показатель для проекта, где классов могут насчитываться сотни и тысячи.

Пример 2.
Из 6 классов один был "закрытым". Он был очень перегруженным как публичными, так и условно скрытыми методами. Они в остальных 5 дочерних классах переопределялись (override) в разных комбинациях. Принципы открытости-закрытости и повторного использования нарушались повсеместно, что быстро похоронило программу.
