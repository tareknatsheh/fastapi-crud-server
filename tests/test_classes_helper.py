import utils.classes_helper as c
import pytest
from models.classes_models import Class

classes_list = [
        {"id": 1, "name": "math", "teacher": "Ms. Johnson", "topic": "Algebra"},
        {"id": 2, "name": "history", "teacher": "Mr. Khalil", "topic": "World War II"},
        {"id": 3, "name": "science", "teacher": "Dr. Lee", "topic": "Chemical Reactions"}
    ]

def test_get_class_by_id():
    assert c.get_class_by_id(classes_list, 1) == Class(**classes_list[0])

def test_no_item_matches_id():
    assert c.get_class_by_id(classes_list, 100) == None

def test_wrong_id_type():
    with pytest.raises(ValueError):
        c.get_class_by_id(classes_list, "a string")

    with pytest.raises(ValueError):
        c.get_class_by_id(classes_list, -10)

def test_empty_classes_list():
    with pytest.raises(ValueError):
        c.get_class_by_id([], 1)

def test_wrong_classes_list_type():
    with pytest.raises(ValueError):
        c.get_class_by_id("a string", 1)

    with pytest.raises(ValueError):
        c.get_class_by_id(None, 1)

def test_a_class_has_specific_keys():
    with pytest.raises(ValueError):
        c.get_class_by_id([{"id": 1}], 1)

    
    