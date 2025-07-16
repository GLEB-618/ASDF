from sqlalchemy import select
from data.database import sync_engine, sync_session_factory, Base
from data.models import *


class SyncORM:

    @staticmethod
    def create_tables():
        try:
            with sync_engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)

                Base.metadata.create_all(bind=conn)
        except Exception as e:
            print(e)
    # @staticmethod
    # async def insert_user_id_table(table, user_id: int) -> None:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = insert(table).values(user_id=user_id).on_conflict_do_nothing()
    #             result = await session.execute(stmt)
    #             await session.commit()

    #             if result.rowcount > 0:
    #                 log.info(f"Пользователь {user_id} добавлен в таблицу {table.__tablename__}")
    #             # else:
    #             #     log.debug(f"Пользователь {user_id} уже существует в таблице {table.__tablename__}")

    #     except Exception as e:
    #         log.error(f"Ошибка при добавлении пользователя {user_id}: {e}")

    # @staticmethod
    # async def select_state(user_id: int) -> str:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(Users.state).where(Users.user_id == user_id)
    #             result = await session.execute(query)
    #             state = result.scalar_one_or_none()

    #             log.debug(f"Получено состояние пользователя {user_id}: {state}")

    #             return state
    #     except Exception as e:
    #         log.error(f"Ошибка при получении состояние пользователя {user_id}: {e}")

    # @staticmethod
    # async def get_position(table, user_id: int) -> int:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(table.position).where(table.user_id == user_id)
    #             result = await session.execute(query)
    #             position = result.scalar_one_or_none()
    #             log.debug(f"Получена позиция пользователя {user_id} в таблице {table.__tablename__}: {position}")
    #             return position
    #     except Exception as e:
    #         log.error(f"Ошибка при получении позиции пользователя {user_id} в таблице {table.__tablename__}: {e}")

    # @staticmethod
    # async def update_state(user_id: int, state: str = "DEFAULT_STATE") -> None:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(Users).where(Users.user_id == user_id)
    #             result = await session.execute(stmt)
    #             user = result.scalar_one_or_none() 
                
    #             if user:
    #                 user.state = state
    #                 await session.commit() 

    #                 log.info(f"Состояние пользователя {user_id} обновлено на {state}")
    #             else:
    #                 log.debug(f"Пользователь {user_id} не найден")

    #                 await AsyncORM.insert_user_id_table(Users, user_id)

    #                 stmt = select(Users).where(Users.user_id == user_id)
    #                 result = await session.execute(stmt)
    #                 user = result.scalar_one_or_none()

    #                 user.state = state
    #                 await session.commit()
    #                 log.info(f"Состояние пользователя {user_id} обновлено на {state}")
    #     except Exception as e:
    #         log.error(f"Ошибка при обновлении состояния пользователя {user_id} на {state}: {e}")

    # @staticmethod
    # async def insert_file_id_dq(file_id: str, text: str = None) -> None:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = insert(DQ).values(file_id=file_id, text=text).on_conflict_do_nothing()
    #             result = await session.execute(stmt)
    #             await session.commit()

    #             if result.rowcount > 0:
    #                 log.info(f"Файл с id {file_id} добавлен в таблицу {DQ.__tablename__}")
    #             else:
    #                 log.debug(f"Файл с id {file_id} уже существует в таблице {DQ.__tablename__}")
    #     except Exception as e:
    #         log.error(f"Ошибка при добавлении id файла в таблицу {DQ.__tablename__}: {e}")

    # @staticmethod
    # async def check_admins(user_id: int) -> bool:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(exists().where(Admins.user_id == user_id))
    #             result = await session.execute(query)
    #             return result.scalar()
    #     except Exception as e:
    #         log.error("Ошибка в функции check_admins: %s", e)

    # @staticmethod
    # async def get_next_photo(user_id: int) -> str:
    #     try:
    #         position = await AsyncORM.get_position(Admins, user_id)
    #         async with async_session_factory() as session:
    #             stmt = select(DQ).where(DQ.active == False).order_by(DQ.id).offset(position).limit(1)
    #             result = await session.execute(stmt)
    #             photo = result.scalar_one_or_none()

    #             if photo:
    #                 photo.active = True
    #                 await session.commit()
    #                 await session.refresh(photo)
    #             return photo.file_id, photo.text
    #     except Exception as e:
    #         log.error("Ошибка в функции get_next_photo: %s", e)

    # @staticmethod
    # async def get_len_photos_by_active(active_status: bool) -> int:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(DQ).where(DQ.active == active_status)
    #             result = await session.execute(stmt)
    #             photos = result.scalars().all()  # Получаем список объектов DQ
    #             return len(photos)  # Список ORM-объектов
    #     except Exception as e:
    #         log.error("Ошибка в функции get_len_photos_by_active: %s", e)

    # @staticmethod
    # async def postpone_photo(file_id: str) -> None:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(DQ).where(DQ.file_id == file_id)
    #             result = await session.execute(stmt)
    #             photo = result.scalar_one_or_none()
                
    #             if photo:
    #                 photo.active = False
    #                 await session.commit()
    #             else:
    #                 log.error(f"Фото с id {file_id} не найдено")
    #     except Exception as e:
    #         log.error(f"Ошибка в функции postpone_photo: {e}")

    # @staticmethod
    # async def update_position(table, user_id: int, position: int) -> None:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(table).where(table.user_id == user_id)
    #             result = await session.execute(stmt)
    #             user = result.scalar_one_or_none()
                
    #             if user:
    #                 user.position = position
    #                 await session.commit()
    #             else:
    #                 log.error(f"Пользователь с id {user_id} не найден")
    #     except Exception as e:
    #         log.error(f"Ошибка в функции update_position: {e}")

    # @staticmethod
    # async def delete_and_save_photo(file_id: str, is_save: bool = True) -> None:
    #     try:
    #         ids = await AsyncORM.get_admin_ids()
    #         for user_id in ids:
    #             position = await AsyncORM.get_position(Admins, user_id)
    #             if position > 0:
    #                 await AsyncORM.update_position(Admins, user_id, position-1)

    #         async with async_session_factory() as session:
    #             stmt = select(DQ).where(DQ.file_id == file_id)
    #             result = await session.execute(stmt)
    #             photo = result.scalar_one_or_none()
    #             await session.delete(photo)

    #             if is_save == True:
    #                 stmt = insert(Photos).values(file_id=file_id).on_conflict_do_nothing()
    #                 await session.execute(stmt)
    #             await session.commit()
    #     except Exception as e:
    #         log.error("Ошибка в функции delete_and_save_photo: %s", e)

    # @staticmethod
    # async def get_categorized(file_id: str) -> list:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(Photos.type, Photos.name, Photos.physical).where(Photos.file_id == file_id)
    #             result = await session.execute(query)
    #             row = result.fetchone()
    #             return row
    #     except Exception as e:
    #         log.error("Ошибка в функции get_categorized: %s", e)
    
    # @staticmethod
    # async def update_categorized(file_id: str, content_type: str, name: str, physical: str) -> list:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(Photos).where(Photos.file_id == file_id)
    #             result = await session.execute(stmt)
    #             photo = result.scalar_one_or_none()
                
    #             if photo:
    #                 photo.type = content_type
    #                 photo.name = name
    #                 photo.physical = physical
    #                 await session.commit()
    #     except Exception as e:
    #         log.error("Ошибка в функции update_categorized: %s", e)

    # @staticmethod
    # async def get_admin_ids() -> list:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(Admins.user_id)  # Выбираем только user_id из таблицы Admins
    #             result = await session.execute(stmt)
    #             admin_ids = result.scalars().all()  # Получаем список всех user_id
    #             return admin_ids
    #     except Exception as e:
    #         log.error("Ошибка в функции get_admin_ids: %s", e)
        
    # @staticmethod
    # async def get_categorized_user(user_id: int) -> int:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(Users.type, Users.name, Users.physical).where(Users.user_id == user_id)
    #             result = await session.execute(query)
    #             row = result.fetchone()
    #             return row
    #     except Exception as e:
    #         log.error("Ошибка в функции get_categorized_user: %s", e)

    # @staticmethod
    # async def get_update_file_ids_user(user_id: int) -> int:
    #     try:
    #         content_type, name, teles = await AsyncORM.get_categorized_user(user_id)
            
    #         async with async_session_factory() as session:
    #             stmt = select(Photos.file_id)
    #             filters = []

    #             if content_type != "any":
    #                 filters.append(Photos.type == content_type)
    #             if name != "any":
    #                 filters.append(Photos.name == name)
    #             if teles != "any":
    #                 filters.append(Photos.physical == teles)

    #             if filters:
    #                 stmt = stmt.where(*filters)

    #             stmt = stmt.order_by(func.random())
    #             result = await session.execute(stmt)
    #             photos_list = result.scalars().all()  # Получаем список всех user_id

    #             stmt = select(Users).where(Users.user_id == user_id)
    #             result = await session.execute(stmt)
    #             user = result.scalar_one_or_none()

    #             if user:
    #                 user.file_ids = photos_list
    #                 await session.commit()

    #             return photos_list
    #     except Exception as e:
    #         log.error("Ошибка в функции get_update_file_ids_user: %s", e)

    # @staticmethod
    # async def get_list_categorized_filter(filter_txt: str):
    #     try:
    #         async with async_session_factory() as session:
    #             if filter_txt == "name":
    #                 filter_sl = Photos.name
    #             elif filter_txt == "physical":
    #                 filter_sl = Photos.physical
    #             stmt = select(filter_sl).order_by(Photos.id)
    #             result = await session.execute(stmt)
    #             ls = result.scalars().all()  # Получаем список всех user_id
    #             return list(set(ls))
    #     except Exception as e:
    #         log.error("Ошибка в функции get_list_categorized_filter: %s", e)

    # @staticmethod
    # async def select_file_ids_user(user_id: int) -> str:
    #     try:
    #         async with async_session_factory() as session:
    #             query = select(Users.file_ids).where(Users.user_id == user_id)
    #             result = await session.execute(query)
    #             state = result.scalar_one_or_none()
    #             return state
    #     except Exception as e:
    #         log.error("Ошибка в функции select_file_ids_user: %s", e)

    # @staticmethod
    # async def update_categorized_user(user_id: int, content_type: str, name: str, physical: str) -> list:
    #     try:
    #         async with async_session_factory() as session:
    #             stmt = select(Users).where(Users.user_id == user_id)
    #             result = await session.execute(stmt)
    #             user = result.scalar_one_or_none()
                
    #             if user:
    #                 user.type = content_type
    #                 user.name = name
    #                 user.physical = physical
    #                 await session.commit()
    #     except Exception as e:
    #         log.error("Ошибка в функции update_categorized_user: %s", e)