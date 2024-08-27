class OSDeploymentProfileService:
    """Сервис Профилей первичной установки ОС."""

    def __init__(
        self,
        unit_of_work: AbstractOSDeploymentProfileUnitOfWork,
        rmq_adapter: OSDeploymentProfileRMQInterface,
    ) -> None:
        """
        Конструктор сервиса Профилей первичной установки ОС.

        Args:
            unit_of_work: Объект шаблона Единица работы.
            rmq_adapter: Адаптер для RMQ.
        """
        self._uow = unit_of_work
        self._rmq_adapter = rmq_adapter

########################## ДО ###########################
# ЦС = 6

    async def activate(
        self,
        profile_uid: types.ProfileOSDeploymentUID,
        modified_by: types.UserLogin,
    ) -> None:
        """
        Активировать профиль.

        Args:
            profile_uid: uid профиля, который активировать
            modified_by: кем активируется профиль

        Raises:
            exceptions.ProfileCanNotBeActivatedError: когда нельзя активировать профиль.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_update(profile_uid)

            profile = await uow.profiles_repo.get_by_uid(profile_uid)
            if profile is None:
                msg = f"Профиль {profile_uid} не найден"
                raise exceptions.ProfileNotExistsError(msg)

            if profile.is_active:
                return

            if not profile.can_be_active:
                msg = f"Профиль {profile.uid} не может быть активирован."
                raise exceptions.ProfileCanNotBeActivatedError(msg)

            profile.activate(
                modified_by=modified_by,
                modified_date=aware_now(),
            )

            default_profile = await uow.profiles_repo.get_default()
            if default_profile is None:
                profile.set_default(
                    modified_by=modified_by,
                    modified_date=aware_now(),
                )

            await uow.profiles_repo.update(profile)
            await uow.commit()

        await self._rmq_adapter.send_profile_activated(profile)
        if profile.is_default:
            await self._rmq_adapter.send_profile_default(profile)



########################## ПОСЛЕ ###########################
# ЦС = 1

    async def activate(
        self,
        profile_uid: types.ProfileOSDeploymentUID,
        modified_by: types.UserLogin,
    ) -> None:
        """
        Активировать профиль.

        Args:
            profile_uid: uid профиля, который активировать
            modified_by: кем активируется профиль

        Raises:
            exceptions.ProfileCanNotBeActivatedError: когда нельзя активировать профиль.
        """
        async with self._uow as uow:
            await uow.access_controller.raise_if_cannot_update(profile_uid)

            profile = await uow.profiles_repo.get_by_uid(profile_uid)
            # Null Object Pattern + Полиморфизм
            profile.raise_if_not_exists()

            if profile.is_active:
                return

            # Null Object Pattern + Полиморфизм
            profile.raise_if_cannot_be_active()

            profile.activate(
                modified_by=modified_by,
                modified_date=aware_now(),
            )

            default_profile = await uow.profiles_repo.get_default()
            default_profile.set_default(profile)

            await uow.profiles_repo.update(profile)
            await uow.commit()

        await self._rmq_adapter.send_profile_activated(profile)
        # проверка условия вынесена в отдельный метод.
        await self.__send_profile_default(profile)

        async def __send_profile_default(self, profile: Profile) -> None:
            if not profile.is_default():
                return
            await self._rmq_adapter.send_profile_activated(profile)

