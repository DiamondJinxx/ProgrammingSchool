# 3. Классы как инкрементальные (incremental) АТД
Мне не удалось найти подходящего слова для incremental :)
частичные, наращиваемые, постепенные, постепенно формируемые...

Как уже объяснялось ранее, основное дополнение, которое объектно-ориентированное программирование добавляет к компонентно-ориентированному программированию -- это наследование. ООП позволяет определять класс постепенно, путём расширения (в том числе дополнения, уточнения, ограничения...) существующих классов. При этом недостаточно просто отметить, какие классы расширяются; для правильного определения нового АТД необходимо больше концепций. Наша модель включает три набора таких концепций:

1. __Наследование__ само по себе, которое определяет, какие именно уже существующие классы расширяются.

2. __Управление доступом к методам класса__: как организуется такой доступ к определённым методам как в новом классе, так и в классах выше по иерархии.

3. __Управление инкапсуляцией__: как в остальной части программы за пределами класса организуется доступ к его атрибутам и методам.

Добавив к этим наборам поддержку сообщений первого класса (для реализации делегатов), получим полностью уникальный способ инкрементального определения АТД.


__Наследование -- это способ конструирования новых классов на основе существующих.__ Наследование в общем случае допускается как единичное (у класса не может быть более одного родителя), так и множественное, и определяет, как существующие атрибуты и методы становятся доступными в новом классе.

Общая схема наследования применима и к атрибутам, и к методам и называется связью (отношением) через перезапись (overriding relation): метод в классе А перезаписывает собой любой метод с такой же сигнатурой (именем метода и списком параметров с определёнными типами) во всех суперклассах А (находящихся выше по иерархии).

Иерархия классов -- это направленный граф с текущим узлом как корнем. Ребра направлены от нижестоящих к вышестоящим классам. Есть два требования для того, чтобы иерархия наследования была корректной.

Во-первых, __отношение наследования должно быть направленным и ациклическим__. Условно говоря, нельзя наследовать класс A от B, а класс B от A.

Во-вторых, после удаления всех переопределённых методов, __каждый оставшийся метод должен иметь уникальную сигнатуру__ и быть определённым только в одном классе в иерархии.

# Рантайм - это всё, что есть

Система программирования не должна строго различать время компиляции и время выполнения. Такое различие -- просто способ помочь компилятору выполнить определенные виды оптимизации, не более. Однако большинство популярных языков, включая Java, C++ и многие другие, вводят такое различие явно. Как правило, некоторые инструкции (например, объявления классов) могут быть "выполнены" только во время компиляции, а остальные -- только во время выполнения. В таком случае компилятор может "выполнить" все описания классов и функций одновременно, без какого-либо вмешательства в выполнение программы, что позволяет провести весьма мощную оптимизацию при генерации кода, а также множество глубоких проверок корректности использования системы типов. Однако такая схема значительно снижает гибкость языка.

# Статическое и динамическое связывание

При выполнении метода "внутри" объекта часто происходит вызов другого метода этого же объекта. В общем случае такой вызов можно считать рекурсивным относительно объекта в целом: объект "вызывает" сам себя. Когда в такой ситуации дополнительно допускается наследование, ситуация усложняется. Обычное наследование подразумевает определение нового АТД, который расширяет существующий АТД. Чтобы реализовать эту схему корректно, потребуются два способа поддержки рекурсивных вызовов: статическое и динамическое связывание.

Из-за полиморфизма не всегда возможно определить на этапе компиляции, объект какого именно класса хранится в некоторой переменной. Динамическое связывание (связывание метода с конкретным классом) подразумевает, что определение нужного метода в иерархии наследования выполняется непосредственно в момент обращения объекта к имени метода в процессе работы программы. Такой подход фактически не позволяет вызывать уже существующие "старые" (родительские) методы, когда мы расширили старый АТД новыми возможностями.

Статическое связывание подразумевает, что класс, в котором находится конкретный вызываемый метод, можно определить непосредственно в момент компиляции (например, с помощью явных синтаксических подсказок имени класса через приведение типов).


# Управление инкапсуляцией

Принцип управления инкапсуляцией в объектно-ориентированном языке заключается в ограничении доступа к атрибутам и методам класса в соответствии с требованиями архитектуры приложения. Каждый член класса дополнительно уточняется областью видимости.

Область видимости -- это та часть кода программы, в которой атрибут или метод виден, т.е. к нему можно получить доступ, указав его имя. Обычно область видимости статически определяется структурой программы. Она также может быть определена динамически, а именно во время выполнения, хотя на практике такой подход почти не применяется.

Языки программирования обычно фиксируют область видимости по умолчанию для каждого члена класса при его объявлении, которая может быть изменена с помощью специальных ключевых слов. Обычно используются public, private и protected. К сожалению, разные языки используют эти слова для определения разных схем видимости.


# Универсальная схема видимости членов класса.
Наиболее фундаментальные формы видимости -- это private и public.

__Приватный__ (private) член класса виден только внутри объекта (экземпляра класса).

__Публичный__ (public) член класса виден где угодно в программе.

__Защищённый__ (protected) член класса виден не только внутри объекта, но и доступен в классах-наследниках.

Хорошая схема, когда атрибуты по умолчанию приватны, и методы по умолчанию публичны.

Подход с приватными и публичными членами естественен, когда мы используем классы для конструирования АТД.

- Класс -- это "инкремент". АТД существует сам по себе, со своими собственными атрибутами и методами. Класс же, который физически "конструирует" АТД в программе, представляет АТД как инкрементальную модификацию своих суперклассов.

- Атрибуты АТД приватны -- невидимы за его пределами, так как АТД формально задаётся только своими операциями (методами).

