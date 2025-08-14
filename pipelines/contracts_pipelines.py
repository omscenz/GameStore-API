def get_main_model_list_pipeline(skip: int = 0, limit: int = 10):
    return [
        {"$match": {"active": True}},
        {"$skip": skip},
        {"$limit": limit},
        # Puedes añadir aquí más etapas si quieres enriquecer con lookup a tipos
        {"$lookup": {
            "from": "types",
            "localField": "type_id",
            "foreignField": "_id",
            "as": "type_info"
        }},
        {"$unwind": {"path": "$type_info", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 1,
            "name": 1,  # Cambia este campo por el que tenga tu modelo principal
            "type_id": 1,
            "active": 1,
            "type_info.description": 1
        }}
    ]

def count_main_model_pipeline():
    return [
        {"$match": {"active": True}},
        {"$count": "total"}
    ]

# Pipeline para verificar si un tipo está asociado a algún documento en modelo principal
def check_type_in_use_pipeline(type_id: str):
    return [
        {"$match": {"type_id": type_id, "active": True}},
        {"$count": "usage_count"}
    ]
