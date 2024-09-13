from fastapi import APIRouter, Depends, HTTPException
from .models import BlockList, BlockListResponse, SiteResponse, UpdateBlockList
from deps.auth.auth import get_current_user
from uuid import uuid4
from app.db import db
from typing import List
from datetime import datetime, timezone


router = APIRouter()


@router.post("", status_code=201, description="Create block list")
async def create_block_list(block_list: BlockList, user=Depends(get_current_user)) -> BlockListResponse:
    owner = user["email"]  # should be id
    block_list_dict = block_list.model_dump()

    id = str(uuid4())
    block_list_dict["_id"] = id
    block_list_dict["owner"] = owner
    for site in block_list_dict["entries"]:
        site["_id"] = str(uuid4())

    insert_id = db["block_lists"].insert_one(block_list_dict).inserted_id
    if not insert_id:
        # alert team of exception
        raise HTTPException(status_code=500, detail="Failed to save list. Please try again later")

    block_list_dict["id"] = block_list_dict.pop("_id")
    for site in block_list_dict["entries"]:
        site["id"] = site.pop("_id")

    res = BlockListResponse(
        id=id,
        name=block_list.name,
        # comment=block_list.comment,
        type=block_list.type,
        created=block_list.created,
        owner=owner,
        entries=[
            SiteResponse(
                    id=site["id"],
                    site_url=site["site_url"],
                    # comment=site.get("comment") or None,
                    created=site["created"]
                ) for site in block_list_dict["entries"]
            ]
    )
    return res


@router.get("", status_code=200, description="Get user block lists")
async def get_user_block_lists(user=Depends(get_current_user)) -> List[BlockListResponse]:
    owner = user["email"]  # should be user_id
    check_redis = False
    # return user

    if not check_redis:
        pass
    else:
        return {"message": "This is coming from redis"}

    block_lists = db["block_lists"].find({"owner": owner})

    if not block_lists:
        raise HTTPException(status_code=404, detail="No lists found for this user. Please create a block list")

    res = [
        BlockListResponse(
            id=block_list["_id"],
            owner=owner,
            name=block_list["name"],
            type=block_list["type"],
            # comment=block_list["comment"],
            created=block_list["created"],
            updated=block_list.get("updated"),
            entries=[SiteResponse(
                id=site.get("_id"),
                site_url=site["site_url"],
                # comment=site["comment"],
                created=site["created"],
                updated=site.get("updated")
            ) for site in block_list["entries"]]
        ) for block_list in block_lists
        ]
    return res


@router.get("/{id}", status_code=200, description="Get single block list", dependencies=[Depends(get_current_user)])
async def get_single_block_list(id: str) -> BlockListResponse:
    block_list = db["block_lists"].find_one({"_id": id})

    if not block_list:
        raise HTTPException(status_code=404, detail="No block list with this ID has been found.")

    res = BlockListResponse(
        id=block_list["_id"],
        owner=block_list["owner"],
        name=block_list["name"],
        type=block_list["type"],
        comment=block_list["comment"],
        created=block_list["created"],
        updated=block_list.get("updated"),
        entries=[SiteResponse(
                id=site["id"],
                site_url=site["site_url"],
                # comment=site["comment"],
                created=site["created"],
                updated=site.get("updated")
            ) for site in block_list["entries"]]
    )
    return res


@router.delete("/{id}", status_code=200, description="Delete Blocklist", dependencies=[Depends(get_current_user)])
def delete_block_list(id: str):
    db["block_lists"].delete_one({"_id": id})
    return {"message": "List deleted successfully!"}


@router.patch("/{id}", status_code=200, dependencies=[Depends(get_current_user)])
def update_block_list(id: str, blockList: UpdateBlockList):
    block_list = blockList.model_dump(exclude_none=True)

    for site in block_list["entries"]:
        if site.get("id"):
            site["_id"] = site.get("id")
        else:
            site["_id"] = str(uuid4())
            site["created"] = datetime.now(timezone.utc)
    db["block_lists"].update_one({"_id": id}, {"$set": block_list})
    return {"message": "Block list updated successfully."}
