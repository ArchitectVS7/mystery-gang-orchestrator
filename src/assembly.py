#!/usr/bin/env python3
"""
Team Assembly for Mystery Gang Orchestrator
Analyzes tasks, selects optimal team, generates assembly scenes
"""

import random
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Supported task types"""
    BACKEND = "backend"
    FRONTEND = "frontend"
    DEBUGGING = "debugging"
    DOCS = "docs"
    TESTING = "testing"
    DEVOPS = "devops"
    GENERAL = "general"


@dataclass
class TaskAnalysis:
    """Result of task analysis"""
    task_type: TaskType
    keywords: List[str]
    confidence: float
    suggested_team: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "type": self.task_type.value,
            "keywords": self.keywords,
            "confidence": self.confidence,
            "suggested_team": self.suggested_team
        }


class TaskAnalyzer:
    """Analyzes incoming tasks to determine type and required skills"""
    
    # Keyword mappings for task types
    KEYWORD_MAP = {
        TaskType.BACKEND: [
            "api", "endpoint", "database", "backend", "server", "rest", "graphql",
            "authentication", "auth", "jwt", "token", "model", "schema", "migration"
        ],
        TaskType.FRONTEND: [
            "ui", "frontend", "component", "react", "vue", "angular", "css",
            "styling", "layout", "responsive", "widget", "interface", "user interface"
        ],
        TaskType.DEBUGGING: [
            "bug", "fix", "error", "exception", "crash", "broken", "issue",
            "debug", "trace", "stack", "null", "undefined", "not working"
        ],
        TaskType.DOCS: [
            "document", "readme", "comment", "explain", "guide", "tutorial",
            "api docs", "specification", "changelog"
        ],
        TaskType.TESTING: [
            "test", "spec", "coverage", "unit test", "integration", "e2e",
            "assert", "mock", "stub", "fixture"
        ],
        TaskType.DEVOPS: [
            "deploy", "docker", "kubernetes", "k8s", "ci/cd", "pipeline",
            "infrastructure", "serverless", "cloud", "aws", "azure", "gcp"
        ]
    }
    
    def analyze(self, task: str) -> TaskAnalysis:
        """Analyze task and return type, keywords, and confidence"""
        task_lower = task.lower()
        
        # Find matching keywords
        matches = {}
        for task_type, keywords in self.KEYWORD_MAP.items():
            count = sum(1 for kw in keywords if kw in task_lower)
            if count > 0:
                matches[task_type] = count
        
        if not matches:
            # Default to general
            return TaskAnalysis(
                task_type=TaskType.GENERAL,
                keywords=[],
                confidence=50.0,
                suggested_team=self._get_default_team()
            )
        
        # Find best match
        best_type = max(matches, key=matches.get)
        confidence = min(100.0, matches[best_type] * 15.0)  # Scale: 1 keyword = 15%, max 100%
        
        # Extract matched keywords
        matched_keywords = [
            kw for kw in self.KEYWORD_MAP[best_type]
            if kw in task_lower
        ]
        
        # Get suggested team
        suggested_team = self._get_team_for_type(best_type)
        
        return TaskAnalysis(
            task_type=best_type,
            keywords=matched_keywords,
            confidence=confidence,
            suggested_team=suggested_team
        )
    
    def _get_default_team(self) -> List[str]:
        """Return default balanced team"""
        return ["fred", "velma", "daphne", "shaggy", "scooby"]
    
    def _get_team_for_type(self, task_type: TaskType) -> List[str]:
        """Get optimal team for task type"""
        team_configs = {
            TaskType.BACKEND: ["fred", "velma", "daphne", "shaggy", "scooby"],
            TaskType.FRONTEND: ["fred", "daphne", "velma", "shaggy", "scooby"],
            TaskType.DEBUGGING: ["scooby", "velma", "daphne", "fred", "shaggy"],
            TaskType.DOCS: ["shaggy", "velma", "fred", "daphne", "scooby"],
            TaskType.TESTING: ["scooby", "daphne", "velma", "shaggy", "fred"],
            TaskType.DEVOPS: ["fred", "velma", "daphne", "scooby", "shaggy"],
            TaskType.GENERAL: ["fred", "velma", "daphne", "shaggy", "scooby"]
        }
        
        return team_configs.get(task_type, self._get_default_team())


class TeamSelector:
    """Selects optimal team based on task analysis"""
    
    def __init__(self):
        self.analyzer = TaskAnalyzer()
    
    def select(self, task: str) -> List[str]:
        """Select team for task"""
        analysis = self.analyzer.analyze(task)
        return analysis.suggested_team
    
    def select_by_type(self, task_type: str) -> List[str]:
        """Select team by explicit task type"""
        try:
            ttype = TaskType(task_type)
        except ValueError:
            ttype = TaskType.GENERAL
        
        return TaskAnalyzer()._get_team_for_type(ttype)


class AssemblySceneGenerator:
    """Generates cartoon-style assembly scenes"""
    
    ASSEMBLY_TEMPLATES = [
        {
            "alarm": "🚨 [ALARM SOUNDS]",
            "intro": "{leader}: {leader_phrase}",
            "responses": [
                "{velma}: {velma_phrase}",
                "{daphne}: {daphne_phrase}",
                "{shaggy}: {shaggy_phrase}",
                "{scooby}: {scooby_phrase}"
            ],
            "departure": "🚐 THE MYSTERY MACHINE IS EN ROUTE TO {destination}!"
        }
    ]
    
    def __init__(self, character_engine):
        self.character_engine = character_engine
    
    def generate(self, team: List[str], task: str, analysis: TaskAnalysis = None) -> str:
        """Generate assembly scene for team and task"""
        template = random.choice(self.ASSEMBLY_TEMPLATES)
        
        # Get characters
        chars = {char_id: self.character_engine.get_character(char_id) for char_id in team}
        
        # Build scene
        lines = []
        
        # Alarm
        lines.append(template["alarm"])
        lines.append("")
        
        # Leader intro (Fred or first character)
        leader_id = team[0]
        leader_phrase = self.character_engine.generate_dialogue(leader_id, "greeting")
        lines.append(f"{chars[leader_id].name.upper()}: {leader_phrase}")
        lines.append("")
        
        # Team responses
        for char_id in team[1:]:
            context = self._get_context_for_char(char_id, analysis)
            phrase = self.character_engine.generate_dialogue(char_id, "greeting", context)
            lines.append(f"{chars[char_id].name.upper()}: {phrase}")
        
        lines.append("")
        
        # Departure
        destination = self._extract_destination(task)
        lines.append(template["departure"].format(destination=destination))
        
        return "\n".join(lines)
    
    def _get_context_for_char(self, char_id: str, analysis: TaskAnalysis) -> str:
        """Get appropriate context for character based on task"""
        if analysis is None:
            return "default"
        
        role_contexts = {
            "velma": "planning" if analysis.task_type in [TaskType.BACKEND, TaskType.FRONTEND] else "discovery",
            "daphne": "review" if analysis.task_type in [TaskType.BACKEND, TaskType.DEVOPS] else "default",
            "shaggy": "simplicity" if analysis.task_type in [TaskType.DEBUGGING, TaskType.DEVOPS] else "default",
            "scooby": "discovery" if analysis.task_type == TaskType.DEBUGGING else "default",
            "fred": "planning"
        }
        
        return role_contexts.get(char_id, "default")
    
    def _extract_destination(self, task: str) -> str:
        """Extract destination from task (file path or feature name)"""
        # Look for file paths
        if "/" in task and "." in task:
            parts = task.split()
            for part in parts:
                if "/" in part and len(part) > 5:
                    return part
        
        # Look for feature names (quoted or capitalized)
        if '"' in task:
            start = task.find('"')
            end = task.find('"', start + 1)
            if end > start:
                return task[start+1:end]
        
        # Default to task summary
        words = task.split()[:5]
        return " ".join(words) + "..."


# Convenience function
def assemble_team(task: str) -> Tuple[List[str], str]:
    """Quick function to assemble team and generate scene"""
    from character import CharacterEngine
    
    char_engine = CharacterEngine()
    selector = TeamSelector()
    scene_gen = AssemblySceneGenerator(char_engine)
    
    team = selector.select(task)
    analysis = TaskAnalyzer().analyze(task)
    scene = scene_gen.generate(team, task, analysis)
    
    return team, scene


if __name__ == "__main__":
    # Test assembly
    from character import CharacterEngine
    
    char_engine = CharacterEngine()
    analyzer = TaskAnalyzer()
    selector = TeamSelector()
    scene_gen = AssemblySceneGenerator(char_engine)
    
    test_tasks = [
        "Create REST API with authentication",
        "Fix null pointer exception in user service",
        "Deploy to Kubernetes cluster",
        "Write documentation for the new feature"
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"TASK: {task}")
        print(f"{'='*60}")
        
        analysis = analyzer.analyze(task)
        print(f"Type: {analysis.task_type.value}")
        print(f"Keywords: {', '.join(analysis.keywords)}")
        print(f"Confidence: {analysis.confidence:.0f}%")
        print(f"Team: {', '.join(analysis.suggested_team)}")
        print()
        
        team = selector.select(task)
        scene = scene_gen.generate(team, task, analysis)
        print(scene)
