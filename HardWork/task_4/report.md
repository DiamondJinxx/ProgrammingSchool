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
        if self._is_specialization_list_view_needed(incoming_event):  
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
import logging
from datetime import datetime
from typing import Sequence

from app import crud
from app.core.constants import AMP_CREATION_SOURCE, ST_AGENT_ACTIVE
from app.handlers.common import get_async_session
from app.schemas.v2.broker import (
    ComputerHardwareRMQSchema,
    ComputerInventoryRMQReceivedSchema,
    HeadersRMQSchema,
)
from app.schemas.v2.broker.computer_software import ComputerSoftwareRMQSchema
from app.schemas.v2.crud import (
    ComputerCRUDCreateSchema,
    ComputerHardwareCRUDCreateSchema,
    ComputerHardwareCRUDGeneralSchema,
    ComputerToInvPackCRUDCreateSchema,
    InventoryPackageCRUDCreateSchema,
)
from app.utils.v2 import computer_license_recalc

logger = logging.getLogger("default")


async def computer_inventory_received(
        data: ComputerInventoryRMQReceivedSchema,
        headers: HeadersRMQSchema = None,  # noqa: ARG001
) -> None:
    """Получены данные программной и аппаратной инвентаризаций целевого компьютера."""
    await _process_hardware_inventory(
        hostname=data.hostname,
        update_date=data.last_modified_date,
        data=data.hardware
    )
    await _process_software_inventory(
        hostname=data.hostname,
        packages=data.software,
    )


async def _process_hardware_inventory(
        hostname: str,
        update_date: datetime,
        data: ComputerHardwareRMQSchema
) -> None:
    """Обработка аппаратной инвентаризации"""
    async with get_async_session() as async_session:
        computer_mdl = await crud.v2.computer.select_one(
            async_session=async_session,
            hostname=hostname,
            deleted=False,
        )

        if not computer_mdl:
            computer_mdl = await crud.v2.computer.insert(
                async_session=async_session,
                obj_in=ComputerCRUDCreateSchema(
                    hostname=hostname,
                    creation_source=AMP_CREATION_SOURCE,
                ),
            )

        if not computer_mdl:
            return

        hardware_data = ComputerHardwareCRUDCreateSchema(
            **data.model_dump(),
            update_date=update_date,
            general=ComputerHardwareCRUDGeneralSchema.model_validate(
                data.hardware_general
            ),
        )

        await crud.v2.computer_hard.insert(
            async_session=async_session,
            computer_uid=computer_mdl.uid,
            obj_in=hardware_data,
        )
        await crud.v2.computer.set_status(
            async_session=async_session,
            obj_id=computer_mdl.uid,
            status=ST_AGENT_ACTIVE,
        )
        await computer_license_recalc(
            async_session=async_session,
            computer_mdl=computer_mdl,
        )
        await async_session.commit()


async def _process_software_inventory(
        hostname: str,
        packages: Sequence[ComputerSoftwareRMQSchema]
) -> None:
    """Обработка программной инвентаризации"""
    async with get_async_session() as async_session:
        computer_mdl = await crud.v2.computer.select_one(
            async_session=async_session,
            hostname=hostname,
            deleted=False,
        )
        if not computer_mdl:
            return

        await computer_mdl.awaitable_attrs.inv_packages
        computer_mdl.inv_packages.clear()

        for package_info in packages:
            inventory_package = await crud.v2.inventory_package.select_one(
                async_session=async_session,
                name=package_info.name,
                version=package_info.version,
                arch=package_info.arch,
            )
            if not inventory_package:
                inv_package_obj_in = InventoryPackageCRUDCreateSchema(
                    name=package_info.name,
                    version=package_info.version,
                    arch=package_info.arch,
                )
                inventory_package = await crud.v2.inventory_package.insert(
                    async_session=async_session,
                    obj_in=inv_package_obj_in,
                )
                if not inventory_package:
                    logger.warning(
                        "Запись inventory_package не создана: %s",
                        inv_package_obj_in.model_dump_json(),
                    )
                    continue

            await crud.v2.computer_to_inventory_package.insert(
                async_session=async_session,
                obj_in=ComputerToInvPackCRUDCreateSchema(
                    computer_uid=computer_mdl.uid,
                    inv_pack_uid=inventory_package.uid,
                    install_date=package_info.install_date,
                ),
            )

        await async_session.commit()
