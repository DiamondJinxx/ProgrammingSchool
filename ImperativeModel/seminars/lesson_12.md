# 12. Мышление в парадигме состояний
Программы, в которых состояние используется бессистемно, очень трудно понять. Например, если состояние проходит по всей программе и везде в ней видимо/доступно, то оно может быть модифицировано в любом месте кода. Единственный способ рассуждать о такой программе -- это пытаться рассматривать всю программу целиком. Но если это возможно для небольших скриптов, то, очевидно, совершенно нереально уже для немного больших программ. Мы вкратце рассмотрим метод, называемый "инвариантные утверждения" (invariant assertions), который позволяет приручить состояние и взять stateful-сложность под линейный контроль. Этот метод может применяться для программ, которые имеют как императивную (использующую состояния), так и декларативную части.

Декларативная часть проявляется в виде логических выражений внутри assert-проверок, которые будем называть утверждения. Абстракции в этом контексте формируются через выведение новых правил доказательства для лингвистических абстракций.

Техника инвариантных утверждений известна в computer science как аксиоматическая семантика (применение исчисления предикатов к теории доказательств), когда семантика каждой конструкции языка определяется как некий набор правил или аксиом. Она была разработана великими математиками, логиками и кибернетиками -- Флойдом, Хоаром и Дейкстрой, в период 1960-1970-е годы. Правила корректности были названы аксиомами, и с тех пор прижилась подобная терминология.

Эта техника не применялась массово потому, что достаточно сложна, и лишь в последнее десятилетие, с мощным развитием темы формальной верификации и появлением прикладных пруф-ассистантов, становится постепенно всё более распространённой.

# Инвариантные утверждения
Метод инвариантных утверждений позволяет рассуждать о частях программы независимо от её других частей. Это даёт нам при работе с состояниями одно из самых сильных свойств декларативного программирования: понимание всей системы складывается из линейной суммы понимания её подсистем. Однако это свойство достигается ценой строгой формальной организации программы.

Базовая идея -- организовываем систему как иерархию АТД. Каждый АТД может использовать другие АТД для своей реализации. Этот подход более глубокий концептуально, нежели знакомая вам схема наследования из классического ООП.
Каждый АТД специфицируется набором инвариантных утверждений, или просто инвариантов.
Инвариант -- это логическое выражение, которое опеределяет связь между аргументами АТД и его внутренним состоянием. Каждая операция АТД предварительно предполагает, что некоторый инвариант истинен, и когда она завершается, гарантирует истинность другого инварианта (гарантируется это на уровне реализации операции). Таким образом, использование инвариантов отделяет реализацию АТД от его использования. Мы можем рассуждать о каждом таком аспекте программы отдельно.

# Понятие утверждения

Для реализации вышеупомянутого подхода вводится понятие утверждения (assertion). 

Утверждение -- это логическое выражение, которое добавляется между двумя исполняемыми инструкциями кода. Утверждение само по себе может трактоваться как логическое выражение, вычисляющее булево значение, хотя тут имеются определённые отличия такого выражения от логических выражений в используемой вычислительной модели. Утверждения могут содержать переменные и идентификаторы ячеек, которые встречаются в коде, но также могут содержать переменные и кванторы, которые не встречаются в языке программирования, а используются только для выражения конкретного отношения. Кванторы обычно рассматриваются как отдельные символы. 

Два классических квантора -- это квантор всеобщности ∀ (для всех...) и квантор существования ∃ (существует хотя бы один...).

## Понятие утверждения частичной корректности

Каждая i-я операция Oi в АТД специфицируется двумя утверждениями Ai и Bi. Спецификация утверждает, что если Ai истинно перед выполнением Oi, то когда Oi завершится, Bi будет истинным.
Это записывается так:

{ Ai } Oi { Bi }
и называется утверждение частичной корректности.

Частичной потому, что утверждение будет корректным при условии, что Oi завершится "нормально" (не учитываем исключительные ситуации и прочие ненормальные ситуации).
Ai называется предусловие, и Bi называется постусловие.
Полная спецификация АТД состоит из утверждений частичной корректности для всех его операций.

# Доказательство корректности АТД

Мы можем достаточно формально описать АТД, но как быть с доказательством корректности его реализации? Для этого надо доказать, что корректно в плане реализации каждое утверждение частичной корректности.

Существует немало формальных техник доказательства корректности непосредственно исходного кода, однако все они пока слишком трудоёмки для прикладного применения. С некоторыми из них мы познакомимся на отдельном мини-курсе -- быстром старте в пруф-чекеры (Coq, Agda...). 



Тут мы немного коснулись обширной теоретической темы доказательства корректности программ. Одну из возможных прикладных её реализаций -- проектирование классов на основе пред- и постусловий -- мы подробно разбирали на первом курсе по ООАП.
Хороший прикладной материал по инвариантным утверждениям, обязательно изучите: [habr.com/ru/company/golovachcourses/blog/222679/](Программирование по контракту)