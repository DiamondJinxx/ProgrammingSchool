# 26. Пример

Данная схема выбора комбинации has-a и is-a на практике нередко представляется весьма распространённым паттерном проектирования Мост/Bridge. Классический пример его применения -- кросс-платформная библиотека компонентов пользовательского интерфейса.

Любой визуальный компонент (например, кнопка) наследуется от класса Window (графическое окно). Окно в свою очередь наследуется от двух классов GeneralWindow (универсальные свойства любого окна) и PlatformWindow (свойства, зависящие от конкретной платформы). Универсальные операции, наследуемые от GeneralWindow, класс Window реализует с помощью операций, наследуемых от PlatformWindow.
Поддержка каждой конкретной платформы реализуется классами-потомками PlatformWindow, по одному на каждую платформу.

Проблема такой схемы в том, что во-первых, множественное наследование поддерживается далеко не во всех современных языках (оно подчас умышленно запрещено). И во-вторых, самое главное, что даже внутри конкретной платформы (например, Windows или Web) графическое представление визуального компонента может меняться в зависимости от контекста его использования (например, в рамках Windows мы хотим представлять некоторый документ в форматах PDF или HTML).

В таком случае мы сохраняем наследование класса Window от класса GeneralWindow (отношение "является"), а связь с конкретной реализацией оформляем в виде отношения "содержит". Включаем в состав класса Window полиморфный атрибут класса PlatformTooklit. В свою очередь для класса PlatformTooklit создаётся набор потомков, реализующих нужный набор операций для конкретного визуального представления.

Универсальные операции GeneralWindow в его потомке -- классе Window переопределяются, и в этих переопределениях выполняются обращения к подходящим операциям потомка класса PlatformTooklit. И вдобавок, в частности, мы получаем такую сильную возможность, как динамическая смена (непосредственно в процессе работы программы) реализации визуального представления для компонентов не только в рамках одной платформы, но и вообще между любыми платформами -- просто изменением содержимого атрибута PlatformTooklit (что, впрочем, на практике не очень актуально).

В данном примере успешно комбинируются все три ключевых механизма ООП: наследование (для обоих классов Window и PlatformTooklit), полиморфизм (для атрибута класса PlatformTooklit) и динамическое связывание (переопределённые методы GeneralWindow).

Самые распространённые ошибки, связанные с некорректным применением наследования:

- путаница между наследованием ("является") и композицией ("содержит");
- в качестве критерия применения наследования выступает некоторое поле-классификатор (пол человека или любой другой перечень из фиксированных значений), которое используется в программе только в статистических целях (отсутствует специфичная логика, связанная с обработкой конкретных значений поля);
- наследование применяется, чтобы получить доступ к удачной реализации класса-предка, который закрыт для изменений (ошибка тут в плохой проработке АТД класса-предка).

## Решение 18 задания

В проекте встречалась реализация адаптера авторизации, сценарии которой могут быть различны: логин-пароль, по реферальной ссылке, через токен.
Вся реализация класса адаптера была представлена в виде нескольких методов с множеством условных конструкций для поддержки разных сценариев.
Более удачным было бы наследование от базового адаптера с изменением логики авторизации предка, или с помощью динамического связывания.
