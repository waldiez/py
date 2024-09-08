"""Importing related string generation functions.

Functions
---------
add_autogen_dot_import
    Add an autogen dot import (from autogen.{x.y} import {z}).
get_imports_string
    Get the imports for the whole file/flow.
"""

from typing import Dict, List, Optional, Set, Tuple

DEFAULT_TYPING_IMPORTS = {
    "Any",
    "Callable",
    "Dict",
    "List",
    "Optional",
    "Tuple",
    "Union",
}


def add_autogen_dot_import(
    current_imports: Dict[str, List[str]], new_import: Tuple[str, str]
) -> Dict[str, List[str]]:
    """Add an autogen dot import (from autogen.{x} import {y}).

    Parameters
    ----------
    current_imports : Dict[str, List[str]]
        The current autogen dot imports.
    new_import : Tuple[str, str]
        The new import.

    Returns
    -------
    Dict[str, List[str]]
        The updated imports.

    Example
    -------
    ```python
    >>> current_imports = {"a": ["b", "c"], "d": ["e"]}
    >>> new_import = ("a", "f")
    >>> add_autogen_dot_import(current_imports, new_import)
    {'a': ['b', 'c', 'f'], 'd': ['e']}
    # and the final string would be:
    from autogen.a import b, c, f
    from autogen.d import e
    ```
    """
    dot_part, module_part = new_import
    if not module_part:
        return current_imports
    imports_copy = current_imports.copy()
    if dot_part not in current_imports:
        imports_copy[dot_part] = []
    imports_copy[dot_part].append(module_part)
    return imports_copy


def get_imports_string(
    imports: Set[str],
    skill_imports: Set[str],
    typing_imports: Optional[Set[str]] = None,
    builtin_imports: Optional[Set[str]] = None,
    other_imports: Optional[Set[str]] = None,
) -> str:
    """Get the imports.

    Parameters
    ----------
    imports : Set[str]
        The flow imports (e.g. from autogen.{x[y.z]} import {w}).
    skill_imports : Set[str]
        The skill imports.
    typing_imports : Set[str], optional
        The typing imports, by default None.
    builtin_imports : Set[str], optional
        The builtin imports, by default None.
    other_imports : Set[str], optional
        Other third party imports, by default None.

    Returns
    -------
    str
        The imports string.

    Example
    -------
    ```python
    >>> autogen_imports = {"from autogen import a", "from autogen.b import c"}
    >>> skill_imports = {"from skill_name import skill_name"}
    >>> get_imports_string(autogen_imports, skill_imports)

    from typing import Any, Callable, Dict, List, Optional, Tuple, Union
    from typing_extensions import Annotated

    from autogen import a
    from autogen.b import c

    from skill_name import skill_name'
    ```
    """
    if not typing_imports:
        typing_imports = DEFAULT_TYPING_IMPORTS
    if not builtin_imports:
        builtin_imports = set()
    if not other_imports:
        other_imports = set()
    string = _get_builtin_imports_string(builtin_imports, typing_imports)
    string += _get_third_party_imports_string(imports, other_imports)
    string += _get_skill_imports_string(skill_imports)
    string = "\n\n".join([line for line in string.split("\n\n") if line])
    while not string.endswith("\n\n"):
        string += "\n"
    return string


# pylint: disable=line-too-long
def _get_builtin_imports_string(
    builtin_imports: Set[str],
    typing_imports: Set[str],
    include_annotations: bool = True,
) -> str:
    """Get the builtin imports."""
    imports = []
    from_imports = []
    for imp in sorted(builtin_imports):
        if imp.startswith("from "):
            from_imports.append(imp)
        elif imp.startswith("import "):
            imports.append(imp)
        else:
            imports.append(f"import {imp}")
    if typing_imports:
        without_from_typing = []
        for typing_import in typing_imports:
            if typing_import.startswith("from typing import "):
                without_from_typing.extend(
                    typing_import.split("from typing import ")[1].split(", ")
                )
            else:
                without_from_typing.append(typing_import)
        from_imports.append(
            "from typing import "
            + ", ".join(sorted(without_from_typing))
            + "  # noqa"
        )
        if include_annotations:
            from_imports.append("from typing_extensions import Annotated")
    string = (
        "\n".join(sorted(imports)) + "\n\n" + "\n".join(sorted(from_imports))
    )
    return string


