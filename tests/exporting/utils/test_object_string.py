"""Test waldiez.exporting.utils.object_string.*."""

from waldiez.exporting.utils.object_string import get_object_string


# fmt: off
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
    assert result == excepted
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

    assert result == excepted

    # Given
    obj4 = {
        "key": 'r"string"'
    }
    # When
    result = get_object_string(obj4, tabs=1)
    # Then
    excepted = """{
        "key": r"string"
    }"""
    assert result == excepted

# fmt: on
