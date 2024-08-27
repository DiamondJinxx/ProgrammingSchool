class OSProfile:

########################## ДО ###########################
# ЦС = 6

    async def update(
        self,
        profile_uid: types.ProfileOSDeploymentUID,
        modified_by: types.UserLogin,
        field_updates: Dict[str, Any],
        etag_value: int,
    ) -> None:
        """
        Обновить Профиль первичной установки ОС.

        Args:
            profile_uid: Идентификатор профиля.
            modified_by: Кем внесены изменения.
            field_updates: Словарь с полями на обновление.
            etag_value: Идентификатор блокировки ETag. Используется для обновления записи.

        Raises:
            exceptions.ProfileNotExistsError: Профиль с таким uid не существует.
            exceptions.ProfileAlreadyExistsError: Профиль с таким именем уже существует.
            exceptions.ActiveProfileNonValidUpdateError: Некорректное обновление профиля.
            exceptions.ProfilePreconditionFailedError: Профиль был изменен другим пользователем.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_update(profile_uid)

            profile = await uow.profiles_repo.get_by_uid(uid=profile_uid)
            if profile is None:
                msg = f'Профиль с идентификатором "{profile_uid}" не существует.'
                raise exceptions.ProfileNotExistsError(msg)

            if etag_value != profile.etag_value:
                raise exceptions.ProfilePreconditionFailedError

            profile.update(
                field_updates=field_updates,
                last_modified_date=aware_now(),
                last_modified_by=modified_by,
            )

            same_name_profile = await uow.profiles_repo.get_by_name(name=profile.name)
            if same_name_profile and same_name_profile.uid != profile.uid:
                msg = f"Профиль с именем {profile.name} уже существует"
                raise exceptions.ProfileAlreadyExistsError(msg)

            bad_update, msg = profile.is_update_valid()
            if bad_update:
                raise exceptions.ActiveProfileNonValidUpdateError(msg)

            await uow.profiles_repo.update(profile)
            await uow.commit()

        if profile.is_active and not profile.only_comment_updated(field_updates):
            # если обновили только комментарий, сообщение в RMQ не отправляется
            await self._rmq_adapter.send_profile_changed(profile=profile)

#################### ПОСЛЕ ########################
# ЦС = 2

    async def update(
        self,
        profile_uid: types.ProfileOSDeploymentUID,
        modified_by: types.UserLogin,
        field_updates: Dict[str, Any],
        etag_value: int,
    ) -> None:
        """
        Обновить Профиль первичной установки ОС.

        Args:
            profile_uid: Идентификатор профиля.
            modified_by: Кем внесены изменения.
            field_updates: Словарь с полями на обновление.
            etag_value: Идентификатор блокировки ETag. Используется для обновления записи.

        Raises:
            exceptions.ProfileNotExistsError: Профиль с таким uid не существует.
            exceptions.ProfileAlreadyExistsError: Профиль с таким именем уже существует.
            exceptions.ActiveProfileNonValidUpdateError: Некорректное обновление профиля.
            exceptions.ProfilePreconditionFailedError: Профиль был изменен другим пользователем.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_update(profile_uid)

            profile = await uow.profiles_repo.get_by_uid(uid=profile_uid)

            # объект profile теперь использует подход Null Object Pattern,
            # а так же Доменная AST проверяет сама себя, скрывая логику проверок в своем модуле.
            profile.raise_if_profile_not_exist()
            profile.raise_if_precondition_failed(etag_value)

            profile.update(
                field_updates=field_updates,
                last_modified_date=aware_now(),
                last_modified_by=modified_by,
            )

            same_name_profile = await uow.profiles_repo.get_by_name(name=profile.name)
            same_name_profile.raise_if_not_equal(profile)

            bad_update, msg = profile.is_update_valid()
            if bad_update:
                raise exceptions.ActiveProfileNonValidUpdateError(msg)

            await uow.profiles_repo.update(profile)
            await uow.commit()

        # небольшая хитрость в функциональном стиле, чтобы избавиться от if 
        changed_profiles = filter(lambda profile: profile.is_active and not profile.only_comment_updated(field_updates))
        asyncstdlib.map(
            self._rmq_adapet.send_profile_changed,
            changed_profiles,
        )
            

    @staticmethod
    def raise_if_profile_not_exist(profile: Optional[Profile], profile_uid: ProfileUID) -> None:
        if profile is None:
            msg = f'Профиль с идентификатором "{profile_uid}" не существует.'
            raise exceptions.ProfileNotExistsError(msg)

    @staticmethod
    def raise_if_precondition_failed(etag_value: int, profile_etag: int) -> None:
        if etag_value != profile.etag_value:
            raise exceptions.ProfilePreconditionFailedError
