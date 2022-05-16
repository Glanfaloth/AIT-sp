from tdw.librarian import ModelLibrarian, ModelRecord

librarian = ModelLibrarian()

tables = librarian.get_all_models_in_wnid("n04379243")  # table
TABLE_NAMES = [
    "sm_table_white",
]
TABLES = [record for record in tables if record.name in TABLE_NAMES]

chairs = librarian.get_all_models_in_wnid("n03001627")
CHAIR_NAMES = [
    "emeco_navy_chair",
    "green_side_chair",
    "lapalma_stil_chair",
    "chair_thonet_marshall",
    "wood_chair",
    "chair_billiani_doll",
    "chair_willisau_riale",
]
CHAIRS = [record for record in chairs if record.name in CHAIR_NAMES]

cups = librarian.get_all_models_in_wnid("n03147509")  # cup
CUPS = [record for record in cups if not record.do_not_use]