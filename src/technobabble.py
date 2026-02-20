#!/usr/bin/env python3
"""
Technobabble Translator for Mystery Gang Orchestrator
Translates technical output into cartoon/game lingo with theme support
"""

import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """Available translation themes"""
    SCOOBY = "scooby"  # Mystery gang
    STAR_TREK = "star_trek"  # Starfleet technobabble
    GHOSTBUSTERS = "ghostbusters"  # Paranormal containment
    SUPERHERO = "superhero"  # Marvel/DC style
    PIRATES = "pirates"  # Pirate crew treasure hunting
    WIZARDS = "wizards"  # Magical academy


@dataclass
class ThemeConfig:
    """Configuration for a theme"""
    id: Theme
    name: str
    description: str
    team_name: str
    vehicle_name: str
    victory_phrase: str
    alarm_sound: str
    character_prefixes: Dict[str, str]  # character_id → title/role name


@dataclass
class TranslationEntry:
    """A single translation mapping"""
    technical: str
    translations: Dict[Theme, str]  # theme → translated text
    category: str  # deployment, debugging, api, etc.


class TechnobabbleDictionary:
    """Manages technical → cartoon translation mappings"""
    
    def __init__(self):
        self.entries: List[TranslationEntry] = []
        self._load_default_mappings()
    
    def _load_default_mappings(self):
        """Load default translation mappings"""
        
        # API/Endpoint mappings
        self.add_mapping(
            "Created API endpoint",
            {
                Theme.SCOOBY: "Calibrated the mystery detection chamber",
                Theme.STAR_TREK: "Established subspace communication array",
                Theme.GHOSTBUSTERS: "Activated proton containment grid",
                Theme.SUPERHERO: "Deployed hero communication uplink",
                Theme.PIRATES: "Hoisted the signal flags, arrr!",
                Theme.WIZARDS: "Conjured messaging crystal matrix"
            },
            "api"
        )
        
        self.add_mapping(
            "Fixed null pointer exception",
            {
                Theme.SCOOBY: "Neutralized the spectral null anomaly",
                Theme.STAR_TREK: "Reconfigured the reverse flux decoupling system",
                Theme.GHOSTBUSTERS: "Contained the negative energy entity",
                Theme.SUPERHERO: "Stabilized the quantum vulnerability field",
                Theme.PIRATES: "Plugged the leak in me hull, arrr!",
                Theme.WIZARDS: "Banished the void spirit from the code"
            },
            "debugging"
        )
        
        self.add_mapping(
            "Deployed to production",
            {
                Theme.SCOOBY: "Released the mystery machine into the wild!",
                Theme.STAR_TREK: "Engaged warp core and departed spacdock",
                Theme.GHOSTBUSTERS: "Activated full containment protocol",
                Theme.SUPERHERO: "Launched into the battlefield!",
                Theme.PIRATES: "Set sail for the open seas!",
                Theme.WIZARDS: "Unleashed the enchantment upon the realm"
            },
            "deployment"
        )
        
        self.add_mapping(
            "Database query executed",
            {
                Theme.SCOOBY: "Searched the ancient archives for clues",
                Theme.STAR_TREK: "Accessed main computer database",
                Theme.GHOSTBUSTERS: "Scanned the ectoplasmic records",
                Theme.SUPERHERO: "Queried the oracle network",
                Theme.PIRATES: "Ransacked the captain's log, arrr!",
                Theme.WIZARDS: "Consulted the library of forbidden knowledge"
            },
            "database"
        )
        
        self.add_mapping(
            "Authentication successful",
            {
                Theme.SCOOBY: "Identity verified - no monsters detected!",
                Theme.STAR_TREK: "Authorization codes accepted",
                Theme.GHOSTBUSTERS: "Ecto-signature confirmed human",
                Theme.SUPERHERO: "Hero credentials validated",
                Theme.PIRATES: "Yer on the crew list, matey!",
                Theme.WIZARDS: "Magical signature matches - welcome, initiate"
            },
            "authentication"
        )
        
        self.add_mapping(
            "Running tests",
            {
                Theme.SCOOBY: "Setting traps to catch the bugs!",
                Theme.STAR_TREK: "Running diagnostic simulations",
                Theme.GHOSTBUSTERS: "Calibrating ghost detection equipment",
                Theme.SUPERHERO: "Testing hero readiness protocols",
                Theme.PIRATES: "Swabbin' the deck and checkin' the cannons!",
                Theme.WIZARDS: "Casting detection cantrips for impurities"
            },
            "testing"
        )
        
        self.add_mapping(
            "All tests passing",
            {
                Theme.SCOOBY: "Scooby-Dooby-Doo! All traps sprung successfully!",
                Theme.STAR_TREK: "All systems nominal, ready for departure",
                Theme.GHOSTBUSTERS: "Containment field stable - no ghosts detected",
                Theme.SUPERHERO: "Hero readiness at 100%!",
                Theme.PIRATES: "Ship shape and Bristol fashion, arrr!",
                Theme.WIZARDS: "Enchantments holding strong - no curses detected"
            },
            "testing"
        )
        
        self.add_mapping(
            "Bug detected",
            {
                Theme.SCOOBY: "Ruh-roh! I rmell a rug!",
                Theme.STAR_TREK: "Anomaly detected in sector 7",
                Theme.GHOSTBUSTERS: "Ecto-readings spiking - we got one!",
                Theme.SUPERHERO: "Threat detected in the perimeter",
                Theme.PIRATES: "There be a stowaway aboard!",
                Theme.WIZARDS: "Dark magic taint detected in the weave"
            },
            "debugging"
        )
        
        self.add_mapping(
            "Code review complete",
            {
                Theme.SCOOBY: "Examined all the clues carefully",
                Theme.STAR_TREK: "Technical analysis complete",
                Theme.GHOSTBUSTERS: "Paranormal inspection finished",
                Theme.SUPERHERO: "Tactical assessment complete",
                Theme.PIRATES: "Inspected every inch of the ship",
                Theme.WIZARDS: "Scryed the runes for hidden flaws"
            },
            "review"
        )
        
        self.add_mapping(
            "Documentation updated",
            {
                Theme.SCOOBY: "Recorded all the mystery details in the log",
                Theme.STAR_TREK: "Ship's log updated",
                Theme.GHOSTBUSTERS: "Case file documentation complete",
                Theme.SUPERHERO: "Mission report filed",
                Theme.PIRATES: "Charted the course in me logbook",
                Theme.WIZARDS: "Inscribed the knowledge in the tome"
            },
            "docs"
        )
        
        self.add_mapping(
            "Performance optimized",
            {
                Theme.SCOOBY: "The mystery machine is running faster than ever!",
                Theme.STAR_TREK: "Warp core efficiency increased to 110%",
                Theme.GHOSTBUSTERS: "Proton pack output maximized",
                Theme.SUPERHERO: "Power levels exceeding maximum capacity!",
                Theme.PIRATES: "She's the fastest ship in the Caribbean!",
                Theme.WIZARDS: "Mana flow optimized - spells cast instantly"
            },
            "performance"
        )
        
        self.add_mapping(
            "Error handling added",
            {
                Theme.SCOOBY: "Added extra safety nets for when things go wrong",
                Theme.STAR_TREK: "Installed redundant safety protocols",
                Theme.GHOSTBUSTERS: "Reinforced containment field safeguards",
                Theme.SUPERHERO: "Activated defensive countermeasures",
                Theme.PIRATES: "Battened down the hatches for storms",
                Theme.WIZARDS: "Warded against magical backlash"
            },
            "safety"
        )
        
        self.add_mapping(
            "Feature implemented",
            {
                Theme.SCOOBY: "Another piece of the mystery solved!",
                Theme.STAR_TREK: "New system module installed and operational",
                Theme.GHOSTBUSTERS: "New ghost-catching gadget online",
                Theme.SUPERHERO: "New ability unlocked and ready",
                Theme.PIRATES: "Added a new cannon to me arsenal!",
                Theme.WIZARDS: "New spell added to the grimoire"
            },
            "feature"
        )
        
        self.add_mapping(
            "Refactoring complete",
            {
                Theme.SCOOBY: "Reorganized all the clues to make more sense",
                Theme.STAR_TREK: "System architecture optimized",
                Theme.GHOSTBUSTERS: "Restructured proton flow for efficiency",
                Theme.SUPERHERO: "Upgraded hero suit with better tech",
                Theme.PIRATES: "Rearranged the cargo hold for better balance",
                Theme.WIZARDS: "Restructured the magical matrix for stability"
            },
            "refactoring"
        )
        
        self.add_mapping(
            "Security vulnerability fixed",
            {
                Theme.SCOOBY: "Plugged the hole where the monster could sneak in!",
                Theme.STAR_TREK: "Patched security breach in deflector shields",
                Theme.GHOSTBUSTERS: "Sealed the ectoplasmic breach",
                Theme.SUPERHERO: "Reinforced the fortress defenses",
                Theme.PIRATES: "Repaired the weak spot in me hull",
                Theme.WIZARDS: "Reinforced the magical wards against intrusion"
            },
            "security"
        )
        
        self.add_mapping(
            "Build successful",
            {
                Theme.SCOOBY: "The mystery machine is ready to roll!",
                Theme.STAR_TREK: "All systems green for departure",
                Theme.GHOSTBUSTERS: "Equipment fully charged and operational",
                Theme.SUPERHERO: "Suit powered up and mission-ready",
                Theme.PIRATES: "Ship fully stocked and ready to sail!",
                Theme.WIZARDS: "Ritual complete - magic flows strong"
            },
            "build"
        )
    
    def add_mapping(self, technical: str, translations: Dict[Theme, str], category: str):
        """Add a new translation mapping"""
        entry = TranslationEntry(
            technical=technical,
            translations=translations,
            category=category
        )
        self.entries.append(entry)
    
    def translate(self, text: str, theme: Theme) -> str:
        """Translate technical text to theme-specific technobabble"""
        text_lower = text.lower()
        
        # Try exact match first
        for entry in self.entries:
            if entry.technical.lower() in text_lower:
                return entry.translations.get(theme, text)
        
        # Try keyword-based translation
        return self._translate_by_keywords(text, theme)
    
    def _translate_by_keywords(self, text: str, theme: Theme) -> str:
        """Fallback keyword-based translation"""
        text_lower = text.lower()
        
        # Generic templates by theme
        templates = {
            Theme.SCOOBY: [
                "Like, we just {action} the thingamajig!",
                "Jinkies! The {component} is all fixed up!",
                "Ranother mystery rolved!"
            ],
            Theme.STAR_TREK: [
                "Reconfigured the {component} array",
                "Recalibrated the {component} matrix",
                "Systems nominal after {action}"
            ],
            Theme.GHOSTBUSTERS: [
                "Contained the {component} anomaly",
                "Proton streams stabilized after {action}",
                "Ecto-readings normal"
            ],
            Theme.SUPERHERO: [
                "Power levels stable after {action}",
                "Hero systems {action} successfully",
                "Mission objective: {action} complete"
            ],
            Theme.PIRATES: [
                "Arrr! We {action} the treasure!",
                "Ship's {component} be working fine now",
                "All hands on deck for {action}!"
            ],
            Theme.WIZARDS: [
                "The {component} runes are aligned",
                "Mana flows freely after {action}",
                "Spell complete: {action}"
            ]
        }
        
        # Extract action/component from text
        action = "configured"
        component = "system"
        
        if "create" in text_lower or "add" in text_lower:
            action = "created"
        elif "fix" in text_lower or "bug" in text_lower:
            action = "repaired"
        elif "deploy" in text_lower:
            action = "deployed"
        elif "test" in text_lower:
            action = "tested"
        
        if "api" in text_lower or "endpoint" in text_lower:
            component = "communication"
        elif "database" in text_lower or "query" in text_lower:
            component = "data"
        elif "auth" in text_lower:
            component = "security"
        elif "ui" in text_lower or "frontend" in text_lower:
            component = "interface"
        
        # Pick random template
        theme_templates = templates.get(theme, templates[Theme.SCOOBY])
        template = random.choice(theme_templates)
        
        return template.format(action=action, component=component)
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(entry.category for entry in self.entries))


