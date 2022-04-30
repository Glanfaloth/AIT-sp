from tdw.librarian import ModelLibrarian, ModelRecord

librarian = ModelLibrarian()
tables = librarian.get_all_models_in_wnid("n04379243")  # table

TABLE_NAMES = [
    "quatre_dining_table",
    "Small_table_green_marble",
    "dining_room_table",
    "sm_table_white",
]
TABLES = [record for record in tables if record.name in TABLE_NAMES]