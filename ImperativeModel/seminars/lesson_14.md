# 14. Programming in large на практике

Но как же надо структурировать будущую большую систему, требования к которой пока слабо понятны? Какую абстракцию тут лучше выбрать, чтобы она хорошо поддерживала и продуктивную командную работу, и методику "от тонкого к толстому"? Один из способов, который проверенно работает на практике -- это структурировать проект как иерархический граф с чётко определенными интерфейсами на каждом уровне.

![Понятная схема](https://skillsmart.ru/data//stt/state1.png)

Проектируемая система состоит из набора узлов (подсистем), где каждый узел связан/взаимодействует с некоторыми другими узлами. Каждый узел -- это экземпляр компонента, но и на уровне системы типов проект организован таким же образом -- в виде иерархии компонентов (например, классов). Интерфейсы здесь -- например, формальнрые наборы операций АТД.

Принципиальный момент, что, как вы, вероятно, догадались, каждый узел в свою очередь декомпозируется в граф со своей внутренней структурой. Декомпозиция заканчивается, когда мы достигаем примитивных компонентов, предоставляемых базовым логическим уровнем.

В реальных проектах уровней декомпозиции немного, часто вполне достаточно двух-трёх уровней "вложенности". Декомпозицию в данном случае не надо путать с методикой проектирования "сверху вниз" (в чём различие, поясняется далее). Практическую методику - реализацию этого подхода с помощью ООП -- вы изучали на двух курсах по ООАП, когда создавали множество почти равноправных АТД.

## 1) Связи между компонентами

Первый шаг в проектировании системы по имеющемуся множеству проектных требований -- это выбор схемы соединения компонентов. Тут возможны два варианта.

### 1. Статическая структура.

Граф компонентов хорошо понятен с самого начала разработки системы. В таком случае компоненты могут быть связаны друг с другом сразу же, когда приложение запускается.

Каждый экземпляр компонента примерно соответствует набору функциональных возможностей, который называют библиотека или модуль.

Важный момент: очень желательно, чтобы каждый экземпляр компонента существовал в системе не более чем в одном виде (паттерн Синглетон), поэтому не следует смешивать компонент и классический класс, подразумевающий порождение множества экземпляров. Тут речь идёт именно о библиотеках или модулях/пакетах. Как вариант, под компонентом можно понимать статический класс. Если библиотека требуется в нескольких разных подсистемах проекта, мы хотим, чтобы все они использовали одну и ту же физическую библиотеку (инстанс).

Статическая структура на практике может реализовываться компонентами как синтаксическими единицами компиляции, хранящимися в отдельных файлах. Такие компоненты называют функторы, которые могут компилироваться независимо от других функторов. Зависимости между функторами задаются через физические имена файлов. Чтобы быть доступным для других функторов, функтор должен быть "записан" в файл, что позволяет однозначно обращаться к нему по имени файла с помощью типовых инструкций любого языка программирования для подключения модулей.

Функтор представляется двумя форматами: файл с исходным текстом, и файл со скомпилированным кодом (например, байт-кодом виртуальной машины или нативным машинным кодом).

Приложение -- обычно один конкретный скомпилированный функтор. Для его запуска все остальные скомпилированные функторы, явно или косвенно связанные с главным, должны быть собраны вместе и "построены" в единое целое. При запуске главного функтора все связанные функторы автоматически линкуются с ним, и создаются их экземпляры. Такая связь может быть статической (на этапе компиляции) или динамической (функторы подгружаются во время работы программы).

### 2. Динамическая структура

Часто приложение выполняет вычисления с компонентами, которые возникают и связываются друг с другом непосредственно во время выполнения. Или программа может создать новый компонент и сохранить его, и т. д. Экземпляры компонентов в данном варианте не обязательно должны быть общими (глобальными) синглетонами; возможно, потребуется несколько экземпляров одного компонента (модуля или типа данных). Например, компонент может реализовать интерфейс к базе данных (что часто требуется в задачах репликации). В зависимости от того, используется ли одна или несколько внешних баз данных, необходимо будет создать один или несколько экземпляров компонента. Это определяется во время выполнения, когда добавляется новая база данных (узел репликации) в горячем режиме.

Функтор в данном случае -- просто ещё одна языковая сущность. Это может быть, например, класс или процедура, возможно, с более строгим описанием их интерфейса.

## 2) Взаимодействие между компонентами
Когда компоненты соединены вместе, они должны начать взаимодействовать друг с другом. Далее приведены шесть наиболее популярных протоколов для такого взаимодействия, в порядке возрастания независимости компонентов.

1. Процедура/функция.

Логика программы последовательна, и один компонент вызывает другой как функцию. Вызывающая сторона может быть не единственным инициатором такого вызова; допустимы вложенные вызовы, когда фокус управления переходит от одного компонента к другому. Но всегда существует только один глобальный фокус управления, который в каждый момент времени напрямую связывает два конкретных компонента.

2. Корутина.

Два компонента выполняются независимо, но последовательно передавая управление друг другу. Выполнилась часть кода одного компонента, затем управление передаётся другому компоненту, который выполняет часть своего кода, и передаёт управление обратно первому компоненту, который продолжает работу с последней промежуточной точки (с сохранением своих локальных состояний), и т. д.
Тут возникает уже несколько фокусов контроля, по одному на каждую корутину. Этот протокол более свободный, нежели предыдущий, но компоненты всё ещё зависимы, поскольку выполняются попеременно и связаны с друг с другом.

3. Параллельность и синхронизм.

Третья схема -- когда каждый компонент развивается независимо от других, и может инициировать и завершать связь с другим компонентом в соответствии с некоторым протоколом, который согласован для обоих компонентов. Компоненты работают параллельно. Тут существует несколько фокусов контроля, которые называются "нити" (threads), мы их проходили на первом курсе по парадигмам. Каждый компонент однако обращается к другим компонентам синхронно: компонент, отправивший кому-то запрос, ожидает ответа, больше ничего не делая до получения ответа (или разрыва связи по ошибке -- таймауту например).

4. Параллельность и асинхронизм.

Множество параллельно работающих компонентов, которые взаимодействуют через асинхронные каналы. Каждый компонент может посылать сообщения другим, однако не обязан пассивно ожидать ответа, и может продолжать свою работу. Асинхронные каналы могут работать по разным схемам (например, обрабатывая сообщения в порядке их поступления, или случайно), и такие каналы называются потоки (streams).
В этой схеме компонент должен знать некоторый идентификатор компонента, с которым он обменивается сообщениями.

5. Параллельный почтовый ящик.

Это разновидность предыдущей схемы, когда асинхронные каналы работают как "почтовые ящики", накапливая поступающие сообщения, каждое из которых адресуется конкретному компоненту. В таком случае появляется возможность выполнять сопоставление с образцом, выделяя нужное подмножество сообщений в канале, и не затрагивая другие сообщения, что очень удобно в параллельных системах. Такая схема реализована, например, в языке Erlang.

6. Согласованная модель.

Это схема, когда отправитель и получатель сообщений не должны знать идентификационную информацию друг друга. Такая абстракция называется пространство кортежей (tuple space) -- парадигма ассоциативной памяти для параллельных/распределённых вычислений, применяемая к интерфейсам компонентов. Компоненты работают параллельно, и взаимодействуют исключительно через общее пространство кортежей.
Один компонент может асинхронно отправить сообщение, а другой -- "получить" его в том смысле, что его надо явно найти по шаблону, как в почтовом ящике.

## Принцип независимости модели
Каждый компонент в системе может разрабатываться в какой-то своей оригинальной вычислительной модели. В процессе разработки внутренняя структура компонента может кардинально изменяться: нередко меняется вычислительная модель, stateless-компонент может стать компонентом с состоянием (или параллельным, или распределённым, и т.д.), или наоборот.

Если такое изменение происходит на уровне реализации компонента, нет необходимости изменять его интерфейс. Интерфейс требуется менять только в том случае, если меняется функциональность компонента, видимая извне. Это важное свойство модульности вычислительных моделей. До тех пор, пока интерфейс остается неизменным, это свойство гарантирует, что нет необходимости изменять что-либо ещё в остальной части системы.

Это базовый принцип проектирования для всех вычислительных моделей:

Интерфейс компонента должен быть независим от вычислительной модели, используемой для реализации компонента. Интерфейс зависит исключительно от внешне видимой функциональности компонента.

Хороший пример этого принципа -- мемоизация. Функция вычисляет некоторый результат, который требует существенного объёма вычислений, и кэширует свои параметры так, что если вызов функции с конкретными значениями уже выполнялся, то сразу выдаётся уже готовый результат, вычисленный ранее. Но несмотря на то, что кэш мемоизации, очевидно, требует работы с состояниями (мы переходим от декларативной модели к stateful-модели), смена внутренней реализации компонента не требует абсолютно никаких изменений в остальном коде системы.
