
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

########################## ДО ###########################
# ЦС = 8

    async def update(
        self,
        computer_uid: types.ComputerUID,
        field_updates: Dict[str, Any],
        directory_uid: Optional[types.DirectoryUID],
        etag_value: int,
    ) -> None:
        """
        Обновить компьютер.

        Args:
            computer_uid: Идентификатор компьютера.
            field_updates: словарь с полями, которые нужно обновить.
            directory_uid: uid директории, в которую поместить компьютер
            etag_value: Идентификатор блокировки ETag. Используется для обновления записи.

        Raises:
            exceptions.ComputerNotExistsError: Указанного компьютера не существует.
            dir_exceptions.DirectoryNotExistsError: Указанной директории не существует.
            exceptions.ComputerPreconditionFailedError: Оптимистическая блокировка.
        """
        async with self._uow as uow:
            computer_agg = await uow.computers_repo.get_by_uid(uid=computer_uid)
            if not computer_agg:
                msg = f'Компьютер с идентификатором "{computer_uid}" не существует.'
                raise exceptions.ComputerNotExistsError(msg)
            if etag_value != computer_agg.computer.etag_value:
                raise exceptions.ComputerPreconditionFailedError

            directory: Optional[Directory] = None

            if directory_uid:
                directory = await uow.directories_repo.get_by_uid(uid=directory_uid)
                if not directory:
                    msg = 'Директории с идентификатором "%s" не существует.' % directory_uid
                    raise dir_exceptions.DirectoryNotExistsError(msg)

            await uow.access_controller.raise_if_cannot_update(uid=computer_agg.directory_uid)

            update_date = aware_now()

            if directory:
                await uow.access_controller.raise_if_cannot_update(uid=directory.uid)
                old_directory = await uow.directories_repo.get_by_uid(uid=computer_agg.directory_uid)
                computer_agg.change_directory(directory, update_date)

            computer_agg.computer.update(
                field_updates=field_updates,
                update_source=types.CommandSource.API,
                update_date=update_date,
            )
            await uow.computers_repo.update(computer=computer_agg)
            await uow.commit()

        await self._rmq.send_updated_message(
            computer=computer_agg.computer,
        )
        if directory:
            await self._rmq_groups.send_computer_added_message(
                directory=directory,
                computer=computer_agg.computer,
            )
            if old_directory:
                await self._rmq_groups.send_computer_removed_message(
                    directory=old_directory,
                    computer=computer_agg.computer,
                )


########################## После ###########################
# ЦС = 1

    async def update(
        self,
        computer_uid: types.ComputerUID,
        field_updates: Dict[str, Any],
        directory_uid: Optional[types.DirectoryUID],
        etag_value: int,
    ) -> None:
        """
        Обновить компьютер.

        Args:
            computer_uid: Идентификатор компьютера.
            field_updates: словарь с полями, которые нужно обновить.
            directory_uid: uid директории, в которую поместить компьютер
            etag_value: Идентификатор блокировки ETag. Используется для обновления записи.

        Raises:
            exceptions.ComputerNotExistsError: Указанного компьютера не существует.
            dir_exceptions.DirectoryNotExistsError: Указанной директории не существует.
            exceptions.ComputerPreconditionFailedError: Оптимистическая блокировка.
        """
        async with self._uow as uow:
            computer_agg = await uow.computers_repo.get_by_uid(uid=computer_uid)

            # поместили проверки в доменную АСД.
            computer_agg.raise_if_not_exists()
            computer_agg.raise_if_preconddition_failed(etag_value)

            # Применили Null Object Pattern для директории и переместил проверку в доменную АСД.
            directory: Directory = await uow.directories_repo.get_by_uid(uid=directory_uid)
            directory.raise_if_not_exists()

            await uow.access_controller.raise_if_cannot_update(computer_agg.directory)
            await uow.access_controller.raise_if_cannot_update(directory)

            update_date = aware_now()

            old_directory = await uow.directories_repo.get_by_uid(uid=computer_agg.directory_uid)
            computer_agg.change_directory(directory, update_date)

            computer_agg.computer.update(
                field_updates=field_updates,
                update_source=types.CommandSource.API,
                update_date=update_date,
            )
            await uow.computers_repo.update(computer=computer_agg)
            await uow.commit()

        await self._rmq.send_updated_message(
            computer=computer_agg.computer,
        )
        # Убрал условия в приватные методы.
        await self.__send_computer_added_message(directory, computer_agg)
        await self.__send_computer_removed_message(old_directory, computer_agg)

    async def __send_computer_added_message(directory: Directory, computer: Computer) -> None:
        if not directory:
            return
        await self._rmq_groups.send_computer_added_message(
            directory=directory,
            computer=computer_agg.computer,
        )

    async def __send_computer_removed_message(directory: Directory, computer: Computer) -> None:
        if not directory:
            return 
        await self._rmq_groups.send_computer_removed_message(
            directory=directory,
            computer=computer_agg.computer,
        )

