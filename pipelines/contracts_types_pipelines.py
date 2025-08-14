def get_main_with_type_pipeline(skip=0, limit=10):
    return [
        {
            "$lookup": {
                "from": "types",
                "localField": "type_id",
                "foreignField": "_id",
                "as": "type_info"
            }
        },
        {"$unwind": "$type_info"},
        {"$match": {"active": True}},
        {"$skip": skip},
        {"$limit": limit},
        {
            "$project": {
                "_id": 1,
                "name": 1,  # Cambia "name" por el campo real del modelo principal
                "type_id": 1,
                "type_description": "$type_info.description",
                "active": 1
            }
        }
    ]

def get_main_by_type_description_pipeline(type_description: str, skip=0, limit=10):
    return [
        {
            "$lookup": {
                "from": "types",
                "localField": "type_id",
                "foreignField": "_id",
                "as": "type_info"
            }
        },
        {"$unwind": "$type_info"},
        {
            "$match": {
                "type_info.description": {"$regex": f"^{type_description}$", "$options": "i"},
                "active": True
            }
        },
        {"$skip": skip},
        {"$limit": limit}
    ]

def count_main_pipeline(type_description=None):
    pipeline = [
        {
            "$lookup": {
                "from": "types",
                "localField": "type_id",
                "foreignField": "_id",
                "as": "type_info"
            }
        },
        {"$unwind": "$type_info"},
        {"$match": {"active": True}}
    ]

    if type_description:
        pipeline.append({
            "$match": {
                "type_info.description": {"$regex": f"^{type_description}$", "$options": "i"}
            }
        })

    pipeline.append({"$count": "total"})

    return pipeline