- Методы определяют внешний интерфейс АТД, поэтому они должны быть видны всем сущностям, заинтересованным в данном АТД. Соответственно, их видимость публична.


# Конструирование иных видимостей

Техники управления инкапсуляцией в коде основаны в основном на двух концепциях: лексической видимости и использовании имён. Приватная и публичная области видимости могут быть легко реализованы с помощью этих двух концепций. Однако многие другие формы видимости также могут быть выражены с их помощью: например, private и protected в C++ и Java, а также гораздо более сложные политики безопасности.

Основная техника заключается в том, чтобы позволить заголовкам методов быть именами как значениями, а не просто жёстко заданными атомами. Имя -- это неизменяемая константа; единственный способ узнать имя -- это получить ссылку на него. Таким образом, программа может передавать ссылку на имя контролируемым образом, именно в те области программы, в которых имя должно быть видно.

По этой причине атомы не являются безопасными: если третья сторона узнает программное представление атома (либо угадав, либо каким-то другим способом), то сможет вызвать соответствующий метод. Имена как значения -- это простой способ устранить такую утечку безопасности. Однако современные языки программирования (Java, C#, C++) поддерживают только атомы в качестве имён (текстовые "константы" в коде, которые обрабатывает компилятор), поэтому в них добавляются специальные инструкции (protected, private) для явного ограничения видимости.

При создании большой программы атомы выигрывают как в плане простоты кода, так и по фактору психологического комфорта во время разработки, потому что "ссылочная" работа со значениями имён методов, конечно, существенно затрудняет понимание. Однако и у значений имён есть свои преимущества, так как их видимость может легко контролироваться динамически, что исключает конфликты наследования, и управление инкапсуляцией становится более простым, поскольку ссылка на объект теперь не имеет права просто так вызвать любой его метод. В результате в программе как раз становится меньше ошибок, и она лучше структурируется, хотя и усилий на её разработку потребуется побольше. Однако это решается хорошим синтаксическим сахаром -- например, явным синтаксическим разделением имён-атомов и имён-значений и удобными средствами работы с ними.


# Альтернативы наследованию
Наследование -- это только один из способов повторного использования уже определённой функциональности при создании новых возможностей. Наследование нередко бывает сложным для правильного использования и требует хорошей подготовки, поскольку подразумевает тесную связь между классом-предком и его потомками-расширениями. Иногда лучше использовать более свободные подходы. Два таких известных подхода -- это __переадресация (forwarding) и делегирование (delegation)__. Оба они определяются на уровне объекта: если объект A не принимает сообщение M, то оно прозрачно передаётся объекту B.

Переадресация и делегирование различаются в том, как они обрабатывают self/this.

__При переадресации объекты A и B работают со своими собственными оригинальными self.__

__При делегировании есть только одна сущность A, и обращение к self внутри B подразумевает self из A.__

Можно сказать, что делегирование, как и наследование реализации, подразумевает общий self. Переадресация же общий self не подразумевает.

Делегирование в общем случае считается мощным механизмом структурирования системы динамически, подразумевая конструирование иерархии объектов, а не классов. Вместо организации наследования объектов через классы (в момент определения класса, фактически во время компиляции), мы позволяем объектам делегировать работу другому объекту в момент физического создания объекта в ходе работы программы.

Делегирование даёт такой же эффект, как и наследование, с двумя важными отличиями: сама иерархия уже строится между объектами, а не между классами, и она может быть (следовательно) изменена в любой момент работы программы.

Важным свойством семантики делегирования считается тот момент, что self всегда сохраняется (оно одно на всех): это self исходного объекта, который инициировал всю цепочку делегирования. Из этого следует, что состояние текущего объекта (атрибуты) также будет состоянием и исходного объекта. В этом смысле другие объекты, участвующие в цепочке делегирования, играют роль классов: только их методы важны при делегировании, а не значения их атрибутов (которые всегда родительские).



# Рефлексия
Система считается рефлексивной, если она может проверять части своего состояния непосредственно во время работы. Рефлексия может быть чисто интроспективной (только чтение внутреннего состояния, без изменения) или интрузивной (допускается как чтение, так и изменение внутреннего состояния). Рефлексия может быть выполнена на высоком или низком уровне абстракции.

Пример рефлексии на высоком уровне -- возможность рассматривать элементы в стеке как замыкания. Этот пример можно объяснить в терминах абстрактной машины. С другой стороны, способность обращаться к оперативной памяти программы напрямую, как к массиву целых чисел -- это рефлексия на низком уровне. Нет простого способа выразить её в абстрактной машине.


# Мета-объектные протоколы
ООП благодаря своему высокому потенциалу, предлагает обширное поле для экспериментов. Например, система может позволять рефлексивное изучение или даже изменение иерархии наследования во время работы программы. Другая возможность -- изменять работу самих объектов на базовом уровне, например, работу наследования (как происходит поиск методов в иерархии классов), или механизм вызова методов.

Определение того, как именно объектная система функционирует на подобных базовых уровнях, называется __мета-объектным протоколом__. Возможность изменять мета-объектный протокол -- мощный способ модификации объектной системы. Мета-объектные протоколы используются в самых разных целях: для отладки, настройки, разделения концепций (например, прозрачным добавлением шифрования, или изменением формата вызова методов). Мета-объектные протоколы были первоначально изобретены в контексте объектной системы Common Lisp Object System (CLOS) и считаются активной областью исследований в ООП.

__Обёртка методов__

Общая схема мета-объектных протоколов подразумевает "оборачивание" методов дополнительным кодом -- перехват каждого вызова метода, и, например, выполнение определенной программистом операции перед вызовом и после вызова, изменение аргументов самого вызова, и т. п.