```
## п.2
Выше приведен пример кода для обработки поступления информации о компьютера - об аппаратных составляющий и об установленных программах. Дизайн кода подразумевает доменное разделение, но в данном случае код болтается в воздухе. Большая цикломатическая сложность небольшой беспорядок. В системе нет другой информации о компьютере - аппаратная и программные части хранят в себе всю информацию о составляющих компьютера - поэтому добавление новых "обработчиков" не требуется, и я предпочту внедрить сервисный слой(поправив так же архитектуру сервиса в целом, внедрив слои инфраструктуры и выделив агрегатные модели) с максимально глупым интерфейсом.

## п.3 
**Исправленная версия примера 3:

```python
import logging
from typing import List, Optional

from acm_lib_message_broker import schemas

from modules import types
from modules.utils.datetime_tz import aware_now, init_utc_tz
from modules.web.app.aggregators.models.v2 import (
    ComputerInventory,
    InventoryPackage,
)
from modules.web.app.infrastructure.rmq.adapters.v2.computers import AbstractComputersRMQAdapter
from modules.web.app.infrastructure.rmq.adapters.v2.groups.interface import AbstractGroupsRMQAdapter

from . import exceptions
from .unit_of_work import AbstractComputerInventorySystemUnitOfWork


class ComputerInventorySystemService:
    """Системный сервис инвентаризации."""

    def __init__(
        self,
        unit_of_work: AbstractComputerInventorySystemUnitOfWork,
        rmq_adapter: AbstractComputersRMQAdapter,
        rmq_groups_adapter: AbstractGroupsRMQAdapter,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Конструктор сервиса инвентаризации.

        Args:
            unit_of_work: Объект шаблона Единица работы.
            rmq_adapter: Адаптер для RMQ.
            rmq_groups_adapter: Адаптер для RMQ для событий групп.
            logger: Логгер.
        """
        self._uow = unit_of_work
        self._rmq = rmq_adapter
        self._rmq_groups = rmq_groups_adapter
        self._logger = logger or logging.getLogger("default")

    async def _get_or_create_computer(
        self,
        uow: AbstractComputerInventorySystemUnitOfWork,
        hostname: types.Hostname,
        segment_uid: types.SegmentUID,
    ) -> ComputerInventory:
        """
        Получить или создать модель целевого компьютера с инвентаризацией.

        Args:
            uow: Единица работы для сервиса инвентаризации
            hostname: Сетевое имя целевого компьютера.
            segment_uid: ID сегмента, к которому принадлежит агент компьютера.

        Returns:
            Модель целевого компьютера с инвентаризацией.
        """
        computer_agg = await uow.computers_repo.get_by_hostname(hostname)

        if not computer_agg:
            directory = await uow.directories_repo.get_default_directory()
            computer_agg = ComputerInventory.create(
                hostname=hostname,
                mac_address=None,
                comment=None,
                created_by=None,
                create_date=aware_now(),
                directory=directory,
            )
            computer_agg.set_agent_active(aware_now())
            computer_agg.set_agent_segment(segment_uid=segment_uid, update_date=aware_now())
            await uow.computers_repo.create(computer_agg)
            await uow.commit()
            await self._rmq.send_created_message(computer_agg.computer)
            await self._rmq_groups.send_computer_added_message(directory, computer_agg.computer)
        else:
            computer_agg.set_agent_active(aware_now())
            computer_agg.set_agent_segment(segment_uid=segment_uid, update_date=aware_now())
            await uow.computers_repo.update(computer_agg)

        return computer_agg

    async def _take_software(
        self,
        uow: AbstractComputerInventorySystemUnitOfWork,
        computer: ComputerInventory,
        software: List[schemas.ComputerSoftwareSchema],
    ) -> None:
        """
        Провести программную инвентаризацию.

        Args:
            uow: Единица работы для сервиса инвентаризации
            computer: Модель целевого компьютера с инвентаризацией.
            hostname: Сетевое имя целевого компьютера.
            software: Данные программной инвентаризации
        """
        computer.unlink_all_inv_packages()
        for package_info in software:
            inventory_package = await uow.inv_packages_repo.get_by_unique_fields(
                name=package_info.name,
                version=package_info.version,
                arch=package_info.arch,
            )
            if not inventory_package:
                inventory_package = InventoryPackage.create(
                    name=package_info.name,
                    version=package_info.version,
                    arch=package_info.arch,
                )
                await uow.inv_packages_repo.create(inventory_package)
            computer.link_inv_package(
                inv_package_uid=inventory_package.uid,
                install_date=init_utc_tz(package_info.install_date) if package_info.install_date else None,
            )

    async def _take_hardware(
        self,
        computer: ComputerInventory,
        hardware: schemas.ComputerHardwareSchema,
    ) -> None:
        """
        Провести аппаратную инвентаризацию.

        Args:
            uow: Единица работы для сервиса инвентаризации
            computer: Модель целевого компьютера с инвентаризацией.
            hardware: Данные аппаратной инвентаризации
        """
        update_date = aware_now()
        computer.set_hardware(
            update_date=update_date,
            system=types.ComputerHardwareSystem.model_validate(hardware.system) if hardware.system else None,
            salt=types.ComputerHardwareSalt.model_validate(hardware.salt) if hardware.salt else None,
            general=types.ComputerHardwareGeneral.model_validate(hardware.general) if hardware.general else None,
            memory=types.ComputerHardwareMemory.model_validate(hardware.memory) if hardware.memory else None,
            cpu=types.ComputerHardwareCPU.model_validate(hardware.cpu) if hardware.cpu else None,
            disk=types.ComputerHardwareDisk.model_validate(hardware.disk) if hardware.disk else None,
            lvm=types.ComputerHardwareLVM.model_validate(hardware.lvm) if hardware.lvm else None,
            volume=types.ComputerHardwareVolume.model_validate(hardware.volume) if hardware.volume else None,
            network=types.ComputerHardwareNetwork.model_validate(hardware.network) if hardware.network else None,
            dns=types.ComputerHardwareDNS.model_validate(hardware.dns) if hardware.dns else None,
            gpu=types.ComputerHardwareGPU.model_validate(hardware.gpu) if hardware.gpu else None,
            monitor=types.ComputerHardwareMonitor.model_validate(hardware.monitor) if hardware.monitor else None,
        )

    async def take_inventory(
        self,
        hostname: types.Hostname,
        segment_uid: types.SegmentUID,
        software: Optional[List[schemas.ComputerSoftwareSchema]],
        hardware: Optional[schemas.ComputerHardwareSchema],
    ) -> None:
        """
        Провести инвентаризацию.

        Args:
            hostname: Сетевое имя целевого компьютера.
            segment_uid: ID сегмента, к которому принадлежит агент компьютера.
            software: данные программной инвентаризации
            hardware: данные аппаратной инвентаризации
        """
        if not hardware and not software:
            msg = f'Данные инвентаризации для компьютера "{hostname}" отсутствуют.'
            raise exceptions.ComputerInventoryRequiredError(msg)

        async with self._uow as uow:
            computer = await self._get_or_create_computer(uow=uow, hostname=hostname, segment_uid=segment_uid)
            if not computer:
                return

            if software:
                await self._take_software(uow=uow, computer=computer, software=software)
            else:
                computer.unlink_all_inv_packages()

            if hardware:
                await self._take_hardware(computer=computer, hardware=hardware)
            else:
                computer.clear_hardware()

            computer.set_agent_interaction_date(aware_now())

            await uow.computers_repo.update(computer)
            await uow.commit()

    async def take_hardware(
        self,
        hostname: types.Hostname,
        segment_uid: types.SegmentUID,
        hardware: schemas.ComputerHardwareSchema,
    ) -> None:
        """
        Провести аппаратную инвентаризацию.

        Args:
            hostname: Сетевое имя целевого компьютера.
            segment_uid: ID сегмента, к которому принадлежит агент компьютера.
            hardware: данные аппаратной инвентаризации.
        """
        async with self._uow as uow:
            computer = await self._get_or_create_computer(uow=uow, hostname=hostname, segment_uid=segment_uid)
            if not computer:
                return

            await self._take_hardware(computer=computer, hardware=hardware)
            computer.set_agent_interaction_date(aware_now())

            await uow.computers_repo.update(computer)
            await uow.commit()

    async def take_software(
        self,
        hostname: types.Hostname,
        segment_uid: types.SegmentUID,
        software: List[schemas.ComputerSoftwareSchema],
    ) -> None:
        """
        Провести аппаратную инвентаризацию.

        Args:
            hostname: Сетевое имя целевого компьютера.
            segment_uid: ID сегмента, к которому принадлежит агент компьютера.
            software: данные программной инвентаризации.
        """
        async with self._uow as uow:
            computer = await self._get_or_create_computer(uow=uow, hostname=hostname, segment_uid=segment_uid)
            if not computer:
                return

            await self._take_software(uow=uow, computer=computer, software=software)
            computer.set_agent_interaction_date(aware_now())

            await uow.computers_repo.update(computer)
            await uow.commit()

```

Итерация заняла ~120-180 минут.
