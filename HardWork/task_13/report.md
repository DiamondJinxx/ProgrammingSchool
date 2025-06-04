## Правило 1

**Пример 1 Оригинал**

**Пример 1 Исправления**

**Пример 2 Оригинал**
**Пример 2 Исправления**

## Правило 2

**Пример 1 Оригинал**
Пример недавно случившейся ситуации, когда пытались переложить вину за ошибку на меня, хотя точек для возникновения ошибки вообще-то две, одна из которых на стороне другого сервиса. Проверить ошибку на стороне другого сервиса ребята конечно забыли :)

```python
from pydantic_settings import BaseSettings, Field


class CommonSettings(BaseSettings):
	"""Общие настройки сервиса."""
    SERVICE_IP_ADDRESS: str | None = Field(
        description="IP адрес репозитория.",
        default=None,
    )
    SERVICE_PORT: int = Field(
        description="Порт репозитория.",
        default=80, # фишка как раз в этом значении по умолчанию.
    )
```

В переменные окружения тупо забыли добавить указания порта. Этот порт нужен, чтобы куча клиентов могли скачивать пакеты для установки.

**Пример 1 Исправления**

```python
from pydantic_settings import BaseSettings, Field


class CommonSettings(BaseSettings):
    """Общие настройки сервиса."""
    SERVICE_IP_ADDRESS: str = Field(
        description="IP адрес репозитория.",
    )
    SERVICE_PORT: int = Field(
        description="Порт репозитория.",
    )
```

Так как это важные данные, я бы запретил в целом запуск сервиса без явного указания нужных переменных окружений. Но есть сопротивления в команде.

**Пример 2 Оригинал**

```python
class ServersUpdateService:
    """Сервис обновления данных серверов."""
    _servers_repo: ServerRepository = ServerRepository()
    _groups_repo: GroupRepository = GroupRepository()
    _rmq_adapter: RMQAdapter = RMQAdapter()

```

Код выше допускает использование только конструктора по умолчанию, что делает объект сервиса, так же совсем не понятно, что там в используемых репозиториях и адаптере для очереди.

**Пример 2 Исправления**

```python
class ServersUpdateService:
    """Сервис обновления данных серверов."""
    _servers_repo: ServersRepository
    _groups_repo: GroupsRepository
    _rmq_adapter: RMQAdapter

    def __init__(
        self,
        servers_repo: ServersRepository,
        groups_repo: GroupsRepository,
        rmq_adapter: RMQAdapter,
    ):
        self._servers_repo = servers_repo
        self._groups_repo = groups_repo
        self._rmq_adapter = rmq_adapter



def build_servers_update_service() -> ServersUpdateService:
    """Билдер сервиса обновления серверов."""
    session = session_maker()
    return ServersUpdateService(
        servers_repo=ServersRepository(session),
        groups_repo=GroupsRepository(session),
        rmq_adapter=build_rmq_adapter(),
    )
```

Добавлены обязательные параметры в конструктор. Так же сделана отдельная точка сборки объекта сервиса, в которой можно управлять конфигурацией объекта под конкретные нужды бизнес логики. Аналогично сделан сборщик адаптера для очереди.

## Правило 3

**Пример 1 Оригинал**

```python
from pydantic import BaseModel, Field

class Server(BaseModel):
	role: str = Field(
		description="Роль сервера в системе",
	)
```

Непонятно, какая может быть роль у сервера. Мы вроде как хотим использовать валидацию с помощью пидантика, но по сути позволяем писать произвольное значение.

**Пример 1 Исправления**

```python
from enum import Enum
from pydantic import BaseModel, Field

class ServerRole(str, Enum):
	"""Роли сервера."""
	STORAGE = "storage"
	REPO = "repository"


class Server(BaseModel):
	role: ServerRole = Field(
		description="Роль сервера в системе",
	)
```

Теперь мы контролируем возможные значения роли сервера и избегаем использование примитивов - использование перечисления спасает от очепяток при использовании литералов.

**Пример 2 Оригинал**

```python
from enum import Enum
from pydantic import BaseModel, Field


class Package(BaseModel):
	name: str = Field(
		description="Название пакета",
	)
	version: str = Field(
		description="Версия пакета",
	)
```

Опять же, для названия и версии пакета наверняка есть какие-то недопустимые символы и маски.

**Пример 2 Исправления**

```python
from enum import Enum
from pydantic import BaseModel, Field

def name_validate(value: str) -> str:
    """Валидация поля содержащего название чего-либо."""
	...

def version_validate(value: str) -> str:
    """Валидация поля содержащего версию чего-либо."""
	...

PackageName = Annotated[str, AfterValidator(name_validate)]
PackageVersion = Annotated[str, AfterValidator(package_validate)]



class Package(BaseModel):
	name: PackageName = Field(
		description="Название пакета",
	)
	version: PackageVersion = Field(
		description="Версия пакета",
	)
```

Добавив типы для названия пакетов и версии мы обезопасились от возможных невалидных значений.
