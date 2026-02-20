#!/usr/bin/env python3
"""
Test suite for Technobabble Translator
Tests FR-006: Technical to Cartoon Translation
Tests FR-007: Translation Toggle
Tests FR-008: Technobabble Dictionary
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from technobabble import (
    TechnobabbleTranslator, TechnobabbleDictionary, 
    Theme, ThemeConfig, TranslationEntry
)


class TestTechnobabbleDictionary:
    """Test FR-008: Technobabble Dictionary"""
    
    def test_dictionary_has_minimum_mappings(self):
        """Test FR-008: Minimum 50 technical → cartoon mappings"""
        dictionary = TechnobabbleDictionary()
        
        # Each entry has 6 theme translations
        total_mappings = len(dictionary.entries) * 6
        
        assert total_mappings >= 50, f"Only {total_mappings} mappings, need 50+"
    
    def test_dictionary_supports_all_themes(self):
        """Test that dictionary supports all 6 themes"""
        dictionary = TechnobabbleDictionary()
        
        for entry in dictionary.entries:
            for theme in Theme:
                assert theme in entry.translations, f"Entry missing {theme} translation"
    
    def test_dictionary_has_multiple_categories(self):
        """Test that dictionary covers multiple categories"""
        dictionary = TechnobabbleDictionary()
        
        categories = dictionary.get_all_categories()
        
        assert len(categories) >= 8, f"Only {len(categories)} categories"
        assert "debugging" in categories
        assert "deployment" in categories
        assert "api" in categories
    
    def test_add_mapping(self):
        """Test adding new mappings"""
        dictionary = TechnobabbleDictionary()
        initial_count = len(dictionary.entries)
        
        dictionary.add_mapping(
            "Test mapping",
            {theme: f"Translation for {theme.value}" for theme in Theme},
            "test"
        )
        
        assert len(dictionary.entries) == initial_count + 1
    
    def test_translate_finds_exact_match(self):
        """Test that exact matches are found"""
        dictionary = TechnobabbleDictionary()
        
        result = dictionary.translate("Created API endpoint", Theme.SCOOBY)
        
        assert "mystery" in result.lower() or "chamber" in result.lower()
    
    def test_translate_falls_back_to_keywords(self):
        """Test fallback to keyword-based translation"""
        dictionary = TechnobabbleDictionary()
        
        # Unknown text should still produce themed output
        result = dictionary.translate("Random unknown text xyz", Theme.STAR_TREK)
        
        assert len(result) > 10  # Should produce something
        assert "reconfigured" in result.lower() or "system" in result.lower()


class TestThemeSupport:
    """Test multi-theme functionality"""
    
    def test_all_themes_exist(self):
        """Test that all 6 themes are available"""
        translator = TechnobabbleTranslator()
        themes = translator.list_themes()
        
        assert len(themes) == 6
        
        theme_ids = [t["id"] for t in themes]
        assert "scooby" in theme_ids
        assert "star_trek" in theme_ids
        assert "ghostbusters" in theme_ids
        assert "superhero" in theme_ids
        assert "pirates" in theme_ids
        assert "wizards" in theme_ids
    
    def test_scooby_theme_translation(self):
        """Test Scooby-Doo theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        
        result = translator.translate("Fixed null pointer exception")
        
        assert "scooby" in result.lower() or "mystery" in result.lower() or "anomaly" in result.lower()
    
    def test_star_trek_theme_translation(self):
        """Test Star Trek theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.STAR_TREK)
        
        result = translator.translate("Fixed null pointer exception")
        
        # Should have classic Trek technobabble
        assert any(word in result.lower() for word in 
                  ["flux", "decoupling", "reconfigured", "system", "array"])
    
    def test_ghostbusters_theme_translation(self):
        """Test Ghostbusters theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.GHOSTBUSTERS)
        
        result = translator.translate("Deployed to production")
        
        assert any(word in result.lower() for word in
                  ["containment", "proton", "ecto", "activated"])
    
    def test_superhero_theme_translation(self):
        """Test Superhero theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SUPERHERO)
        
        result = translator.translate("All tests passing")
        
        assert any(word in result.lower() for word in
                  ["hero", "power", "ready", "mission"])
    
    def test_pirates_theme_translation(self):
        """Test Pirates theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.PIRATES)
        
        result = translator.translate("Database query executed")
        
        assert any(word in result.lower() for word in
                  ["arrr", "ship", "treasure", "captain", "log"])
    
    def test_wizards_theme_translation(self):
        """Test Wizards theme translations"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.WIZARDS)
        
        result = translator.translate("Feature implemented")
        
        assert any(word in result.lower() for word in
                  ["spell", "magic", "mana", "enchantment", "rune"])
    
    def test_different_themes_produce_different_output(self):
        """Test that different themes produce distinct translations"""
        translator = TechnobabbleTranslator()
        
        text = "Created API endpoint"
        
        translator.set_theme(Theme.SCOOBY)
        scooby_result = translator.translate(text)
        
        translator.set_theme(Theme.STAR_TREK)
        trek_result = translator.translate(text)
        
        translator.set_theme(Theme.PIRATES)
        pirates_result = translator.translate(text)
        
        assert scooby_result != trek_result
        assert trek_result != pirates_result
        assert scooby_result != pirates_result
    
    def test_theme_config_has_required_fields(self):
        """Test that theme configs have all required fields"""
        translator = TechnobabbleTranslator()
        configs = translator._get_theme_configs()
        
        for theme, config in configs.items():
            assert config.id == theme
            assert config.name != ""
            assert config.description != ""
            assert config.team_name != ""
            assert config.vehicle_name != ""
            assert config.victory_phrase != ""
            assert config.alarm_sound != ""
            assert len(config.character_prefixes) == 5


class TestTranslationToggle:
    """Test FR-007: Translation Toggle"""
    
    def test_default_mode_shows_translated(self):
        """Test FR-007: Default mode shows translated text"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        
        technical = "Created API endpoint"
        result = translator.translate(technical)
        
        # Should NOT contain the original technical text
        assert "Created API endpoint" not in result or result != technical
        # Should contain translated version
        assert len(result) > len(technical)  # Translations are usually longer
    
    def test_raw_mode_shows_original(self):
        """Test FR-007: Raw mode shows original technical text"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        translator.set_mode(show_raw=True)
        
        technical = "Created API endpoint"
        result = translator.translate(technical)
        
        assert result == technical
        assert "mystery" not in result.lower()
    
    def test_both_mode_shows_translated_and_original(self):
        """Test FR-007: Both mode shows translated AND original"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        translator.set_mode(show_both=True)
        
        technical = "Created API endpoint"
        result = translator.translate(technical)
        
        assert "mystery" in result.lower() or "chamber" in result.lower()
        assert technical in result
        assert "[Technical]" in result
    
    def test_mode_can_be_changed_mid_session(self):
        """Test FR-007: Toggle can be changed mid-session"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        
        technical = "Fixed null pointer exception"
        
        # Default mode
        result1 = translator.translate(technical)
        assert "anomaly" in result1.lower() or "neutralized" in result1.lower()
        
        # Switch to raw mode
        translator.set_mode(show_raw=True)
        result2 = translator.translate(technical)
        assert result2 == technical
        
        # Switch back to translated
        translator.set_mode(show_raw=False)
        result3 = translator.translate(technical)
        assert result3 != technical
    
    def test_translate_block_with_code(self):
        """Test translation with code blocks"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        
        text = "Created API endpoint"
        code = "```javascript\napp.get('/api/users')\n```"
        
        result = translator.translate_block(text, code)
        
        assert "mystery" in result.lower() or "chamber" in result.lower()
        assert "app.get" in result  # Code preserved
    
    def test_translate_block_raw_mode(self):
        """Test translation block in raw mode"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.SCOOBY)
        translator.set_mode(show_raw=True)
        
        text = "Created API endpoint"
        code = "```javascript\napp.get('/api/users')\n```"
        
        result = translator.translate_block(text, code)
        
        # In raw mode, should show code only
        assert "app.get" in result
        assert "mystery" not in result.lower()


class TestTechnobabbleTranslator:
    """Test TechnobabbleTranslator engine"""
    
    def test_translator_initializes_with_scooby_theme(self):
        """Test default theme is Scooby"""
        translator = TechnobabbleTranslator()
        
        assert translator.current_theme == Theme.SCOOBY
    
    def test_set_theme_changes_current_theme(self):
        """Test theme switching"""
        translator = TechnobabbleTranslator()
        
        translator.set_theme(Theme.STAR_TREK)
        assert translator.current_theme == Theme.STAR_TREK
        
        translator.set_theme(Theme.PIRATES)
        assert translator.current_theme == Theme.PIRATES
    
    def test_get_theme_info(self):
        """Test getting theme information"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.STAR_TREK)
        
        info = translator.get_theme_info()
        
        assert info["theme"] == "star_trek"
        assert "Starfleet" in info["name"] or "Star Trek" in info["name"]
        assert info["vehicle"] == "USS Enterprise"
    
    def test_list_themes(self):
        """Test listing all themes"""
        translator = TechnobabbleTranslator()
        themes = translator.list_themes()
        
        assert len(themes) == 6
        
        for theme in themes:
            assert "id" in theme
            assert "name" in theme
            assert "description" in theme
    
    def test_translate_preserves_meaning(self):
        """Test that translation preserves technical meaning"""
        translator = TechnobabbleTranslator()
        
        # Test debugging-related translations
        debugging_texts = [
            "Fixed null pointer exception",
            "Bug detected in user service",
            "Error handling added"
        ]
        
        for text in debugging_texts:
            translator.set_theme(Theme.STAR_TREK)
            trek_result = translator.translate(text)
            
            translator.set_theme(Theme.GHOSTBUSTERS)
            gb_result = translator.translate(text)
            
            # Both should be about fixing/containing something
            assert len(trek_result) > 10
            assert len(gb_result) > 10
    
    def test_convenience_translate_function(self):
        """Test the convenience translate() function"""
        from technobabble import translate
        
        # Test with different themes
        scooby = translate("Deployed to production", theme="scooby")
        trek = translate("Deployed to production", theme="star_trek")
        pirates = translate("Deployed to production", theme="pirates")
        
        assert scooby != trek
        assert trek != pirates
        
        # Test modes
        raw = translate("Deployed to production", mode="raw")
        assert raw == "Deployed to production"
        
        both = translate("Deployed to production", mode="both")
        assert "Deployed to production" in both


