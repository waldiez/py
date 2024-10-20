"""Test waldiez.exporting.utils.comments.*."""

from waldiez.exporting.utils.comments import (
    PYLINT_RULES,
    comment,
    get_comment,
    get_pylint_ignore_comment,
)


def test_comment() -> None:
    """Test comment."""
    assert comment(True, 2) == "# ## "
    assert comment(False) == "# "
    assert comment(True) == "# # "
    assert comment(False, 2) == "# "


def test_get_comment() -> None:
    """Test get_comment."""
    assert get_comment("agents", True) == "\n# ## Agents\n"
    assert get_comment("skills", False) == "\n# Skills\n"
    assert get_comment("models", True) == "\n# ## Models\n"
    assert get_comment("nested", False) == "\n# Nested Chats\n"
    assert get_comment("run", True) == "\n# ## Run the flow\n"
    assert get_comment("logging", False) == "\n# Start Logging\n"
    assert get_comment("invalid", False) == "# "  # type: ignore


def test_get_pylint_ignore_comment() -> None:
    """Test get_pylint_ignore_comment."""
    no_rules_string = ",".join(PYLINT_RULES)
    assert (
        get_pylint_ignore_comment(False)
        == f"# pylint: disable={no_rules_string}\n"
    )
    assert (
        get_pylint_ignore_comment(True)
        == f"\n# pylint: disable={no_rules_string}\n"
    )
    assert get_pylint_ignore_comment(
        True, ["invalid-name", "line-too-long"]
    ) == ("\n# pylint: disable=invalid-name,line-too-long\n")
    assert get_pylint_ignore_comment(False, ["invalid-name"]) == (
        "# pylint: disable=invalid-name\n"
    )
    assert get_pylint_ignore_comment(True, ["line-too-long"]) == (
        "\n# pylint: disable=line-too-long\n"
    )
    assert get_pylint_ignore_comment(
        False, ["invalid-name", "line-too-long"]
    ) == ("# pylint: disable=invalid-name,line-too-long\n")
    assert get_pylint_ignore_comment(True, ["invalid-name"]) == (
        "\n# pylint: disable=invalid-name\n"
    )