class TechnobabbleTranslator:
    """Main translator engine with theme support"""
    
    def __init__(self):
        self.dictionary = TechnobabbleDictionary()
        self.current_theme = Theme.SCOOBY
        self.show_raw = False
        self.show_both = False
    
    def set_theme(self, theme: Theme):
        """Set the current translation theme"""
        self.current_theme = theme
    
    def set_mode(self, show_raw: bool = False, show_both: bool = False):
        """Set output mode"""
        self.show_raw = show_raw
        self.show_both = show_both
    
    def translate(self, technical_text: str, original_text: str = None) -> str:
        """
        Translate technical output based on current mode
        
        Args:
            technical_text: The technical output to translate
            original_text: Optional original text for context
        
        Returns:
            Formatted output based on mode settings
        """
        translated = self.dictionary.translate(technical_text, self.current_theme)
        
        if self.show_raw:
            # Show only original
            return technical_text
        elif self.show_both:
            # Show both side-by-side
            return f"{translated}\n\n[Technical]\n{technical_text}"
        else:
            # Show only translated (default)
            return translated
    
    def translate_block(self, text: str, code_block: str = None) -> str:
        """
        Translate a block of text with optional code
        
        Args:
            text: Description/explanation text
            code_block: Optional code block to preserve
        
        Returns:
            Formatted output with translation
        """
        translated = self.translate(text)
        
        if code_block and not self.show_raw:
            return f"{translated}\n\n{code_block}"
        elif code_block and self.show_both:
            return f"{translated}\n\n[Original Code]\n{code_block}"
        elif code_block:
            return code_block
        
        return translated
    
    def get_theme_info(self) -> Dict:
        """Get information about current theme"""
        theme_configs = self._get_theme_configs()
        config = theme_configs.get(self.current_theme)
        
        return {
            "theme": self.current_theme.value,
            "name": config.name if config else "Unknown",
            "description": config.description if config else "",
            "team_name": config.team_name if config else "",
            "vehicle": config.vehicle_name if config else ""
        }
    
    def _get_theme_configs(self) -> Dict[Theme, ThemeConfig]:
        """Get all theme configurations"""
        return {
            Theme.SCOOBY: ThemeConfig(
                id=Theme.SCOOBY,
                name="Scooby-Doo Mystery Gang",
                description="Classic mystery-solving with the gang",
                team_name="Mystery Inc.",
                vehicle_name="The Mystery Machine",
                victory_phrase="Scooby-Dooby-Doo!",
                alarm_sound="🚨 [SPOOKY MUSIC PLAYS]",
                character_prefixes={
                    "fred": "Leader",
                    "velma": "Brains",
                    "daphne": "Style",
                    "shaggy": "Heart",
                    "scooby": "Mascot"
                }
            ),
            Theme.STAR_TREK: ThemeConfig(
                id=Theme.STAR_TREK,
                name="Starfleet Command",
                description="Star Trek technobabble and exploration",
                team_name="USS Enterprise Crew",
                vehicle_name="USS Enterprise",
                victory_phrase="Engage!",
                alarm_sound="🚨 [RED ALERT]",
                character_prefixes={
                    "fred": "Captain",
                    "velma": "Science Officer",
                    "daphne": "Security Chief",
                    "shaggy": "Ensign",
                    "scooby": "Chief Engineer"
                }
            ),
            Theme.GHOSTBUSTERS: ThemeConfig(
                id=Theme.GHOSTBUSTERS,
                name="Ghostbusters",
                description="Paranormal containment and proton packs",
                team_name="Ghostbusters",
                vehicle_name="Ecto-1",
                victory_phrase="We came, we saw, we kicked it!",
                alarm_sound="🚨 [PKE METER SPIKING]",
                character_prefixes={
                    "fred": "Leader",
                    "velma": "Researcher",
                    "daphne": "Field Tech",
                    "shaggy": "Rookie",
                    "scooby": "Mascot"
                }
            ),
            Theme.SUPERHERO: ThemeConfig(
                id=Theme.SUPERHERO,
                name="Superhero Team",
                description="Marvel/DC style heroics",
                team_name="The Avengers",
                vehicle_name="Quinjet",
                victory_phrase="Avengers, assemble!",
                alarm_sound="🚨 [ALERT: THREAT DETECTED]",
                character_prefixes={
                    "fred": "Team Leader",
                    "velma": "Tech Genius",
                    "daphne": "Tactical Specialist",
                    "shaggy": "Reluctant Hero",
                    "scooby": "Mascot"
                }
            ),
            Theme.PIRATES: ThemeConfig(
                id=Theme.PIRATES,
                name="Pirate Crew",
                description="Treasure hunting on the high seas",
                team_name="The Black Pearl Crew",
                vehicle_name="The Black Pearl",
                victory_phrase="The treasure is ours, arrr!",
                alarm_sound="🚨 [MAN THE CANNONS!]",
                character_prefixes={
                    "fred": "Captain",
                    "velma": "Quartermaster",
                    "daphne": "First Mate",
                    "shaggy": "Cabin Boy",
                    "scooby": "Ship's Mascot"
                }
            ),
            Theme.WIZARDS: ThemeConfig(
                id=Theme.WIZARDS,
                name="Wizard Academy",
                description="Magical education and spellcasting",
                team_name="The Order",
                vehicle_name="Flying Carriage",
                victory_phrase="The magic flows strong!",
                alarm_sound="🚨 [MAGICAL DISTURBANCE DETECTED]",
                character_prefixes={
                    "fred": "Headmaster",
                    "velma": "Archmage",
                    "daphne": "Potions Master",
                    "shaggy": "Apprentice",
                    "scooby": "Familiar"
                }
            )
        }
    
    def list_themes(self) -> List[Dict]:
        """List all available themes"""
        configs = self._get_theme_configs()
        return [
            {
                "id": theme.value,
                "name": config.name,
                "description": config.description
            }
            for theme, config in configs.items()
        ]


