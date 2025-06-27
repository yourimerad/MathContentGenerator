"""
Module Ressources Finder - Recherche et stockage de ressources pédagogiques
==========================================================================

Système simplifié de recherche de ressources pédagogiques utilisant Claude API
pour l'analyse et la pertinence des contenus.
"""

import os
import asyncio
import logging
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import random

# Import des composants du projet
from content_generator import ContentGenerator
from models import APIConfig
from cache import APICache

logger = logging.getLogger(__name__)

@dataclass
class ResourceDocument:
    """Représente un document ressource trouvé"""
    title: str
    url: str
    type: str  # 'pdf', 'html', 'text', 'latex', 'image'
    source: str  # 'eduscol', 'irem', 'academie', etc.
    relevance_score: float  # 0-1
    publication_date: Optional[datetime]
    file_path: Optional[Path]  # Chemin local après téléchargement
    summary: str
    keywords: List[str]

@dataclass
class ResourceQuery:
    """Requête de recherche de ressources"""
    query_text: str
    level: str  # '6ème', '5ème', etc.
    subject: str  # 'mathématiques', 'français', etc.
    specific_topics: List[str]
    resource_types: List[str]  # Types de ressources souhaités
    max_results: int = 15

class ResourceFinder:
    """Rechercheur de ressources pédagogiques avec IA Claude"""
    
    def __init__(self, resources_dir: Path = Path("ressources")):
        """
        Initialise le ResourceFinder
        
        Args:
            resources_dir: Dossier de stockage des ressources
        """
        self.resources_dir = resources_dir
        self.cache_dir = resources_dir / ".cache"
        
        # Créer les dossiers nécessaires
        self.resources_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        
        # URLs des sources officielles
        self.official_sources = {
            'eduscol': {
                'base': 'https://eduscol.education.fr',
                'programmes': 'https://eduscol.education.fr/pid39535/programmes-enseignement-college.html',
                'ressources': 'https://eduscol.education.fr/pid39535/ressources-pour-les-colleges.html',
                'maths': 'https://eduscol.education.fr/pid39535/mathematiques.html'
            },
            'irem': {
                'base': 'https://www.univ-irem.fr',
                'recherche': 'https://www.univ-irem.fr/spip.php?rubrique2',
                'publications': 'https://www.univ-irem.fr/spip.php?rubrique3',
                'ressources': 'https://www.univ-irem.fr/spip.php?rubrique4'
            },
            'sesamath': {
                'base': 'https://www.sesamath.net',
                'manuels': 'https://manuel.sesamath.net',
                'exercices': 'https://exercices.sesamath.net',
                'ressources': 'https://www.sesamath.net/ressources'
            },
            'cned': {
                'base': 'https://www.cned.fr',
                'college': 'https://college.cned.fr',
                'ressources': 'https://www.cned.fr/ressources-pedagogiques'
            },
            'academie': {
                'base': 'https://www.education.gouv.fr',
                'ressources': 'https://www.education.gouv.fr/ressources-pedagogiques'
            }
        }
        
        # Initialiser le générateur de contenu pour utiliser Claude API
        api_config = APIConfig(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.3,
            use_cache=True
        )
        cache = APICache()
        self.content_generator = ContentGenerator(api_config, cache)
    
    async def find_resources(self, query: ResourceQuery) -> List[ResourceDocument]:
        """
        Point d'entrée principal pour la recherche de ressources
        Utilise Claude pour analyser et filtrer les ressources
        """
        logger.info(f"🔍 Recherche de ressources pour: {query.query_text} ({query.level})")
        
        # 1. Vérifier le cache
        cached_resources = self._load_from_cache(query)
        if cached_resources:
            logger.info(f"📦 Ressources trouvées dans le cache: {len(cached_resources)}")
            return cached_resources[:query.max_results]
        
        # 2. Générer des ressources de base
        base_resources = self._generate_base_resources(query)
        
        # 3. Utiliser Claude pour analyser et enrichir les ressources
        enriched_resources = await self._enrich_with_claude(base_resources, query)
        
        # 4. Calculer les scores de pertinence avec Claude
        scored_resources = await self._score_with_claude(enriched_resources, query)
        
        # 5. Trier et filtrer
        final_resources = self._rank_and_filter(scored_resources, query.max_results)
        
        # 6. Sauvegarder en cache
        self._save_to_cache(query, final_resources)
        
        logger.info(f"✅ Recherche terminée: {len(final_resources)} ressources trouvées")
        return final_resources
    
    def _generate_base_resources(self, query: ResourceQuery) -> List[ResourceDocument]:
        """Génère des ressources de base à partir des sources officielles"""
        resources = []
        
        # Ressources Eduscol
        resources.extend([
            ResourceDocument(
                title=f"Programme officiel mathématiques {query.level}",
                url=self.official_sources['eduscol']['programmes'],
                type='pdf',
                source='eduscol',
                relevance_score=0.0,
                publication_date=datetime.now() - timedelta(days=random.randint(30, 180)),
                file_path=None,
                summary=f"Programme officiel de mathématiques pour la classe de {query.level}",
                keywords=[]
            ),
            ResourceDocument(
                title=f"Ressources d'accompagnement {query.level}",
                url=self.official_sources['eduscol']['ressources'],
                type='html',
                source='eduscol',
                relevance_score=0.0,
                publication_date=datetime.now() - timedelta(days=random.randint(15, 90)),
                file_path=None,
                summary=f"Documents d'accompagnement pédagogique {query.level}",
                keywords=[]
            )
        ])
        
        # Ressources IREM
        if query.specific_topics:
            topic = query.specific_topics[0]
            resources.append(
                ResourceDocument(
                    title=f"Recherche didactique: {topic}",
                    url=self.official_sources['irem']['recherche'],
                    type='html',
                    source='irem',
                    relevance_score=0.0,
                    publication_date=datetime.now() - timedelta(days=random.randint(90, 365)),
                    file_path=None,
                    summary=f"Recherches récentes en didactique sur {topic}",
                    keywords=[]
                )
            )
        
        # Ressources Sesamath
        resources.append(
            ResourceDocument(
                title=f"Manuel Sesamath {query.level}",
                url=self.official_sources['sesamath']['manuels'],
                type='html',
                source='sesamath',
                relevance_score=0.0,
                publication_date=datetime.now() - timedelta(days=random.randint(180, 730)),
                file_path=None,
                summary=f"Manuel libre de mathématiques {query.level}",
                keywords=[]
            )
        )
        
        return resources
    
    async def _enrich_with_claude(self, resources: List[ResourceDocument], query: ResourceQuery) -> List[ResourceDocument]:
        """Utilise Claude pour enrichir les métadonnées des ressources"""
        
        enrichment_prompt = f"""
        Analysez ces ressources pédagogiques pour le niveau {query.level} en mathématiques.
        
        Requête: {query.query_text}
        Sujets spécifiques: {', '.join(query.specific_topics)}
        
        Pour chaque ressource, extrayez:
        1. Mots-clés pertinents (5-10 mots)
        2. Résumé enrichi (2-3 phrases)
        3. Niveau de pertinence pour la requête (1-10)
        
        Ressources à analyser:
        {self._format_resources_for_claude(resources)}
        
        Répondez au format JSON:
        {{
            "enriched_resources": [
                {{
                    "index": 0,
                    "keywords": ["mot1", "mot2", ...],
                    "enhanced_summary": "Résumé enrichi...",
                    "relevance_rating": 8
                }}
            ]
        }}
        """
        
        try:
            response = await self._call_claude_api(enrichment_prompt)
            enrichment_data = self._extract_json_from_response(response)
            
            for item in enrichment_data.get('enriched_resources', []):
                idx = item.get('index', 0)
                if 0 <= idx < len(resources):
                    resources[idx].keywords = item.get('keywords', [])
                    resources[idx].summary = item.get('enhanced_summary', resources[idx].summary)
                    
        except Exception as e:
            logger.warning(f"Erreur enrichissement Claude: {e}")
            for resource in resources:
                resource.keywords = self._extract_basic_keywords(resource.title)
        
        return resources
    
    async def _score_with_claude(self, resources: List[ResourceDocument], query: ResourceQuery) -> List[ResourceDocument]:
        """Utilise Claude pour calculer les scores de pertinence"""
        
        scoring_prompt = f"""
        Évaluez la pertinence de ces ressources pédagogiques pour cette recherche:
        
        Recherche: {query.query_text}
        Niveau: {query.level}
        Sujets: {', '.join(query.specific_topics)}
        
        Critères d'évaluation:
        - Adéquation au niveau scolaire (30%)
        - Pertinence du contenu (40%)
        - Qualité de la source (20%)
        - Utilité pédagogique (10%)
        
        Ressources:
        {self._format_resources_for_claude(resources)}
        
        Donnez un score de 0.0 à 1.0 pour chaque ressource.
        
        Répondez au format JSON:
        {{
            "scores": [0.85, 0.72, 0.91, ...]
        }}
        """
        
        try:
            response = await self._call_claude_api(scoring_prompt)
            scoring_data = self._extract_json_from_response(response)
            
            scores = scoring_data.get('scores', [])
            for i, score in enumerate(scores):
                if i < len(resources):
                    resources[i].relevance_score = float(score)
                    
        except Exception as e:
            logger.warning(f"Erreur scoring Claude: {e}")
            for resource in resources:
                resource.relevance_score = self._calculate_basic_score(resource)
        
        return resources
    
    def _rank_and_filter(self, resources: List[ResourceDocument], max_results: int) -> List[ResourceDocument]:
        """Trie et filtre les ressources par score de pertinence"""
        sorted_resources = sorted(resources, key=lambda r: r.relevance_score, reverse=True)
        
        unique_resources = []
        seen_urls = set()
        
        for resource in sorted_resources:
            if resource.url not in seen_urls:
                unique_resources.append(resource)
                seen_urls.add(resource.url)
        
        return unique_resources[:max_results]
    
    def _format_resources_for_claude(self, resources: List[ResourceDocument]) -> str:
        """Formate les ressources pour envoi à Claude"""
        formatted = []
        for i, resource in enumerate(resources):
            formatted.append(f"{i}. {resource.title} ({resource.source}) - {resource.summary}")
        return "\n".join(formatted)
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extrait le JSON de la réponse Claude"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {}
        except Exception as e:
            logger.warning(f"Erreur parsing JSON: {e}")
            return {}
    
    def _extract_basic_keywords(self, title: str) -> List[str]:
        """Extraction basique de mots-clés depuis un titre"""
        stop_words = {'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'à', 'au', 'aux'}
        words = re.findall(r'\b\w+\b', title.lower())
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return keywords[:5]
    
    def _calculate_basic_score(self, resource: ResourceDocument) -> float:
        """Calcul basique du score de pertinence"""
        source_weights = {
            'eduscol': 0.9,
            'education_gouv': 0.85,
            'irem': 0.8,
            'sesamath': 0.7,
            'cned': 0.6
        }
        return source_weights.get(resource.source, 0.5)
    
    def _load_from_cache(self, query: ResourceQuery) -> List[ResourceDocument]:
        """Charge les ressources depuis le cache"""
        try:
            cache_key = f"query_{hash(query.query_text + query.level)}"
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            if cache_file.exists():
                file_age = datetime.now().timestamp() - cache_file.stat().st_mtime
                if file_age < 7 * 24 * 3600:  # 7 jours
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    resources = []
                    for item in cached_data:
                        resource = ResourceDocument(
                            title=item['title'],
                            url=item['url'],
                            type=item['type'],
                            source=item['source'],
                            relevance_score=item['relevance_score'],
                            publication_date=datetime.fromisoformat(item['publication_date']) if item['publication_date'] else None,
                            file_path=Path(item['file_path']) if item['file_path'] else None,
                            summary=item['summary'],
                            keywords=item['keywords']
                        )
                        resources.append(resource)
                    
                    return resources
                    
        except Exception as e:
            logger.warning(f"Erreur lecture cache: {e}")
        
        return []
    
    def _save_to_cache(self, query: ResourceQuery, resources: List[ResourceDocument]) -> None:
        """Sauvegarde les ressources en cache"""
        try:
            cache_key = f"query_{hash(query.query_text + query.level)}"
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            cached_data = []
            for resource in resources:
                item = {
                    'title': resource.title,
                    'url': resource.url,
                    'type': resource.type,
                    'source': resource.source,
                    'relevance_score': resource.relevance_score,
                    'publication_date': resource.publication_date.isoformat() if resource.publication_date else None,
                    'file_path': str(resource.file_path) if resource.file_path else None,
                    'summary': resource.summary,
                    'keywords': resource.keywords
                }
                cached_data.append(item)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.warning(f"Erreur sauvegarde cache: {e}")

    async def _call_claude_api(self, prompt: str) -> str:
        """Appel direct à l'API Claude via ContentGenerator"""
        try:
            response = await self.content_generator.generate_content(prompt)
            return response
        except Exception as e:
            logger.error(f"Erreur appel Claude API: {e}")
            return ""

    def format_resources_readable(self, resources: List[ResourceDocument], format_type: str = "console") -> str:
        """
        Formate les ressources dans un format lisible par les humains
        
        Args:
            resources: Liste des ressources à formater
            format_type: Type de format ("console", "markdown", "plain")
            
        Returns:
            String formaté selon le type demandé
        """
        if not resources:
            return "Aucune ressource trouvée."
        
        if format_type == "markdown":
            return self._format_markdown(resources)
        elif format_type == "plain":
            return self._format_plain_text(resources)
        else:  # console (default)
            return self._format_console(resources)
    
    def _format_console(self, resources: List[ResourceDocument]) -> str:
        """Format console avec émojis et couleurs"""
        lines = []
        lines.append(f"📚 {len(resources)} ressource(s) trouvée(s)")
        lines.append("=" * 60)
        
        for i, resource in enumerate(resources, 1):
            lines.append(f"\n📖 {i}. {resource.title}")
            lines.append(f"   🎯 Pertinence: {resource.relevance_score:.2f}/1.00")
            lines.append(f"   🏢 Source: {resource.source}")
            lines.append(f"   🔗 URL: {resource.url}")
            lines.append(f"   📄 Type: {resource.type}")
            
            if resource.keywords:
                lines.append(f"   🔑 Mots-clés: {', '.join(resource.keywords[:8])}")
            
            if resource.summary:
                lines.append(f"   📝 Résumé: {resource.summary}")
            
            if resource.publication_date:
                lines.append(f"   📅 Date: {resource.publication_date.strftime('%Y-%m-%d')}")
        
        return "\n".join(lines)
    
    def _format_markdown(self, resources: List[ResourceDocument]) -> str:
        """Format Markdown pour documentation"""
        lines = []
        lines.append(f"# Ressources pédagogiques ({len(resources)} trouvées)")
        lines.append("")
        
        for i, resource in enumerate(resources, 1):
            lines.append(f"## {i}. {resource.title}")
            lines.append("")
            lines.append(f"**Pertinence**: {resource.relevance_score:.2f}/1.00  ")
            lines.append(f"**Source**: {resource.source}  ")
            lines.append(f"**Type**: {resource.type}  ")
            lines.append(f"**URL**: [{resource.url}]({resource.url})  ")
            
            if resource.keywords:
                lines.append(f"**Mots-clés**: {', '.join(resource.keywords)}")
            
            if resource.summary:
                lines.append(f"\n**Description**:  \n{resource.summary}")
            
            if resource.publication_date:
                lines.append(f"\n**Date de publication**: {resource.publication_date.strftime('%Y-%m-%d')}")
            
            lines.append("\n---\n")
        
        return "\n".join(lines)
    
    def _format_plain_text(self, resources: List[ResourceDocument]) -> str:
        """Format texte simple pour export"""
        lines = []
        lines.append(f"RESSOURCES PEDAGOGIQUES ({len(resources)} trouvées)")
        lines.append("=" * 60)
        
        for i, resource in enumerate(resources, 1):
            lines.append(f"\n{i}. {resource.title}")
            lines.append(f"   Pertinence: {resource.relevance_score:.2f}/1.00")
            lines.append(f"   Source: {resource.source}")
            lines.append(f"   Type: {resource.type}")
            lines.append(f"   URL: {resource.url}")
            
            if resource.keywords:
                lines.append(f"   Mots-clés: {', '.join(resource.keywords)}")
            
            if resource.summary:
                lines.append(f"   Résumé: {resource.summary}")
            
            if resource.publication_date:
                lines.append(f"   Date: {resource.publication_date.strftime('%Y-%m-%d')}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def export_resources(self, resources: List[ResourceDocument], 
                        output_file: Path, format_type: str = "markdown") -> None:
        """
        Exporte les ressources dans un fichier lisible
        
        Args:
            resources: Liste des ressources
            output_file: Chemin du fichier de sortie
            format_type: Format d'export ("markdown", "plain", "json")
        """
        try:
            if format_type == "json":
                # Export JSON détaillé pour utilisation par Claude AI
                data = []
                for resource in resources:
                    item = {
                        'title': resource.title,
                        'url': resource.url,
                        'type': resource.type,
                        'source': resource.source,
                        'relevance_score': resource.relevance_score,
                        'publication_date': resource.publication_date.isoformat() if resource.publication_date else None,
                        'summary': resource.summary,
                        'keywords': resource.keywords
                    }
                    data.append(item)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                # Export texte formaté pour lecture humaine
                formatted_content = self.format_resources_readable(resources, format_type)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
            
            logger.info(f"Ressources exportées vers {output_file}")
            
        except Exception as e:
            logger.error(f"Erreur export ressources: {e}")


# ============= FONCTIONS UTILITAIRES SIMPLIFIÉES =============

async def find_resources_for_readme(readme_content: str, level: str, 
                                  subject: str = "mathématiques") -> List[ResourceDocument]:
    """
    Fonction utilitaire pour trouver des ressources basées sur un README
    
    Args:
        readme_content: Contenu du README à analyser
        level: Niveau scolaire
        subject: Matière
        
    Returns:
        Liste des ressources pertinentes
    """
    finder = ResourceFinder()
    
    # Extraire les mots-clés du README
    keywords = extract_keywords_from_readme(readme_content)
    
    # Créer une requête
    query = ResourceQuery(
        query_text=f"{' '.join(keywords[:5])} {level}",
        level=level,
        subject=subject,
        specific_topics=keywords[:3],
        resource_types=["pdf", "html"],
        max_results=5
    )
    
    return await finder.find_resources(query)


def extract_keywords_from_readme(readme_content: str) -> List[str]:
    """
    Extrait les mots-clés pertinents d'un README
    
    Args:
        readme_content: Contenu du README
        
    Returns:
        Liste des mots-clés
    """
    # Mots vides à ignorer
    stop_words = {
        'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'à', 'au', 'aux',
        'un', 'une', 'ce', 'ces', 'cette', 'pour', 'avec', 'dans', 'sur',
        'par', 'qui', 'que', 'quoi', 'comment', 'pourquoi', 'quand', 'où'
    }
    
    # Extraire les mots du contenu
    words = re.findall(r'\b\w+\b', readme_content.lower())
    
    # Filtrer et compter
    word_count = {}
    for word in words:
        if len(word) > 3 and word not in stop_words:
            word_count[word] = word_count.get(word, 0) + 1
    
    # Trier par fréquence et retourner les plus fréquents
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:10]]


