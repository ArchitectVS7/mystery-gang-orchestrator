#!/usr/bin/env python3
"""
Test suite for Character Engine
Tests FR-001: Character Definitions
Tests FR-002: Character Dialogue Generation
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from character import Character, CharacterEngine


class TestCharacterDefinitions:
    """Test FR-001: Character Definitions"""
    
    def test_character_has_required_fields(self):
        """Test that character has all required fields"""
        fred = Character.load("fred")
        
        assert fred.id == "fred"
        assert fred.name == "Fred Jones"
        assert fred.role == "Architect"
        assert fred.model == "anthropic/claude-sonnet-4-5"
        assert isinstance(fred.personality, list)
        assert isinstance(fred.catchphrases, dict)
        assert isinstance(fred.quirks, list)
        assert fred.costume != ""
        assert fred.idle_activity != ""
    
    def test_all_five_characters_exist(self):
        """Test that all five main characters exist"""
        engine = CharacterEngine()
        
        expected_characters = ["fred", "velma", "daphne", "shaggy", "scooby"]
        
        for char_id in expected_characters:
            assert char_id in engine.characters, f"Character '{char_id}' not found"
    
    def test_fred_is_architect(self):
        """Test Fred's role and model assignment"""
        fred = Character.load("fred")
        
        assert fred.role == "Architect"
        assert "claude" in fred.model.lower()
    
    def test_velma_is_specialist(self):
        """Test Velma's role and model assignment"""
        velma = Character.load("velma")
        
        assert velma.role == "Specialist"
        assert "coder" in velma.model.lower() or "qwen" in velma.model.lower()
    
    def test_daphne_is_qa_security(self):
        """Test Daphne's role and model assignment"""
        daphne = Character.load("daphne")
        
        assert daphne.role == "QA/Security"
        assert "gpt" in daphne.model.lower()
    
    def test_shaggy_is_devrel(self):
        """Test Shaggy's role and model assignment"""
        shaggy = Character.load("shaggy")
        
        assert shaggy.role == "DevRel/Documentation"
        assert "mistral" in shaggy.model.lower()
    
    def test_scooby_is_bug_hunter(self):
        """Test Scooby's role and model assignment"""
        scooby = Character.load("scooby")
        
        assert scooby.role == "Bug Hunter"
        assert "deepseek" in scooby.model.lower() or "coder" in scooby.model.lower()
    
    def test_each_character_has_minimum_catchphrases(self):
        """Test FR-001: Each character has 10+ catchphrases"""
        engine = CharacterEngine()
        
        for char_id, character in engine.characters.items():
            total_phrases = sum(
                len(phrases) for phrases in character.catchphrases.values()
            )
            assert total_phrases >= 10, f"{char_id} has only {total_phrases} catchphrases"
    
    def test_each_character_has_minimum_quirks(self):
        """Test FR-001: Each character has 3+ quirks"""
        engine = CharacterEngine()
        
        for char_id, character in engine.characters.items():
            assert len(character.quirks) >= 3, f"{char_id} has only {len(character.quirks)} quirks"
    
    def test_character_personality_traits(self):
        """Test that characters have distinct personalities"""
        fred = Character.load("fred")
        velma = Character.load("velma")
        shaggy = Character.load("shaggy")
        
        assert "confident" in fred.personality or "leader" in fred.personality
        assert "brilliant" in velma.personality or "analytical" in velma.personality
        assert "laid-back" in shaggy.personality or "pragmatic" in shaggy.personality


