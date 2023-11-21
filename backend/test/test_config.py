# Definisci l'ordine dei test in un dizionario
TEST_ORDER = {
    "test_setup": {"setup": "order=1"},
    "test_users": {
        "test_create_users": ["fail", "pass"],
        "test_read_users": ["fail", "pass"],
        "test_update_users": ["fail", "pass"],
        "test_delete_users": ["fail", "pass"],
    },
    "test_classes": {
        "test_create_classes": ["fail", "pass"],
    },
}
