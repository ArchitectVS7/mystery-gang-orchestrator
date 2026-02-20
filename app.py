#!/usr/bin/env python3
"""
Mystery Gang Orchestrator — Streamlit Web Demo

Install deps:  pip install -e ".[web]"
Run:           streamlit run app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
from character import CharacterEngine
from assembly import TaskAnalyzer, TeamSelector, AssemblySceneGenerator, TaskType, TaskAnalysis
from technobabble import TechnobabbleTranslator, Theme

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Gang Orchestrator",
    page_icon="🔍",
    layout="wide",
    menu_items={"About": "github.com/ArchitectVS7/mystery-gang-orchestrator"},
)

# ── Constants ─────────────────────────────────────────────────────────────────
THEME_OPTIONS: dict[str, Theme] = {
    "🐕  Scooby-Doo": Theme.SCOOBY,
    "🖖  Star Trek": Theme.STAR_TREK,
    "👻  Ghostbusters": Theme.GHOSTBUSTERS,
    "🦸  Superhero": Theme.SUPERHERO,
    "🏴‍☠️  Pirates": Theme.PIRATES,
    "🧙  Wizards": Theme.WIZARDS,
}

CHARACTER_EMOJI = {
    "fred": "👔",
    "velma": "🧡",
    "daphne": "💜",
    "shaggy": "🟢",
    "scooby": "🐕",
}

SAMPLE_TASKS = [
    "Create REST API with authentication",
    "Fix null pointer exception in user service",
    "Deploy to Kubernetes cluster",
    "Write documentation for the new API",
    "Add unit tests for the auth module",
    "Optimize database query performance",
    "Build React component for the dashboard",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _generate_deliverables(analysis: TaskAnalysis) -> list[str]:
    """Return deliverable strings derived from task type and keywords."""
    keywords = analysis.keywords
    primary_map = {
        TaskType.BACKEND: f"REST API implemented ({', '.join(keywords[:2]) or 'endpoints'} covered)",
        TaskType.FRONTEND: f"UI component built ({', '.join(keywords[:2]) or 'interface'} complete)",
        TaskType.DEBUGGING: f"Bug resolved ({keywords[0] if keywords else 'issue'} fixed)",
        TaskType.DOCS: f"Documentation written ({', '.join(keywords[:2]) or 'guide'} complete)",
        TaskType.TESTING: f"Test suite passing ({', '.join(keywords[:2]) or 'coverage'} verified)",
        TaskType.DEVOPS: f"Pipeline configured ({', '.join(keywords[:2]) or 'infra'} deployed)",
        TaskType.GENERAL: "Mission objective completed",
    }
    return [
        primary_map.get(analysis.task_type, "Primary objective complete"),
        "Error handling added",
        "Documentation updated",
        "All tests passing",
        "Bug fixed",
    ]


def _render_deliverable(technical: str, translated: str, mode: str):
    if mode == "Raw":
        st.markdown(f"✓ `{technical}`")
    elif mode == "Both":
        st.markdown(f"✓ {translated}")
        st.caption(f"  ↳ `{technical}`")
    else:
        st.markdown(f"✓ {translated}")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎭 Mystery Gang")
    st.caption("Agent orchestration as Saturday morning cartoons")
    st.divider()

    theme_label = st.selectbox("Theme", list(THEME_OPTIONS.keys()))
    selected_theme = THEME_OPTIONS[theme_label]

    mode = st.radio("Output Mode", ["Translated", "Raw", "Both"])

    st.divider()
    st.caption(
        "LLM translation is enabled automatically when "
        "`ANTHROPIC_API_KEY` is set in the environment."
    )

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("🔍 Mystery Gang Orchestrator")
st.caption("Transform boring agent output into cartoon adventures — pick a theme and run a mission.")

col_task, col_sample = st.columns([3, 1])
with col_task:
    task = st.text_input(
        "Mission Briefing",
        value="Create REST API with authentication",
        placeholder="Describe the task for the gang…",
    )
with col_sample:
    st.markdown("<br>", unsafe_allow_html=True)
    sample = st.selectbox("Sample tasks", ["—"] + SAMPLE_TASKS, label_visibility="collapsed")
    if sample != "—":
        task = sample

run = st.button("🚨 Assemble the Gang!", type="primary", use_container_width=True)

if not run or not task:
    st.stop()

# ── Initialise engines ────────────────────────────────────────────────────────
char_engine = CharacterEngine()
analyzer = TaskAnalyzer()
selector = TeamSelector()
scene_gen = AssemblySceneGenerator(char_engine)
translator = TechnobabbleTranslator(use_llm=True)
translator.set_theme(selected_theme)
translator.set_mode(show_raw=(mode == "Raw"), show_both=(mode == "Both"))

theme_info = translator.get_theme_info()

# ── Mission Analysis ──────────────────────────────────────────────────────────
st.divider()
st.subheader("📊 Mission Analysis")

analysis = analyzer.analyze(task)

m1, m2, m3 = st.columns(3)
m1.metric("Task Type", analysis.task_type.value.title())
m2.metric("Confidence", f"{analysis.confidence:.0f}%")
m3.metric("Team", theme_info["team_name"])

if analysis.keywords:
    st.caption(f"Keywords detected: {', '.join(analysis.keywords)}")

# ── Team Assembly ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("🚨 Team Assembled")

team = selector.select(task)

team_cols = st.columns(len(team))
for i, char_id in enumerate(team):
    char = char_engine.get_character(char_id)
    with team_cols[i]:
        st.markdown(f"### {CHARACTER_EMOJI.get(char_id, '🎭')}")
        st.markdown(f"**{char.name.split()[0]}**")
        st.caption(char.role)

with st.expander("View assembly scene"):
    scene = scene_gen.generate(team, task, analysis)
    st.code(scene, language=None)

# ── Work Session ──────────────────────────────────────────────────────────────
st.divider()
st.subheader("💬 Work Session")

# Fred — planning
char = char_engine.get_character("fred")
with st.chat_message("Fred", avatar=CHARACTER_EMOJI["fred"]):
    st.markdown(f"**{char.name}**")
    st.write(char_engine.generate_dialogue("fred", "planning", task))

# Velma — researches + API endpoint
char = char_engine.get_character("velma")
with st.chat_message("Velma", avatar=CHARACTER_EMOJI["velma"]):
    st.markdown(f"**{char.name}**")
    st.write(char_engine.generate_dialogue("velma", "discovery", task))
    st.info(f"🔧 {translator.translate('Created API endpoint')}")

# Daphne — review + error handling
char = char_engine.get_character("daphne")
with st.chat_message("Daphne", avatar=CHARACTER_EMOJI["daphne"]):
    st.markdown(f"**{char.name}**")
    st.write(char_engine.generate_dialogue("daphne", "review", task))
    st.info(f"🔧 {translator.translate('Error handling added')}")

# Shaggy — docs
char = char_engine.get_character("shaggy")
with st.chat_message("Shaggy", avatar=CHARACTER_EMOJI["shaggy"]):
    st.markdown(f"**{char.name}**")
    st.write(char_engine.generate_dialogue("shaggy", "default", task))
    st.info(f"🔧 {translator.translate('Documentation updated')}")

# Scooby — bug detected
char = char_engine.get_character("scooby")
with st.chat_message("Scooby", avatar=CHARACTER_EMOJI["scooby"]):
    st.markdown(f"**{char.name}**")
    st.write(char_engine.generate_dialogue("scooby", "discovery", task))
    st.warning(f"🐛 {translator.translate('Bug detected in user service')}")

# Velma — bug fixed
with st.chat_message("Velma", avatar=CHARACTER_EMOJI["velma"]):
    char = char_engine.get_character("velma")
    st.markdown(f"**{char.name}**")
    st.write("Jinkies! I found the solution in the docs!")
    st.success(f"✅ {translator.translate('Fixed null pointer exception')}")

# Scooby — tests
with st.chat_message("Scooby", avatar=CHARACTER_EMOJI["scooby"]):
    st.markdown("**Scooby-Doo**")
    st.write("Rerr rerr rerr! Running the tests now!")
    st.success(f"🎉 {translator.translate('All tests passing')}")

# ── Victory ───────────────────────────────────────────────────────────────────
st.divider()
victory_phrase = translator._get_theme_configs()[selected_theme].victory_phrase
st.success(f"## ✅ Mission Complete — {victory_phrase}")

st.subheader("📦 Deliverables")
for technical in _generate_deliverables(analysis):
    translated = translator.translate(technical)
    _render_deliverable(technical, translated, mode)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.divider()
s1, s2, s3, s4 = st.columns(4)
s1.metric("Theme", selected_theme.value.replace("_", " ").title())
s2.metric("Mode", mode)
s3.metric("Team Size", len(team))
s4.metric("Task Type", analysis.task_type.value.title())
