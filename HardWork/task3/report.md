# HardWork: TDD

## Пример 1:


Версия п.1:
```python
from src.app.menu.main_menu import main_menu
from src.app.types.menu_actions import MenuActions

# Тест, который следует коду и слишком много знает о внутренностях кода из-за использования MenuActions перечисления
# основная причина подобной кривизны теста - отсутствующий интерфейс для модуля создания главного меню
def _test_action_btns_create() -> None:
    """Тест создания меню основных действий пользователя"""
    menu = main_menu()
    assert menu
    assert menu.keyboard
    keyboard = menu.keyboard[0] + menu.keyboard[1]
    for index, btn in enumerate(keyboard):
        assert btn
        assert btn["text"] != list(MenuActions)[0].value
```

Версия п.3:
```python
from src.app.menu import main_menu_fixed
from src.app.types.menu_actions import MenuActions


# Добавив интерфейс для работы с модулем меню, получаем тест, который перестает знать о внутренностях модуля
# и задает спецификацию - "меню должно содержать кнопки со следующими названиями"
def test_mein_menu() -> None:
    """Тест создания меню основных действий пользователя"""
    actions = ["Главное меню", "Ученики","Учителя", "Записаться на урок"]
    menu = main_menu_fixed(actions)
    assert menu
    assert menu.keyboard
    keyboard = menu.keyboard[0] + menu.keyboard[1]
    for index, btns in enumerate(keyboard):
        assert btns
        assert btns["text"] == actions[index]
```

## Пример 2:

Версия п.1:
```python
from src.app.handlers.actions.command import TeachersHandler


# тест опять же лезет сильно внутрь модуля обработчика события, сцеплен с ним.
# Тест связан с кодом, а не с дизайном. Как и все следующие тесты.
def test_teacher_handler_can_handle_teacher_list_event() -> None:
    """Проверка возможности обработать событие запроса списка учителей."""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    event_data = "teacher_list"
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act, Assert
    # Забираемся в кишочки обработчика. Очень плохая практика - использовать снаружи защищенные методы.
    assert handler._is_list_view_needed(event_data)


def test_teacher_handler_can_handle_teacher_bio_event() -> None:
    """Проверка возможности обработать событие запроса детальной информации учителя."""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    # так же тест сильно знает про проект - что именно такой строковый литерал используется в проекте. Стоит добавить константы на уровне проекта, конкретнее в модуле обработчика.
    event_data = "teacher_bio"
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act, Assert
    assert handler._is_bio_view_needed(event_data)


def test_teacher_handler_cant_handle_not_teacher_events() -> None:
    """Обработчик событий учителей не должен обрабатывать события, несвязанные с учителем"""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    event_data = "other_event"
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act, Assert
    assert not handler._is_bio_view_needed(event_data)
    assert not handler._is_list_view_needed(event_data)

```

Версия п.3
```python
from src.app.handlers.actions.command import TeachersHandler
# введены константы для единой точки изменений. Теперь код следует дизайну проекта.
from src.app.types.events.teachers import TeacherHandlingEvents


def test_teacher_handler_can_handle_teacher_list_event() -> None:
    """Проверка возможности обработать событие запроса списка учителей."""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    event_data = TeacherHandlingEvents.LIST
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act
    # Предоставляется интерфейс для проверки возможности обработки события.
    # тест перестал знать о внутренностях модуля и теперь тест и тестируемый модуль связанны через интерфейс модуля.
    # Аналогично тестам ниже

    result = handler.can_handle_event(event_data)
    # Assert
    assert result


def test_teacher_handler_can_handle_teacher_info_event() -> None:
    """Проверка возможности обработать событие запроса детальной информации учителя."""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    event_data = TeacherHandlingEvents.INFO
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act
    result = handler.can_handle_event(event_data)

    # Assert
    assert result


def test_teacher_handler_cant_handle_not_teacher_events() -> None:
    """Обработчик событий учителей не должен обрабатывать события, несвязанные с учителем"""
    # Arrange
    mock_logger = mock_logger()
    mock_bot = mock_bot()
    event_data = "other_event"
    handler = TeachersHandler(mock_bot, mock_logger)

    # Act
    result = handler.can_handle_event(event_data)

    # Assert
    assert not result

```

# О TDD, BDD и трех уровнях рассуждений о программной системе

О TDD я слышал давно и ознакомился с ним по книгам Роберта Мартина(он хоть и консультант на текущий момент, но разрабом
все же был). И так как я на момент ознакомления с темой испытывал большие сложности по причине отсутствия тестов в 
проекте. Просто было тяжело разрабатывать. Начал писать тесты для своих модулей, чтобы тесты становились спецификациями
к коду. Сначала получалось не очень, но со временем более менее тесты стали получаться в виде спецификаций. Из нового из
материалов я понял, почему юнит тесты сами по себе бесполезны, до этого не понимал, почему периодически кто-то так 
думает.

Перейдя на новое место работы я познакомился с Behave тестами и я впервые услышал про BDD. Я оценил полезность 
методологии, однако сами тесты приходилось писать самим, пока мы не спихнули эту работу на тестировщиков. Ведь они
должны лучше знать спецификации системы, которую тестируют. Пока я писал сценарии behave тестов, я начал интуитивно
формировать постулат "пиши декларативно какие действия произошли и что требуется получить, как инструкцию". 

В последствии внедрения в проект модульной архитектуру(после архитектуры MVP), я наткнулся на следующие мысли: "делаем 
максимально просто и связываем модули по интерфейсам". После этой мысли мои навыки написания кода будто в целом 
улучшилось: возведя инкапсуляцию модулей в абсолют, мой результат в коде стал выглядеть лучше. Более гибким. Более
простым в чтении. И тут я заметил, что у кода проекта выстраивается древовидная структура зависимостей. Тот самый
иерархический граф с четко определенными интерфейсами из занятий по императивной модели.

Тут же я вступил в КБ нашего проекта(как лид одной из команды) и начал учиться строить непосредственно системы, а не 
только отдельные сервисы. И вот тут я подошел к тому, что поведение системы нужно рассматривать отстраненно от кода.
Мы начинаем с того, что понимаем, какое поведение системы нам нужно, какими инструментами мы добиваемся требуемого 
поведения, код по итогу рождался будто сам. Но полноты картины с 3 уровнем рассуждений о системе у меня не было.

Из нового для себя я узнал:
1) Что я находился преимужественно на 2/1 уровнях - в дебагере и трейсахт я провожу минимум времени, больше читаю код.
2) Про формальные методы я вообще ничего не знал. Примеры из урока расширили границы моего понимания, мозг хрустнул, 
я хочу по-новому смотреть на код - через FOL & HOL. То, как через них верифицируется код в примерах, побудило меня
наработать на своих проектах навык верификации своей работы. Пуская и без пруф ассистеров, но в мышлении я точно хочу
опираться на вышеуказанные принципы.
3) Материалы из прошлых курсов открываются с новой стороны. Опять перечитывать и собирать воедино...