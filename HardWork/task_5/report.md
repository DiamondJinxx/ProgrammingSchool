# Рефлексия
Одно время считал, что самодокументирующийся код - таблетка от всех болезней, ибо плюсовый код читать периодически было совсем тяжко, а комментарии в коде были особо и ни о чем. Читай их, не читай, один фиг ни про код ничего не поймешь, ни про то, как данный кусочек кода в проекте в целом участвует. Приходилось подолгу вчитываться и держать в голове множество других частей системы, чтобы в конце концов разобраться. В те моменты, комментарии "высокого уровня" были бы в самый раз. На личном проекте попробую поиграться с комментариями и сравнить, насколько подход с комментариями "высокого уровня" превосходит подход с описанием работы кода. Уверен, что для меня будущего я сделаю хорошую услугу. Кстати, после того, как взглянул на код Дяди Боба, чувствую, что его книги пожалуй удалю из библиотеки :)

# Пример 1
```python
# Является частью функциональности обработки действий пользователя. 
# Используется как точка входа в процессе сопоставления пользовательской команды и домена,
# к которому команда принадлежит. 
class HandlerOrchestrator:
    """Распределитель запросов между обработчиками пользовательских команд"""

    def __init__(
        self,
        handlers: list[DomainHandler],
        logger: Logger,
    ):
        """Конструктор оркестратора."""
        self._domain_handlers = handlers
        self._logger = logger

    def notify_handler(
        self,
        chat_id: int,
        action_data: ActionData,
    ) -> None:
        """Оповестить доменные обработчики о команде пользователя."""
        self._logger.debug(
            "Получена команда '%s' от пользователя",
            event_data,
        )
        for handler in self._domain_handlers:
            handler.execute_command(
                chat_id=chat_id,
                action_data=action_data,
            )

```

# Пример 2
```python
# Отвечает за обработку команд назначенной доменной области(Учителя, Запись на занятия, Уроки, и т.д.).
# Используется HandlerOrchestrator для  маршрутизации пользовательской команды до конечного обработчика .
class DomainHandler(abc.ABC):
    """Обработчик событий/команд определенной доменной области"""

    def __init__(
        self,
        bot: TeleBot,
        logger: Logger,
        domain: str,
        action_handlers_mapper: dict[str, CommandHandlerBase],
    ):
        """Конструктор обработчика"""
        self._bot = bot
        self._logger = logger
        self._domain = domain
        self._handler_mapper = action_handlers_mapper

    def execute_command(
        self,
        chat_id: int,
        action_data: ActionData,
    ) -> None:
        """Обработка команды пользователя."""
        handler = self._handler_mapper.get(action_data.command)
        if not handler:
            self._logger.debug(
                "Для команды '%s' отсутствует обработчик в домене '%s'",
                action_data.command,
                self._domain,
            )
            return
        return handler.handle(
            bot=self._bot,
            chat_id=chat_id,
            action_data=action_data,
        )
```

# Пример 3
```python
# Отвечает за формирования ui компонента для подтверждения/отмены записи ученика на занятие к преподавателю. 
# Используется в цепочке команд записи на занятие к преподавателю.
def build_manager_confirm_registration(
    manager: Teacher,
    callback_data_id: int,
) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn_confirm = types.InlineKeyboardButton(
        text="Подтвердить",
        callback_data=SignUpActionData(
			command=LessonsHandlingEvents.SIGNUP_CONFIRM,
			cb_id=callback_data_id,
        ).json(),
    )
    btn_no_confirm = types.InlineKeyboardButton(
        text="Отменить",
        callback_data=SignUpActionData(
			command=LessonsHandlingEvents.SIGNUP_NO_CONFIRM,
			cb_id=callback_data_id,
        ).json(),
    )
    markup.add(btn_confirm)
    markup.add(btn_no_confirm)

    return markup

```
