"""Test waldiez.exporting.utils.object_string.*."""

from waldiez.exporting.utils.object_string import get_object_string


def test_get_object_string() -> None:
    """Test get_object_string."""
    # Given
    obj1 = {
        "key1": "value1",
        "key2": ["value2", None],
        "key3": {"key4": "value4"},
    }
    # When
    result = get_object_string(obj1, tabs=0)
    # Then
    excepted = """{
    "key1": "value1",
    "key2": [
        "value2",
        None
    ],
    "key3": {
        "key4": "value4"
    }
}"""
    assert result == excepted

    # Given
    obj2 = {
        "key1": "value1",
        "key2": ["value2", "value3"],
        "key3": {"key4": "value4"},
    }
    # When
    result = get_object_string(obj2, tabs=1)
    # Then
    excepted = """{
        "key1": "value1",
        "key2": [
            "value2",
            "value3"
        ],
        "key3": {
            "key4": "value4"
        }
    }"""
    # Given
    obj3 = ["value1", {"value2": {"key1": 4}}]
    # When
    result = get_object_string(obj3, tabs=1)
    # Then
    excepted = """[
        "value1",
        {
            "value2": {
                "key1": 4
            }
        }
    ]"""