# Convenience function
def translate(text: str, theme: str = "scooby", mode: str = "translated") -> str:
    """Quick translation function"""
    translator = TechnobabbleTranslator()
    
    try:
        translator.set_theme(Theme(theme))
    except ValueError:
        translator.set_theme(Theme.SCOOBY)
    
    if mode == "raw":
        translator.set_mode(show_raw=True)
    elif mode == "both":
        translator.set_mode(show_both=True)
    
    return translator.translate(text)


if __name__ == "__main__":
    # Test translation
    translator = TechnobabbleTranslator()
    
    test_texts = [
        "Created API endpoint",
        "Fixed null pointer exception",
        "Deployed to production",
        "All tests passing",
        "Bug detected in user service"
    ]
    
    print("🎭 Technobabble Translator Test\n")
    
    for theme in Theme:
        print(f"\n{'='*60}")
        print(f"THEME: {theme.value.upper()}")
        print(f"{'='*60}")
        
        translator.set_theme(theme)
        
        for text in test_texts:
            translated = translator.translate(text)
            print(f"\n  Original: {text}")
            print(f"  → {translated}")
    
    print(f"\n\n📊 Available Themes:")
    for info in translator.list_themes():
        print(f"  • {info['id']}: {info['name']}")
        print(f"    {info['description']}")
