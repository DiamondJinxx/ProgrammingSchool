# 11. Ковариантность и контравариантность

Уточняющие комментарии про расширение и специализацию в ходе наследования.

Когда мы смотрим на класс как на тип, то при спуске по иерархии наследования мы получаем всё более специализированные типы, так как всё чаще не можем использовать оригинальные методы предков из-за их переопределения. Например, не имеет смысла двухсвязному списку наследовать методы из однонаправленного списка -- большинство их придётся переопределять. Причём ряд этих методов придётся переопределять только потому, что внутри, в реализации они работают с разными типами (например, с разными типами узлов в списке), а сам алгоритм остаётся по сути оригинальным. Мы просто его копируем, лишь модифицируя объекты некоторых типов. Не возникает никаких конфликтов с системой типов, однако эта система типов и никак нам не помогает в избегании дублирования кода (или как минимум, дублирования семантики).

Проблема в подобных случаях по сути единственная: **нам надо сохранить родительскую логику, "параметризуя" её типами**. Тут надо исходить из возможностей конкретного языка программирования, позволяет ли он автоматически связывать, по мере спуска по иерархии, типы атрибутов класса с типом текущего объекта без явного переопределения логики (определения типов полей мы задаём относительные, а не абсолютные -- относительно текущего типа). Это так называемая ковариантная типизация. Чаще всего она реализуется в форме обобщённых типов: если мы определяем контейнер, параметризованный типом Кот (который есть потомок типа Животное), то естественно, что этот тип "контейнер котов" автоматически будет потомком (частным случаем) типа "контейнер животных" (ковариантность типу-параметру Кот), и ему будут доступны все соответствующие методы типа-предка.

Другая схема ковариантности: переопределённый метод родительского класса может возвращать значение типа, который есть потомок типа значения, возвращаемого родительским методом.

Противоположный подход -- **контравариантность**, когда схема наследования переворачивается. Тут классический пример -- это делегаты (объекты, указывающие на функции). Есть обобщённый (параметризованный типом "Универсальный список") делегат "действие A над универсальным списком", который считается уже потомком делегата "действие А над связным списком" (при том, что связный список -- потомок универсального списка). В таком случае, подразумевая действия над универсальными списками, мы корректно сохраняем допустимость для них лишь ограниченного набора операций для связных списков, и не более. Потому что некоторое действие, специфичное именно для связного списка, нельзя применять к его предку, универсальному списку, такое действие не поддерживающему.

Это более простой формальный подход, так называемый subtyping, в чём-то более элегантный, однако на практике рекомендуется всегда ориентироваться на более практичные ковариантные подходы, подразумевающие специализацию кода, более естественно отражающую иерархию наследования.

Ковариантность - можем использовать более дочерний тип, но не родительский.
контравариантность - можем использовать родительский тип, но не дочерний.
