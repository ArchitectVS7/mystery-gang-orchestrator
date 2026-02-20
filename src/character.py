#!/usr/bin/env python3
"""
Character Engine for Mystery Gang Orchestrator
Manages character definitions, dialogue generation, and personality injection
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Character:
    """Represents a mystery gang character"""
    id: str
    name: str
    role: str
    model: str
    personality: List[str]
    catchphrases: Dict[str, List[str]]
    quirks: List[str]
    costume: str
    idle_activity: str
    
    @classmethod
    def load(cls, character_id: str, data_dir: Path = None) -> 'Character':
        """Load character from JSON file"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        
        with open(data_dir / "characters.json") as f:
            data = json.load(f)
        
        if character_id not in data:
            raise ValueError(f"Character '{character_id}' not found")
        
        char_data = data[character_id]
        return cls(
            id=char_data["id"],
            name=char_data["name"],
            role=char_data["role"],
            model=char_data["model"],
            personality=char_data["personality"],
            catchphrases=char_data["catchphrases"],
            quirks=char_data["quirks"],
            costume=char_data["costume"],
            idle_activity=char_data["idle_activity"]
        )
    
    def get_catchphrase(self, context: str = "default") -> str:
        """Get a catchphrase appropriate for the context"""
        if context in self.catchphrases:
            phrases = self.catchphrases[context]
        else:
            phrases = self.catchphrases.get("default", ["..."])
        
        return random.choice(phrases)
    
    def generate_dialogue(self, context: str, task_context: str = "") -> str:
        """Generate character-specific dialogue"""
        base_phrase = self.get_catchphrase(context)
        
        # Add personality-based commentary
        commentary = self._generate_commentary(context, task_context)
        
        if commentary:
            return f"{base_phrase} {commentary}"
        return base_phrase
    
    def _generate_commentary(self, context: str, task_context: str) -> str:
        """Generate context-aware commentary based on personality"""
        commentaries = {
            "planning": [
                f"Let me think about this systematically...",
                f"I'll need to consider all the angles...",
                f"This requires careful planning..."
            ],
            "discovery": [
                f"Fascinating! I found something interesting...",
                f"The data reveals...",
                f"According to my research..."
            ],
            "problem": [
                f"This is concerning...",
                f"We need to address this carefully...",
                f"I'm detecting an issue..."
            ],
            "success": [
                f"Excellent work!",
                f"That went perfectly!",
                f"Mission accomplished!"
            ]
        }
        
        if context in commentaries:
            return random.choice(commentaries[context])
        return ""
    
    def to_dict(self) -> Dict:
        """Convert character to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "model": self.model,
            "personality": self.personality,
            "quirks": self.quirks,
            "costume": self.costume,
            "idle_activity": self.idle_activity
        }


class CharacterEngine:
    """Manages all characters and dialogue generation"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / "data"
        self.characters: Dict[str, Character] = {}
        self.used_catchphrases: Dict[str, List[str]] = {}
        self._load_all_characters()
    
    def _load_all_characters(self):
        """Load all characters from data directory"""
        with open(self.data_dir / "characters.json") as f:
            data = json.load(f)
        
        for char_id in data.keys():
            self.characters[char_id] = Character.load(char_id, self.data_dir)
            self.used_catchphrases[char_id] = []
    
    def get_character(self, character_id: str) -> Character:
        """Get character by ID"""
        if character_id not in self.characters:
            raise ValueError(f"Character '{character_id}' not found")
        return self.characters[character_id]
    
    def get_all_characters(self) -> List[Character]:
        """Get all available characters"""
        return list(self.characters.values())
    
    def generate_dialogue(self, character_id: str, context: str, 
                         task_context: str = "", avoid_repeats: bool = True) -> str:
        """Generate dialogue for a character, optionally avoiding repeats"""
        character = self.get_character(character_id)
        
        # Get catchphrase, avoiding repeats if requested
        if avoid_repeats:
            phrase = self._get_unique_catchphrase(character, context)
        else:
            phrase = character.get_catchphrase(context)
        
        # Generate commentary
        commentary = character._generate_commentary(context, task_context)
        
        dialogue = f"{phrase}"
        if commentary:
            dialogue += f" {commentary}"
        
        return dialogue
    
    def _get_unique_catchphrase(self, character: Character, context: str) -> str:
        """Get a catchphrase that hasn't been used recently"""
        if context in character.catchphrases:
            available = [
                p for p in character.catchphrases[context]
                if p not in self.used_catchphrases[character.id]
            ]
            
            if not available:
                # Reset used phrases if all have been used
                self.used_catchphrases[character.id] = []
                available = character.catchphrases[context]
            
            phrase = random.choice(available)
            self.used_catchphrases[character.id].append(phrase)
            
            # Keep only last 10 used phrases
            if len(self.used_catchphrases[character.id]) > 10:
                self.used_catchphrases[character.id] = self.used_catchphrases[character.id][-10:]
            
            return phrase
        
        return character.get_catchphrase("default")
    
    def reset_used_phrases(self, character_id: str = None):
        """Reset used catchphrases for a character or all characters"""
        if character_id:
            self.used_catchphrases[character_id] = []
        else:
            for char_id in self.used_catchphrases:
                self.used_catchphrases[char_id] = []
    
    def get_team_roster(self, team_ids: List[str]) -> List[Dict]:
        """Get roster information for a team"""
        return [
            self.characters[char_id].to_dict()
            for char_id in team_ids
            if char_id in self.characters
        ]


# Convenience functions
def load_character(character_id: str) -> Character:
    """Load a character by ID"""
    return Character.load(character_id)

def get_all_characters() -> List[Character]:
    """Get all available characters"""
    engine = CharacterEngine()
    return engine.get_all_characters()


if __name__ == "__main__":
    # Test character loading
    engine = CharacterEngine()
    
    print("🎭 Mystery Gang Character Engine Test\n")
    
    for char_id in ["fred", "velma", "daphne", "shaggy", "scooby"]:
        char = engine.get_character(char_id)
        print(f"{char.name} ({char.role})")
        print(f"  Model: {char.model}")
        print(f"  Personality: {', '.join(char.personality)}")
        print(f"  Sample dialogue: {engine.generate_dialogue(char_id, 'greeting')}")
        print()
