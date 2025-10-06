"""
test_summarizer.py
Tests simples pour la fonction de résumé
"""

import os
import pytest
from unittest.mock import Mock, patch
from project_summarizer.utils.summarizer import summarize_text


class TestSummarizeText:
    """Groupe de tests pour summarize_text"""
    
    @pytest.fixture
    def sample_text(self):
        """Texte d'exemple pour les tests"""
        return """
        L'intelligence artificielle (IA) est un domaine de l'informatique 
        qui vise à créer des machines capables d'effectuer des tâches 
        nécessitant normalement l'intelligence humaine. Les applications 
        incluent la reconnaissance vocale, la vision par ordinateur et 
        le traitement du langage naturel.
        """
    
    def test_summarize_returns_string(self, sample_text):
        """Test 1: Vérifie que la fonction retourne une chaîne"""
        # On simule (mock) l'appel API pour ne pas dépenser de crédits
        with patch('project_summarizer.utils.summarizer.ChatGroq') as mock_groq:
            # Simuler une réponse
            mock_instance = Mock()
            mock_instance.invoke.return_value = "Résumé simulé"
            mock_groq.return_value = mock_instance
            
            result = summarize_text(sample_text)
            
            assert isinstance(result, str)
    
    def test_summarize_with_empty_text(self):
        """Test 2: Vérifie le comportement avec du texte vide"""
        with patch('project_summarizer.utils.summarizer.ChatGroq') as mock_groq:
            mock_instance = Mock()
            mock_instance.invoke.return_value = ""
            mock_groq.return_value = mock_instance
            
            result = summarize_text("")
            
            assert isinstance(result, str)
    
    def test_summarize_uses_api_key(self, sample_text):
        """Test 3: Vérifie que l'API key est utilisée"""
        # Définir une fausse clé API
        os.environ["GROQ_API_KEY"] = "fake-api-key-for-testing"
        
        with patch('project_summarizer.utils.summarizer.ChatGroq') as mock_groq:
            mock_instance = Mock()
            mock_instance.invoke.return_value = "Résumé"
            mock_groq.return_value = mock_instance
            
            summarize_text(sample_text)
            
            # Vérifier que ChatGroq a été appelé avec la clé API
            mock_groq.assert_called_once()
            call_kwargs = mock_groq.call_args[1]
            assert "api_key" in call_kwargs
    
    @pytest.mark.skipif(
        not os.getenv("GROQ_API_KEY"),
        reason="Nécessite une vraie clé API (coûte des crédits)"
    )
    def test_summarize_real_api(self, sample_text):
        """Test 4: Test avec la vraie API (optionnel, à exécuter manuellement)"""
        result = summarize_text(sample_text)
        
        assert len(result) > 0
        assert len(result) < len(sample_text)  # Le résumé doit être plus court