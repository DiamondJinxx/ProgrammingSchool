import pytest


pytestmark = [pytest.mark.django_db]



@pytest.fixture
def vehicle_type(mixer):
    return mixer.blend(
        'auto.VehicleType', 
        description="Тестовое Грузовое ТС"
    )


@pytest.fixture
def brand(mixer, vehicle_type):
    return mixer.blend(
        'auto.Brand',
        name='Бренд для теста',
        vehicle_type=vehicle_type
    )


@pytest.fixture
def vehicle(mixer, brand):
    return mixer.blend(
        'auto.Vehicle', 
        brand=brand
    )


def test_vehicle_list(
    api,
    vehicle_type,
    brand,
    vehicle
) -> None:
    result = api.get('/api/v1/auto')

    assert result[0]['id'] == vehicle.id
    assert result[0]['brand_id'] == brand.id


def test_vehicle_retrieve(
    api,
    vehicle_type,
    brand,
    vehicle
) -> None:
    result = api.get(f'/api/v1/auto{vehicle.id}/')

    assert result[0]['id'] == vehicle.id
    assert result[0]['brand_id'] == brand.id
