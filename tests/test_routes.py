import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("test@test.com")


@pytest.fixture(scope="module")
async def dummy_event() -> Event:
    new_event = Event(
        creator="test@test.com",
        title="The Beginning of it all",
        image="http://toimage.com/that_image.png",
        description="This should perform some function",
        tags=['Python', 'fastapi'],
        location="Teams"
    )

    await Event.insert_one(new_event)
    yield new_event


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient,
                         dummy_event: Event) -> None:
    response = await default_client.get("/event/")
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(dummy_event.id)


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, dummy_event: Event) -> None:
    url = f"/event/{str(dummy_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == dummy_event.creator
    assert response.json()["_id"] == str(dummy_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient,
                          access_token: str) -> None:
    payload = {
        "title": "The Beginning of it all",
        "image": "http://toimage.com/that_image.png",
        "description": "This should perform some function",
        "tags": ['Python', 'fastapi'],
        "location": "Teams"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "Message": "Event successfully added"
    }

    response = await default_client.post("/event/new", json=payload,
                                         headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient,
                            dummy_event: Event, access_token: str) -> None:
    payload = {
        "title": "Update FastAPI event"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/update_event/{str(dummy_event.id)}"

    response = await default_client.put(url, json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, dummy_event: Event,
                            access_token: str) -> None:
    test_response = {
        "Message": "Event Deleted Successfully"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{dummy_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient,
                               dummy_event: Event) -> None:
    url = f"/event/{str(dummy_event)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == dummy_event.creator
    assert response.json()["_id"] == str(dummy_event.id)