def _get_autogen_import(import_string: str) -> List[str]:
    """Get the autogen import.

    In case the import is a "full" import statement,
    we keep only the module to import.
    """
    things = []
    if import_string.startswith("from autogen import "):
        import_part = import_string.split("from autogen import ")[1]
        things = import_part.split(", ")
    return things


def _prepare_imports(
    autogen_imports: Set[str],
    autogen_dot_imports: Dict[str, List[str]],
    other_imports: Set[str],
) -> Tuple[List[str], Dict[str, List[str]]]:
    plain_imports = []  # plain `import {x}`
    autogen_imports_list = []  # from autogen import {y}
    for autogen_import in autogen_imports:
        autogen_imports_list.extend(_get_autogen_import(autogen_import))
    from_imports_dict: Dict[str, List[str]] = {
        "autogen": autogen_imports_list,
    }
    # from autogen.{z} import {w}  # z could be "a.b.c.."
    for autogen_dot_package, autogen_dot_modules in autogen_dot_imports.items():
        sub_package = f"autogen.{autogen_dot_package}"
        if sub_package not in from_imports_dict:
            from_imports_dict[sub_package] = []
        from_imports_dict[sub_package].extend(autogen_dot_modules)
    for imp in other_imports:
        if imp.startswith("from "):
            line_parts = imp.split("from ")
            package = line_parts[1].split(" import ")[0]
            if package not in from_imports_dict:
                from_imports_dict[package] = []
            import_part = line_parts[1].split(" import ")[1]
            things = import_part.split(", ")
            from_imports_dict[package].extend(things)
        elif imp.startswith("import "):
            plain_imports.append(imp)
        else:
            plain_imports.append(f"import {imp}")
    plain_imports.sort()
    return plain_imports, from_imports_dict


def _get_autogen_imports(
    imports: Set[str],
) -> Tuple[Set[str], Dict[str, List[str]], Set[str]]:
    """Get the autogen imports."""
    autogen_imports = set()
    _autogen_dot_imports: Dict[str, List[str]] = {}
    remaining_imports: Set[str] = set()
    for imp in imports:
        if imp.startswith("from autogen import "):
            autogen_imports.add(imp)
        elif imp.startswith("from autogen."):
            parts = imp.split("from autogen.")[1].split(" import ")
            if len(parts) == 2:
                package = parts[0]
                module = parts[1]
                if package not in _autogen_dot_imports:
                    _autogen_dot_imports[package] = []
                _autogen_dot_imports[package].append(module)
        else:
            remaining_imports.add(imp)
    # sort the autogen imports
    autogen_imports = set(sorted(list(autogen_imports)))
    autogen_dot_imports = {}
    # sort the autogen dot imports (both keys and values)
    sorted_keys = sorted(_autogen_dot_imports.keys())
    for key in sorted_keys:
        autogen_dot_imports[key] = sorted(_autogen_dot_imports[key])
    return autogen_imports, autogen_dot_imports, remaining_imports


def _get_third_party_imports_string(
    imports: Set[str],
    other_imports: Set[str],
) -> str:
    """Get the third party imports."""
    autogen_imports, autogen_dot_imports, rest = _get_autogen_imports(imports)
    rest.update(other_imports)
    plain_imports, from_imports_dict = _prepare_imports(
        autogen_imports=autogen_imports,
        autogen_dot_imports=autogen_dot_imports,
        other_imports=rest,
    )
    from_imports = []
    # pylint: disable=inconsistent-quotes
    for package, modules in from_imports_dict.items():
        # remove duplicates
        modules = sorted(set(modules))
        if modules:
            from_imports.append(f"from {package} import {', '.join(modules)}")
    string = (
        "\n\n" + "\n".join(plain_imports) + "\n\n" + "\n".join(from_imports)
    )
    return string


def _get_skill_imports_string(skill_imports: Set[str]) -> str:
    """Get the skill imports."""
    if not skill_imports:
        return ""
    string = "\n\n" + "\n".join(sorted(skill_imports)) + "\n"
    return string
