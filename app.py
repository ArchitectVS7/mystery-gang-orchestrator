#!/usr/bin/env python3
"""
Mystery Gang Orchestrator — Streamlit Web App

Run:   streamlit run app.py
Deps:  pip install -e ".[web]"

Two modes:
  Simulation    — canned gang work-session (no external system needed)
  Event Log     — load a real agent run as JSON and watch the gang narrate it
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

from character import CharacterEngine
from assembly import TaskAnalyzer, TeamSelector, AssemblySceneGenerator, TaskType, TaskAnalysis
from technobabble import TechnobabbleTranslator, Theme
from event_schema import CharacterMapping, EventLog
from event_renderer import render_event_log, extract_deliverables, NarrationItem

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Gang Orchestrator",
    page_icon="🔍",
    layout="wide",
)

THEME_OPTIONS: dict = {
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

SAMPLE_LOG_PATH = Path(__file__).parent / "data" / "sample_run.json"


# ── Shared helpers ────────────────────────────────────────────────────────────

def _make_engines(selected_theme: Theme, mode: str):
    char_engine = CharacterEngine()
    translator = TechnobabbleTranslator(use_llm=True)
    translator.set_theme(selected_theme)
    translator.set_mode(show_raw=(mode == "Raw"), show_both=(mode == "Both"))
    return char_engine, translator


def _render_narration_item(item: NarrationItem, char_engine, mode: str):
    """Render one NarrationItem as a Streamlit chat message."""
    char = char_engine.get_character(item.character_id)
    avatar = CHARACTER_EMOJI.get(item.character_id, "🎭")

    with st.chat_message(item.character_id, avatar=avatar):
        st.markdown(f"**{char.name}**")

        if item.dialogue:
            st.write(item.dialogue)

        if mode == "Both" and item.update:
            st.caption(f"↳ `{item.raw_content}`")

        if item.update:
            if item.update_style == "success":
                st.success(f"✅ {item.update}")
            elif item.update_style == "error":
                st.error(f"🚨 {item.update}")
            elif item.update_style == "warning":
                st.warning(f"⚠️ {item.update}")
            else:
                st.info(f"🔧 {item.update}")


def _render_deliverable(technical: str, translated: str, mode: str):
    if mode == "Raw":
        st.markdown(f"✓ `{technical}`")
    elif mode == "Both":
        st.markdown(f"✓ {translated}")
        st.caption(f"  ↳ `{technical}`")
    else:
        st.markdown(f"✓ {translated}")


def _simulation_deliverables(analysis: TaskAnalysis) -> list:
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


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎭 Mystery Gang")
    st.caption("Agent orchestration as Saturday morning cartoons")
    st.divider()

    theme_label = st.selectbox("Theme", list(THEME_OPTIONS.keys()))
    selected_theme = THEME_OPTIONS[theme_label]

    mode = st.radio("Output Mode", ["Translated", "Raw", "Both"])

    st.divider()
    source = st.radio("Mission Source", ["Simulation", "Event Log"])

    st.divider()
    if source == "Event Log":
        st.caption(
            "Upload a JSON event log from your agent system, or use the "
            "built-in sample run to see the format."
        )
    else:
        st.caption(
            "Simulation mode runs a canned work session — no external "
            "system required."
        )

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("🔍 Mystery Gang Orchestrator")
st.caption("Transform agent output into cartoon adventures — pick a theme and run a mission.")

# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION MODE
# ══════════════════════════════════════════════════════════════════════════════
if source == "Simulation":
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

    char_engine, translator = _make_engines(selected_theme, mode)
    theme_info = translator.get_theme_info()
    analyzer = TaskAnalyzer()
    selector = TeamSelector()
    scene_gen = AssemblySceneGenerator(char_engine)

    # Analysis
    st.divider()
    st.subheader("📊 Mission Analysis")
    analysis = analyzer.analyze(task)
    m1, m2, m3 = st.columns(3)
    m1.metric("Task Type", analysis.task_type.value.title())
    m2.metric("Confidence", f"{analysis.confidence:.0f}%")
    m3.metric("Team", theme_info["team_name"])
    if analysis.keywords:
        st.caption(f"Keywords detected: {', '.join(analysis.keywords)}")

    # Assembly
    st.divider()
    st.subheader("🚨 Team Assembled")
    team = selector.select(task)
    cols = st.columns(len(team))
    for i, char_id in enumerate(team):
        char = char_engine.get_character(char_id)
        with cols[i]:
            st.markdown(f"### {CHARACTER_EMOJI.get(char_id, '🎭')}")
            st.markdown(f"**{char.name.split()[0]}**")
            st.caption(char.role)
    with st.expander("View assembly scene"):
        scene = scene_gen.generate(team, task, analysis)
        st.code(scene, language=None)

    # Work session
    st.divider()
    st.subheader("💬 Work Session")

    with st.chat_message("fred", avatar=CHARACTER_EMOJI["fred"]):
        char = char_engine.get_character("fred")
        st.markdown(f"**{char.name}**")
        st.write(char_engine.generate_dialogue("fred", "planning", task))

    with st.chat_message("velma", avatar=CHARACTER_EMOJI["velma"]):
        char = char_engine.get_character("velma")
        st.markdown(f"**{char.name}**")
        st.write(char_engine.generate_dialogue("velma", "discovery", task))
        st.info(f"🔧 {translator.translate('Created API endpoint')}")
        if mode == "Both":
            st.caption("↳ `Created API endpoint`")

    with st.chat_message("daphne", avatar=CHARACTER_EMOJI["daphne"]):
        char = char_engine.get_character("daphne")
        st.markdown(f"**{char.name}**")
        st.write(char_engine.generate_dialogue("daphne", "review", task))
        st.info(f"🔧 {translator.translate('Error handling added')}")
        if mode == "Both":
            st.caption("↳ `Error handling added`")

    with st.chat_message("shaggy", avatar=CHARACTER_EMOJI["shaggy"]):
        char = char_engine.get_character("shaggy")
        st.markdown(f"**{char.name}**")
        st.write(char_engine.generate_dialogue("shaggy", "default", task))
        st.info(f"🔧 {translator.translate('Documentation updated')}")
        if mode == "Both":
            st.caption("↳ `Documentation updated`")

    with st.chat_message("scooby", avatar=CHARACTER_EMOJI["scooby"]):
        char = char_engine.get_character("scooby")
        st.markdown(f"**{char.name}**")
        st.write(char_engine.generate_dialogue("scooby", "discovery", task))
        st.warning(f"🐛 {translator.translate('Bug detected in user service')}")
        if mode == "Both":
            st.caption("↳ `Bug detected in user service`")

    with st.chat_message("velma", avatar=CHARACTER_EMOJI["velma"]):
        char = char_engine.get_character("velma")
        st.markdown(f"**{char.name}**")
        st.write("Jinkies! I found the solution in the docs!")
        st.success(f"✅ {translator.translate('Fixed null pointer exception')}")
        if mode == "Both":
            st.caption("↳ `Fixed null pointer exception`")

    with st.chat_message("scooby", avatar=CHARACTER_EMOJI["scooby"]):
        st.markdown("**Scooby-Doo**")
        st.write("Rerr rerr rerr! Running the tests now!")
        st.success(f"🎉 {translator.translate('All tests passing')}")
        if mode == "Both":
            st.caption("↳ `All tests passing`")

    # Victory
    st.divider()
    victory = translator._get_theme_configs()[selected_theme].victory_phrase
    st.success(f"## ✅ {victory}")

    st.subheader("📦 Deliverables")
    for technical in _simulation_deliverables(analysis):
        _render_deliverable(technical, translator.translate(technical), mode)

    st.divider()
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Theme", selected_theme.value.replace("_", " ").title())
    s2.metric("Mode", mode)
    s3.metric("Team Size", len(team))
    s4.metric("Task Type", analysis.task_type.value.title())


# ══════════════════════════════════════════════════════════════════════════════
# EVENT LOG MODE
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("Load a JSON event log from your agent system to watch the gang narrate a real run.")

    # Character mapping
    with st.expander("⚙️ Agent → Character mapping", expanded=False):
        st.caption(
            "Map your system's agent IDs to gang characters. "
            "Substring matching works — `my_planner_agent` matches `planner` → Fred."
        )
        default_mapping = CharacterMapping.default().mappings
        mapping_json = st.text_area(
            "Mapping JSON (agent_id → character_id)",
            value=json.dumps(default_mapping, indent=2),
            height=220,
        )
        try:
            char_mapping = CharacterMapping.from_dict(json.loads(mapping_json))
            st.success("Mapping valid")
        except (json.JSONDecodeError, Exception) as e:
            st.error(f"Invalid JSON: {e}")
            char_mapping = CharacterMapping.default()

    # Log source
    col_upload, col_sample = st.columns([2, 1])
    with col_upload:
        uploaded = st.file_uploader(
            "Upload event log (.json)",
            type=["json"],
            help="JSON array of agent events. See data/sample_run.json for the format.",
        )
    with col_sample:
        st.markdown("<br><br>", unsafe_allow_html=True)
        use_sample = st.button("Use sample run", help="Load the built-in sample run from data/sample_run.json")

    run = st.button("🚨 Visualize Run!", type="primary", use_container_width=True)

    if not run:
        # Show the schema when idle so users know what format to emit
        with st.expander("📋 Event schema — what your system needs to emit"):
            st.code(
                json.dumps(
                    [
                        {
                            "event_type": "task_start",
                            "agent_id": "orchestrator",
                            "content": "Your task description here",
                            "timestamp": 1700000000.0,
                            "metadata": {}
                        },
                        {
                            "event_type": "tool_call",
                            "agent_id": "coder",
                            "content": "write_file(path='main.py', ...)",
                            "timestamp": 1700000005.0,
                            "metadata": {"tool": "write_file"}
                        },
                        {
                            "event_type": "tool_result",
                            "agent_id": "coder",
                            "content": "Successfully created main.py",
                            "timestamp": 1700000006.0,
                            "metadata": {}
                        },
                        {
                            "event_type": "task_complete",
                            "agent_id": "orchestrator",
                            "content": "Task finished.",
                            "timestamp": 1700000030.0,
                            "metadata": {}
                        }
                    ],
                    indent=2
                ),
                language="json",
            )
            st.caption(
                "Supported event_type values: `task_start`, `agent_thinking`, "
                "`tool_call`, `tool_result`, `agent_message`, `error`, `task_complete`"
            )
        st.stop()

    # Load the log
    raw_json = None
    if use_sample:
        with open(SAMPLE_LOG_PATH) as f:
            raw_json = json.load(f)
        st.info("Loaded built-in sample run.")
    elif uploaded:
        raw_json = json.loads(uploaded.read())
    else:
        st.warning("Upload a log file or click 'Use sample run' first.")
        st.stop()

    log = EventLog.from_json(raw_json)

    if not log.events:
        st.error("Event log is empty.")
        st.stop()

    char_engine, translator = _make_engines(selected_theme, mode)
    theme_info = translator.get_theme_info()

    # Run header
    st.divider()
    st.subheader("📊 Run Summary")
    total = len(log.events)
    tool_calls = sum(1 for e in log.events if e.event_type.value == "tool_call")
    agents = list(dict.fromkeys(e.agent_id for e in log.events))  # ordered unique

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Events", total)
    m2.metric("Tool Calls", tool_calls)
    m3.metric("Agents", len(agents))
    m4.metric("Team", theme_info["team_name"])

    if log.task:
        st.caption(f"Task: {log.task}")

    # Show agent → character mapping in use
    with st.expander("Agent roster"):
        for agent_id in agents:
            char_id = char_mapping.get_character(agent_id)
            char = char_engine.get_character(char_id)
            emoji = CHARACTER_EMOJI.get(char_id, "🎭")
            st.markdown(f"- **{agent_id}** → {emoji} {char.name} ({char.role})")

    # Work session
    st.divider()
    st.subheader("💬 The Gang Narrates")

    items = render_event_log(log, char_mapping, char_engine, translator)
    for item in items:
        _render_narration_item(item, char_engine, mode)

    # Victory
    st.divider()
    victory = translator._get_theme_configs()[selected_theme].victory_phrase
    st.success(f"## ✅ Run Complete — {victory}")

    st.subheader("📦 Deliverables")
    deliverables = extract_deliverables(log, translator)
    if deliverables:
        for d in deliverables:
            st.markdown(f"✓ {d}")
    else:
        st.caption("No tool results or completion events found in this log.")

    st.divider()
    s1, s2, s3 = st.columns(3)
    s1.metric("Theme", selected_theme.value.replace("_", " ").title())
    s2.metric("Mode", mode)
    s3.metric("Narration Steps", len(items))
