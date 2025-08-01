# 2. Введение

В первом цикле, посвящённом проектированию классов, мы видели, что даже простой подход к правильному проектированию классов на основе АТД как автономных сущностей предоставляет отличные возможности для формирования библиотек классов под конкретную предметную область, которые удобно использовать и модифицировать. Интерфейсы полностью отделены от реализаций; универсальный подход АТД (набор операций, отделённых от состояний) обеспечивает высокую гибкость; предусловия и постусловия позволяют достаточно строго контролировать корректность семантики классов и их целостность. В программировании вообще популярен и хорошо работает принцип Keep it simple, stupid (KISS), предполагающий, что большинство систем работают тем лучше, чем они проще.

Однако когда мы задумываемся о расширении нашего набора автономных классов, оказывается, что для этого требуются более мощные механизмы. В частности, наследование как концепция повторного использования кода позволила нам создать иерархию классов, где никакие методы практически не дублировались, а её структура довольно легко расширялась новыми идеологически схожими классами (различные виды списков). Это соответствие принципу You aren't gonna need it (YAGNI) -- избегание любой избыточной функциональности.

Формальный подход к наследованию подразумевает три принципиально разные возможности:
-- расширение класса-родителя (наследник задаёт более общий случай родителя);
-- специализация класса-родителя (наследник задаёт более специализированный случай родителя);
-- комбинация нескольких родительских классов.

Далеко не все языки поддерживают все эти виды отношений, мы рассмотрим универсальную, не зависящую от языков, концепцию наследования, из которой на практике вы можете применять наиболее подходящие вам приёмы.
