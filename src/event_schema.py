#!/usr/bin/env python3
"""
event_schema.py — Framework-agnostic agent event model

Any agent system can emit events in this format (JSON lines or a JSON array)
and the Mystery Gang Orchestrator will narrate them.

Minimal event dict:
    {"event_type": "agent_message", "agent_id": "planner", "content": "..."}

Full event dict:
    {
        "event_type": "tool_call",
        "agent_id":   "coder",
        "content":    "write_file(path='auth.py', ...)",
        "timestamp":  1700000005.0,
        "metadata":   {"tool": "write_file", "path": "auth.py"}
    }

Supported event_type values:
    task_start      — the orchestrator received a new task
    agent_thinking  — an agent is reasoning (may not produce visible output)
    tool_call       — an agent invoked a tool
    tool_result     — the result of a tool call
    agent_message   — an agent produced a message for the team
    error           — something went wrong
    task_complete   — the run finished
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EventType(Enum):
    TASK_START = "task_start"
    AGENT_THINKING = "agent_thinking"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    AGENT_MESSAGE = "agent_message"
    ERROR = "error"
    TASK_COMPLETE = "task_complete"


@dataclass
class AgentEvent:
    """One event emitted by an agent framework."""

    event_type: EventType
    agent_id: str
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentEvent":
        return cls(
            event_type=EventType(data["event_type"]),
            agent_id=data.get("agent_id", "unknown"),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "agent_id": self.agent_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class EventLog:
    """A complete agent run as an ordered list of events."""

    events: List[AgentEvent]
    task: str = ""

    @classmethod
    def from_json(cls, data: List[Dict]) -> "EventLog":
        events = [AgentEvent.from_dict(e) for e in data]
        task = ""
        for e in events:
            if e.event_type == EventType.TASK_START:
                task = e.content
                break
        return cls(events=events, task=task)

    @classmethod
    def from_jsonl(cls, text: str) -> "EventLog":
        """Parse newline-delimited JSON (one event per line)."""
        import json
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        return cls.from_json(rows)


# ── Character mapping ─────────────────────────────────────────────────────────

# Default role-name → gang-character mapping.
# Covers the most common agent role names across frameworks.
_DEFAULT_MAPPINGS: Dict[str, str] = {
    # Planners / orchestrators → Fred (leader, architect)
    "orchestrator": "fred",
    "planner": "fred",
    "architect": "fred",
    "coordinator": "fred",
    "manager": "fred",
    # Researchers / analysts → Velma (brains, specialist)
    "researcher": "velma",
    "analyst": "velma",
    "coder": "velma",
    "developer": "velma",
    "engineer": "velma",
    # Reviewers / security → Daphne (QA, safety)
    "reviewer": "daphne",
    "qa": "daphne",
    "security": "daphne",
    "validator": "daphne",
    "auditor": "daphne",
    # Writers / docs → Shaggy (DevRel, pragmatist)
    "documenter": "shaggy",
    "writer": "shaggy",
    "reporter": "shaggy",
    "summarizer": "shaggy",
    # Testers / debuggers → Scooby (bug hunter)
    "tester": "scooby",
    "debugger": "scooby",
    "explorer": "scooby",
    "scanner": "scooby",
}


@dataclass
class CharacterMapping:
    """Maps agent_id strings to Mystery Gang character IDs."""

    mappings: Dict[str, str]
    default_character: str = "fred"

    def get_character(self, agent_id: str) -> str:
        """Return a character ID for the given agent.

        Resolution order:
        1. Exact match on agent_id
        2. Any mapping key that is a substring of agent_id (role-name detection)
        3. default_character
        """
        if agent_id in self.mappings:
            return self.mappings[agent_id]
        agent_lower = agent_id.lower()
        for key, char in self.mappings.items():
            if key in agent_lower:
                return char
        return self.default_character

    @classmethod
    def default(cls) -> "CharacterMapping":
        return cls(mappings=dict(_DEFAULT_MAPPINGS))

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "CharacterMapping":
        return cls(mappings=data)
