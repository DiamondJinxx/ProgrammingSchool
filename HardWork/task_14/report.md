# Пример 1

на текущий момент код следующий:

```python
async def delete_user_access_control_lists(self, user_uid: apps_types.UserUID) -> None:
    """
    Удаляет записи ACL по всем категориям для пользователя.

    Args:
        user_uid: Идентификатор пользователя.
    """
    session = async_session_maker()
    acl_repo = ACLRepository(session=session)
    await acl_repo.delete_all(user_uid=user_uid)
    await session.commit()
    session.close()

```

Базово, тут мы можем забыть закрыть сессию, что приведет к утечке. Простой фикс с использованием
абстракции "контекстный менеджер":

```python
async def delete_user_access_control_lists(self, user_uid: apps_types.UserUID) -> None:
    """
    Удаляет записи ACL по всем категориям для пользователя.

    Args:
        user_uid: Идентификатор пользователя.
    """
    async with async_session_maker() as session:
        acl_repo = ACLRepository(session=session)
        await acl_repo.delete_all(user_uid=user_uid)
        await session.commit()
```

Перекладываем ответственность за ресурс на RAII подход.

# Пример 2

Если присмотреться к исправленной версии прошлого примера, то можем заметить, что в методе
может потребоваться проводить еще какие манипуляции с БД и в целом работать с сессией БД как-то запарно.

Давайте попробуем переложить ответственность за это(а так же за транзакционность и контролем, чтобы все репозиториии работали с одной сессией БД) на паттерн UnitOfWork, тогда метод станет выглядеть так:

```python
async def delete_user_access_control_lists(self, user_uid: apps_types.UserUID) -> None:
    """
    Удаляет записи ACL по всем категориям для пользователя.

    Args:
        user_uid: Идентификатор пользователя.
    """
    async with self._uow as uow:  # инициализация репозиториев и сессии спрятана тут внутри
        await uow.acl_repo.delete_all(user_uid=user_uid)
        await uow.commit()  # коммит не для сессии, а для объекта UnitOfWork. Оставим явно.
```

# Привер 3

```python

@router.get(
    "/",
)
async def get_servers(
    page_params,
    user
    filter_params,
) -> ListResponseSchema[ServerSchema]:
    """
    Список серверов.

    Args:
        page_params: Параметры пагинации;
        filter_params: параметры фильтрации серверов;
        user: Информация об авторизованном пользователе.
    """
    async with async_session_factory() as session:
        servers_repo = ServerRepo(session)
        acl_controller = ACLController(session, user_uid=user.uid)

        # сложная работа с правами, ручка в перспективе сильно растолстее
        acl_controller.raise_if_cannot_read()
        # тут плохо, так как паттерн "Репозиторий" перегружается работой с фильтрами и пагинацией
        servers, total = await server_repo.get_all(
            page_params,
            filter_params,
        )
        # преобразование для схемы тоже можно куда-нибудь спрятать
        servers = [ServerSchema.model_validate(server.to_dict()) for server in servers]

        return BaseListResponseSchema(total=total, content=servers)

```

Прибегнув к CQRS, возьмем оттуда абстракцию Query. Реализовав ее, получим следущий код
обработчика запроса:

```python

@router.get(
    "/",
)
async def get_servers(
    page_params,
    user
    filter_params,
) -> ListResponseSchema[ServerSchema]:
    """
    Список серверов.

    Args:
        page_params: Параметры пагинации;
        filter_params: параметры фильтрации серверов;
        user: Информация об авторизованном пользователе.
    """
    async with async_session_factory() as session:
        queries = deps.build_queries(session=session, user_uid=user.uid)
        servers, total = await queries.get_list(
            page_params,
            filter_params,
        )

    return BaseListResponseSchema(total=total, content=servers)

```

Разгрузили репозиторий от работы с фильтрами и пагинацией. Спрятали работу с правами.
Сразу преобразуем данные до нужной схемы.
