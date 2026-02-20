#!/usr/bin/env python3
"""
event_renderer.py — Convert an EventLog into gang narration

Takes raw agent events and produces NarrationItems: character dialogue +
translated technical updates ready for display (CLI or Streamlit).
"""

from dataclasses import dataclass
from typing import List, Optional

from event_schema import AgentEvent, EventLog, EventType, CharacterMapping


# ── Output model ──────────────────────────────────────────────────────────────

@dataclass
class NarrationItem:
    """One rendered moment in the gang's narration of an agent run."""

    character_id: str           # fred | velma | daphne | shaggy | scooby
    dialogue: Optional[str]     # In-character speech (None for silent updates)
    update: Optional[str]       # Translated technical update (tool call / result)
    update_style: str           # "info" | "success" | "warning" | "error"
    raw_content: str            # Original agent content (for "both" mode)
    event_type: EventType


# ── Context tables ────────────────────────────────────────────────────────────

_DIALOGUE_CONTEXTS = {
    EventType.TASK_START: "greeting",
    EventType.AGENT_THINKING: "planning",
    EventType.AGENT_MESSAGE: "discovery",
    EventType.TASK_COMPLETE: "success",
    EventType.ERROR: "problem",
}

_UPDATE_STYLES = {
    EventType.TOOL_CALL: "info",
    EventType.TOOL_RESULT: "success",
    EventType.ERROR: "error",
    EventType.TASK_COMPLETE: "success",
}


# ── Renderer ──────────────────────────────────────────────────────────────────

def render_event_log(
    log: EventLog,
    char_mapping: CharacterMapping,
    char_engine,
    translator,
) -> List[NarrationItem]:
    """Convert an EventLog into an ordered list of NarrationItems.

    Tool call + tool result pairs are merged into a single item so the UI
    shows one character speaking rather than two bare technical updates.

    Args:
        log:          The parsed agent event log.
        char_mapping: Maps agent IDs to gang characters.
        char_engine:  CharacterEngine instance for dialogue generation.
        translator:   TechnobabbleTranslator instance for text translation.

    Returns:
        List of NarrationItems in chronological order.
    """
    items: List[NarrationItem] = []
    events = log.events
    i = 0

    while i < len(events):
        event = events[i]
        char_id = char_mapping.get_character(event.agent_id)

        # ── Narrative events (character speaks) ───────────────────────────
        if event.event_type in (
            EventType.TASK_START,
            EventType.AGENT_THINKING,
            EventType.AGENT_MESSAGE,
        ):
            context = _DIALOGUE_CONTEXTS.get(event.event_type, "default")
            dialogue = char_engine.generate_dialogue(char_id, context, event.content)
            items.append(NarrationItem(
                character_id=char_id,
                dialogue=dialogue,
                update=None,
                update_style="info",
                raw_content=event.content,
                event_type=event.event_type,
            ))

        # ── Tool call — peek ahead for result and merge ───────────────────
        elif event.event_type == EventType.TOOL_CALL:
            translated_call = translator.translate(event.content)
            merged_result: Optional[str] = None
            result_style = "info"

            if i + 1 < len(events) and events[i + 1].event_type == EventType.TOOL_RESULT:
                i += 1
                result_event = events[i]
                merged_result = translator.translate(result_event.content)
                result_style = "success"

            dialogue = char_engine.generate_dialogue(char_id, "planning", event.content)
            items.append(NarrationItem(
                character_id=char_id,
                dialogue=dialogue,
                update=merged_result if merged_result else translated_call,
                update_style=result_style,
                raw_content=event.content,
                event_type=event.event_type,
            ))

        # ── Standalone tool result (no preceding call) ────────────────────
        elif event.event_type == EventType.TOOL_RESULT:
            items.append(NarrationItem(
                character_id=char_id,
                dialogue=None,
                update=translator.translate(event.content),
                update_style="success",
                raw_content=event.content,
                event_type=event.event_type,
            ))

        # ── Error ─────────────────────────────────────────────────────────
        elif event.event_type == EventType.ERROR:
            dialogue = char_engine.generate_dialogue(char_id, "problem", event.content)
            items.append(NarrationItem(
                character_id=char_id,
                dialogue=dialogue,
                update=translator.translate(event.content),
                update_style="error",
                raw_content=event.content,
                event_type=event.event_type,
            ))

        # ── Task complete ─────────────────────────────────────────────────
        elif event.event_type == EventType.TASK_COMPLETE:
            dialogue = char_engine.generate_dialogue(char_id, "success", event.content)
            items.append(NarrationItem(
                character_id=char_id,
                dialogue=dialogue,
                update=translator.translate(event.content),
                update_style="success",
                raw_content=event.content,
                event_type=event.event_type,
            ))

        i += 1

    return items


def extract_deliverables(log: EventLog, translator) -> List[str]:
    """Pull tool_result and task_complete content as deliverables.

    Returns translated strings ready for display.
    """
    deliverables = []
    for event in log.events:
        if event.event_type in (EventType.TOOL_RESULT, EventType.TASK_COMPLETE):
            deliverables.append(translator.translate(event.content))
    return deliverables
