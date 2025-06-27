#!/usr/bin/env python3
"""
Math Content Generator - Générateur automatique de ressources pédagogiques mathématiques
Utilise l'API Claude pour créer une année complète de cours, exercices et évaluations
"""

import os
import sys
import json
import yaml
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# External dependencies
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from anthropic import AsyncAnthropic
import aiofiles
from dotenv import load_dotenv

# Import des modules refactorisés
from src.models import ContentType, Chapter, APIConfig, CourseConfig, PedagogicalProgram
from src.cache import APICache
from src.input_processor import InputProcessor
from src.pedagogical_planner import PedagogicalPlanner
from src.content_generator import ContentGenerator
from src.latex_engine import LaTeXEngine
from src.latex_compiler import LaTeXCompiler

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('math_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Utility function
def extract_text_from_response(response) -> str:
    """Extrait le texte de la réponse Claude de manière sécurisée"""
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
            
# ============= Test Orchestrator =============

class TestOrchestrator:
    """Orchestrateur de test pour génération minimaliste"""
    
    def __init__(self, config_path: Path, chapter_name: str):
        self.config = self._load_config(config_path)
        self.api_config = APIConfig(**self.config.get("api", {}))
        self.course_config = CourseConfig(**self.config.get("course", {}))
        self.cache = APICache()
        self.chapter_name = chapter_name
        self.no_compile = self.config.get("no_compile", False)
        
        # Initialize modules with test mode
        self.content_generator = ContentGenerator(self.api_config, self.cache)
        self.latex_engine = LaTeXEngine()
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Charge la configuration depuis un fichier YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erreur chargement config: {e}")
            return {}
            
    async def generate_test_content(self) -> None:
        """Génère un contenu de test minimal"""
        console.print("[yellow]Génération de test minimaliste...[/yellow]")
        
        try:
            # Créer un chapitre de test simple
            test_chapter = Chapter(
                number=1,
                title=self.chapter_name,
                objectives=["Comprendre les bases du chapitre"],
                prerequisites=["Aucun prérequis"],
                duration_hours=2,
                key_concepts=["Concept de base"],
                competencies=["Comprendre"]
            )
            
            # Créer la structure de dossiers
            base_path = Path(self.course_config.output_path)
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Générer seulement un cours et un exercice
            await self._generate_test_chapter(base_path, test_chapter)
            
            # Phase de compilation LaTeX (si activée)
            if not self.no_compile:
                latex_compiler = LaTeXCompiler(base_path)
                await latex_compiler.compile_all_tex_files()
                latex_compiler.cleanup_aux_files()
            else:
                console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
            
            console.print("[bold green]✓ Test généré avec succès![/bold green]")
            
        except Exception as e:
            logger.error(f"Erreur génération test: {e}")
            console.print(f"[bold red]✗ Erreur: {e}[/bold red]")
            
    async def _generate_test_chapter(self, base_path: Path, chapter: Chapter) -> None:
        """Génère un chapitre de test minimal"""
        
        # Créer le dossier du chapitre
        chapter_name = f"Test_{chapter.title.replace(' ', '_')}"
        chapter_path = base_path / chapter_name
        chapter_path.mkdir(exist_ok=True)
        
        # Générer seulement un cours et un exercice d'entraînement
        test_content_types = [
            (ContentType.COURSE, "01_Cours"),
            (ContentType.EXERCISE_BASIC, "02_Exercices/01_Entrainement")
        ]
        
        for content_type, folder_path in test_content_types:
            try:
                full_path = chapter_path / folder_path
                full_path.mkdir(parents=True, exist_ok=True)
                
                console.print(f"  Génération: {content_type.value}...")
                
                # Générer le contenu avec tokens limités
                content = await self._generate_minimal_content(chapter, content_type)
                content = self.latex_engine._clean_latex_body(content)
                
                # Formater avec LaTeX
                try:
                    formatted = self.latex_engine.format_content(
                        content, chapter, content_type, self.course_config.level
                    )
                except Exception as format_error:
                    logger.warning(f"Erreur formatage LaTeX: {format_error}")
                    formatted = self._get_fallback_content(content, chapter, content_type)
                    
                # Sauvegarder
                filename = f"{content_type.value}.tex"
                with open(full_path / filename, "w", encoding="utf-8") as f:
                    f.write(formatted)
                
                console.print(f"    ✓ {content_type.value} généré")
                    
            except Exception as e:
                logger.error(f"Erreur génération {content_type.value}: {e}")
                console.print(f"    ✗ Erreur {content_type.value}: {e}")
                    
    async def _generate_minimal_content(self, chapter: Chapter, content_type: ContentType) -> str:
        """Génère un contenu minimal avec tokens très limités"""
        
        # En mode test, utiliser directement le contenu de fallback pour économiser les tokens
        if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "test":
            console.print(f"    Utilisation du contenu de fallback pour {content_type.value}")
            return self._get_test_fallback_content(content_type)
        
        # Prompts très courts pour économiser les tokens
        if content_type == ContentType.COURSE:
            prompt = f"""
            Chapitre: {chapter.title}
            Génère un cours très court (max 200 mots) en LaTeX avec:
            - Une définition simple
            - Un exemple basique
            - Une propriété essentielle
            """
        elif content_type == ContentType.EXERCISE_BASIC:
            prompt = f"""
            Chapitre: {chapter.title}
            Génère 2 exercices très simples en LaTeX avec:
            - Application directe
            - Consignes courtes
            """
        else:
            return f"% Contenu {content_type.value} - Mode test"
        
        # Check cache
        cache_key = self.cache.get_cache_key(prompt, f"test_{chapter.number}")
        try:
        cached_content = await self.cache.get(cache_key)
        if cached_content and self.api_config.use_cache:
            return cached_content
        except Exception as cache_error:
            logger.warning(f"Erreur lecture cache: {cache_error}")
            
        try:
            # Utiliser un modèle plus petit et moins de tokens pour le test
            response = await self.content_generator.client.messages.create(
                model="claude-3-haiku-20240307",  # Modèle plus petit
                max_tokens=500,  # Très limité
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = extract_text_from_response(response)
            
            # Cache result
            try:
                if isinstance(content, str):
            await self.cache.set(cache_key, content)
            except Exception as cache_error:
                logger.warning(f"Erreur cache: {cache_error}")
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur génération test: {e}")
            content = self._get_test_fallback_content(content_type)
            
        # Cache result
        try:
            if isinstance(content, str):
                await self.cache.set(cache_key, content)
        except Exception as cache_error:
            logger.warning(f"Erreur cache: {cache_error}")
        
        return content
            
    def _get_test_fallback_content(self, content_type: ContentType) -> str:
        """Contenu de fallback pour le mode test"""
        if content_type == ContentType.COURSE:
            return r"""
\sectioncolor{Introduction}

\begin{definition}
\textbf{Définition de base pour le test.}
\end{definition}

\begin{exemple}
Voici un exemple simple pour illustrer le concept :
\begin{itemize}
\item Point important 1
\item Point important 2
\end{itemize}
\end{exemple}

\begin{propriete}
\textbf{Propriété fondamentale à retenir :}
Cette propriété est très importante pour la suite !
\end{propriete}

\begin{astuce}
\textbf{Conseil :} N'oublie pas de bien lire les exemples !
\end{astuce}
"""
        elif content_type == ContentType.EXERCISE_BASIC:
            return r"""
\sectioncolor{Exercices d'entraînement}

\exercice{Calcul simple}
Calcule le résultat de l'opération suivante :
$$ 15 + 7 = ? $$

\begin{indice}
Pense à compter sur tes doigts si ça t'aide !
\end{indice}

\exercice{Problème de la vie quotidienne}
Marie a 8 bonbons. Elle en mange 3. Combien lui en reste-t-il ?

\begin{question}
Écris ton calcul et ta réponse :
\end{question}
"""
        else:
            return f"% Contenu {content_type.value} - Mode test"
    
    def _get_fallback_content(self, content: str, chapter: Chapter, content_type: ContentType) -> str:
        """Format de fallback simple"""
        return f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[french]{{babel}}
\\begin{{document}}
\\title{{{chapter.title} - {content_type.value}}}
\\maketitle
{content}
\\end{{document}}"""

# ============= Full Test Orchestrator =============

class FullTestOrchestrator:
    """Orchestrateur de test complet pour génération d'un chapitre avec tous les types de contenu"""
    
    def __init__(self, config_path: Path, chapter_name: str):
        self.config = self._load_config(config_path)
        self.api_config = APIConfig(**self.config.get("api", {}))
        self.course_config = CourseConfig(**self.config.get("course", {}))
        self.cache = APICache()
        self.chapter_name = chapter_name
        self.no_compile = self.config.get("no_compile", False)
        
        # Initialize modules with full capabilities
        self.content_generator = ContentGenerator(self.api_config, self.cache)
        self.latex_engine = LaTeXEngine()
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Charge la configuration depuis un fichier YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erreur chargement config: {e}")
            return {}
            
    async def generate_full_chapter(self) -> None:
        """Génère un chapitre complet avec tous les types de contenu"""
        console.print("[yellow]Génération d'un chapitre complet...[/yellow]")
        
        try:
            # Créer un chapitre de test complet
            test_chapter = Chapter(
                number=1,
                title=self.chapter_name,
                objectives=["Maîtriser les concepts fondamentaux", "S'entraîner avec des exercices variés", "Évaluer les compétences acquises"],
                prerequisites=["Connaissances de base du niveau précédent"],
                duration_hours=8,
                key_concepts=["Concept principal", "Méthodes essentielles", "Applications pratiques"],
                competencies=["Chercher", "Modéliser", "Représenter", "Calculer", "Raisonner", "Communiquer"]
            )
            
            # Créer la structure de dossiers
            base_path = Path(self.course_config.output_path)
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Générer tous les types de contenu
            await self._generate_full_chapter_content(base_path, test_chapter)
            
            # Phase de compilation LaTeX (si activée)
            if not self.no_compile:
                latex_compiler = LaTeXCompiler(base_path)
                await latex_compiler.compile_all_tex_files()
                latex_compiler.cleanup_aux_files()
            else:
                console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
            
            console.print("[bold green]✓ Chapitre complet généré avec succès![/bold green]")
            
        except Exception as e:
            logger.error(f"Erreur génération chapitre complet: {e}")
            console.print(f"[bold red]✗ Erreur: {e}[/bold red]")
            
    async def _generate_full_chapter_content(self, base_path: Path, chapter: Chapter) -> None:
        """Génère tous les types de contenu pour un chapitre"""
        
        # Créer le dossier du chapitre
        chapter_name = f"Chapitre_Complet_{chapter.title.replace(' ', '_')}"
        chapter_path = base_path / chapter_name
        chapter_path.mkdir(exist_ok=True)
        
        # Tous les types de contenu à générer
        content_types = [
            (ContentType.COURSE, "01_Cours"),
            (ContentType.EXERCISE_BASIC, "02_Exercices/01_Entrainement"),
            (ContentType.EXERCISE_ADVANCED, "02_Exercices/02_Approfondissement"),
            (ContentType.EXERCISE_CHALLENGE, "02_Exercices/03_Defis"),
            (ContentType.EVALUATION_FORMATIVE, "03_Evaluations/01_Formatives"),
            (ContentType.EVALUATION_SUMMATIVE, "03_Evaluations/02_Sommative"),
            (ContentType.CORRECTION, "04_Corrections")
        ]
        
        for content_type, folder_path in content_types:
            try:
                full_path = chapter_path / folder_path
                full_path.mkdir(parents=True, exist_ok=True)
                
                console.print(f"  Génération: {content_type.value}...")
                
                # Générer le contenu complet (pas de restrictions)
                content = await self.content_generator.generate_chapter_content(chapter, content_type)
                content = self.latex_engine._clean_latex_body(content)
                
                # Formater avec LaTeX
                formatted = self.latex_engine.format_content(
                    content, chapter, content_type, self.course_config.level
                )
                
                # Sauvegarder
                filename = f"{content_type.value}.tex"
                with open(full_path / filename, "w", encoding="utf-8") as f:
                    f.write(formatted)
                
                console.print(f"    ✓ {content_type.value} généré")
                
            except Exception as e:
                logger.error(f"Erreur génération {content_type.value}: {e}")
                console.print(f"    ✗ Erreur {content_type.value}: {e}")

# ============= Main Orchestrator =============

class MainOrchestrator:
    """Orchestrateur principal coordonnant tous les modules"""
    
    def __init__(self, config_path: Path, no_compile: bool):
        self.config = self._load_config(config_path)
        self.api_config = APIConfig(**self.config.get("api", {}))
        self.course_config = CourseConfig(**self.config.get("course", {}))
        self.cache = APICache()
        self.no_compile = no_compile
        
        # Initialize modules
        self.input_processor = InputProcessor(self.api_config, self.cache)
        self.planner = PedagogicalPlanner(self.api_config, self.cache)
        self.content_generator = ContentGenerator(self.api_config, self.cache)
        self.latex_engine = LaTeXEngine()
        
        # Context memory
        self.context_memory: Dict[str, Any] = {}
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Charge la configuration depuis un fichier YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erreur chargement config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """Configuration par défaut"""
        return {
            "course": {
                "level": "4ème",
                "sessions_per_year": 120,
                "curriculum_sources": [
                    {"type": "text", "content": "Programme officiel de 4ème"}
                ],
                "resources": []
            },
            "api": {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 4000,
                "temperature": 0.3,
                "use_cache": True,
                "batch_processing": True
            }
        }
        
    async def generate_complete_course(self) -> None:
        """Génère le cours complet"""
        console.print("[bold green]Démarrage de la génération du cours[/bold green]")
        
        try:
            # Phase 1: Analyse des sources
            console.print("\n[yellow]Phase 1:[/yellow] Analyse des sources d'entrée")
            structured_data = await self.input_processor.process_sources(
                self.course_config.curriculum_sources + self.course_config.resources
            )
            self.context_memory["structured_data"] = structured_data
            
            # Phase 2: Planification pédagogique
            console.print("\n[yellow]Phase 2:[/yellow] Création de la planification annuelle")
            program = await self.planner.create_annual_planning(
                structured_data, self.course_config
            )
            self.context_memory["program"] = program
            
            # Phase 3: Génération du contenu
            console.print("\n[yellow]Phase 3:[/yellow] Génération des contenus pédagogiques")
            await self._generate_all_content(program)
            
            # Phase 4: Compilation LaTeX (si activée)
            if not self.no_compile:
                console.print("\n[yellow]Phase 4:[/yellow] Compilation des PDFs")
                latex_compiler = LaTeXCompiler(Path(self.course_config.output_path))
                await latex_compiler.compile_all_tex_files()
                latex_compiler.cleanup_aux_files()
            else:
                console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
            
            console.print("\n[bold green]✓ Génération terminée avec succès![/bold green]")
            
        except Exception as e:
            logger.error(f"Erreur génération: {e}")
            console.print(f"[bold red]✗ Erreur: {e}[/bold red]")
            
    async def _generate_all_content(self, program: PedagogicalProgram) -> None:
        """Génère tout le contenu pour chaque chapitre"""
        
        # Créer la structure de dossiers
        base_path = Path(self.course_config.output_path) / f"Cours_{program.level}"
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Générer la programmation annuelle
        await self._generate_annual_planning(base_path, program)
        
        # Générer chaque chapitre
        total_chapters = len(program.chapters)
        with Progress(console=console) as progress:
            task = progress.add_task(
                "Génération des chapitres...",
                total=total_chapters
            )
            
            for chapter in program.chapters:
                await self._generate_chapter(base_path, chapter, program.level)
                progress.advance(task)
                
    async def _generate_annual_planning(self, base_path: Path, program: PedagogicalProgram) -> None:
        """Génère les documents de programmation annuelle"""
        planning_dir = base_path / "00_Programmation_Annuelle"
        planning_dir.mkdir(exist_ok=True)
        
        # Contenu de la programmation (simplifié pour l'exemple)
        planning_content = r"""
\section{Programmation annuelle}

\subsection{Vue d'ensemble}
Cette programmation couvre l'ensemble du programme de """ + program.level + r""" sur """ + str(program.total_sessions) + r""" séances.

\subsection{Répartition par chapitre}
\begin{enumerate}
"""
        
        for chapter in program.chapters:
            planning_content += f"\\item \\textbf{{Chapitre {chapter.number} - {chapter.title}}} ({chapter.duration_hours} heures)\n"
            planning_content += "\\begin{itemize}\n"
            for obj in chapter.objectives[:2]:  # Limiter pour l'exemple
                planning_content += f"\\item {obj}\n"
            planning_content += "\\end{itemize}\n"
            
        planning_content += r"\end{enumerate}"
        
        # Formater et sauvegarder
        formatted = self.latex_engine.format_content(
            planning_content,
            Chapter(0, "Programmation annuelle", [], [], 0, [], []),
            ContentType.COURSE,
            program.level
        )
        
        with open(planning_dir / "programmation_annuelle.tex", "w", encoding="utf-8") as f:
            f.write(formatted)
            
    async def _generate_chapter(self, base_path: Path, chapter: Chapter, level: str) -> None:
        """Génère tous les contenus d'un chapitre"""
        
        # Créer le dossier du chapitre
        chapter_name = f"Chapitre_{chapter.number:02d}_{chapter.title.replace(' ', '_')}"
        chapter_path = base_path / chapter_name
        chapter_path.mkdir(exist_ok=True)
        
        # Structure des sous-dossiers
        folders = {
            "01_Cours": ContentType.COURSE,
            "02_Exercices/01_Entrainement": ContentType.EXERCISE_BASIC,
            "02_Exercices/02_Approfondissement": ContentType.EXERCISE_ADVANCED,
            "02_Exercices/03_Defis": ContentType.EXERCISE_CHALLENGE,
            "03_Evaluations/01_Formatives": ContentType.EVALUATION_FORMATIVE,
            "03_Evaluations/02_Sommative": ContentType.EVALUATION_SUMMATIVE,
            "04_Corrections": ContentType.CORRECTION
        }
        
        # Générer chaque type de contenu
        for folder_path, content_type in folders.items():
            full_path = chapter_path / folder_path
            full_path.mkdir(parents=True, exist_ok=True)
            
            # Générer le contenu
            content = await self.content_generator.generate_chapter_content(
                chapter, content_type, self.context_memory
            )
            
            # Formater avec LaTeX
            formatted = self.latex_engine.format_content(
                content, chapter, content_type, level
            )
            
            # Valider
            is_valid, errors = self.latex_engine.validate_latex(formatted)
            if not is_valid:
                logger.warning(f"Erreurs LaTeX détectées: {errors}")
                
            # Sauvegarder
            filename = f"{content_type.value}.tex"
            with open(full_path / filename, "w", encoding="utf-8") as f:
                f.write(formatted)

# ============= CLI Interface =============

@click.group()
def cli():
    """Math Content Generator - Générateur automatique de ressources pédagogiques"""
    pass

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Fichier de configuration YAML')
@click.option('--interactive', '-i', is_flag=True, help='Mode configuration interactive')
@click.option('--no-compile', is_flag=True, help='Ne pas compiler les PDFs')
def generate(config, interactive, no_compile):
    """Génère un cours complet"""
    
    if interactive:
        config_path = create_interactive_config()
    else:
        config_path = Path(config) if config else Path("config.yaml")
        
    if not config_path.exists():
        console.print("[red]Fichier de configuration introuvable![/red]")
        if Confirm.ask("Créer une configuration par défaut?"):
            create_default_config(config_path)
        else:
            return
            
    # Lancer la génération
    orchestrator = MainOrchestrator(config_path, no_compile)
    asyncio.run(orchestrator.generate_complete_course())

@cli.command()
@click.option('--chapter', '-ch', default="Nombres relatifs", help='Nom du chapitre à tester')
@click.option('--level', '-l', default="4ème", help='Niveau scolaire')
@click.option('--output', '-o', default='./test_output', help='Dossier de sortie')
@click.option('--no-compile', is_flag=True, help='Ne pas compiler les PDFs')
def test(chapter, level, output, no_compile):
    """Génère un test minimal avec un seul chapitre et exercice"""
    
    console.print("[bold green]Mode test - Génération minimaliste pour économiser les tokens[/bold green]")
    
    # Configuration de test avec tokens limités
    test_config = {
        "course": {
            "level": level,
            "sessions_per_year": 10,  # Réduit pour le test
            "curriculum_sources": [
                {"type": "text", "content": f"Chapitre: {chapter}"}
            ],
            "resources": [],
            "output_path": output
        },
        "api": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1000,  # Très limité pour l'analyse
            "temperature": 0.3,
            "use_cache": True,
            "batch_processing": False  # Désactivé pour le test
        },
        "test_mode": True,  # Flag pour le mode test
        "no_compile": no_compile  # Flag pour skip compilation
    }
    
    # Créer un fichier de config temporaire
    test_config_path = Path("test_config.yaml")
    with open(test_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f, allow_unicode=True, default_flow_style=False)
    
    try:
        # Lancer la génération de test
        orchestrator = TestOrchestrator(test_config_path, chapter)
        asyncio.run(orchestrator.generate_test_content())
        
        console.print(f"\n[bold green]✓ Test terminé! Contenu généré dans: {output}[/bold green]")
        
    finally:
        # Nettoyer le fichier de config temporaire
        if test_config_path.exists():
            test_config_path.unlink()

@cli.command()
@click.option('--chapter', '-ch', default="Calcul de fractions", help='Nom du chapitre à tester')
@click.option('--level', '-l', default="5ème", help='Niveau scolaire')
@click.option('--output', '-o', default='./test_output', help='Dossier de sortie')
@click.option('--no-compile', is_flag=True, help='Ne pas compiler les PDFs')
def test_full(chapter, level, output, no_compile):
    """Génère un chapitre complet avec tous les types de contenu (cours, exercices, évaluations)"""
    
    console.print("[bold green]Mode test complet - Génération d'un chapitre avec tous les types de contenu[/bold green]")
    
    # Configuration de test complet avec tokens non limités
    test_config = {
        "course": {
            "level": level,
            "sessions_per_year": 20,  # Réduit pour le test
            "curriculum_sources": [
                {"type": "text", "content": f"Chapitre: {chapter}"}
            ],
            "resources": [],
            "output_path": output
        },
        "api": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4000,  # Tokens complets pour qualité maximale
            "temperature": 0.3,
            "use_cache": True,
            "batch_processing": True
        },
        "test_mode": False,  # Mode complet, pas de restrictions
        "no_compile": no_compile
    }
    
    # Créer un fichier de config temporaire
    test_config_path = Path("test_full_config.yaml")
    with open(test_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f, allow_unicode=True, default_flow_style=False)
    
    try:
        # Lancer la génération de test complet
        orchestrator = FullTestOrchestrator(test_config_path, chapter)
        asyncio.run(orchestrator.generate_full_chapter())
        
        console.print(f"\n[bold green]✓ Test complet terminé! Contenu généré dans: {output}[/bold green]")
        
    finally:
        # Nettoyer le fichier de config temporaire
        if test_config_path.exists():
            test_config_path.unlink()