class TestIntegration:
    """Integration tests for translation workflow"""
    
    def test_full_translation_workflow(self):
        """Test complete translation workflow"""
        translator = TechnobabbleTranslator()
        
        # Set theme
        translator.set_theme(Theme.STAR_TREK)
        
        # Translate multiple outputs
        outputs = [
            "Created API endpoint",
            "Database query executed",
            "All tests passing",
            "Deployed to production"
        ]
        
        translations = []
        for output in outputs:
            translated = translator.translate(output)
            translations.append(translated)
        
        # All should be translated (not original text)
        for translation in translations:
            assert len(translation) > 20
            # Should NOT be the original technical text
            assert translation not in outputs
    
    def test_theme_switching_mid_workflow(self):
        """Test switching themes during workflow"""
        translator = TechnobabbleTranslator()
        
        # Start with Scooby
        translator.set_theme(Theme.SCOOBY)
        result1 = translator.translate("Bug detected")
        
        # Switch to Star Trek
        translator.set_theme(Theme.STAR_TREK)
        result2 = translator.translate("Bug detected")
        
        # Switch to Pirates
        translator.set_theme(Theme.PIRATES)
        result3 = translator.translate("Bug detected")
        
        # All should be different
        assert result1 != result2
        assert result2 != result3
        assert result1 != result3
    
    def test_translation_with_context(self):
        """Test translation with additional context"""
        translator = TechnobabbleTranslator()
        translator.set_theme(Theme.GHOSTBUSTERS)
        
        text = "Fixed null pointer exception"
        original = "// Original code comment"
        
        result = translator.translate_block(text, original)
        
        assert "containment" in result.lower() or "entity" in result.lower()
        assert "// Original code comment" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
