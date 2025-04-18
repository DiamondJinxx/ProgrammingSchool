# 6. Объектно-ориентированное программирование

Разработчики, знакомые с ООП, наверняка уже распознали в компонетно-ориентированном программировании ряд знакомых черт ООП, которое добавляет к компонентному подходу четвёртую характеристику.

Это наследование, которое важно даже не столько как техническая возможность расширения типов, сколько как возможность развивать систему очень плавно, постепенно, небольшими шагами, через небольшие расширения или модификации другой системы.

Постепенно развиваемые компоненты называются классы, и их экземпляры называются объекты.

Наследование -- это способ структурирования программ, при котором новая реализация основывается на уже существующей. Большой плюс наследования, что оно существенно снижает избыточность и дублирование кода за счёт повторного использования, и представляет собой весьма мощный и гибкий инструмент. Но это и большой минус: компоненты начинают сильно зависеть от компонентов, которые они наследуют, и в результате подобными зависимостями становится сложно управлять.

Подавляющая часть литературы по объектно-ориентированному проектированию, например, по шаблонам проектирования, фокусируется на обучении правильному использованию наследования. Хотя композиция -- подход менее гибкий, чем наследование, он гораздо проще в использовании, и рекомендуется использовать композицию везде, где это возможно, а наследование применять только тогда, когда композиции недостаточно, а наследование подходит к задаче естественно, а иерархии получаются неглубокие (2-3 уровня).

Я сторонник достаточно активного грамотного использования наследования (умеренной глубины), потому что с его помощью удаётся создавать очень аккуратные модульные системы с очень невысокой связностью между модулями. Как это делать, отдельно разбирается на курсах по ООАП.