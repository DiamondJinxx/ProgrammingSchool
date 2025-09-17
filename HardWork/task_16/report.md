# Неочевидные проектные ошибки (1)

## Пример 1

**Было**

Есть класс, каждое из полей которого это базовый тип языка(кроме UUID).
Валидация полей происходит в сервисах. По ошибке можно создать объект
и записать неправильные значения.

```python

class Device(Base):
    """Сущность устройство."""

    uid: UUID = Field(
        description="Уникальный ID записи.",
    )
    external_id: str = Field(
        description="Уникальный идентификатор устройства, передаваемый внешним сервисом.",
    )
    name: str = Field(
        description="Имя устройства.",
    )
    comment: str = Field(
        description="Комментарий.",
    )
```

**Стало**

Сделали специальные типы данных для полей. Каждый тип содержит валидацию по
требуемым для типа правилам. При создании или обновлении нельзя записать значения,
непрудсмотренные системой. Проверка переместилась из нижнего уровня бизнес-логики
на уровень системы типов приложения.

```python
class Device(Base):
    """Сущность устройство."""

    uid: DeviceUID = Field(
        description="Уникальный ID записи.",
    )
    external_id: DeviceExtID = Field(
        description="Уникальный идентификатор устройства, передаваемый внешним сервисом.",
    )
    name: DeviceName = Field(
        description="Имя устройства.",
    )
    comment: DeviceComment = Field(
        description="Комментарий.",
    )
```

## Пример 2

**Было**

Аналогично первому примеру, можем по ошибке работать с невалидными значениями.

```python
class Segment(Base):
    """Сущность сегмент."""

    uid: UUID = Field(
        description="Уникальный ID записи.",
    )
    type: str = Field(
        description="Тип сегмента.",
    )
    name: str = Field(
        description="Наименование сегмента",
    )
    comment: str = Field(
        description="Комментарий.",
    )
```

**Стало**

Добавил типы с правилами валидации, проверка ошибок перенес на уровен системы типов.
Допустить ошибку стало сложно, насильно записать невалидные значения не получится.

```python

class Segment(Base):
    """Сущность сегмент."""

    uid: SegmentUID = Field(
        description="Уникальный ID записи.",
    )
    type: SegmentType = Field(
        description="Тип сегмента.",
    )
    name: SegmentName = Field(
        description="Наименование сегмента",
    )
    comment: Comment = Field(
        description="Комментарий.",
    )
```

## Пример 3

**Было**

Параметры пагинации для АПИ задаются типо int. Из-за чего на фронте есть лишнии проверки,
на бекенде в запросы к БД можно передавать отрицательные значения.

```python

class PageParams(Base):
    """ Параметры пагинации."""

    skip: int = 0
    limit: int = 500
```

**Стало**

В систему типов средствами фреймворка добавил типизацию и требование, чтобы передаваемые значения
были строго больше 0.

```python

class PageParams(Base):
    """ Параметры пагинации."""

    skip: int = Field(
        Query(
            ge=0,
            default=0,
        )
    )

    limit: int = Field(
        Query(
            ge=0,
            default=500,
        )
    )
```

## Пример 4

**Было**

В АПИ методах создания объекта возможно передать любые строковые значения,
из-за чего присутствуют цепочки проверок на стороне фронтенда и бекенда.

```python

class SegmentCreateSchema(Base):
    """Схема для создания сегмента."""

    name: str
    comment: str | None
```

**Стало**

Используя добавленные типы в первом примере поправим схему, чтобы перенсти
проверки на систему типов проекта.

```python

class SegmentCreateSchema(Base):
    """Схема для создания сегмента."""

    name: SegmentName = Field(
        max_length=256,
    )
    comment: Comment | None = Field(default=None)
```

## Пример 5

**Было**

Аналогично 4 примеру, только для АПИ метода обновления сущности.

```python
class SegmentUpdateSchema(Base):
    """Схема для обновления"""

    name: str | None
    comment: str | None
```

**Стало**

```python
class SegmentUpdateSchema(Base):
    """Схема для обновления"""

    name: SegmentName | None = Field(
        max_length=256,
        default=None,
    )
    comment: Comment | None = Field(
        default=None,
    )
```
