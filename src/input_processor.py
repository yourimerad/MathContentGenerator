import os
import re
import json
from typing import Dict, Any, List, Optional
from anthropic import AsyncAnthropic
from src.models import APIConfig
from src.cache import APICache
import PyPDF2
import aiofiles
import logging

logger = logging.getLogger(__name__)

def extract_text_from_response(response) -> str:
    try:
        if hasattr(response, 'content') and response.content:
            content_block = response.content[0]
            if hasattr(content_block, 'text'):
                return content_block.text
            elif hasattr(content_block, 'type') and content_block.type == 'text':
                return content_block.text
        return ""
    except Exception as e:
        logger.error(f"Erreur extraction texte réponse: {e}")
        return ""

class InputProcessor:
    """Parse automatiquement tous types de programmes/ressources via Claude API"""
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def process_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """Traite toutes les sources d'entrée et extrait les informations structurées"""
        all_content = []
        for source in sources:
            content = await self._extract_content(source)
            all_content.append(content)
        structured_data = await self._analyze_with_claude(all_content)
        return structured_data
    
    async def _extract_content(self, source: Dict[str, str]) -> str:
        source_type = source.get("type", "text")
        if source_type == "pdf":
            return await self._extract_pdf(source["path"])
        elif source_type == "url":
            return await self._extract_url(source["url"])
        elif source_type == "text":
            return source["content"]
        elif source_type == "image":
            return await self._extract_image(source["path"])
        else:
            return source.get("content", "")
    
    async def _extract_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            return ""
    
    async def _extract_url(self, url: str) -> str:
        return f"Contenu extrait de {url}"
    
    async def _extract_image(self, image_path: str) -> str:
        return f"Texte extrait de l'image {image_path}"
    
    async def _analyze_with_claude(self, contents: List[str]) -> Dict[str, Any]:
        prompt = f"""
        Analyse les contenus suivants provenant de différentes sources pédagogiques et extrais:
        1. Les objectifs pédagogiques
        2. Les compétences visées
        3. La structure du programme (chapitres/thèmes)
        4. Les prérequis
        5. Les critères d'évaluation
        Contenus à analyser:
        {' '.join(contents[:3000])}
        Retourne une structure JSON avec ces informations.
        """
        cache_key = self.cache.get_cache_key(prompt)
        cached_result = await self.cache.get(cache_key)
        if cached_result and self.api_config.use_cache:
            return cached_result
        try:
            response = await self.client.messages.create(
                model=self.api_config.model,
                max_tokens=self.api_config.max_tokens,
                temperature=self.api_config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._parse_claude_response(extract_text_from_response(response))
            await self.cache.set(cache_key, result)
            return result
        except Exception as e:
            logger.error(f"Erreur API Claude: {e}")
            return self._get_default_structure()
    
    def _parse_claude_response(self, response: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict[str, Any]:
        return {
            "objectives": ["Objectifs à définir"],
            "competencies": ["Compétences à définir"],
            "chapters": [],
            "prerequisites": [],
            "evaluation_criteria": {}
        }
