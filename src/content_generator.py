import os
import logging
from anthropic import AsyncAnthropic
from typing import Optional, Dict, Any, List
from src.models import APIConfig, Chapter, ContentType
from src.cache import APICache
# TODO: Importer les modules une fois implémentés
# from src.resource_finder import ResourceFinder, find_resources_for_readme
# from src.pedagogical_validator import PedagogicalValidator

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

class ContentGenerator:
    """
    Génère le contenu pédagogique via Claude API
    
    TODO: INTÉGRATION AVEC RESOURCE FINDER ET VALIDATION
    ===================================================
    
    Le ContentGenerator doit être refactorisé pour intégrer:
    1. ResourceFinder pour enrichir le contenu avec des ressources
    2. PedagogicalValidator pour valider le contenu généré
    3. Analyse des READMEs détaillés créés par PedagogicalPlanner
    
    NOUVEAU WORKFLOW:
    1. Analyser le README détaillé du chapitre (créé par PedagogicalPlanner)
    2. Faire appel à ResourceFinder pour trouver ressources spécialisées
    3. Générer le contenu basé sur README + ressources
    4. Valider le contenu généré avec PedagogicalValidator
    5. Itérer si nécessaire pour améliorer la qualité
    """
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # TODO: Initialiser les nouveaux modules
        # self.resource_finder = ResourceFinder()
        # self.validator = PedagogicalValidator(api_config, cache)
    async def generate_chapter_content(
        self,
        chapter: Chapter,
        content_type: ContentType,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        prompt = self._build_prompt(chapter, content_type, context)
        cache_key = self.cache.get_cache_key(prompt, str(chapter.number))
        cached_content = await self.cache.get(cache_key)
        if cached_content and self.api_config.use_cache:
            return cached_content
        try:
            response = await self.client.messages.create(
                model=self.api_config.model,
                max_tokens=self.api_config.max_tokens,
                temperature=self.api_config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            content = extract_text_from_response(response)
            await self.cache.set(cache_key, content)
            return content
        except Exception as e:
            logger.error(f"Erreur génération contenu: {e}")
            return self._get_default_content(content_type)
    def _build_prompt(self, chapter: Chapter, content_type: ContentType, context: Optional[Dict[str, Any]] = None) -> str:
        if context is None:
            context = {}
        base_context = f"""
        Chapitre {chapter.number}: {chapter.title}
        Objectifs: {', '.join(chapter.objectives)}
        Concepts clés: {', '.join(chapter.key_concepts)}
        Prérequis: {', '.join(chapter.prerequisites)}
        """
        if content_type == ContentType.COURSE:
            return f"""{base_context}
            Génère un cours complet en LaTeX incluant:
            1. Introduction motivante avec exemple concret
            2. Définitions dans des environnements \\begin{{definition}}
            3. Propriétés avec démonstrations dans \\begin{{propriete}}
            4. Exemples détaillés dans \\begin{{exemple}}
            5. Méthodes types dans \\begin{{methode}}
            6. Synthèse finale
            Le cours doit être progressif, clair et adapté au niveau 4ème.
            """
        elif content_type == ContentType.EXERCISE_BASIC:
            return f"""{base_context}
            Génère 10 exercices d'entraînement en LaTeX:
            - Application directe des notions
            - Difficulté progressive
            - Consignes claires
            - Numérotation avec \\exercice{{}}
            """
        elif content_type == ContentType.EXERCISE_ADVANCED:
            return f"""{base_context}
            Génère 8 exercices d'approfondissement en LaTeX:
            - Synthèse de plusieurs notions
            - Problèmes contextualisés
            - Raisonnement élaboré
            """
        elif content_type == ContentType.EXERCISE_CHALLENGE:
            return f"""{base_context}
            Génère 5 exercices défis en LaTeX:
            - Problèmes ouverts
            - Situations complexes
            - Créativité mathématique
            """
        elif content_type == ContentType.EVALUATION_FORMATIVE:
            return f"""{base_context}
            Génère une évaluation formative en LaTeX:
            - 5 questions courtes (QCM, vrai/faux)
            - 3 exercices d'application
            - Barème sur 20 points
            - Durée: 30 minutes
            """
        elif content_type == ContentType.EVALUATION_SUMMATIVE:
            return f"""{base_context}
            Génère une évaluation sommative complète en LaTeX:
            - Questions de cours (4 points)
            - Exercices d'application (8 points)
            - Problème de synthèse (8 points)
            - Barème détaillé
            - Durée: 1 heure
            """
        elif content_type == ContentType.CORRECTION:
            return f"""{base_context}
            Génère les corrections détaillées en LaTeX pour tous les exercices et évaluations:
            - Solutions pas à pas
            - Points clés en couleur
            - Erreurs fréquentes à éviter
            - Méthodes alternatives
            """
    def _get_default_content(self, content_type: ContentType) -> str:
        return f"% Contenu {content_type.value} à générer\n\\textit{{Contenu en cours de génération...}}"

    # ============= NOUVELLES MÉTHODES À IMPLÉMENTER =============
    
    async def generate_enhanced_chapter_content(
        self,
        chapter: Chapter,
        content_type: ContentType,
        chapter_readme_path: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        TODO: Génération de contenu enrichie avec ResourceFinder et validation
        
        NOUVEAU PROCESSUS:
        1. Lire le README détaillé du chapitre (créé par PedagogicalPlanner)
        2. Extraire les points clés et orientations didactiques
        3. Faire appel à ResourceFinder pour ressources spécialisées
        4. Générer le contenu en s'appuyant sur README + ressources
        5. Valider le contenu avec PedagogicalValidator
        6. Itérer si problèmes détectés
        
        Args:
            chapter: Informations du chapitre
            content_type: Type de contenu à générer
            chapter_readme_path: Chemin vers le README détaillé du chapitre
            context: Contexte additionnel
            
        Returns:
            Contenu généré et validé
        """
        
        # TODO: Étape 1 - Lire et analyser le README détaillé
        detailed_readme = await self._read_chapter_readme(chapter_readme_path)
        pedagogical_guidance = await self._extract_pedagogical_guidance(detailed_readme, chapter)
        
        # TODO: Étape 2 - Rechercher ressources spécialisées
        # specialized_resources = await self.resource_finder.find_resources(ResourceQuery(
        #     query_text=f"{content_type.value} {chapter.title} didactique",
        #     level=context.get('level', '5ème'),
        #     subject="mathématiques",
        #     specific_topics=[chapter.title],
        #     resource_types=["pdf", "html"],
        #     max_results=8
        # ))
        
        # TODO: Étape 3 - Générer contenu enrichi
        # enriched_content = await self._generate_content_with_resources(
        #     chapter, content_type, pedagogical_guidance, specialized_resources
        # )
        
        # TODO: Étape 4 - Valider le contenu généré
        # validation_report = await self.validator.validate_generated_content(
        #     enriched_content, content_type.value, chapter, context.get('level', '5ème')
        # )
        
        # TODO: Étape 5 - Itérer si nécessaire
        # if not validation_report.is_valid:
        #     enriched_content = await self._improve_content_based_on_validation(
        #         enriched_content, validation_report, chapter, content_type
        #     )
        
        # TODO: Version actuelle (à remplacer)
        return await self.generate_chapter_content(chapter, content_type, context)
    
    async def _read_chapter_readme(self, readme_path: str) -> str:
        """
        TODO: Lire le README détaillé d'un chapitre
        
        Le README contient:
        - Analyse du programme officiel
        - Logique pédagogique et progression
        - Difficultés connues et erreurs typiques
        - Suggestions méthodologiques
        - Liens avec autres chapitres
        - Ressources complémentaires
        """
        # TODO: Lecture et parsing du README
        return "TODO: Contenu README à lire"
    
    async def _extract_pedagogical_guidance(self, readme_content: str, chapter: Chapter) -> Dict[str, Any]:
        """
        TODO: Extraire les orientations pédagogiques du README
        
        EXTRACTION:
        1. Analyse NLP du README pour identifier:
           - Objectifs pédagogiques prioritaires
           - Difficultés principales identifiées
           - Méthodes recommandées
           - Erreurs à éviter
           - Progression suggérée
        
        2. Structuration de l'information pour utilisation dans la génération
        """
        # TODO: Analyse du README via Claude
        prompt = f"""
        Analyse ce README détaillé pour le chapitre "{chapter.title}":
        
        {readme_content}
        
        Extrais les orientations pédagogiques clés:
        1. Objectifs prioritaires
        2. Difficultés principales à anticiper
        3. Méthodes recommandées
        4. Erreurs typiques à éviter
        5. Progression suggérée
        
        Retourne un JSON structuré.
        """
        
        # TODO: Appel Claude et parsing de la réponse
        return {"objectives": [], "difficulties": [], "methods": [], "progression": []}
    
    async def _generate_content_with_resources(
        self,
        chapter: Chapter,
        content_type: ContentType,
        pedagogical_guidance: Dict[str, Any],
        resources: List
    ) -> str:
        """
        TODO: Générer le contenu en s'appuyant sur les ressources et orientations
        
        ENRICHISSEMENT:
        1. Intégrer les orientations pédagogiques du README
        2. S'appuyer sur les ressources trouvées par ResourceFinder
        3. Adapter le prompt de génération avec ces informations
        4. Générer un contenu plus pertinent et documenté
        """
        
        # TODO: Construction d'un prompt enrichi
        base_prompt = self._build_prompt(chapter, content_type)
        
        # TODO: Enrichissement avec orientations pédagogiques
        pedagogical_section = f"""
        
        ORIENTATIONS PÉDAGOGIQUES SPÉCIALISÉES:
        - Objectifs prioritaires: {pedagogical_guidance.get('objectives', [])}
        - Difficultés à anticiper: {pedagogical_guidance.get('difficulties', [])}
        - Méthodes recommandées: {pedagogical_guidance.get('methods', [])}
        - Progression suggérée: {pedagogical_guidance.get('progression', [])}
        """
        
        # TODO: Enrichissement avec ressources
        resources_section = f"""
        
        RESSOURCES SPÉCIALISÉES DISPONIBLES:
        [TODO: Intégrer contenu des ressources trouvées]
        """
        
        enriched_prompt = base_prompt + pedagogical_section + resources_section
        
        # TODO: Génération avec prompt enrichi
        return await self._generate_with_enriched_prompt(enriched_prompt)
    
    async def _generate_with_enriched_prompt(self, prompt: str) -> str:
        """
        TODO: Générer le contenu avec un prompt enrichi
        
        Utilise un prompt plus long et détaillé qui intègre:
        - Les orientations pédagogiques du README
        - Les ressources spécialisées trouvées
        - Les bonnes pratiques didactiques
        """
        # TODO: Génération via Claude avec prompt enrichi
        try:
            response = await self.client.messages.create(
                model=self.api_config.model,
                max_tokens=int(self.api_config.max_tokens * 1.5),  # Plus de tokens pour contenu enrichi
                temperature=self.api_config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return extract_text_from_response(response)
            
        except Exception as e:
            logger.error(f"Erreur génération enrichie: {e}")
            return "TODO: Contenu enrichi à générer"
    
    async def _improve_content_based_on_validation(
        self,
        content: str,
        validation_report,
        chapter: Chapter,
        content_type: ContentType
    ) -> str:
        """
        TODO: Améliorer le contenu basé sur le rapport de validation
        
        AMÉLIORATIONS:
        1. Analyser les problèmes identifiés par le validateur
        2. Créer un prompt de correction spécialisé
        3. Régénérer les parties problématiques
        4. Valider à nouveau si nécessaire
        """
        
        # TODO: Analyse des problèmes de validation
        issues = validation_report.issues
        critical_issues = [issue for issue in issues if issue.level.value == "critical"]
        warning_issues = [issue for issue in issues if issue.level.value == "warning"]
        
        # TODO: Construction du prompt de correction
        improvement_prompt = f"""
        Améliore ce contenu {content_type.value} pour le chapitre {chapter.title}:
        
        CONTENU ACTUEL:
        {content}
        
        PROBLÈMES IDENTIFIÉS:
        Critiques: {[issue.message for issue in critical_issues]}
        Avertissements: {[issue.message for issue in warning_issues]}
        
        SUGGESTIONS D'AMÉLIORATION:
        {validation_report.recommendations}
        
        Corrige les problèmes identifiés en conservant la structure générale.
        """
        
        # TODO: Génération du contenu amélioré
        return await self._generate_with_enriched_prompt(improvement_prompt)
