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
**Исправленная версия примера 1:**
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
from enum import Enum  
import json  
  
from src.app.infrastructure.db import session_factory  
from src.app.infrastructure.db.models import CallbackData, Teacher  
from src.app.infrastructure.db.repos.callback_data import CallbackDataRepo  
from src.app.infrastructure.db.repos.teachers import TeachersRepo  
from src.app.menu import lessons as menu_builder  
from src.app.types.events import LessonsHandlingEvents  
  
from .base import HandlerInterface  


  
  
class LessonsHandlingEvents(str, Enum):  
    """Множество событий в доменной области 'Занятия'"""  
  
    CHOICE_DAY = "choice_day"  
    CHOICE_TIME = "choice_time"
    SIGNUP_CONFIRM = "signup_confirm"  
    SIGNUP_NO_CONFIRM = "signup_no_confirm"  
    SIGNUP_END = "signup_end"
  
  
class LessonsHandler(HandlerInterface):  
    def handle(  
        self,  
        chat_id: int,  
        event_data: str,  
    ) -> None:  
        event_data = json.loads(event_data)  
        incoming_event = event_data["event"]  
        self._logger.debug(  
            "%s: Обработчик вызван для события %s",  
            str(type(self)),  
            incoming_event,  
        )  
        if self._is_choice_day(incoming_event):  
            with session_factory() as session:  
                teacher_id = event_data["teacher_id"]  
                callback_data = CallbackData(teacher_id=teacher_id)  
                repo = CallbackDataRepo(session)  
                repo.create(callback_data)  
                session.commit()  
                markup = menu_builder.build_days_for_sign_up(callback_data.id)  
                self._bot.send_message(  
                    chat_id,  
                    "Выберете день",  
                    reply_markup=markup,  
                )  
  
            return  
  
        if self._is_choice_time(incoming_event):  
            print(event_data)  
            with session_factory() as session:  
                repo = CallbackDataRepo(session)  
                cb_data = repo.get_by_id(event_data["cb_id"])  
                cb_data.day = event_data["day"]  
                repo.update(cb_data)  
                session.commit()  
                markup = menu_builder.build_hours_for_sign_up(cb_id=cb_data.id)  
                self._bot.send_message(  
                    chat_id,  
                    "Выберете время",  
                    reply_markup=markup,  
                )  
                return  
  
        if self._is_signup_end(incoming_event):  
            print(event_data)  
            with session_factory() as session:  
                repo = CallbackDataRepo(session)  
                cb_data = repo.get_by_id(event_data["cb_id"])  
                cb_data.time = event_data["time"]  
                repo.update(cb_data)  
                session.commit()  
                teachers_repo = TeachersRepo(session)  
                teacher = teachers_repo.get_by_id(cb_data.teacher_id)  
                self._bot.send_message(  
                    chat_id,  
                    f"Уведомление о записи на занятие отправлено менеджеру и будет принято после оплаты.\n"  
                    "Оплатите занятие любым удобным для вас способом из ниже перечисленных: "                    f"{teacher.detail.payments}",  
                )  
                manager = teachers_repo.get_manager()  
                self._send_request_for_lesson_registration_to_manager(  
                    manager=manager,  
                    teacher=teacher,  
                    cb_data=cb_data,  
                )  
            return  
        if self._is_signup_confirm(incoming_event):  
            with session_factory() as session:  
                cb_data_repo = CallbackDataRepo(session)  
                cb_data = cb_data_repo.get_by_id(event_data["cb_id"])  
                teachers_repo = TeachersRepo(session)  
                teacher = teachers_repo.get_by_id(cb_data.teacher_id)  
                self._notify_user_about_confirm(  
                    chat_id=chat_id,  
                    teacher=teacher,  
                )  
                self._notify_teacher_about_confirm(  
                    teacher=teacher,  
                    cb_data=cb_data,  
                    user="Симпотичный Дима",  
                )  
            return  
  
    def can_handle_event(self, event_data: str) -> bool:  
        event_data = json.loads(event_data)  
        event = event_data["event"]  
        return event in [  
            LessonsHandlingEvents.CHOICE_DAY,  
            LessonsHandlingEvents.CHOICE_TIME,  
            LessonsHandlingEvents.SIGNUP_END,  
            LessonsHandlingEvents.SIGNUP_CONFIRM,  
        ]  
  
    def _send_request_for_lesson_registration_to_manager(  
        self,  
        manager: Teacher,  
        teacher: Teacher,  
        cb_data: CallbackData,  
    ) -> None:  
        markup = menu_builder.build_manager_confirm_registration(  
            manager=manager,  
            callback_data_id=cb_data.id,  
        )  
        txt = (  
            "Новая запись! Проверьте оплату и подтвердите регистрацию!"  
            f"Учитель: {teacher.full_name}"  
            f"Ученик: {teacher.full_name}"  
            f"Дата и время записи: {cb_data.date_time}"  
        )  
        self._bot.send_message(  
            manager.chat_id,  
            text=txt,  
            reply_markup=markup,  
        )  
  
    def _notify_user_about_confirm(  
        self,  
        chat_id: int,  
        teacher: Teacher,  
    ) -> None:  
        """"""  
        self._bot.send_message(  
            chat_id=chat_id,  
            text="Ваша запись подтверждена менеджером!\n"
            "Пожалуйста, напишите преподавателю сообщение,
	        " чтобы он был в курсе, что вы точно человек :)"
			f"Преподаватель в телеграмме: {teacher.tg_username}",
        )  
  
    def _notify_teacher_about_confirm(  
        self,  
        teacher: Teacher,  
        cb_data: CallbackData,  
        user: str,  
    ) -> None:  
        txt = f"Новая запись!" 
        f"На урок записан {user}"
        f"Дата и время записи: {cb_data.date_time}"  
        self._bot.send_message(  
            teacher.chat_id,  
            text=txt,  
        )  
  
    @staticmethod  
    def _is_choice_day(incoming_event: str) -> bool:  
        return incoming_event == LessonsHandlingEvents.CHOICE_DAY  
  
    @staticmethod  
    def _is_choice_time(incoming_event: str) -> bool:  
        return incoming_event == LessonsHandlingEvents.CHOICE_TIME  
  
    @staticmethod  
    def _is_signup_end(incoming_event: str) -> bool:  
        return incoming_event == LessonsHandlingEvents.SIGNUP_END  
  
    @staticmethod  
    def _is_signup_confirm(incoming_event: str) -> bool:  
        return incoming_event == LessonsHandlingEvents.SIGNUP_CONFIRM
