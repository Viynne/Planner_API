from fastapi import APIRouter, HTTPException, status, Depends
from beanie import PydanticObjectId
from models.events import Event, EventUpdate
from typing import List
from database.connection import Database
from auth.authenticate import authenticate


event_route = APIRouter(tags=["Events"])

event_db = Database(Event)


@event_route.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_db.get_all()
    return events


@event_route.get("/{event_id}", response_model=Event)
async def retrieve_event_by_id(event_id: PydanticObjectId) -> Event:
    event = await event_db.get(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with provided ID not found"
        )
    return event


@event_route.post("/new")
async def add_new_event(new_event: Event, user: str = Depends(authenticate)) -> dict:
    new_event.creator = user
    await event_db.create_db(new_event)
    return {
        "Message": f"Event successfully added"
    }


@event_route.put("/update_event/{event_id}", response_model=Event)
async def edit_specified_event(event_id: PydanticObjectId, patch_data: EventUpdate,
                               user: str = Depends(authenticate)) -> Event:
    event = await event_db.get(event_id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    update_event = await event_db.update(event_id, patch_data)
    if not update_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found"
        )
    return update_event


@event_route.delete("/{event_id}")
async def delete_event(event_id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_db.get(event_id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    event = await event_db.deleted(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID not Found"
        )
    return {
        "Message": "Event Deleted Successfully"
    }
