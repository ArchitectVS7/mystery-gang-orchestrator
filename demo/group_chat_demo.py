#!/usr/bin/env python3
"""
Mystery Gang Group Chat Demo
Simulates a real-time group chat session with the gang
"""

import sys
import time
import random
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from character import CharacterEngine
from assembly import TaskAnalyzer, TeamSelector, AssemblySceneGenerator
from technobabble import TechnobabbleTranslator, Theme


class GroupChatDemo:
    """Simulates a group chat session with the Mystery Gang"""
    
    def __init__(self, theme: Theme = Theme.SCOOBY):
        self.char_engine = CharacterEngine()
        self.analyzer = TaskAnalyzer()
        self.selector = TeamSelector()
        self.scene_gen = AssemblySceneGenerator(self.char_engine)
        self.translator = TechnobabbleTranslator()
        self.translator.set_theme(theme)
        
        self.theme = theme
        self.chat_history = []
        self.reactions = []
    
    def print_header(self):
        """Print chat header"""
        theme_info = self.translator.get_theme_info()
        
        print("\n" + "="*70)
        print(f"  🎭 MYSTERY GANG GROUP CHAT - {theme_info['name'].upper()}")
        print("="*70)
        print(f"  Team: {theme_info['team_name']}")
        print(f"  Vehicle: {theme_info['vehicle']}")
        print(f"  Mode: Translated (toggle with --raw or --both)")
        print("="*70 + "\n")
    
    def print_message(self, character_id: str, message: str, delay: float = 0.5):
        """Print a character message with typing effect"""
        char = self.char_engine.get_character(character_id)
        
        # Format message
        formatted = f"{char.name}: {message}"
        
        print(formatted)
        self.chat_history.append({
            "character": character_id,
            "message": message,
            "timestamp": time.time()
        })
        
        # Simulate typing delay
        time.sleep(delay)
    
    def print_reaction(self, emoji: str, character_id: str = None):
        """Print a reaction emoji"""
        if character_id:
            char = self.char_engine.get_character(character_id)
            reaction = f"  {char.name.split()[0]}: {emoji}"
        else:
            reaction = f"  {emoji}"
        
        print(reaction)
        self.reactions.append({
            "emoji": emoji,
            "character": character_id,
            "timestamp": time.time()
        })
        
        time.sleep(0.2)
    
    def print_technical_update(self, technical: str, translated: str = None):
        """Print a technical update with translation"""
        if translated is None:
            translated = self.translator.translate(technical)
        
        print(f"\n  🔧 {translated}")
        time.sleep(0.3)
    
    def run_demo(self, task: str, show_raw: bool = False, show_both: bool = False):
        """Run the full group chat demo"""
        
        if show_raw:
            self.translator.set_mode(show_raw=True)
        elif show_both:
            self.translator.set_mode(show_both=True)
        
        self.print_header()
        
        # Phase 1: Task Assignment
        print("📋 INCOMING TASK:")
        print(f"   {task}")
        print()
        time.sleep(1)
        
        # Phase 2: Analysis
        analysis = self.analyzer.analyze(task)
        print(f"📊 Task Analysis:")
        print(f"   Type: {analysis.task_type.value}")
        print(f"   Keywords: {', '.join(analysis.keywords)}")
        print(f"   Confidence: {analysis.confidence:.0f}%")
        print()
        time.sleep(1)
        
        # Phase 3: Team Assembly
        print("🚨 ASSEMBLING TEAM...")
        print()
        time.sleep(0.5)
        
        team = self.selector.select(task)
        scene = self.scene_gen.generate(team, task, analysis)
        
        # Print assembly scene
        for line in scene.split('\n'):
            print(line)
            time.sleep(0.3)
        
        print()
        time.sleep(1)
        
        # Phase 4: Group Chat - Work Session
        print("\n💬 WORK SESSION BEGINS\n")
        print("-"*70 + "\n")
        
        # Fred kicks off
        self.print_message("fred", self.char_engine.generate_dialogue("fred", "planning", task))
        self.print_reaction("📋", "daphne")
        
        # Velma starts researching
        self.print_message("velma", self.char_engine.generate_dialogue("velma", "discovery", task))
        self.print_technical_update(
            "Created API endpoint",
            self.translator.translate("Created API endpoint")
        )
        self.print_reaction("✅", "fred")
        self.print_reaction("🔍", "scooby")
        
        # Daphne reviews
        self.print_message("daphne", self.char_engine.generate_dialogue("daphne", "review", task))
        self.print_technical_update(
            "Added error handling",
            self.translator.translate("Error handling added")
        )
        self.print_reaction("🛡️", "velma")
        
        # Shaggy documents
        self.print_message("shaggy", self.char_engine.generate_dialogue("shaggy", "default", task))
        self.print_technical_update(
            "Documentation updated",
            self.translator.translate("Documentation updated")
        )
        self.print_reaction("📝", "fred")
        self.print_reaction("👍", "daphne")
        
        # Scooby finds a bug
        self.print_message("scooby", self.char_engine.generate_dialogue("scooby", "discovery", task))
        self.print_reaction("😱", "shaggy")
        
        self.print_technical_update(
            "Bug detected in user service",
            self.translator.translate("Bug detected in user service")
        )
        
        # Velma fixes it
        self.print_message("velma", "Jinkies! I found the solution in the docs!")
        self.print_technical_update(
            "Fixed null pointer exception",
            self.translator.translate("Fixed null pointer exception")
        )
        self.print_reaction("🧠", "fred")
        self.print_reaction("🎯", "daphne")
        
        # Run tests
        self.print_message("scooby", "Running tests now...")
        self.print_technical_update(
            "Running tests",
            self.translator.translate("Running tests")
        )
        time.sleep(0.5)
        
        self.print_technical_update(
            "All tests passing",
            self.translator.translate("All tests passing")
        )
        self.print_reaction("🎉", "fred")
        self.print_reaction("🎉", "velma")
        self.print_reaction("🎉", "daphne")
        self.print_reaction("🎉", "shaggy")
        self.print_reaction("🐾", "scooby")
        
        # Victory!
        print("\n" + "-"*70)
        print("\n✅ MISSION COMPLETE!\n")
        
        victory_phrase = self.translator._get_theme_configs()[self.theme].victory_phrase
        print(f"   {victory_phrase}")
        print()
        
        # Summary
        print("📦 DELIVERABLES:")
        deliverables = [
            ("API endpoints created", "resonance chamber calibrated"),
            ("Authentication implemented", "security protocols engaged"),
            ("Error handling added", "safety nets deployed"),
            ("Documentation written", "logs recorded"),
            ("15 tests passing", "all traps sprung successfully"),
            ("Bug fixed", "spectral anomaly neutralized")
        ]
        
        for technical, translated in deliverables:
            if show_raw:
                print(f"   ✓ {technical}")
            elif show_both:
                print(f"   ✓ {translated}")
                print(f"     [{technical}]")
            else:
                print(f"   ✓ {translated}")
        
        print()
        
        # Stats
        print("📊 SESSION STATS:")
        print(f"   Messages: {len(self.chat_history)}")
        print(f"   Reactions: {len(self.reactions)}")
        print(f"   Theme: {self.theme.value}")
        print(f"   Mode: {'raw' if show_raw else 'both' if show_both else 'translated'}")
        print()
        
        print("="*70)
        print("  Demo complete! Run with --raw or --both to see translation toggle")
        print("="*70 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mystery Gang Group Chat Demo")
    parser.add_argument(
        "--theme", 
        choices=["scooby", "star_trek", "ghostbusters", "superhero", "pirates", "wizards"],
        default="scooby",
        help="Translation theme"
    )
    parser.add_argument(
        "--task",
        default="Create REST API with authentication",
        help="Task to execute"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Show raw technical output (no translation)"
    )
    parser.add_argument(
        "--both",
        action="store_true",
        help="Show both translated and raw output"
    )
    
    args = parser.parse_args()
    
    # Convert theme string to enum
    theme_map = {
        "scooby": Theme.SCOOBY,
        "star_trek": Theme.STAR_TREK,
        "ghostbusters": Theme.GHOSTBUSTERS,
        "superhero": Theme.SUPERHERO,
        "pirates": Theme.PIRATES,
        "wizards": Theme.WIZARDS
    }
    
    theme = theme_map[args.theme]
    
    # Run demo
    demo = GroupChatDemo(theme=theme)
    demo.run_demo(args.task, show_raw=args.raw, show_both=args.both)


if __name__ == "__main__":
    main()
