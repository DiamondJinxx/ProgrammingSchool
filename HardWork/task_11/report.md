**Пример 1**

Было

```python
def build_dimension_from_extractable(ext_mdl: Extractable) -> Dimension:
    """
    Построить модель из модели-источника.

    Args:
        ext_mdl: ORM модель-источник.
    """
    return Dimension(
        uid=uuid.uuid4(),
        acm_uid=ext_mdl.uid,
        name=ext_mdl.name,
        version=ext_mdl.version,
        specified=ext_mdl.specified,
        lsb_distrib_description=ext_mdl.params.lsb_distrib_description or _NOT_DEFINED,
        creation_date=ext_mdl.creation_date,
        update_date=ext_mdl.update_date,
        delete_date=ext_mdl.delete_date,
        deleted=ext_mdl.deleted,
    )

```

Стало

```python
def build_dimension_from_extractable(ext_mdl: Extractable) -> Dimension:
    """
    Построить модель из модели-источника.

    Args:
        ext_mdl: ORM модель-источник.
    """
    # вынесем вычисления конечного результата в отдельное место
    lsb_distrib_description=ext_mdl.params.lsb_distrib_description or _NOT_DEFINED,
    return Dimension(
        uid=uuid.uuid4(),
        acm_uid=ext_mdl.uid,
        name=ext_mdl.name,
        version=ext_mdl.version,
        specified=ext_mdl.specified,
        lsb_distrib_description=lsb_distrib_description,
        creation_date=ext_mdl.creation_date,
        update_date=ext_mdl.update_date,
        delete_date=ext_mdl.delete_date,
        deleted=ext_mdl.deleted,
    )
```

**Пример 2**

Было

```python
def build_dimension_from_extractable(ext_mdl: Extractable) -> Dimension:
    """
    Построить модель из модели-источника.

    Args:
        ext_mdl: ORM модель-источник.
    """
    return Dimension(
        uid=uuid.uuid4(),
        acm_uid=ext_mdl.uid,
        name=ext_mdl.name,
        version=ext_mdl.version,
        chassis=_format_chassis(ext_mdl.params.chassis),
        osarch=_format_osarch(ext_mdl.params.osarch),
        astra_modeswitch=_format_astra_modeswitch(ext_mdl.params.astra_modeswitch),
        status=_format_status(ext_mdl.status),
        creation_date=ext_mdl.creation_date,
        update_date=ext_mdl.update_date,
        delete_date=ext_mdl.delete_date,
        deleted=ext_mdl.deleted,
    )

```

Стало

```python

def build_dimension_from_extractable(ext_mdl: Extractable) -> Dimension:
    """
    Построить модель из модели-источника.

    Args:
        ext_mdl: ORM модель-источник.
    """
    # вынесем получение форматтированого значения выше
    formatted_chassis=_format_chassis(ext_mdl.params.chassis),
    formatted_osarch=_format_osarch(ext_mdl.params.osarch),
    formatted_modeswitch=_format_astra_modeswitch(ext_mdl.params.modeswitch),
    formatted_status=_format_status(ext_mdl.status),
    return Dimension(
        uid=uuid.uuid4(),
        acm_uid=ext_mdl.uid,
        name=ext_mdl.name,
        version=ext_mdl.version,
        chassis=formatted_chassis,
        osarch=formatted_osarch,
        modeswitch=formatted_astra_modeswitch,
        status=formatted_status,
        creation_date=ext_mdl.creation_date,
        update_date=ext_mdl.update_date,
        delete_date=ext_mdl.delete_date,
        deleted=ext_mdl.deleted,
    )

```

**Пример 3**

Было

```python
dwh_session.add(build_dimension_from_orm(extract_data(ext_package)))

```

Стало

```python
# Развернули цепочку вызовов
extracted_data = extract_data(ext_package)
dim_software_package = build_dimension_from_orm(ext_package)
dwh_session.add(dim_software_package)

```

**Пример 4**

Было

```python
dim = get_first(list(filter(lambda dim: dim.acm_uid == ext_mdl.uid, dimensions)))
```

Стало

```python
# Развернули цепочку вызовов
fileted_dimensions = list(filter(lambda dim: dim.acm_uid == ext_mdl.uid, dimensions))
dim = get_first(fileted_dimensions)
```

**Пример 5**

Было

```python
dim = next(
    [
        dim for dim in dimensions if dim.uid == needed_uid
    ],
    get_default_object(),
)
```

Стало

```python
# Спрятали логику в отдельный метод
dim = find_in_list_by_uid(needed_uid, dimesions)
```
