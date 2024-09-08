"""Waldie Skill model."""

from typing import Dict, List

from pydantic import Field, model_validator
from typing_extensions import Annotated, Literal, Self

from ..common import WaldieBase, parse_code_string
from .skill_data import WaldieSkillData


class WaldieSkill(WaldieBase):
    """Waldie Skill.

    Attributes
    ----------
    id : str
        The ID of the skill.
    type : Literal["skill"]
        The type of the "node" in a graph: "skill".
    name : str
        The name of the skill.
    description : str
        The description of the skill.
    tags : List[str]
        The tags of the skill.
    requirements : List[str]
        The requirements of the skill.
    data : WaldieSkillData
        The data of the skill. See `WaldieSkillData`.
    """

    id: Annotated[
        str, Field(..., title="ID", description="The ID of the skill.")
    ]
    type: Annotated[
        Literal["skill"],
        Field(
            default="skill",
            title="Type",
            description="The type of the 'node' in a graph.",
        ),
    ]
    name: Annotated[
        str, Field(..., title="Name", description="The name of the skill.")
    ]
    description: Annotated[
        str,
        Field(
            ...,
            title="Description",
            description="The description of the skill.",
        ),
    ]
    tags: Annotated[
        List[str],
        Field(
            title="Tags",
            description="The tags of the skill.",
            default_factory=list,
        ),
    ]
    requirements: Annotated[
        List[str],
        Field(
            title="Requirements",
            description="The requirements of the skill.",
            default_factory=list,
        ),
    ]
    data: Annotated[
        WaldieSkillData,
        Field(..., title="Data", description="The data of the skill."),
    ]

    @model_validator(mode="after")
    def validate_data(self) -> Self:
        """Validate the data.

        Returns
        -------
        WaldieSkill
            The skill.

        Raises
        ------
        ValueError
            If the skill name is not in the content.
            If the skill content is invalid.
        """
        search = f"def {self.name}("
        if search not in self.data.content:
            raise ValueError(
                f"The skill name '{self.name}' is not in the content."
            )
        error, tree = parse_code_string(self.data.content)
        if error is not None or tree is None:
            raise ValueError(f"Invalid skill content: {error}")
        return self

    @property
    def content(self) -> str:
        """Get the content (source) of the skill."""
        return self.data.content

    @property
    def secrets(self) -> Dict[str, str]:
        """Get the secrets (environment variables) of the skill."""
        return self.data.secrets or {}
