
from io import BytesIO
from unittest.mock import AsyncMock, Mock

import pytest

from src.services.stones import StoneService


@pytest.mark.asyncio
async def test_upload_image_rollback_on_database_error():
    repository = Mock()
    repository.get_stone_from_id = AsyncMock(return_value=Mock(id=1))
    repository.create_stone_image = AsyncMock(
        side_effect=RuntimeError("Database error")
    )

    storage = Mock()
    storage.upload = AsyncMock()
    storage.delete = AsyncMock()

    transaction = Mock()
    transaction.commit = AsyncMock()
    transaction.rollback = AsyncMock()

    service = StoneService(
        repo=repository,
        storage=storage,
        transaction=transaction,
    )

    file = BytesIO(b"fake image content")

    with pytest.raises(RuntimeError, match="Database error"):
        await service.upload_file(
            stone_id=1,
            file=file,
            content_type="image/jpeg",
        )

  
    repository.get_stone_from_id.assert_awaited_once_with(1)
    storage.upload.assert_awaited_once()
    repository.create_stone_image.assert_awaited_once()

    transaction.commit.assert_not_awaited()
    transaction.rollback.assert_awaited_once()
    storage.delete.assert_awaited_once()

    uploaded_key = storage.upload.await_args.kwargs["key"]
    deleted_key = storage.delete.await_args.args[0]

    assert deleted_key == uploaded_key
    assert uploaded_key.startswith("stones/1/")

@pytest.mark.asyncio
async def test_upload_image_success():
    # Arrange — подготавливаем зависимости
    repository = Mock()
    repository.get_stone_from_id = AsyncMock(
        return_value=Mock(id=1)
    )
    repository.create_stone_image = AsyncMock(
        return_value=Mock(id=10)
    )

    storage = Mock()
    storage.upload = AsyncMock()
    storage.delete = AsyncMock()

    transaction = Mock()
    transaction.commit = AsyncMock()
    transaction.rollback = AsyncMock()

    service = StoneService(
        repo=repository,
        storage=storage,
        transaction=transaction,
    )

    file = BytesIO(b"fake image content")

    # Act — выполняем успешную загрузку
    key = await service.upload_file(
        stone_id=1,
        file=file,
        content_type="image/jpeg",
    )

    # Assert — проверяем вызовы
    repository.get_stone_from_id.assert_awaited_once_with(1)
    storage.upload.assert_awaited_once()
    repository.create_stone_image.assert_awaited_once()
    transaction.commit.assert_awaited_once()

    # При успехе компенсация не выполняется
    transaction.rollback.assert_not_awaited()
    storage.delete.assert_not_awaited()

    # Проверяем ключ загруженного изображения
    uploaded_key = storage.upload.await_args.kwargs["key"]

    assert key == uploaded_key
    assert uploaded_key.startswith("stones/1/")

    # Проверяем, что в PostgreSQL сохраняется тот же ключ
    repository.create_stone_image.assert_awaited_once_with(
        stone_id=1,
        object_key=uploaded_key,
    )


@pytest.mark.asyncio
async def test_upload_image_cleanup_failure_preserves_database_error():
    # Arrange
    repository = Mock()
    repository.get_stone_from_id = AsyncMock(
        return_value=Mock(id=1)
    )
    repository.create_stone_image = AsyncMock(
        side_effect=RuntimeError("Database error")
    )

    storage = Mock()
    storage.upload = AsyncMock()
    storage.delete = AsyncMock(
        side_effect=OSError("MinIO unavailable")
    )

    transaction = Mock()
    transaction.commit = AsyncMock()
    transaction.rollback = AsyncMock()

    service = StoneService(
        repo=repository,
        storage=storage,
        transaction=transaction,
    )

    file = BytesIO(b"fake image content")

    # Act + Assert
    with pytest.raises(RuntimeError, match="Database error"):
        await service.upload_file(
            stone_id=1,
            file=file,
            content_type="image/jpeg",
        )

    # PostgreSQL transaction must be rolled back
    transaction.rollback.assert_awaited_once()
    transaction.commit.assert_not_awaited()

    # Cleanup must be attempted
    storage.upload.assert_awaited_once()
    storage.delete.assert_awaited_once()

    # The same uploaded object must be deleted
    uploaded_key = storage.upload.await_args.kwargs["key"]
    storage.delete.assert_awaited_once_with(uploaded_key)
