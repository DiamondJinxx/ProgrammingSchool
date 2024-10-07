## Пример 1:
```python
import json  
from pathlib import Path  
  
from sqlalchemy import select  
from telebot.callback_data import CallbackData  
  
from src.app.infrastructure.db import session_factory  
from src.app.infrastructure.db.models import Teacher  
from src.app.infrastructure.db.models import Specialization  
from src.app.menu import teachers as menu_builder  
from src.app.menu import specializations as menu_builder  


def handle_events(event_date):
	event_data = json.loads(event_data)  
    incoming_event = event_data["event"]  
    self._logger.debug(  
        "%s: Обработчик вызван для события %s",  
        str(type(self)),  
        incoming_event,  
    )  
    with session_factory() as session:  
        specialization_select_stmt = select(Specialization)  
        if self._is_specializtion_list_view_needed(incoming_event):  
            specializations = session.scalars(
	            specialization_select_stmt,
            ).all()  
            markup = menu_builder.build_specializations_list(
	            specializations,
            )
            self._bot.send_message(  
                chat_id,  
                "Выберете преподавателя",  
                reply_markup=markup,  
            )  
            return  
        if self._is_specialization_info_view_needed(incoming_event):  
            spec_id = event_data["specialization_id"]  
            where_stmt = specialization_select_stmt.where(  
                Specialization.id == spec_id,  
            )  
            specialization = session.scalar(where_stmt)  
            markup = menu_builder.build_specialization_info(
	            specialization,
            )
            self._bot.send_message(  
                chat_id,  
                text="Выберите преподавателя",  
                reply_markup=markup,  
            )  
	            return

        teacher_select_stmt = select(Teacher)  
        if self._is_list_view_needed(incoming_event):  
            teachers = session.scalars(
	            teacher_select_stmt,
			).all()  
            markup = menu_builder.build_teachers_list(teachers)  
            self._bot.send_message(  
                chat_id,  
                "Выберете преподавателя",  
                reply_markup=markup,  
            )  
            return  
        if self._is_teacher_info_view_needed(incoming_event):  
            teacher_id = event_data["teacher_id"]  
            where_stmt = teacher_select_stmt.where(  
                Teacher.id == teacher_id,  
            )  
            teacher = session.scalar(where_stmt)  
            markup = menu_builder.build_teacher_info(teacher)  
            with Path(teacher.photo_path).open("rb") as photo:  
                caption = self._teacher_caption(teacher)  
                self._bot.send_photo(  
                    chat_id,  
                    photo=photo,  
                    caption=caption,  
                    reply_markup=markup,  
                )  
                return  
  

def _teacher_caption(teacher: Teacher) -> str:  
    specialization = ",".join([spec.name for spec in teacher.specializations])  
    return f"{teacher.full_name}\n{specialization}\n\n{teacher.about}"  
  

def _is_teacher_list_view_needed(incoming_event: str) -> bool:  
    return incoming_event == "teachers_list"  
  

def _is_teacher_info_view_needed(incoming_event: str) -> bool:  
    return incoming_event == "teachers_info"  


def _is_specializtion_list_view_needed(incoming_event: str) -> bool:  
    return incoming_event in ["specializations_list", "specializations_from_teacher"]
  

def _is_specialization_info_view_needed(incoming_event: str) -> bool:  
    return incoming_event == "specializations_info"
```

## п.2
Назначение кода, приведенного выше - в том, чтобы в зависимости от входящего события дать соответствующего реакцию системы. Код дизайну в целом соответствует, если посмотреть на код подольше. Сильно напрашивается другой код, который сходу даст понимание дизайна системы и упростит расширение и поддержку.
## п.3
##Исправленная версия примера 1:
```python
from enum import Enum  
  
class HandlerInterface(abc.ABC):  
    """Интерфейс обработчиков нажатия на кнопки"""  
  
    def __init__(  
        self,  
        bot: TeleBot,  
        logger: Logger,  
    ):  
        """Конструктор обработчика."""  
        self._bot = bot  
        self._logger = logger  
  
    def take_event(  
        self,  
        chat_id: int,  
        event_data: str,  
    ) -> None:  
        """Обработка нажатия кнопки от пользователя."""  
        if not self.can_handle_event(event_data):  
            self._logger.debug(  
                "Для %s отсутствует зарегистрированное событие %s",  
                str(type(self)),  
                event_data,  
            )  
            return None  
        return self._handle(  
            chat_id=chat_id,  
            event_data=event_data,  
        )  

	@abc.abstractmethod
	def _handle(self, chat_id: int, event_data: CallbackData):
		"""Обработать событие."""
  
    @abc.abstractmethod  
    def can_handle_event(self, event_data: CallbackData) -> bool:  
        """Проверка возможности обработать событие."""

  
class SpecializationsHandlingEvents(str, Enum):  
	"""Множество событий в домене специализаций."""
  
    LIST = "specializations_list"  
    INFO = "specialization"  
    FROM_TEACHER = "specializations_from_teacher"


class SpecializationsHandler(HandlerInterface):  
    def _handle(  
        self,  
        chat_id: int,  
        event_data: CallbackData,  
    ) -> None:  
		...
  
    def can_handle_event(self, event_data: CallbackData) -> bool:  
        event = json.loads(event_data)["event"]  
        return event in [  
            SpecializationsHandlingEvents.LIST,  
            SpecializationsHandlingEvents.FROM_TEACHER,  
            SpecializationsHandlingEvents.INFO,  
        ]


class TeacherHandlingEvents(str, Enum):  
	"""Множество событий в домене учителей"""  
	LIST = "teachers_list"  
	INFO = "teacher"


class TeachersHandler(HandlerInterface):  
	def _handle(  
		self,  
		chat_id: int,  
		event_data: CallbackData,  
	) -> None:  
		...

	def can_handle_event(self, event_data: CallbackData) -> bool:  
		event = json.loads(event_data)["event"]  
		return event in [  
			TeacherHandlingEvents.LIST,  
			TeacherHandlingEvents.INFO,  
		]


class HandlerOrchestrator:  
    """Распределитель запросов между обработчиками нажатия кнопок"""  
  
    def __init__(  
        self,  
        handlers: list[HandlerInterface],  
        logger: Logger,  
    ):  
        """Конструктор оркестратора."""  
        self._handlers = handlers  
        self._logger = logger  
  
    def notify_handler(  
        self,  
        chat_id: int,  
        event_data: str,  
    ) -> None:  
        """"""  
        self._logger.debug(  
            "Получено пользовательское событие '%s'",  
            event_data,  
        )  
        for handler in self._handlers:  
            handler.take_event(  
                chat_id=chat_id,  
                event_data=event_data,  
            )  


def build_handlers_orch(
	bot: TeleBot,
	logger: Logger,
) -> HandlerOrchestrator:  
    teacher_handler = TeachersHandler(  
        logger=logger,  
        bot=bot,  
    )  
    activities_handler = SpecializationsHandler(  
        logger=logger,  
        bot=bot,  
    )  
	# Добавляем новый обработчик
    # lessons_handler = LessonsHandler(  
    #    logger=logger,  
    #    bot=bot,  
    #)  
    orch = HandlerOrchestrator(  
        handlers=[  
            teacher_handler,  
            activities_handler,  
            # lessons_handler,  
        ],  
        logger=logger,  
    )  
    return orch
```

Итерация заняла ~40-50 минут.

# Пример 2.
```python
```

## п.2

## п.3
**Исправленая версия примера 2:
```python
```