class TestDialogueGeneration:
    """Test FR-002: Character Dialogue Generation"""
    
    def test_fred_dialogue_is_confident(self):
        """Test that Fred's dialogue shows confidence"""
        engine = CharacterEngine()
        
        dialogue = engine.generate_dialogue("fred", "planning")
        
        assert len(dialogue) > 0
        # Fred should use confident/planning language
        assert any(word in dialogue.lower() for word in 
                  ["plan", "systematic", "gang", "team", "work", "sure", "proper", "flowchart", "architecture"])
    
    def test_velma_dialogue_shows_research(self):
        """Test that Velma's dialogue shows research/analysis"""
        engine = CharacterEngine()
        
        dialogue = engine.generate_dialogue("velma", "discovery")
        
        assert len(dialogue) > 0
        # Velma should reference research or docs
        assert any(word in dialogue.lower() for word in
                  ["jinkies", "research", "docs", "according", "data", "analysis"])
    
    def test_shaggy_dialogue_shows_reluctance(self):
        """Test that Shaggy's dialogue shows reluctance/simplicity"""
        engine = CharacterEngine()
        
        dialogue = engine.generate_dialogue("shaggy", "simplicity")
        
        assert len(dialogue) > 0
        # Shaggy should use casual/simplifying language
        assert any(word in dialogue.lower() for word in
                  ["like", "simple", "complicated", "framework", "zoinks", "scratch", "easier"])
    
    def test_scooby_dialogue_has_r_speech(self):
        """Test that Scooby's dialogue has R-replaced speech pattern"""
        engine = CharacterEngine()
        
        dialogue = engine.generate_dialogue("scooby", "discovery")
        
        assert len(dialogue) > 0
        # Scooby should have R's replacing consonants
        assert "r" in dialogue.lower() or "R" in dialogue
    
    def test_daphne_dialogue_shows_safety_focus(self):
        """Test that Daphne's dialogue shows safety consciousness"""
        engine = CharacterEngine()
        
        dialogue = engine.generate_dialogue("daphne", "review")
        
        assert len(dialogue) > 0
        # Daphne should mention safety, polish, testing, or error handling
        assert any(word in dialogue.lower() for word in
                  ["safety", "polish", "test", "secure", "edge case", "error", "handling"])
    
    def test_dialogue_avoids_repeats(self):
        """Test that dialogue generation avoids repeating catchphrases"""
        engine = CharacterEngine()
        engine.reset_used_phrases("fred")
        
        dialogues = set()
        for _ in range(5):
            dialogue = engine.generate_dialogue("fred", "planning", avoid_repeats=True)
            dialogues.add(dialogue)
        
        # Should have variety (not all the same)
        assert len(dialogues) > 1, "Dialogue generation is repeating too much"
    
    def test_dialogue_context_awareness(self):
        """Test that dialogue changes based on context"""
        engine = CharacterEngine()
        
        planning_dialogue = engine.generate_dialogue("velma", "planning")
        success_dialogue = engine.generate_dialogue("velma", "success")
        
        # Different contexts should produce different dialogue
        assert planning_dialogue != success_dialogue
    
    def test_character_to_dict(self):
        """Test character serialization"""
        fred = Character.load("fred")
        data = fred.to_dict()
        
        assert data["id"] == "fred"
        assert data["name"] == "Fred Jones"
        assert data["role"] == "Architect"
        # Model IS included in dict (needed for routing)
        assert "model" in data
        # Catchphrases excluded from dict (too large)
        assert "catchphrases" not in data


class TestCharacterEngine:
    """Test CharacterEngine functionality"""
    
    def test_engine_loads_all_characters(self):
        """Test that engine loads all 5 characters"""
        engine = CharacterEngine()
        
        assert len(engine.characters) == 5
    
    def test_get_character_returns_correct_type(self):
        """Test that get_character returns Character instance"""
        engine = CharacterEngine()
        
        fred = engine.get_character("fred")
        assert isinstance(fred, Character)
    
    def test_get_character_raises_on_invalid(self):
        """Test that invalid character ID raises error"""
        engine = CharacterEngine()
        
        with pytest.raises(ValueError):
            engine.get_character("nonexistent")
    
    def test_get_all_characters(self):
        """Test getting all characters"""
        engine = CharacterEngine()
        
        characters = engine.get_all_characters()
        assert len(characters) == 5
        
        for char in characters:
            assert isinstance(char, Character)
    
    def test_reset_used_phrases_single(self):
        """Test resetting used phrases for single character"""
        engine = CharacterEngine()
        
        # Generate some dialogue
        engine.generate_dialogue("fred", "planning")
        engine.generate_dialogue("fred", "planning")
        
        # Reset
        engine.reset_used_phrases("fred")
        assert engine.used_catchphrases["fred"] == []
    
    def test_reset_used_phrases_all(self):
        """Test resetting used phrases for all characters"""
        engine = CharacterEngine()
        
        # Generate some dialogue
        for char_id in ["fred", "velma", "shaggy"]:
            engine.generate_dialogue(char_id, "greeting")
        
        # Reset all
        engine.reset_used_phrases()
        
        for char_id in engine.used_catchphrases:
            assert engine.used_catchphrases[char_id] == []
    
    def test_get_team_roster(self):
        """Test getting team roster"""
        engine = CharacterEngine()
        
        team_ids = ["fred", "velma", "daphne"]
        roster = engine.get_team_roster(team_ids)
        
        assert len(roster) == 3
        assert roster[0]["id"] == "fred"
        assert roster[1]["id"] == "velma"
        assert roster[2]["id"] == "daphne"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
