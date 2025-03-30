### Пример 1.1
```python

class Directory:
    ...
    childrens: list[Self]

    @property
    def is_leaf(self) -> bool:
        return not self.childrens

# в тестах
def test_add_children_directory() -> None:
    """Тест добавления дочерних директорий"""
    directory = DirectoryFactory()
    childrens = [ DirectoryFactory() for i in range(5)]
    directory.add_childrens(childrens)
    assert childrens == directory.childrens
    assert not directory.is_leaf

```
###  1.1 Исправленная версия
```python

class Directory:
    ...
    childrens: list[Self]

# Нигде в бизнес логике не используется данный метод, собственно тут целесообразно его полностью удалить
def test_add_children_directory() -> None:
    """Тест добавления дочерних директорий"""
    directory = DirectoryFactory()
    childrens = [ DirectoryFactory() for i in range(5)]
    directory.add_childrens(childrens)
    assert childrens == directory.childrens

```
### Пример 1.2
###  1.2 Исправленная версия
### Пример 1.3
```python
async def handle(
	self,
	segment_uid: apps_types.SegmentUID,
	server_hostname: apps_types.Hostname | None,
	server_mac_address: apps_types.MacAddress | None,
	server_ip_address: apps_types.IPAddress | None,
	server_port: apps_types.Port,
) -> apps_types.ServerUID:
	"""
	Синхронизировать данные по сегментному серверу репозиториев.

	Args:
		segment_uid: UID сегмента, к которому привязывается сервер
		server_hostname: имя хоста сервера
		server_mac_address: mac адрес сервера
		server_ip_address: ip адрес хоста сервера
		server_port: Сетевой порт сервера
	"""

```
###  1.3 Исправленная версия
```python
async def handle(
	self,
	segment_uid: apps_types.SegmentUID,
	# Объединил все, что относится к системной информации сервера в класс
	server_system_info: ServerSystemInfo,
) -> apps_types.ServerUID:
	"""
	Синхронизировать данные по сегментному серверу репозиториев.

	Args:
		segment_uid: UID сегмента, к которому привязывается сервер
		server_system_info: Системная информация серверa.
	"""
```
### Пример 1.4
```python
def aware_now() -> dt.datetime:
    """Получить текущую "безопасную" дату со временем по UTC с явно указанной временной зоной UTC."""
    return dt.datetime.now(tz=dt.UTC)

# в другом файле
def now_with_tz() -> dt.datetime:
    """Получить текущую дату со временем по UTC с явно указанной временной зоной UTC."""
    return dt.datetime.now(tz=dt.UTC)
```
###  1.4 Исправленная версия
```python
# оставим только одну реализацию, с более подходящим именем
def aware_now() -> dt.datetime:
    """Получить текущую "безопасную" дату со временем по UTC с явно указанной временной зоной UTC."""
    return dt.datetime.now(tz=dt.UTC)
```
### Пример 1.5
```python
@router.post(
    "/",
    summary="Запрос на создание объекта компьютер",
    description="Добавление целевого компьютера",
)
async def create_computer(
    item_in: schemas.ComputerCreateSchema,
    user: Annotated[UserInfo, Depends(get_user_info)],
    response: Response,
) -> BaseResponseSchema[q_schemas.ComputerDetailsSchema | None]:
    """
    Создание Целевого компьютера.

    Args:
        item_in: Входные параметры, необходимые для создания Целевого компьютера.
        user: Информация об авторизованном пользователе.
        response: Объект ответа.
    """
    computer_service = deps.build_service(user.uid)
    new_computer = await computer_service.create(
        created_by=user.login,
        **item_in.model_dump(),
    )

    async with async_session_factory() as session:
        queries = deps.build_queries(session=session, user_uid=user.uid)
        etag_value, new_computer_query_model = await queries.get_by_uid(new_computer.uid)

    enrich_etag_headers(response, etag_value)
    return BaseResponseSchema(content=new_computer_query_model)

# в другом файле
class ComputersUserService:
    """Пользовательский сервис целевых компьютеров, обремененный контроллером прав доступа."""

    def __init__(
        self,
        unit_of_work: AbstractComputersUserUnitOfWork,
        rmq_adapter: AbstractComputersRMQAdapter,
        rmq_groups_adapter: AbstractGroupsRMQAdapter,
    ) -> None:
        """
        Конструктор сервиса Целевых компьютеров.

        Args:
            unit_of_work: Объект шаблона Единица работы.
            rmq_adapter: Адаптер для RMQ.
            rmq_groups_adapter: Адаптер для RMQ для событий групп.
        """
        self._uow = unit_of_work
        self._rmq = rmq_adapter
        self._rmq_groups = rmq_groups_adapter

    async def create(
        self,
        hostname: apps_types.FQDN,
        created_by: apps_types.UserLogin,
        directory_uid: apps_types.DirectoryUID,
        mac_address: apps_types.MacAddress | None = None,
        comment: apps_types.Comment | None = None,
    ) -> apps_types.ComputerUID:
        """
        Создать компьютер.

        Args:
            hostname: Доменное имя нового компьютера.
            created_by: Кем создан компьютер.
            directory_uid: Идентификатор директории, в которую будет помещён компьютер. Если None, то компьютер
                будет создан в директории по умолчанию.
            mac_address: MAC-адрес нового компьютера.
            comment: Комментарий к новому компьютеру.

        Raises:
            exceptions.ComputerAlreadyExistsError: Компьютер с таким доменным именем уже существует.
            dir_exceptions.DirectoryNotExistsError: Указанной директории не существует.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_create()
            await uow.access_controller.raise_if_cannot_update(uid=directory_uid)

            computer_agg = await uow.computers_repo.get_by_fqdn(hostname)
            if computer_agg:
                msg = f'Компьютер с доменным именем "{hostname}" уже существует.'
                raise exceptions.ComputerAlreadyExistsError(msg)

            directory = await uow.directories_repo.get_by_uid(uid=directory_uid)
            if not directory:
                msg = f'Директории с идентификатором "{directory_uid}" не существует.'
                raise dir_exceptions.DirectoryNotExistsError(msg)

            await uow.access_controller.raise_if_cannot_update(uid=directory.uid)

            computer_agg = ComputerDirectory.create(
                fqdn=hostname,
                directory=directory,
                mac_address=mac_address,
                comment=comment,
                create_date=aware_now(),
                created_by=created_by,
            )
            await uow.computers_repo.create(computer=computer_agg)
            await uow.commit()

        return computer_agg.computer
```
###  1.5 Исправленная версия
```python
@router.post(
    "/",
    summary="Запрос на создание объекта компьютер",
    description="Добавление целевого компьютера",
)
async def create_computer(
    item_in: schemas.ComputerCreateSchema,
    user: Annotated[UserInfo, Depends(get_user_info)],
    response: Response,
) -> BaseResponseSchema[q_schemas.ComputerDetailsSchema | None]:
    """
    Создание Целевого компьютера.

    Args:
        item_in: Входные параметры, необходимые для создания Целевого компьютера.
        user: Информация об авторизованном пользователе.
        response: Объект ответа.
    """
    computer_service = deps.build_service(user.uid)
	# запрашиваем только нужный uid
    new_computer_uid = await computer_service.create(
        created_by=user.login,
        **item_in.model_dump(),
    )

    async with async_session_factory() as session:
        queries = deps.build_queries(session=session, user_uid=user.uid)
        etag_value, new_computer = await queries.get_by_uid(new_computer.uid)

    enrich_etag_headers(response, etag_value)
    return BaseResponseSchema(content=new_computer)

# в другом файле
class ComputersUserService:
    """Пользовательский сервис целевых компьютеров, обремененный контроллером прав доступа."""

    def __init__(
        self,
        unit_of_work: AbstractComputersUserUnitOfWork,
        rmq_adapter: AbstractComputersRMQAdapter,
        rmq_groups_adapter: AbstractGroupsRMQAdapter,
    ) -> None:
        """
        Конструктор сервиса Целевых компьютеров.

        Args:
            unit_of_work: Объект шаблона Единица работы.
            rmq_adapter: Адаптер для RMQ.
            rmq_groups_adapter: Адаптер для RMQ для событий групп.
        """
        self._uow = unit_of_work
        self._rmq = rmq_adapter
        self._rmq_groups = rmq_groups_adapter

    async def create(
        self,
        hostname: apps_types.FQDN,
        created_by: apps_types.UserLogin,
        directory_uid: apps_types.DirectoryUID,
        mac_address: apps_types.MacAddress | None = None,
        comment: apps_types.Comment | None = None,
    ) -> apps_types.ComputerUID:
        """
        Создать компьютер.

        Args:
            hostname: Доменное имя нового компьютера.
            created_by: Кем создан компьютер.
            directory_uid: Идентификатор директории, в которую будет помещён компьютер. Если None, то компьютер
                будет создан в директории по умолчанию.
            mac_address: MAC-адрес нового компьютера.
            comment: Комментарий к новому компьютеру.

        Raises:
            exceptions.ComputerAlreadyExistsError: Компьютер с таким доменным именем уже существует.
            dir_exceptions.DirectoryNotExistsError: Указанной директории не существует.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_create()
            await uow.access_controller.raise_if_cannot_update(uid=directory_uid)

            computer_agg = await uow.computers_repo.get_by_fqdn(hostname)
            if computer_agg:
                msg = f'Компьютер с доменным именем "{hostname}" уже существует.'
                raise exceptions.ComputerAlreadyExistsError(msg)

            directory = await uow.directories_repo.get_by_uid(uid=directory_uid)
            if not directory:
                msg = f'Директории с идентификатором "{directory_uid}" не существует.'
                raise dir_exceptions.DirectoryNotExistsError(msg)

            await uow.access_controller.raise_if_cannot_update(uid=directory.uid)

            computer_agg = ComputerDirectory.create(
                fqdn=hostname,
                directory=directory,
                mac_address=mac_address,
                comment=comment,
                create_date=aware_now(),
                created_by=created_by,
            )
            await uow.computers_repo.create(computer=computer_agg)
            await uow.commit()

		# возвращаем только нужный uid
        return computer_agg.computer.uid
```