"""Test waldiez.exporting.flow.flow*."""

from waldiez.exporting.flow.flow import export_flow
from waldiez.models import Waldiez

from ..flow_helpers import get_flow


def test_export_flow() -> None:
    """Test export_flow."""
    # Given
    flow = get_flow()

    # when
    agents_names = {}
    agents = []
    model_names = {}
    models = []
    skill_names = {}
    skills = []
    chat_names = {}
    chats = []
    for agent in flow.data.agents.members:
        agents_names[agent.id] = agent.name
        agents.append(agent)
    for model in flow.data.models:
        model_names[model.id] = model.name
        models.append(model)
    for skill in flow.data.skills:
        skill_names[skill.id] = skill.name
        skills.append(skill)
    for chat in flow.data.chats:
        chat_names[chat.id] = chat.name
        chats.append(chat)
    for notebook in [True, False]:
        exported = export_flow(
            waldiez=Waldiez(flow=flow),
            agents=(agents, agents_names),
            models=(models, model_names),
            skills=(skills, skill_names),
            chats=(chats, chat_names),
            output_dir=None,
            notebook=notebook,
        )
        # passing the flow validation should be enough (to cover "export_flow")
        # we can check the (full) file contents in waldiez.exporter
        assert exported