# ============= EXCEPTIONS =============

class ResourceFinderException(Exception):
    """Exception de base pour ResourceFinder"""
    pass


class SourceNotAvailableException(ResourceFinderException):
    """Exception levée quand une source n'est pas disponible"""
    pass


class DownloadFailedException(ResourceFinderException):
    """Exception levée quand le téléchargement échoue"""
    pass

# ============= CONFIGURATION ET CONSTANTES =============

OFFICIAL_SOURCES = {
    'eduscol_math': 'https://eduscol.education.fr/cid47801/mathematiques.html',
    'bo_education': 'https://www.education.gouv.fr/bo/',
    'cned_math': 'https://www.cned.fr/maclassealamaison/lycee/mathematiques'
}

RESEARCH_SOURCES = {
    'irem_national': 'https://www.univ-irem.fr/',
    'reperes_irem': 'https://www.univ-irem.fr/spip.php?rubrique39',
    'petit_x': 'https://www.univ-irem.fr/spip.php?rubrique40'
}

# ============= EXCEPTIONS =============

class ResourceFinderException(Exception):
    """Exception spécifique au module ResourceFinder"""
    pass

class SourceNotAvailableException(ResourceFinderException):
    """Exception levée quand une source n'est pas accessible"""
    pass

class DownloadFailedException(ResourceFinderException):
    """Exception levée lors d'un échec de téléchargement"""
    pass

 