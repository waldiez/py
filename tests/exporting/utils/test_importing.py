"""Test waldiez.exporting.utils.importing.*."""

from waldiez.exporting.utils.importing import (
    DEFAULT_TYPING_IMPORTS,
    add_autogen_dot_import,
    get_imports_string,
)


def test_add_autogen_dot_import() -> None:
    """Test add_autogen_dot_import."""
    # Given
    current_imports = {"a": ["b", "c"], "d": ["e"]}
    new_import = ("a", "f")
    # When/Then
    assert add_autogen_dot_import(current_imports, new_import) == {
        "a": ["b", "c", "f"],
        "d": ["e"],
    }
    # Given
    current_imports = {"a": ["b", "c"], "d": ["e"]}
    new_import = ("e", "f")
    # When/Then
    assert add_autogen_dot_import(current_imports, new_import) == {
        "a": ["b", "c"],
        "d": ["e"],
        "e": ["f"],
    }
    # Given
    current_imports = {"a": ["b", "c"], "d": ["e"]}
    new_import = ("e", "")
    # When/Then
    assert add_autogen_dot_import(current_imports, new_import) == {
        "a": ["b", "c"],
        "d": ["e"],
    }


def test_get_imports_string() -> None:
    """Test get_imports_string."""
    # Given
    imports = {
        "from other import f",
        "from autogen import a, b",
        "from autogen.a import b, c",
        "from autogen.d import e",
    }
    skill_imports = {"from c import c", "from d import d"}
    no_typing_string = ", ".join(sorted(DEFAULT_TYPING_IMPORTS))
    # When
    imports_string = get_imports_string(imports, skill_imports)
    # Then
    assert imports_string == (
        f"from typing import {no_typing_string}  # noqa\n"
        "from typing_extensions import Annotated\n\n"
        "from autogen import a, b\n"
        "from autogen.a import b, c\n"
        "from autogen.d import e\n"
        "from other import f\n\n"
        "from c import c\n"
        "from d import d\n\n"
    )
    # Given
    imports = set()
    skill_imports = set()
    # When/Then
    assert get_imports_string(imports, skill_imports) == (
        f"from typing import {no_typing_string}  # noqa\n"
        "from typing_extensions import Annotated\n\n"
    )
    # Given
    imports = {"from autogen import a, b"}
    skill_imports = set()
    builtin_imports = {"os", "import sys", "from pathlib import Path"}
    typing_imports = {"Any", "from typing import List"}
    # When/Then
    assert get_imports_string(
        imports,
        skill_imports,
        typing_imports,
        builtin_imports,
    ) == (
        "import os\n"
        "import sys\n\n"
        "from pathlib import Path\n"
        "from typing import Any, List  # noqa\n"
        "from typing_extensions import Annotated\n\n"
        "from autogen import a, b\n\n"
    )
    # Given
    imports = {
        "pandas",
        "from sklearn import tree",
        "import numpy as np",
    }
    skill_imports = set()
    builtin_imports = {"os", "import sys", "from pathlib import Path"}
    typing_imports = {"Any", "from typing import List"}
    local_imports = {
        "from waldiez_api_keys import get_model_api_key",
    }
    # When/Then
    assert get_imports_string(
        imports,
        skill_imports,
        typing_imports,
        builtin_imports,
        local_imports,
    ) == (
        "import os\n"
        "import sys\n\n"
        "from pathlib import Path\n"
        "from typing import Any, List  # noqa\n"
        "from typing_extensions import Annotated\n\n"
        "import numpy as np\n"
        "import pandas\n\n"
        "from sklearn import tree\n\n"
        "from waldiez_api_keys import get_model_api_key\n\n"
    )