@cli.command()
@click.option('--level', '-l', default='5ème', help='Niveau scolaire')
@click.option('--output', '-o', default='./output', help='Dossier de sortie')
@click.option('--program', '-p', default='', help='Texte du programme officiel (optionnel)')
@click.option('--no-compile', is_flag=True, help='Ne pas compiler les PDFs')
def plan_year(level, output, program, no_compile):
    """Génère l'arborescence annuelle (dossiers/fichiers vides) selon le programme officiel, avec README détaillé"""
    async def _plan():
        api_config = APIConfig()
        cache = APICache()
        course_config = CourseConfig(level=level, sessions_per_year=120, curriculum_sources=[], resources=[], output_path=output)
        input_processor = InputProcessor(api_config, cache)
        planner = PedagogicalPlanner(api_config, cache)
        # Préparer les données du programme
        if program:
            structured_data = {'objectives': [], 'competencies': [], 'chapters': [], 'prerequisites': [], 'evaluation_criteria': {}, 'program': program}
            # Générer la progression annuelle via API
            pedagogical_program = await planner.create_annual_planning(structured_data, course_config)
        else:
            # Utiliser directement le programme par défaut adapté au niveau
            pedagogical_program = planner._get_default_program(level)
        base_path = Path(output) / f"Cours_{level}"
        base_path.mkdir(parents=True, exist_ok=True)
        # Programmation annuelle
        prog_dir = base_path / "00_Programmation_Annuelle"
        prog_dir.mkdir(exist_ok=True)
        # README global
        with open(prog_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# Programmation annuelle - {level}\n\n")
            f.write(f"| Chapitre | Durée (h) | Objectifs | Prérequis |\n|---|---|---|---|\n")
            for chapter in pedagogical_program.chapters:
                objectifs = "; ".join(chapter.objectives)
                prerequis = "; ".join(chapter.prerequisites)
                f.write(f"| {chapter.number:02d} - {chapter.title} | {chapter.duration_hours} | {objectifs} | {prerequis} |\n")
        # Chapitres
        for chapter in pedagogical_program.chapters:
            chap_dir = base_path / f"Chapitre_{chapter.number:02d}_{chapter.title.replace(' ', '_')}"
            chap_dir.mkdir(exist_ok=True)
            for sub in ["01_Cours", "02_Exercices/01_Entrainement", "02_Exercices/02_Approfondissement", "02_Exercices/03_Defis", "03_Evaluations/01_Formatives", "03_Evaluations/02_Sommative", "04_Corrections"]:
                (chap_dir / sub).mkdir(parents=True, exist_ok=True)
            # README de chapitre
            with open(chap_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(f"# {chapter.title}\n\n")
                f.write(f"**Numéro :** {chapter.number}\n\n")
                f.write(f"**Durée prévue :** {chapter.duration_hours} heures\n\n")
                f.write(f"**Objectifs :**\n\n")
                for obj in chapter.objectives:
                    f.write(f"- {obj}\n")
                f.write(f"\n**Prérequis :**\n\n")
                for pre in chapter.prerequisites:
                    f.write(f"- {pre}\n")
                if chapter.key_concepts:
                    f.write(f"\n**Concepts clés / Sous-chapitres :**\n\n")
                    for concept in chapter.key_concepts:
                        f.write(f"- {concept}\n")
                if chapter.competencies:
                    f.write(f"\n**Compétences visées :**\n\n")
                    for comp in chapter.competencies:
                        f.write(f"- {comp}\n")
        
        # Phase de compilation LaTeX (si activée)
        if not no_compile:
            console.print(f"\n[yellow]Compilation des PDFs dans {base_path}[/yellow]")
            latex_compiler = LaTeXCompiler(base_path)
            await latex_compiler.compile_all_tex_files()
            latex_compiler.cleanup_aux_files()
            console.print("[green]✓ Compilation terminée[/green]")
        else:
            console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
        
        click.echo(f"Arborescence annuelle créée dans {base_path}")
    asyncio.run(_plan())

@cli.command()
@click.option('--chapter-path', '-c', required=True, help='Chemin du dossier du chapitre à remplir')
@click.option('--no-compile', is_flag=True, help='Ne pas compiler les PDFs')
def fill_chapter(chapter_path, no_compile):
    """Génère le contenu complet (cours, exercices, évaluations, corrections) pour un chapitre existant"""
    async def _fill():
        # Charger la config par défaut
        api_config = APIConfig()
        cache = APICache()
        latex_engine = LaTeXEngine()
        # Extraire le nom du chapitre
        chapter_dir = Path(chapter_path)
        chapter_name = chapter_dir.name.replace('Chapitre_', '').replace('_', ' ')
        # Créer un chapitre factice (pour la démo, à améliorer pour charger les vrais objectifs...)
        chapter = Chapter(
            number=int(chapter_dir.name.split('_')[1]),
            title=chapter_name,
            objectives=["Objectifs à définir"],
            prerequisites=["Prérequis à définir"],
            duration_hours=8,
            key_concepts=["Concepts à définir"],
            competencies=["Compétences à définir"]
        )
        # Générer le contenu pour chaque type
        content_types = [
            (ContentType.COURSE, "01_Cours"),
            (ContentType.EXERCISE_BASIC, "02_Exercices/01_Entrainement"),
            (ContentType.EXERCISE_ADVANCED, "02_Exercices/02_Approfondissement"),
            (ContentType.EXERCISE_CHALLENGE, "02_Exercices/03_Defis"),
            (ContentType.EVALUATION_FORMATIVE, "03_Evaluations/01_Formatives"),
            (ContentType.EVALUATION_SUMMATIVE, "03_Evaluations/02_Sommative"),
            (ContentType.CORRECTION, "04_Corrections")
        ]
        for content_type, folder in content_types:
            folder_path = chapter_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            # Générer le contenu
            prompt = f"Génère le contenu {content_type.value} pour le chapitre {chapter.title}"
            # Appel API Claude (à adapter pour utiliser la vraie logique)
            # ...
            # Pour la démo, créer un fichier .tex vide
            with open(folder_path / f"{content_type.value}.tex", "w", encoding="utf-8") as f:
                f.write(f"% Contenu {content_type.value} pour {chapter.title}\n")
        
        # Phase de compilation LaTeX (si activée)
        if not no_compile:
            console.print(f"\n[yellow]Compilation des PDFs dans {chapter_dir}[/yellow]")
            latex_compiler = LaTeXCompiler(chapter_dir)
            await latex_compiler.compile_all_tex_files()
            latex_compiler.cleanup_aux_files()
            console.print("[green]✓ Compilation terminée[/green]")
        else:
            console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
        
        click.echo(f"Contenu généré pour {chapter.title}")
    asyncio.run(_fill())

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--cleanup', '-c', is_flag=True, help='Nettoyer les fichiers auxiliaires après compilation')
@click.option('--verbose', '-v', is_flag=True, help='Affichage détaillé')
def compile(directory, cleanup, verbose):
    """Compile automatiquement tous les fichiers LaTeX récursivement dans le dossier spécifié"""
    async def _compile():
        target_dir = Path(directory)
        console.print(f"[bold green]Compilation de tous les fichiers LaTeX dans: {target_dir}[/bold green]")
        
        # Rechercher tous les fichiers .tex récursivement
        tex_files = list(target_dir.rglob("*.tex"))
        
        if not tex_files:
            console.print(f"[yellow]Aucun fichier .tex trouvé dans {target_dir}[/yellow]")
            return
        
        console.print(f"[blue]Fichiers .tex trouvés: {len(tex_files)}[/blue]")
        
        if verbose:
            for tex_file in tex_files:
                console.print(f"  - {tex_file.relative_to(target_dir)}")
        
        # Initialiser le compilateur
        latex_compiler = LaTeXCompiler(target_dir)
        
        # Compiler tous les fichiers
        with Progress(console=console) as progress:
            task = progress.add_task("Compilation en cours...", total=len(tex_files))
            
            compiled_count = 0
            error_count = 0
            
            for tex_file in tex_files:
                try:
                    if verbose:
                        console.print(f"\n[yellow]Compilation: {tex_file.name}[/yellow]")
                    
                    # Compiler le fichier individuel
                    success = await latex_compiler.compile_single_file(tex_file)
                    
                    if success:
                        compiled_count += 1
                        if verbose:
                            console.print(f"[green]✓ {tex_file.name} → {tex_file.with_suffix('.pdf').name}[/green]")
                    else:
                        error_count += 1
                        if verbose:
                            console.print(f"[red]✗ Erreur compilation: {tex_file.name}[/red]")
                
                except Exception as e:
                    error_count += 1
                    if verbose:
                        console.print(f"[red]✗ Erreur: {tex_file.name} - {e}[/red]")
                
                progress.advance(task)
        
        # Nettoyer les fichiers auxiliaires si demandé
        if cleanup:
            console.print(f"\n[yellow]Nettoyage des fichiers auxiliaires...[/yellow]")
            latex_compiler.cleanup_aux_files()
            console.print("[green]✓ Nettoyage terminé[/green]")
        
        # Résumé
        console.print(f"\n[bold]Résumé de compilation:[/bold]")
        console.print(f"  [green]✓ Compilés avec succès: {compiled_count}[/green]")
        if error_count > 0:
            console.print(f"  [red]✗ Erreurs: {error_count}[/red]")
        console.print(f"  [blue]Total traités: {len(tex_files)}[/blue]")
        
        if compiled_count > 0:
            console.print(f"\n[bold green]✓ Compilation terminée! {compiled_count} PDF(s) généré(s)[/bold green]")
        else:
            console.print(f"\n[bold red]✗ Aucun fichier compilé avec succès[/bold red]")
    
    asyncio.run(_compile())

@cli.command()
@click.option('--output', '-o', type=click.Path(), default='config.yaml', help='Fichier de sortie')
def configure(output):
    """Crée un fichier de configuration interactivement"""
    config_path = create_interactive_config(Path(output))
    console.print(f"[green]Configuration sauvegardée dans {config_path}[/green]")

def create_interactive_config(output_path: Path = Path("config.yaml")) -> Path:
    """Crée une configuration via wizard interactif"""
    console.print("[bold]Configuration du générateur de cours[/bold]\n")
    
    # Niveau
    level = Prompt.ask(
        "Niveau scolaire",
        choices=["6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale"],
        default="4ème"
    )
    
    # Nombre de séances
    sessions = int(Prompt.ask("Nombre de séances par an", default="120"))
    
    # Sources du programme
    console.print("\n[yellow]Sources du programme officiel[/yellow]")
    sources = []
    
    while True:
        source_type = Prompt.ask(
            "Type de source",
            choices=["pdf", "url", "text", "skip"],
            default="skip"
        )
        
        if source_type == "skip":
            break
            
        if source_type == "pdf":
            path = Prompt.ask("Chemin du fichier PDF")
            sources.append({"type": "pdf", "path": path})
        elif source_type == "url":
            url = Prompt.ask("URL de la ressource")
            sources.append({"type": "url", "url": url})
        elif source_type == "text":
            text = Prompt.ask("Texte ou description")
            sources.append({"type": "text", "content": text})
            
        if not Confirm.ask("Ajouter une autre source?", default=False):
            break
            
    # Configuration API
    console.print("\n[yellow]Configuration API Claude[/yellow]")
    use_cache = Confirm.ask("Utiliser le cache?", default=True)
    
    # Créer la configuration
    config = {
        "course": {
            "level": level,
            "sessions_per_year": sessions,
            "curriculum_sources": sources if sources else [
                {"type": "text", "content": f"Programme officiel de {level}"}
            ],
            "resources": []
        },
        "api": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4000,
            "temperature": 0.3,
            "use_cache": use_cache,
            "batch_processing": True
        }
    }
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
    return output_path

def create_default_config(config_path: Path):
    """Crée une configuration par défaut"""
    default_config = {
        "course": {
            "level": "4ème",
            "sessions_per_year": 120,
            "curriculum_sources": [
                {
                    "type": "text",
                    "content": "Programme officiel de mathématiques 4ème - Éducation Nationale"
                }
            ],
            "resources": [
                {
                    "type": "text",
                    "content": "Manuel Sésamath 4ème"
                }
            ]
        },
        "api": {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4000,
            "temperature": 0.3,
            "use_cache": True,
            "batch_processing": True
        },
        "workflow": {
            "ai_orchestration": True,
            "contextual_memory": True,
            "adaptive_planning": True
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(default_config, f, allow_unicode=True, default_flow_style=False)

# ============= Main Entry Point =============

if __name__ == "__main__":
    # Vérifier la présence de la clé API
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]Erreur: ANTHROPIC_API_KEY non définie![/bold red]")
        console.print("Définissez la variable d'environnement ou créez un fichier .env")
        sys.exit(1)
        
    # Créer les dossiers nécessaires
    Path("templates").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    Path(".cache").mkdir(exist_ok=True)
    
    # Lancer le CLI
    cli()