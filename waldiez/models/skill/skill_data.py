"""Waldiez Skill model."""

from typing import Dict

from pydantic import Field
from typing_extensions import Annotated

from ..common import WaldiezBase


class WaldiezSkillData(WaldiezBase):
    """Waldiez Skill Data.

    Attributes
    ----------
    content : str
        The content (source code) of the skill.
    secrets : Dict[str, str]
        The secrets (environment variables) of the skill.
    """

    content: Annotated[
        str,
        Field(
            ...,
            title="Content",
            description="The content (source code) of the skill.",
        ),
    ]
    secrets: Annotated[
        Dict[str, str],
        Field(
            default_factory=dict,
            title="Secrets",
            description="The secrets (environment variables) of the skill.",
        ),
    ]