```

## п.2
Код выше добавляет обработчик событий, связанных с доменной областью "Занятия". Правильный дизайн для кода - класс LessonsHandler станет "медиатором" для конкретных событий в данной доменной области. В первом примере мы можем добавить доменную область, для обработки нового семейства событий, в этом же кусочке кода основная идея в добавлении логики для конкретного события в доменной области. Текущий код дизайну не соответствует.
## п.3
**Исправленная версия примера 2:
```python
from enum import Enum  
import json  
  
from src.app.infrastructure.db import session_factory  
from src.app.infrastructure.db.models import CallbackData, Teacher  
from src.app.infrastructure.db.repos.callback_data import CallbackDataRepo  
from src.app.infrastructure.db.repos.teachers import TeachersRepo  
from src.app.menu import lessons as menu_builder  
from src.app.types.events import LessonsHandlingEvents  
  
from .base import HandlerInterface


class ActionHandlerInterface(abc.ABC):
    """Интерфейс обработчика действия пользователя."""

	@abc.abstractmethod
	def handle(
		bot: Telebot,
		chat_id: int,  
        action_data: ActionData,  
	) -> None:
	"""Обработать действие пользователя."""


class DomainHandlerInterface(abc.ABC):  
    """Интерфейс обработчиков событий/действий доменных областей."""  
  
	# дополним конструктор базового класса обработчиков
    def __init__(  
        self,  
        bot: TeleBot,  
        logger: Logger,
        action_handlers_mapper: Dict[str, EventHadlerInterface] 
    ):  
        """Конструктор обработчика."""  
        self._bot = bot  
        self._logger = logger  
		self._handlers_mapper = action_handlers_mapper
  
    def take_event(  
        self,
        chat_id: int,
        action_data: ActionData,
    ) -> None:
        """Обработка доменного пользовательского события."""
		action_type = action_data.type
		handler = self._handlers_mapper.get(
			action_data.type,
		)
        if not handler:
            self._logger.debug(
                "Для %s отсутствует обработчик для события %s",
                str(type(self)),
                action_type,
            )  
            return None  
        return handler.handle(
			bot=self._bot,
            chat_id=chat_id,
            action_data=action_data,
        )  


