import os
import re
import json
import logging
from anthropic import AsyncAnthropic
from typing import Dict, Any, List
from src.models import APIConfig, CourseConfig, PedagogicalProgram, Chapter
from src.cache import APICache
# TODO: Importer le module ResourceFinder une fois implémenté
# from src.resource_finder import ResourceFinder, find_resources_for_readme

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

class PedagogicalPlanner:
    """
    Planification pédagogique optimisée via Claude API
    
    TODO: INTÉGRATION AVEC RESOURCE FINDER
    =====================================
    
    Le PedagogicalPlanner doit être refactorisé pour intégrer le ResourceFinder
    dans son workflow de création de progression annuelle.
    
    NOUVEAU WORKFLOW:
    1. Analyser la demande utilisateur (niveau, spécificités, horaires)
    2. Créer un README concis de la demande
    3. Utiliser ResourceFinder pour trouver ressources officielles (Eduscol, BO, IREM)
    4. Analyser les ressources pour comprendre le programme officiel
    5. Créer la progression annuelle basée sur les ressources
    6. Pour chaque chapitre: nouvelle requête ResourceFinder spécialisée
    7. Rédiger README détaillé par chapitre avec analyse didactique approfondie
    
    RESSOURCES À UTILISER:
    - Documents Eduscol par niveau
    - Programmes officiels (BO)
    - Documents méthodologiques pour professeurs
    - Papiers de recherche didactique récents
    - Guides d'accompagnement pédagogique
    """
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # TODO: Initialiser ResourceFinder
        # self.resource_finder = ResourceFinder()
        
    async def create_annual_planning(
        self, 
        structured_data: Dict[str, Any],
        course_config: CourseConfig
    ) -> PedagogicalProgram:
        """Crée la planification annuelle optimale"""
        prompt = f"""
        Crée une planification pédagogique annuelle optimale pour:
        - Niveau: {course_config.level}
        - Nombre de séances: {course_config.sessions_per_year}
        - Programme: {json.dumps(structured_data, ensure_ascii=False)}
        La planification doit inclure:
        1. Organisation logique des chapitres
        2. Progression adaptée au niveau
        3. Répartition temporelle équilibrée
        4. Gestion des prérequis
        5. Moments d'évaluation stratégiques
        Retourne un JSON structuré avec tous les chapitres planifiés.
        """
        try:
            response = await self.client.messages.create(
                model=self.api_config.model,
                max_tokens=self.api_config.max_tokens,
                temperature=self.api_config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            planning_data = self._parse_planning_response(extract_text_from_response(response))
            return self._create_program_object(planning_data, course_config.level)
        except Exception as e:
            logger.error(f"Erreur planification: {e}")
            return self._get_default_program(course_config.level)
    
    def _parse_planning_response(self, response: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return {}
    
    def _create_program_object(self, data: Dict[str, Any], level: str) -> PedagogicalProgram:
        chapters = []
        for i, chap_data in enumerate(data.get("chapters", []), 1):
            chapter = Chapter(
                number=i,
                title=chap_data.get("title", f"Chapitre {i}"),
                objectives=chap_data.get("objectives", []),
                prerequisites=chap_data.get("prerequisites", []),
                duration_hours=chap_data.get("duration", 8),
                key_concepts=chap_data.get("concepts", []),
                competencies=chap_data.get("competencies", [])
            )
            chapters.append(chapter)
        return PedagogicalProgram(
            level=level,
            total_sessions=data.get("total_sessions", 120),
            chapters=chapters,
            general_objectives=data.get("general_objectives", []),
            evaluation_criteria=data.get("evaluation_criteria", {})
        )
    
    def _get_default_program(self, level: str) -> PedagogicalProgram:
        """Programme par défaut adapté au niveau"""
        
        if level == "6ème":
            chapters = [
                Chapter(
                    number=1,
                    title="Nombres entiers et décimaux",
                    objectives=["Maîtriser l'écriture et la comparaison des nombres", "Effectuer des calculs avec les nombres entiers et décimaux"],
                    prerequisites=["Numération de base", "Opérations élémentaires"],
                    duration_hours=10,
                    key_concepts=["Écriture des nombres", "Comparaison", "Ordre de grandeur"],
                    competencies=["Calculer", "Représenter"]
                ),
                Chapter(
                    number=2,
                    title="Addition et soustraction",
                    objectives=["Maîtriser les techniques opératoires", "Résoudre des problèmes"],
                    prerequisites=["Nombres entiers et décimaux"],
                    duration_hours=8,
                    key_concepts=["Techniques opératoires", "Ordre de grandeur", "Problèmes"],
                    competencies=["Calculer", "Chercher"]
                ),
                Chapter(
                    number=3,
                    title="Multiplication",
                    objectives=["Connaître les tables de multiplication", "Maîtriser la technique opératoire"],
                    prerequisites=["Addition", "Soustraction"],
                    duration_hours=10,
                    key_concepts=["Tables de multiplication", "Technique opératoire", "Distributivité"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=4,
                    title="Division",
                    objectives=["Comprendre le sens de la division", "Maîtriser la division euclidienne"],
                    prerequisites=["Multiplication"],
                    duration_hours=10,
                    key_concepts=["Division euclidienne", "Quotient et reste", "Multiples et diviseurs"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=5,
                    title="Fractions",
                    objectives=["Comprendre la notion de fraction", "Comparer des fractions simples"],
                    prerequisites=["Division", "Partage"],
                    duration_hours=12,
                    key_concepts=["Fraction comme quotient", "Fractions égales", "Comparaison"],
                    competencies=["Représenter", "Raisonner"]
                ),
                Chapter(
                    number=6,
                    title="Géométrie - Figures planes",
                    objectives=["Reconnaître et construire les figures usuelles", "Utiliser les instruments de géométrie"],
                    prerequisites=["Notions de base de géométrie"],
                    duration_hours=12,
                    key_concepts=["Triangle", "Quadrilatères", "Cercle", "Construction"],
                    competencies=["Représenter", "Construire"]
                ),
                Chapter(
                    number=7,
                    title="Périmètres et aires",
                    objectives=["Calculer des périmètres et des aires", "Résoudre des problèmes géométriques"],
                    prerequisites=["Figures planes", "Multiplication"],
                    duration_hours=10,
                    key_concepts=["Périmètre", "Aire", "Unités de mesure"],
                    competencies=["Calculer", "Modéliser"]
                ),
                Chapter(
                    number=8,
                    title="Proportionnalité",
                    objectives=["Reconnaître une situation de proportionnalité", "Résoudre des problèmes"],
                    prerequisites=["Multiplication", "Division"],
                    duration_hours=10,
                    key_concepts=["Tableau de proportionnalité", "Coefficient", "Pourcentages simples"],
                    competencies=["Chercher", "Modéliser"]
                ),
                Chapter(
                    number=9,
                    title="Volumes",
                    objectives=["Calculer des volumes de solides usuels", "Comprendre les unités de volume"],
                    prerequisites=["Aires", "Multiplication"],
                    duration_hours=8,
                    key_concepts=["Cube", "Pavé droit", "Unités de volume"],
                    competencies=["Calculer", "Représenter"]
                ),
                Chapter(
                    number=10,
                    title="Statistiques",
                    objectives=["Lire et interpréter des graphiques", "Organiser des données"],
                    prerequisites=["Lecture de nombres"],
                    duration_hours=8,
                    key_concepts=["Graphiques", "Tableaux", "Moyenne simple"],
                    competencies=["Représenter", "Interpréter"]
                )
            ]
        elif level == "5ème":
            chapters = [
                Chapter(
                    number=1,
                    title="Nombres relatifs",
                    objectives=["Comprendre la notion de nombre relatif", "Se repérer sur une droite graduée"],
                    prerequisites=["Nombres entiers et décimaux"],
                    duration_hours=10,
                    key_concepts=["Nombres positifs et négatifs", "Droite graduée", "Comparaison"],
                    competencies=["Représenter", "Raisonner"]
                ),
                Chapter(
                    number=2,
                    title="Addition et soustraction de nombres relatifs",
                    objectives=["Effectuer des calculs avec les nombres relatifs", "Simplifier l'écriture"],
                    prerequisites=["Nombres relatifs"],
                    duration_hours=12,
                    key_concepts=["Règles d'addition", "Règles de soustraction", "Simplification"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=3,
                    title="Fractions - Operations",
                    objectives=["Additionner et soustraire des fractions", "Multiplier par un nombre entier"],
                    prerequisites=["Fractions de 6ème", "Nombres relatifs"],
                    duration_hours=15,
                    key_concepts=["Dénominateur commun", "Multiplication de fractions", "Simplification"],
                    competencies=["Calculer", "Modéliser"]
                ),
                Chapter(
                    number=4,
                    title="Expressions littérales",
                    objectives=["Utiliser des lettres pour exprimer des formules", "Substituer une valeur"],
                    prerequisites=["Opérations de base"],
                    duration_hours=12,
                    key_concepts=["Variable", "Expression", "Substitution", "Formules"],
                    competencies=["Modéliser", "Calculer"]
                ),
                Chapter(
                    number=5,
                    title="Équations",
                    objectives=["Résoudre des équations simples", "Tester une égalité"],
                    prerequisites=["Expressions littérales", "Nombres relatifs"],
                    duration_hours=12,
                    key_concepts=["Équation", "Solution", "Méthodes de résolution"],
                    competencies=["Chercher", "Raisonner"]
                ),
                Chapter(
                    number=6,
                    title="Triangles",
                    objectives=["Construire des triangles", "Connaître les propriétés"],
                    prerequisites=["Géométrie de 6ème"],
                    duration_hours=10,
                    key_concepts=["Construction", "Inégalité triangulaire", "Médiatrice"],
                    competencies=["Construire", "Raisonner"]
                ),
                Chapter(
                    number=7,
                    title="Parallélogrammes",
                    objectives=["Reconnaître et construire des parallélogrammes", "Connaître les propriétés"],
                    prerequisites=["Triangles", "Géométrie de base"],
                    duration_hours=12,
                    key_concepts=["Parallélogramme", "Rectangle", "Losange", "Carré"],
                    competencies=["Construire", "Raisonner"]
                ),
                Chapter(
                    number=8,
                    title="Symétrie centrale",
                    objectives=["Construire le symétrique d'une figure", "Reconnaître une symétrie centrale"],
                    prerequisites=["Figures géométriques"],
                    duration_hours=10,
                    key_concepts=["Centre de symétrie", "Image", "Conservation"],
                    competencies=["Construire", "Représenter"]
                ),
                Chapter(
                    number=9,
                    title="Proportionnalité et pourcentages",
                    objectives=["Résoudre des problèmes de proportionnalité", "Calculer des pourcentages"],
                    prerequisites=["Proportionnalité de 6ème"],
                    duration_hours=12,
                    key_concepts=["Coefficient de proportionnalité", "Pourcentages", "Échelles"],
                    competencies=["Modéliser", "Calculer"]
                ),
                Chapter(
                    number=10,
                    title="Aires et volumes",
                    objectives=["Calculer des aires et volumes", "Utiliser les formules"],
                    prerequisites=["Géométrie", "Expressions littérales"],
                    duration_hours=10,
                    key_concepts=["Formules d'aires", "Volumes", "Unités"],
                    competencies=["Calculer", "Modéliser"]
                )
            ]
        elif level == "4ème":
            chapters = [
                Chapter(
                    number=1,
                    title="Nombres relatifs et opérations",
                    objectives=["Maîtriser les opérations sur les nombres relatifs"],
                    prerequisites=["Nombres entiers", "Opérations de base"],
                    duration_hours=12,
                    key_concepts=["Nombres relatifs", "Addition", "Soustraction", "Multiplication"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=2,
                    title="Calcul littéral",
                    objectives=["Développer et factoriser des expressions"],
                    prerequisites=["Nombres relatifs", "Priorités opératoires"],
                    duration_hours=15,
                    key_concepts=["Variable", "Expression littérale", "Développement", "Factorisation"],
                    competencies=["Modéliser", "Calculer"]
                ),
                Chapter(
                    number=3,
                    title="Équations et inéquations",
                    objectives=["Résoudre des équations et inéquations du premier degré"],
                    prerequisites=["Calcul littéral", "Nombres relatifs"],
                    duration_hours=12,
                    key_concepts=["Équation du premier degré", "Inéquations", "Méthodes de résolution"],
                    competencies=["Chercher", "Raisonner"]
                ),
                Chapter(
                    number=4,
                    title="Théorème de Pythagore",
                    objectives=["Appliquer le théorème de Pythagore", "Démontrer qu'un triangle est rectangle"],
                    prerequisites=["Triangles rectangles", "Calculs avec les racines"],
                    duration_hours=12,
                    key_concepts=["Théorème de Pythagore", "Réciproque", "Hypoténuse"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=5,
                    title="Proportionnalité - Vitesse",
                    objectives=["Résoudre des problèmes de proportionnalité", "Calculer des vitesses"],
                    prerequisites=["Proportionnalité de 5ème"],
                    duration_hours=10,
                    key_concepts=["Vitesse moyenne", "Débit", "Échelles"],
                    competencies=["Modéliser", "Calculer"]
                ),
                Chapter(
                    number=6,
                    title="Fractions et nombres décimaux",
                    objectives=["Effectuer des opérations sur les fractions", "Passer d'une écriture à l'autre"],
                    prerequisites=["Fractions de 5ème"],
                    duration_hours=12,
                    key_concepts=["Opérations sur les fractions", "Écritures décimales", "Simplification"],
                    competencies=["Calculer", "Représenter"]
                ),
                Chapter(
                    number=7,
                    title="Puissances",
                    objectives=["Utiliser les puissances de 10", "Écriture scientifique"],
                    prerequisites=["Multiplication", "Nombres décimaux"],
                    duration_hours=10,
                    key_concepts=["Puissances de 10", "Écriture scientifique", "Ordres de grandeur"],
                    competencies=["Calculer", "Représenter"]
                ),
                Chapter(
                    number=8,
                    title="Statistiques",
                    objectives=["Calculer des moyennes pondérées", "Interpréter des graphiques"],
                    prerequisites=["Statistiques de 5ème"],
                    duration_hours=8,
                    key_concepts=["Moyenne pondérée", "Fréquences", "Graphiques"],
                    competencies=["Calculer", "Interpréter"]
                )
            ]
        elif level == "3ème":
            chapters = [
                Chapter(
                    number=1,
                    title="Calcul littéral et identités remarquables",
                    objectives=["Maîtriser les identités remarquables", "Factoriser des expressions"],
                    prerequisites=["Calcul littéral de 4ème"],
                    duration_hours=15,
                    key_concepts=["Identités remarquables", "Factorisation", "Développement"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=2,
                    title="Équations et systèmes",
                    objectives=["Résoudre des systèmes d'équations", "Méthodes de résolution"],
                    prerequisites=["Équations de 4ème"],
                    duration_hours=12,
                    key_concepts=["Système d'équations", "Substitution", "Combinaison"],
                    competencies=["Chercher", "Modéliser"]
                ),
                Chapter(
                    number=3,
                    title="Fonctions",
                    objectives=["Comprendre la notion de fonction", "Représenter graphiquement"],
                    prerequisites=["Calcul littéral", "Repérage"],
                    duration_hours=15,
                    key_concepts=["Fonction", "Image", "Antécédent", "Représentation graphique"],
                    competencies=["Modéliser", "Représenter"]
                ),
                Chapter(
                    number=4,
                    title="Théorème de Thalès",
                    objectives=["Appliquer le théorème de Thalès", "Calculer des longueurs"],
                    prerequisites=["Géométrie plane", "Proportionnalité"],
                    duration_hours=12,
                    key_concepts=["Théorème de Thalès", "Réciproque", "Configuration"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=5,
                    title="Trigonométrie",
                    objectives=["Utiliser les rapports trigonométriques", "Résoudre des triangles rectangles"],
                    prerequisites=["Théorème de Pythagore", "Triangle rectangle"],
                    duration_hours=12,
                    key_concepts=["Cosinus", "Sinus", "Tangente"],
                    competencies=["Calculer", "Modéliser"]
                ),
                Chapter(
                    number=6,
                    title="Probabilités",
                    objectives=["Calculer des probabilités simples", "Comprendre l'équiprobabilité"],
                    prerequisites=["Fractions", "Pourcentages"],
                    duration_hours=10,
                    key_concepts=["Probabilité", "Équiprobabilité", "Événements"],
                    competencies=["Modéliser", "Calculer"]
                ),
                Chapter(
                    number=7,
                    title="Géométrie dans l'espace",
                    objectives=["Calculer des volumes", "Représenter des solides"],
                    prerequisites=["Géométrie plane", "Formules d'aires"],
                    duration_hours=10,
                    key_concepts=["Sphère", "Cône", "Pyramide", "Volumes"],
                    competencies=["Représenter", "Calculer"]
                )
            ]
        else:  # Fallback pour les autres niveaux
            chapters = [
                Chapter(
                    number=1,
                    title="Introduction aux mathématiques",
                    objectives=["Se familiariser avec les concepts de base"],
                    prerequisites=["Connaissances du niveau précédent"],
                    duration_hours=10,
                    key_concepts=["Concepts de base", "Méthodes fondamentales"],
                    competencies=["Calculer", "Raisonner"]
                ),
                Chapter(
                    number=2,
                    title="Approfondissement",
                    objectives=["Développer les compétences mathématiques"],
                    prerequisites=["Introduction"],
                    duration_hours=12,
                    key_concepts=["Approfondissement", "Applications"],
                    competencies=["Modéliser", "Représenter"]
                )
            ]
        
        return PedagogicalProgram(
            level=level,
            total_sessions=120,
            chapters=chapters,
            general_objectives=["Développer le raisonnement mathématique", "Acquérir les compétences du programme"],
            evaluation_criteria={"competences": ["Chercher", "Modéliser", "Représenter", "Calculer", "Raisonner", "Communiquer"]}
        )

    # ============= NOUVELLES MÉTHODES À IMPLÉMENTER =============
    
    def _create_user_request_readme(self, course_config: CourseConfig, structured_data: Dict[str, Any]) -> str:
        """
        TODO: Créer un README concis de la demande utilisateur
        
        CONTENU À INCLURE:
        - Niveau scolaire et effectifs
        - Spécificités pédagogiques demandées
        - Contraintes horaires et organisationnelles
        - Objectifs généraux souhaités
        - Contexte de l'établissement si fourni
        
        Ce README sera envoyé au ResourceFinder pour trouver les ressources
        officielles appropriées.
        """
        # TODO: Logique de création du README concis
        return f"""
        DEMANDE DE CRÉATION DE PROGRAMME - {course_config.level}
        
        Niveau: {course_config.level}
        Nombre de séances annuelles: {course_config.sessions_per_year}
        Objectifs généraux: {structured_data.get('objectives', ['À définir'])}
        Spécificités: {structured_data.get('specifics', ['Standard'])}
        """
    
    async def _analyze_official_resources(self, resources: List, course_config: CourseConfig) -> Dict[str, Any]:
        """
        TODO: Analyser les ressources officielles pour extraire le programme
        
        ANALYSE À EFFECTUER:
        1. Extraction des objectifs officiels du BO
        2. Identification des compétences attendues
        3. Analyse de la progression recommandée
        4. Extraction des attendus de fin de cycle
        5. Synthèse des orientations didactiques
        
        SOURCES À PRIORISER:
        - Programmes officiels (BO)
        - Documents d'accompagnement Eduscol
        - Ressources pour faire la classe
        """
        # TODO: Logique d'analyse des ressources officielles
        return {"program": "TODO: Analyse à implémenter"}
    
    async def _create_planning_from_resources(self, official_program: Dict[str, Any], 
                                            course_config: CourseConfig) -> Dict[str, Any]:
        """
        TODO: Créer la planification basée sur les ressources officielles
        
        PROCESSUS:
        1. Structurer la progression selon les recommandations officielles
        2. Adapter les durées aux contraintes horaires
        3. Intégrer les compétences transversales
        4. Planifier les évaluations selon les cycles
        5. Respecter les attendus de fin de cycle
        """
        # TODO: Logique de création de planification
        return {"planning": "TODO: Planification à implémenter"}
    
    async def _generate_detailed_chapter_readmes(self, program: PedagogicalProgram) -> None:
        """
        TODO: Générer des READMEs détaillés pour chaque chapitre
        
        PROCESSUS POUR CHAQUE CHAPITRE:
        1. Nouvelle requête ResourceFinder spécialisée sur le chapitre
        2. Analyse didactique approfondie via Claude
        3. Étude des recherches récentes en didactique
        4. Rédaction README détaillé avec:
           - Analyse du programme officiel pour ce chapitre
           - Logique pédagogique et progression interne
           - Difficultés connues et erreurs typiques
           - Suggestions méthodologiques
           - Liens avec autres chapitres
           - Ressources complémentaires
        
        Ce README détaillé sera utilisé par ContentGenerator.
        """
        for chapter in program.chapters:
            try:
                # TODO: Requête ResourceFinder spécialisée
                # chapter_resources = await self.resource_finder.find_resources(ResourceQuery(
                #     query_text=f"Didactique {chapter.title} {program.level}",
                #     level=program.level,
                #     subject="mathématiques", 
                #     specific_topics=[chapter.title],
                #     resource_types=["pdf", "html"],
                #     max_results=10
                # ))
                
                # TODO: Analyse didactique approfondie
                # detailed_readme = await self._create_detailed_chapter_readme(
                #     chapter, chapter_resources, program.level
                # )
                
                # TODO: Sauvegarde du README détaillé
                logger.info(f"TODO: Générer README détaillé pour {chapter.title}")
                
            except Exception as e:
                logger.error(f"Erreur génération README chapitre {chapter.title}: {e}")
    
    async def _create_detailed_chapter_readme(self, chapter: Chapter, resources: List,
                                            level: str) -> str:
        """
        TODO: Créer un README détaillé pour un chapitre spécifique
        
        CONTENU DU README DÉTAILLÉ:
        
        # [TITRE DU CHAPITRE]
        
        ## Analyse du programme officiel
        [Extraction précise des attendus du BO pour ce chapitre]
        
        ## Logique pédagogique et progression
        [Analyse de la recherche didactique récente]
        [Progression recommandée étape par étape]
        
        ## Difficultés connues et erreurs typiques
        [Obstacles didactiques identifiés par la recherche]
        [Erreurs fréquentes des élèves et remédiations]
        
        ## Suggestions méthodologiques  
        [Approches pédagogiques efficaces]
        [Activités et situations-problèmes recommandées]
        
        ## Liens avec autres chapitres
        [Prérequis détaillés et liens avec la suite]
        
        ## Ressources complémentaires
        [Liens vers ressources trouvées par ResourceFinder]
        """
        
        # TODO: Analyse approfondie via Claude avec les ressources
        prompt = f"""
        Analyse didactique approfondie pour le chapitre "{chapter.title}" en {level}.
        
        Ressources disponibles: [TODO: Intégrer ressources]
        
        Rédige un README détaillé incluant:
        1. Analyse précise du programme officiel
        2. Logique pédagogique basée sur la recherche
        3. Difficultés connues et erreurs typiques
        4. Suggestions méthodologiques concrètes
        5. Progression étape par étape
        6. Liens avec autres chapitres
        
        Base-toi sur les recherches en didactique des mathématiques.
        """
        
        # TODO: Appel Claude avec prompt enrichi des ressources
        return "TODO: README détaillé à générer"
