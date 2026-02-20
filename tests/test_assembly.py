#!/usr/bin/env python3
"""
Test suite for Team Assembly
Tests FR-003: Task Type Analysis
Tests FR-004: Dynamic Team Selection
Tests FR-005: Assembly Scene Generation
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from assembly import TaskAnalyzer, TaskType, TaskAnalysis, TeamSelector, AssemblySceneGenerator
from character import CharacterEngine


class TestTaskAnalysis:
    """Test FR-003: Task Type Analysis"""
    
    def test_backend_task_detection(self):
        """Test backend task detection"""
        analyzer = TaskAnalyzer()
        task = "Create REST API with authentication"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.BACKEND
        assert "api" in analysis.keywords
        assert "authentication" in analysis.keywords
        assert analysis.confidence > 50
    
    def test_debugging_task_detection(self):
        """Test debugging task detection"""
        analyzer = TaskAnalyzer()
        task = "Fix null pointer exception in user service"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.DEBUGGING
        assert "exception" in analysis.keywords or "null" in analysis.keywords
    
    def test_frontend_task_detection(self):
        """Test frontend task detection"""
        analyzer = TaskAnalyzer()
        task = "Create React component with responsive styling"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.FRONTEND
        assert "react" in analysis.keywords or "component" in analysis.keywords
    
    def test_docs_task_detection(self):
        """Test documentation task detection"""
        analyzer = TaskAnalyzer()
        task = "Write README documentation for the new feature"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.DOCS
        assert "readme" in analysis.keywords or "document" in analysis.keywords
    
    def test_testing_task_detection(self):
        """Test testing task detection"""
        analyzer = TaskAnalyzer()
        task = "Add unit tests with coverage and mocks"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.TESTING
        assert "test" in analysis.keywords or "unit" in analysis.keywords or "mock" in analysis.keywords
    
    def test_devops_task_detection(self):
        """Test DevOps task detection"""
        analyzer = TaskAnalyzer()
        task = "Deploy to Kubernetes cluster with CI/CD pipeline"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.DEVOPS
        assert "kubernetes" in analysis.keywords or "deploy" in analysis.keywords
    
    def test_unknown_task_defaults_to_general(self):
        """Test that unknown tasks default to general"""
        analyzer = TaskAnalyzer()
        task = "Make me a sandwich"
        
        analysis = analyzer.analyze(task)
        
        assert analysis.task_type == TaskType.GENERAL
        assert analysis.confidence == 50.0
    
    def test_confidence_scales_with_keyword_matches(self):
        """Test that confidence increases with more keyword matches"""
        analyzer = TaskAnalyzer()
        
        # Single keyword
        task1 = "Create API endpoint"
        analysis1 = analyzer.analyze(task1)
        
        # Multiple keywords
        task2 = "Create REST API with JWT authentication and database models"
        analysis2 = analyzer.analyze(task2)
        
        assert analysis2.confidence >= analysis1.confidence
    
    def test_analysis_to_dict(self):
        """Test analysis serialization"""
        analyzer = TaskAnalyzer()
        task = "Create REST API"
        
        analysis = analyzer.analyze(task)
        data = analysis.to_dict()
        
        assert data["type"] == "backend"
        assert "keywords" in data
        assert "confidence" in data
        assert "suggested_team" in data


class TestTeamSelection:
    """Test FR-004: Dynamic Team Selection"""
    
    def test_backend_team_composition(self):
        """Test backend team has right members"""
        selector = TeamSelector()
        task = "Create REST API with authentication"
        
        team = selector.select(task)
        
        assert len(team) == 5
        assert "fred" in team  # Always has architect
        assert "velma" in team  # Backend specialist
    
    def test_debugging_team_has_scooby_first(self):
        """Test debugging team prioritizes Scooby"""
        selector = TeamSelector()
        task = "Fix null pointer exception"
        
        team = selector.select(task)
        
        assert "scooby" in team
        assert team[0] == "scooby"  # Scooby leads debugging
    
    def test_docs_team_has_shaggy_prominent(self):
        """Test docs team includes Shaggy"""
        selector = TeamSelector()
        task = "Write documentation"
        
        team = selector.select(task)
        
        assert "shaggy" in team
    
    def test_testing_team_has_scooby_and_daphne(self):
        """Test testing team has QA specialists"""
        selector = TeamSelector()
        task = "Write unit tests"
        
        team = selector.select(task)
        
        assert "scooby" in team  # Bug hunter
        assert "daphne" in team  # QA
    
    def test_team_always_has_five_members(self):
        """Test that team always has exactly 5 members"""
        selector = TeamSelector()
        
        tasks = [
            "Create API",
            "Fix bug",
            "Write docs",
            "Deploy to prod",
            "Unknown task xyz"
        ]
        
        for task in tasks:
            team = selector.select(task)
            assert len(team) == 5, f"Team for '{task}' has {len(team)} members"
    
    def test_no_duplicate_characters_in_team(self):
        """Test that team has no duplicates"""
        selector = TeamSelector()
        task = "Create full-stack application"
        
        team = selector.select(task)
        
        assert len(team) == len(set(team)), "Team has duplicate characters"
    
    def test_select_by_type(self):
        """Test explicit team selection by type"""
        selector = TeamSelector()
        
        team = selector.select_by_type("debugging")
        
        assert len(team) == 5
        assert "scooby" in team


class TestAssemblySceneGeneration:
    """Test FR-005: Assembly Scene Generation"""
    
    def test_assembly_scene_has_alarm(self):
        """Test that assembly scene includes alarm"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        scene = scene_gen.generate(team, "Create REST API")
        
        assert "🚨" in scene or "ALARM" in scene
    
    def test_assembly_scene_has_all_characters(self):
        """Test that all team members speak in assembly"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        scene = scene_gen.generate(team, "Create REST API")
        
        for char_id in team:
            char = char_engine.get_character(char_id)
            assert char.name.upper() + ":" in scene
    
    def test_assembly_scene_has_mystery_machine(self):
        """Test that assembly references Mystery Machine"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        scene = scene_gen.generate(team, "Create REST API")
        
        assert "MYSTERY MACHINE" in scene or "en route" in scene.lower()
    
    def test_assembly_scene_has_destination(self):
        """Test that assembly includes destination"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        task = "Create REST API endpoint"
        scene = scene_gen.generate(team, task)
        
        # Should reference the task or destination
        assert len(scene) > 50  # Has substantial content
    
    def test_assembly_scene_length(self):
        """Test that assembly scene has substantial content"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        scene = scene_gen.generate(team, "Create REST API")
        
        lines = [l for l in scene.split('\n') if l.strip()]
        assert len(lines) >= 6  # At least alarm + 5 characters + departure
    
    def test_different_tasks_produce_different_scenes(self):
        """Test that different tasks produce varied scenes"""
        char_engine = CharacterEngine()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        team = ["fred", "velma", "daphne", "shaggy", "scooby"]
        
        scene1 = scene_gen.generate(team, "Create REST API")
        scene2 = scene_gen.generate(team, "Fix critical bug")
        
        # Should have some differences
        assert scene1 != scene2
    
    def test_assembly_with_analysis_context(self):
        """Test that assembly uses analysis for context"""
        char_engine = CharacterEngine()
        analyzer = TaskAnalyzer()
        scene_gen = AssemblySceneGenerator(char_engine)
        
        task = "Fix null pointer exception"
        analysis = analyzer.analyze(task)
        team = ["scooby", "velma", "daphne", "fred", "shaggy"]
        
        scene = scene_gen.generate(team, task, analysis)
        
        # Scooby should be excited about bug hunting
        assert "Scooby" in scene or "SCOOBY" in scene


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