class LessonDayChoiceActionHandler(ActionHandlerInterface):
	"""Обработчик действия выбора дня для занятия."""
	
	def handle(
        self,  
        chat_id: int,  
        action_data: str,  
	) -> None:
		with session_factory() as session:  
			teacher_id = event_data["teacher_id"]  
			callback_data = CallbackData(teacher_id=teacher_id)  
			repo = CallbackDataRepo(session)  
			repo.create(callback_data)  
			session.commit()  
			markup = menu_builder.build_days_for_sign_up(callback_data.id)  
			self._bot.send_message(  
				chat_id,
				"Выберете день",
				reply_markup=markup,
			)
		return  

class LessonTimeChoiceActionHandler(ActionHandlerInterface):
	"""Обработчик действия выбора времени для занятия."""
	
	def handle(
        self,  
        chat_id: int,  
        action_data: ActionData,  
	) -> None:
        with session_factory() as session:
            repo = CallbackDataRepo(session)
            cb_data = repo.get_by_id(action_data.cb_id)
            cb_data.day = action_data.time
            repo.update(cb_data)
            session.commit()
            markup = menu_builder.build_hours_for_sign_up(cb_id=cb_data.id)
		    self._bot.send_message(
		        chat_id,  
		        "Выберете время",  
		        reply_markup=markup,  
		    )  
		    return


class LessonSignUpEndActionHandler(ActionHandlerInterface):
	"""Обработчик действия окончания процесса записи на занятие."""
	
	def handle(
        self,
        chat_id: int,
        action_data: ActionData,
	) -> None:
        with session_factory() as session:  
            repo = CallbackDataRepo(session)  
            cb_data = repo.get_by_id(action_data.cb_id)  
            cb_data.time = action_data.time
            repo.update(cb_data)  
            session.commit()  
            teachers_repo = TeachersRepo(session)  
            teacher = teachers_repo.get_by_id(cb_data.teacher_id)  
            self._bot.send_message(  
                chat_id,  
                f"Уведомление о записи на занятие отправлено менеджеру и будет принято после оплаты.\n"  
                "Оплатите занятие любым удобным для вас способом из ниже перечисленных: \n"
                f"{teacher.detail.payments}",
            )
            manager = teachers_repo.get_manager()
		    self._send_request_for_lesson_registration_to_manager(
                manager=manager,
                teacher=teacher,
                cb_data=cb_data,
            )  
		return


class LessonConfirmActionHandler(ActionHandlerInterface):
	"""Обработчик действия подтверждения менеджером записи на занятие."""
	
	def handle(
        self,  
        chat_id: int,  
        action_data: ActionData,  
	) -> None:
        with session_factory() as session:  
            cb_data_repo = CallbackDataRepo(session)
            cb_data = cb_data_repo.get_by_id(action_data.cb_id)
            teachers_repo = TeachersRepo(session)
            teacher = teachers_repo.get_by_id(cb_data.teacher_id)
            self._notify_user_about_confirm(
                chat_id=chat_id,
                teacher=teacher,  
			)
            self._notify_teacher_about_confirm(
                teacher=teacher,
                cb_data=cb_data,
                user="Симпотичный Дима",  
			)
		return  


class LessonsHandlingEvents(str, Enum):  
    """Множество событий в доменной области 'Занятия'"""  
  
    CHOICE_DAY = "choice_day"  
    CHOICE_TIME = "choice_time"
    SIGNUP_CONFIRM = "signup_confirm"  
    SIGNUP_NO_CONFIRM = "signup_no_confirm"  
    SIGNUP_END = "signup_end"

  
class LessonsDomainHandler(DomainHandlerInterface):  
	"""Обработчик действий/событий в доменной области 'Занятия' """


def build_lessons_domain_handler(
	bot: Telebot,
	logger: Logger,								 
) -> LessonsDomainHandler:
    return LessonsDomainHandler(
		bot=bot,
		logger=logger,
		action_handlers_mapper={
            LessonsHandlingEvents.CHOICE_DAY.value = LessonDayChoiceActionHandler
            LessonsHandlingEvents.CHOICE_TIME.value = LessonTimeChoiceActionHandler,
            LessonsHandlingEvents.SIGNUP_END.value = LessonSignUpEndActionHandler,
            LessonsHandlingEvents.SIGNUP_CONFIRM.value = LessonConfirmActionHandler,
        }
	)
```
Итерация заняла ~80-100 минут.

# Пример 3
```python
```
## п.2

## п.3 
**Исправленная версия примера 3:

```python
```

Итерация заняла ~80-100 минут.
