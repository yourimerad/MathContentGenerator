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
from dataclasses import dataclass, field
from enum import Enum
import re
from abc import ABC, abstractmethod

# External dependencies
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from anthropic import Anthropic, AsyncAnthropic
from jinja2 import Environment, FileSystemLoader
import PyPDF2
import aiofiles
from dotenv import load_dotenv

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

# ============= Utility Functions =============

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

# ============= Data Models =============

class ContentType(Enum):
    COURSE = "cours"
    EXERCISE_BASIC = "exercices_entrainement"
    EXERCISE_ADVANCED = "exercices_approfondissement"
    EXERCISE_CHALLENGE = "exercices_defis"
    EVALUATION_FORMATIVE = "evaluation_formative"
    EVALUATION_SUMMATIVE = "evaluation_sommative"
    CORRECTION = "corrections"

@dataclass
class Chapter:
    """Représente un chapitre du cours"""
    number: int
    title: str
    objectives: List[str]
    prerequisites: List[str]
    duration_hours: int
    key_concepts: List[str]
    competencies: List[str]
    
@dataclass
class PedagogicalProgram:
    """Programme pédagogique structuré"""
    level: str
    total_sessions: int
    chapters: List[Chapter]
    general_objectives: List[str]
    evaluation_criteria: Dict[str, Any]
    
@dataclass
class APIConfig:
    """Configuration API Claude"""
    model: str = "claude-3-sonnet-20240229"
    max_tokens: int = 4000
    temperature: float = 0.3
    use_cache: bool = True
    batch_processing: bool = True
    retry_attempts: int = 3
    
@dataclass
class CourseConfig:
    """Configuration du cours"""
    level: str
    sessions_per_year: int
    curriculum_sources: List[Dict[str, str]]
    resources: List[Dict[str, str]]
    output_path: Path = field(default_factory=lambda: Path("./output"))
    
# ============= Cache System =============

class APICache:
    """Système de cache pour optimiser les appels API"""
    def __init__(self, cache_dir: Path = Path(".cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache: Dict[str, Any] = {}
        
    def get_cache_key(self, prompt: str, context: Optional[str] = None) -> str:
        """Génère une clé de cache unique"""
        import hashlib
        content = f"{prompt}:{context or ''}"
        return hashlib.md5(content.encode()).hexdigest()
        
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if key in self.memory_cache:
            return self.memory_cache[key]
            
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            async with aiofiles.open(cache_file, 'r') as f:
                data = json.loads(await f.read())
                self.memory_cache[key] = data
                return data
        return None
        
    async def set(self, key: str, value: Any) -> None:
        """Stocke une valeur dans le cache"""
        self.memory_cache[key] = value
        cache_file = self.cache_dir / f"{key}.json"
        async with aiofiles.open(cache_file, 'w') as f:
            await f.write(json.dumps(value, ensure_ascii=False, indent=2))

# ============= Input Processor =============

class InputProcessor:
    """Parse automatiquement tous types de programmes/ressources via Claude API"""
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def process_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """Traite toutes les sources d'entrée et extrait les informations structurées"""
        all_content = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyse des sources...", total=len(sources))
            
            for source in sources:
                content = await self._extract_content(source)
                all_content.append(content)
                progress.advance(task)
                
        # Analyse globale via Claude
        structured_data = await self._analyze_with_claude(all_content)
        return structured_data
        
    async def _extract_content(self, source: Dict[str, str]) -> str:
        """Extrait le contenu selon le type de source"""
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
        """Extrait le texte d'un PDF"""
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
        """Extrait le contenu d'une URL (simulé)"""
        # En production, utiliser aiohttp ou requests
        return f"Contenu extrait de {url}"
        
    async def _extract_image(self, image_path: str) -> str:
        """Extrait le texte d'une image via OCR (simulé)"""
        # En production, utiliser pytesseract ou l'API Claude avec vision
        return f"Texte extrait de l'image {image_path}"
        
    async def _analyze_with_claude(self, contents: List[str]) -> Dict[str, Any]:
        """Analyse le contenu via Claude API pour extraire les informations structurées"""
        prompt = f"""
        Analyse les contenus suivants provenant de différentes sources pédagogiques et extrais:
        1. Les objectifs pédagogiques
        2. Les compétences visées
        3. La structure du programme (chapitres/thèmes)
        4. Les prérequis
        5. Les critères d'évaluation
        
        Contenus à analyser:
        {' '.join(contents[:3000])}  # Limite pour l'exemple
        
        Retourne une structure JSON avec ces informations.
        """
        
        # Check cache
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
            
            # Parse response
            result = self._parse_claude_response(extract_text_from_response(response))
            
            # Cache result
            await self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur API Claude: {e}")
            return self._get_default_structure()
            
    def _parse_claude_response(self, response: str) -> Dict[str, Any]:
        """Parse la réponse de Claude"""
        try:
            # Extraire le JSON de la réponse
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._get_default_structure()
        
    def _get_default_structure(self) -> Dict[str, Any]:
        """Structure par défaut en cas d'erreur"""
        return {
            "objectives": ["Objectifs à définir"],
            "competencies": ["Compétences à définir"],
            "chapters": [],
            "prerequisites": [],
            "evaluation_criteria": {}
        }

# ============= Pedagogical Planner =============

class PedagogicalPlanner:
    """Planification pédagogique optimisée via Claude API"""
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
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
        """Parse la réponse de planification"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return {}
        
    def _create_program_object(self, data: Dict[str, Any], level: str) -> PedagogicalProgram:
        """Crée l'objet PedagogicalProgram"""
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
        """Programme par défaut pour le niveau 4ème"""
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
            # Ajouter d'autres chapitres...
        ]
        
        return PedagogicalProgram(
            level=level,
            total_sessions=120,
            chapters=chapters,
            general_objectives=["Développer le raisonnement mathématique"],
            evaluation_criteria={"competences": ["Chercher", "Modéliser", "Représenter", "Calculer", "Raisonner", "Communiquer"]}
        )

# ============= Content Generator =============

class ContentGenerator:
    """Génère le contenu pédagogique via Claude API"""
    
    def __init__(self, api_config: APIConfig, cache: APICache):
        self.api_config = api_config
        self.cache = cache
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def generate_chapter_content(
        self,
        chapter: Chapter,
        content_type: ContentType,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Génère un contenu spécifique pour un chapitre"""
        
        prompt = self._build_prompt(chapter, content_type, context)
        
        # Check cache
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
            
            # Cache result
            await self.cache.set(cache_key, content)
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur génération contenu: {e}")
            return self._get_default_content(content_type)
            
    def _build_prompt(self, chapter: Chapter, content_type: ContentType, context: Optional[Dict[str, Any]] = None) -> str:
        """Construit le prompt selon le type de contenu"""
        
        # Ensure context is not None
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
        """Contenu par défaut en cas d'erreur"""
        return f"% Contenu {content_type.value} à générer\n\\textit{{Contenu en cours de génération...}}"

# ============= LaTeX Engine =============

class LaTeXEngine:
    """Moteur LaTeX pour le formatage et la compilation"""
    
    def __init__(self, template_dir: Path = Path("templates")):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self._create_default_templates()
        
    def _create_default_templates(self):
        """Crée les templates LaTeX par défaut"""
        self.template_dir.mkdir(exist_ok=True)
        
        # Template principal - Version enfant-friendly simplifiée
        main_template = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{fancyhdr}
\usepackage{enumerate}
\usepackage{hyperref}
\usepackage{fontawesome}
\usepackage{tcolorbox}

\geometry{margin=2.5cm}

% Couleurs enfant-friendly
\definecolor{primary}{RGB}{52, 152, 219}
\definecolor{secondary}{RGB}{46, 204, 113}
\definecolor{accent}{RGB}{155, 89, 182}
\definecolor{warning}{RGB}{230, 126, 34}
\definecolor{success}{RGB}{39, 174, 96}
\definecolor{lightgray}{RGB}{236, 240, 241}

% Configuration des liens
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    urlcolor=accent,
    citecolor=secondary
}

% Définitions des environnements enfant-friendly
\newtheorem{definition}{Définition}[section]
\newtheorem{propriete}{Propriété}[section]
\newtheorem{theoreme}{Théorème}[section]

% Environnements colorés et amicaux
\newenvironment{exemple}{\begin{tcolorbox}[colback=lightgray,colframe=primary,title=\textbf{\textcolor{primary}{Exemple}}]}{\end{tcolorbox}}
\newenvironment{methode}{\begin{tcolorbox}[colback=lightgray,colframe=secondary,title=\textbf{\textcolor{secondary}{Méthode}}]}{\end{tcolorbox}}
\newenvironment{remarque}{\begin{tcolorbox}[colback=lightgray,colframe=warning,title=\textbf{\textcolor{warning}{Remarque importante}}]}{\end{tcolorbox}}
\newenvironment{astuce}{\begin{tcolorbox}[colback=lightgray,colframe=accent,title=\textbf{\textcolor{accent}{Astuce}}]}{\end{tcolorbox}}

% Compteur d'exercices avec icône
\newcounter{exercicecounter}
\newcommand{\exercice}[1]{\stepcounter{exercicecounter}\textbf{\textcolor{primary}{Exercice \theexercicecounter}} \textcolor{primary}{#1}}

% Titre de section coloré
\newcommand{\sectioncolor}[1]{\section{\textcolor{primary}{#1}}}

% En-tête et pied de page enfant-friendly
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{\textbf{{{ level }} - {{ chapter_title }}}}}
\fancyhead[R]{\textcolor{accent}{\textbf{{{ document_type }}}}}
\fancyfoot[C]{\textcolor{primary}{\thepage}}
\renewcommand{\headrulewidth}{2pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \headrulewidth\hfill}}

% Titre principal avec style enfant-friendly
\title{\Huge\textcolor{primary}{\textbf{{{ title }}}}\\[0.5cm]
\Large\textcolor{accent}{Cours de Mathématiques}}
\author{\Large\textcolor{secondary}{\textbf{Généré automatiquement}}}
\date{\Large\textcolor{warning}{\textbf{\today}}}

\begin{document}

% Page de titre colorée
\begin{titlepage}
\begin{center}
\vspace*{2cm}

% Logo ou icône
\begin{tikzpicture}
\draw[fill=primary,rounded corners=10pt] (0,0) rectangle (4,4);
\node[white,font=\Huge] at (2,2) {M};
\end{tikzpicture}

\vspace{1cm}

{\Huge\textcolor{primary}{\textbf{{{ title }}}}}

\vspace{0.5cm}

{\Large\textcolor{accent}{Cours de Mathématiques}}

\vspace{1cm}

{\Large\textcolor{secondary}{\textbf{{{ level }}}}}

\vspace{0.5cm}

{\large\textcolor{warning}{\textbf{\today}}}

\vspace{2cm}

% Boîte d'objectifs
\begin{tcolorbox}[colback=lightgray,colframe=success,title=\textbf{\textcolor{success}{Objectifs du cours}}]
\begin{itemize}
\item Comprendre les concepts mathématiques
\item S'entraîner avec des exercices
\item Progresser étape par étape
\end{itemize}
\end{tcolorbox}

\end{center}
\end{titlepage}

% Table des matières
\tableofcontents
\newpage

% Contenu principal
{{ content }}

% Page de fin avec encouragement
\newpage
\begin{center}
\begin{tcolorbox}[colback=lightgray,colframe=success,title=\textbf{\textcolor{success}{Bravo !}}]
\Large\textbf{\textcolor{success}{Tu as terminé ce cours !}}\\[0.5cm]
\textcolor{secondary}{Continue à t'entraîner et tu deviendras un expert en mathématiques !}\\[0.5cm]
\textcolor{accent}{*****}
\end{tcolorbox}
\end{center}

\end{document}
"""
        
        # Template pour exercices enfant-friendly simplifié
        exercise_template = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{fancyhdr}
\usepackage{enumerate}
\usepackage{hyperref}
\usepackage{fontawesome}
\usepackage{tcolorbox}

\geometry{margin=2.5cm}

% Couleurs enfant-friendly
\definecolor{primary}{RGB}{52, 152, 219}
\definecolor{secondary}{RGB}{46, 204, 113}
\definecolor{accent}{RGB}{155, 89, 182}
\definecolor{warning}{RGB}{230, 126, 34}
\definecolor{success}{RGB}{39, 174, 96}
\definecolor{lightgray}{RGB}{236, 240, 241}

% Configuration des liens
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    urlcolor=accent,
    citecolor=secondary
}

% Compteur d'exercices avec icône
\newcounter{exercicecounter}
\newcommand{\exercice}[1]{\stepcounter{exercicecounter}\textbf{\textcolor{primary}{Exercice \theexercicecounter}} \textcolor{primary}{#1}}

% Environnements colorés pour exercices
\newenvironment{question}{\begin{tcolorbox}[colback=lightgray,colframe=primary,title=\textbf{\textcolor{primary}{Question}}]}{\end{tcolorbox}}
\newenvironment{indice}{\begin{tcolorbox}[colback=lightgray,colframe=accent,title=\textbf{\textcolor{accent}{Indice}}]}{\end{tcolorbox}}

% En-tête et pied de page
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{\textbf{{{ level }} - {{ chapter_title }}}}}
\fancyhead[R]{\textcolor{accent}{\textbf{{{ document_type }}}}}
\fancyfoot[C]{\textcolor{primary}{\thepage}}
\renewcommand{\headrulewidth}{2pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \headrulewidth\hfill}}

% Titre principal
\title{\Huge\textcolor{primary}{\textbf{{{ title }}}}\\[0.5cm]
\Large\textcolor{accent}{Exercices de Mathématiques}}
\author{\Large\textcolor{secondary}{\textbf{Généré automatiquement}}}
\date{\Large\textcolor{warning}{\textbf{\today}}}

\begin{document}

% Page de titre pour exercices
\begin{titlepage}
\begin{center}
\vspace*{2cm}

% Logo exercices
\begin{tikzpicture}
\draw[fill=secondary,rounded corners=10pt] (0,0) rectangle (4,4);
\node[white,font=\Huge] at (2,2) {E};
\end{tikzpicture}

\vspace{1cm}

{\Huge\textcolor{primary}{\textbf{{{ title }}}}}

\vspace{0.5cm}

{\Large\textcolor{accent}{Exercices de Mathématiques}}

\vspace{1cm}

{\Large\textcolor{secondary}{\textbf{{{ level }}}}}

\vspace{0.5cm}

{\large\textcolor{warning}{\textbf{\today}}}

\vspace{2cm}

% Instructions pour les exercices
\begin{tcolorbox}[colback=lightgray,colframe=warning,title=\textbf{\textcolor{warning}{Instructions}}]
\begin{itemize}
\item Lis bien chaque question
\item Prends ton temps pour réfléchir
\item N'hésite pas à demander de l'aide si besoin
\item Vérifie tes réponses
\end{itemize}
\end{tcolorbox}

\end{center}
\end{titlepage}

% Contenu des exercices
{{ content }}

% Page de fin avec encouragement
\newpage
\begin{center}
\begin{tcolorbox}[colback=lightgray,colframe=success,title=\textbf{\textcolor{success}{Excellent travail !}}]
\Large\textbf{\textcolor{success}{Tu as terminé tous les exercices !}}\\[0.5cm]
\textcolor{secondary}{Continue à t'entraîner pour devenir encore plus fort en mathématiques !}\\[0.5cm]
\textcolor{accent}{*****}
\end{tcolorbox}
\end{center}

\end{document}
"""
        
        # Sauvegarder les templates
        with open(self.template_dir / "main.tex", "w", encoding="utf-8") as f:
            f.write(main_template)
            
        with open(self.template_dir / "exercise.tex", "w", encoding="utf-8") as f:
            f.write(exercise_template)
            
    def format_content(
        self,
        content: str,
        chapter: Chapter,
        content_type: ContentType,
        level: str
    ) -> str:
        """Formate le contenu avec le template approprié"""
        
        # Choisir le template selon le type de contenu
        if content_type in [ContentType.EXERCISE_BASIC, ContentType.EXERCISE_ADVANCED, ContentType.EXERCISE_CHALLENGE]:
            template = self.env.get_template("exercise.tex")
        else:
            template = self.env.get_template("main.tex")
        
        document_type_map = {
            ContentType.COURSE: "Cours",
            ContentType.EXERCISE_BASIC: "Exercices - Entraînement",
            ContentType.EXERCISE_ADVANCED: "Exercices - Approfondissement",
            ContentType.EXERCISE_CHALLENGE: "Exercices - Défis",
            ContentType.EVALUATION_FORMATIVE: "Évaluation formative",
            ContentType.EVALUATION_SUMMATIVE: "Évaluation sommative",
            ContentType.CORRECTION: "Corrections"
        }
        
        formatted = template.render(
            title=f"Chapitre {chapter.number} - {chapter.title}",
            level=level,
            chapter_title=chapter.title,
            document_type=document_type_map.get(content_type, "Document"),
            content=content
        )
        
        return formatted
        
    def validate_latex(self, content: str) -> Tuple[bool, List[str]]:
        """Valide la syntaxe LaTeX"""
        errors = []
        
        # Vérifications basiques
        if content.count(r'\begin{') != content.count(r'\end{'):
            errors.append("Environnements non équilibrés")
            
        if content.count('{') != content.count('}'):
            errors.append("Accolades non équilibrées")
            
        if content.count('$') % 2 != 0:
            errors.append("Délimiteurs mathématiques non équilibrés")
            
        return len(errors) == 0, errors
        
    def _create_child_friendly_fallback(self, content: str, chapter: Chapter, content_type: ContentType, level: str) -> str:
        """Crée un format LaTeX enfant-friendly en cas d'erreur de template"""
        
        # Template de base avec toutes les définitions nécessaires
        latex_template = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{fancyhdr}
\usepackage{enumerate}
\usepackage{hyperref}
\usepackage{fontawesome}
\usepackage{tcolorbox}

\geometry{margin=2.5cm}

% Couleurs enfant-friendly
\definecolor{primary}{RGB}{52, 152, 219}
\definecolor{secondary}{RGB}{46, 204, 113}
\definecolor{accent}{RGB}{155, 89, 182}
\definecolor{warning}{RGB}{230, 126, 34}
\definecolor{success}{RGB}{39, 174, 96}
\definecolor{lightgray}{RGB}{236, 240, 241}

% Configuration des liens
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    urlcolor=accent,
    citecolor=secondary
}

% Définitions des environnements enfant-friendly
\newtheorem{definition}{Définition}[section]
\newtheorem{propriete}{Propriété}[section]
\newtheorem{theoreme}{Théorème}[section]

% Environnements colorés et amicaux
\newenvironment{exemple}{\begin{tcolorbox}[colback=lightgray,colframe=primary,title=\textbf{\textcolor{primary}{Exemple}}]}{\end{tcolorbox}}
\newenvironment{methode}{\begin{tcolorbox}[colback=lightgray,colframe=secondary,title=\textbf{\textcolor{secondary}{Méthode}}]}{\end{tcolorbox}}
\newenvironment{remarque}{\begin{tcolorbox}[colback=lightgray,colframe=warning,title=\textbf{\textcolor{warning}{Remarque importante}}]}{\end{tcolorbox}}
\newenvironment{astuce}{\begin{tcolorbox}[colback=lightgray,colframe=accent,title=\textbf{\textcolor{accent}{Astuce}}]}{\end{tcolorbox}}

% Compteur d'exercices avec icône
\newcounter{exercicecounter}
\newcommand{\exercice}[1]{\stepcounter{exercicecounter}\textbf{\textcolor{primary}{Exercice \theexercicecounter}} \textcolor{primary}{#1}}

% Titre de section coloré
\newcommand{\sectioncolor}[1]{\section{\textcolor{primary}{#1}}}

% Environnements pour exercices
\newenvironment{question}{\begin{tcolorbox}[colback=lightgray,colframe=primary,title=\textbf{\textcolor{primary}{Question}}]}{\end{tcolorbox}}
\newenvironment{indice}{\begin{tcolorbox}[colback=lightgray,colframe=accent,title=\textbf{\textcolor{accent}{Indice}}]}{\end{tcolorbox}}

% En-tête et pied de page enfant-friendly
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{\textbf{LEVEL - CHAPTER_TITLE}}}
\fancyhead[R]{\textcolor{accent}{\textbf{CONTENT_TYPE}}}
\fancyfoot[C]{\textcolor{primary}{\thepage}}
\renewcommand{\headrulewidth}{2pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{primary}\leaders\hrule height \headrulewidth\hfill}}

% Titre principal avec style enfant-friendly
\title{\Huge\textcolor{primary}{\textbf{CHAPTER_TITLE}}\\[0.5cm]
\Large\textcolor{accent}{Cours de Mathématiques}}
\author{\Large\textcolor{secondary}{\textbf{Généré automatiquement}}}
\date{\Large\textcolor{warning}{\textbf{\today}}}

\begin{document}

% Page de titre colorée
\begin{titlepage}
\begin{center}
\vspace*{2cm}

% Logo ou icône
\begin{tikzpicture}
\draw[fill=primary,rounded corners=10pt] (0,0) rectangle (4,4);
\node[white,font=\Huge] at (2,2) {M};
\end{tikzpicture}

\vspace{1cm}

{\Huge\textcolor{primary}{\textbf{CHAPTER_TITLE}}}

\vspace{0.5cm}

{\Large\textcolor{accent}{Cours de Mathématiques}}

\vspace{1cm}

{\Large\textcolor{secondary}{\textbf{LEVEL}}}

\vspace{0.5cm}

{\large\textcolor{warning}{\textbf{\today}}}

\vspace{2cm}

% Boîte d'objectifs
\begin{tcolorbox}[colback=lightgray,colframe=success,title=\textbf{\textcolor{success}{Objectifs du cours}}]
\begin{itemize}
\item Comprendre les concepts mathématiques
\item S'entraîner avec des exercices
\item Progresser étape par étape
\end{itemize}
\end{tcolorbox}

\end{center}
\end{titlepage}

% Table des matières
\tableofcontents
\newpage

% Contenu principal
CONTENT

% Page de fin avec encouragement
\newpage
\begin{center}
\begin{tcolorbox}[colback=lightgray,colframe=success,title=\textbf{\textcolor{success}{Bravo !}}]
\Large\textbf{\textcolor{success}{Tu as terminé ce cours !}}\\[0.5cm]
\textcolor{secondary}{Continue à t'entraîner et tu deviendras un expert en mathématiques !}\\[0.5cm]
\textcolor{accent}{*****}
\end{tcolorbox}
\end{center}

\end{document}
"""
        
        # Remplacer les placeholders
        formatted = latex_template.replace("LEVEL", level)
        formatted = formatted.replace("CHAPTER_TITLE", chapter.title)
        formatted = formatted.replace("CONTENT_TYPE", content_type.value)
        formatted = formatted.replace("CONTENT", content)
        
        return formatted

# ============= LaTeX Compiler =============

class LaTeXCompiler:
    """Compileur LaTeX pour générer des PDFs"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.compilation_log = []
        
    async def compile_all_tex_files(self) -> None:
        """Compile tous les fichiers .tex en PDF"""
        console.print("\n[yellow]Phase de compilation LaTeX...[/yellow]")
        
        # Trouver tous les fichiers .tex
        tex_files = list(self.output_dir.rglob("*.tex"))
        
        if not tex_files:
            console.print("  Aucun fichier .tex trouvé à compiler")
            return
            
        console.print(f"  {len(tex_files)} fichiers .tex trouvés")
        
        # Compiler chaque fichier
        with Progress(console=console) as progress:
            task = progress.add_task("Compilation PDF...", total=len(tex_files))
            
            for tex_file in tex_files:
                try:
                    await self._compile_single_file(tex_file, progress, task)
                except Exception as e:
                    logger.error(f"Erreur compilation {tex_file}: {e}")
                    self.compilation_log.append(f"ERREUR: {tex_file} - {e}")
                
                progress.advance(task)
                
        # Afficher le résumé
        self._show_compilation_summary()
        
    async def _compile_single_file(self, tex_file: Path, progress, task) -> None:
        """Compile un seul fichier .tex en PDF"""
        
        # Déterminer le répertoire de travail
        work_dir = tex_file.parent
        
        # Vérifier si pdflatex est disponible
        if not await self._check_pdflatex():
            raise Exception("pdflatex non trouvé. Installez LaTeX pour compiler les PDFs.")
            
        # Compiler avec pdflatex
        cmd = [
            "pdflatex",
            "-interaction=nonstopmode",  # Mode non-interactif
            str(tex_file.name)  # Nom du fichier
        ]
        
        try:
            # Première compilation
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=work_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Deuxième compilation pour les références (si nécessaire)
            if process.returncode == 0:
                process2 = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=work_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout2, stderr2 = await process2.communicate()
                
                # Vérifier si le PDF a été créé
                pdf_file = tex_file.with_suffix('.pdf')
                if pdf_file.exists():
                    self.compilation_log.append(f"✓ {tex_file.name} → {pdf_file.name}")
                    progress.update(task, description=f"Compilé: {tex_file.name}")
                else:
                    raise Exception("PDF non généré")
            else:
                error_msg = stderr.decode() if stderr else "Erreur inconnue"
                raise Exception(f"Erreur pdflatex: {error_msg}")
                
        except Exception as e:
            raise Exception(f"Erreur compilation: {e}")
            
    async def _check_pdflatex(self) -> bool:
        """Vérifie si pdflatex est disponible"""
        try:
            process = await asyncio.create_subprocess_exec(
                "pdflatex", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            return process.returncode == 0
            
        except FileNotFoundError:
            return False
            
    def _show_compilation_summary(self) -> None:
        """Affiche un résumé de la compilation"""
        if not self.compilation_log:
            return
            
        console.print("\n[bold]Résumé de la compilation:[/bold]")
        
        success_count = sum(1 for log in self.compilation_log if log.startswith("✓"))
        error_count = sum(1 for log in self.compilation_log if log.startswith("ERREUR"))
        
        for log in self.compilation_log:
            if log.startswith("✓"):
                console.print(f"  [green]{log}[/green]")
            else:
                console.print(f"  [red]{log}[/red]")
                
        console.print(f"\n[bold]Total: {success_count} succès, {error_count} erreurs[/bold]")
        
        if error_count > 0:
            console.print("\n[yellow]Note:[/yellow] Certains fichiers n'ont pas pu être compilés.")
            console.print("Vérifiez que LaTeX est installé et que les fichiers .tex sont valides.")
            
    def cleanup_aux_files(self) -> None:
        """Nettoie les fichiers auxiliaires LaTeX"""
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm']
        
        for ext in aux_extensions:
            for aux_file in self.output_dir.rglob(f"*{ext}"):
                try:
                    aux_file.unlink()
                except Exception as e:
                    logger.warning(f"Impossible de supprimer {aux_file}: {e}")

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
                
                # Nettoyer les fichiers auxiliaires
                latex_compiler.cleanup_aux_files()
            else:
                console.print("\n[yellow]Compilation PDF désactivée (--no-compile)[/yellow]")
            
            console.print("[bold green]✓ Test généré avec succès![/bold green]")
            
        except Exception as e:
            logger.error(f"Erreur génération test: {e}")
            console.print(f"[bold red]✗ Erreur: {e}[/bold red]")
            # Continue anyway to show what was generated
            
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
                
                # Formater avec LaTeX
                try:
                    formatted = self.latex_engine.format_content(
                        content,
                        chapter,
                        content_type,
                        self.course_config.level
                    )
                except Exception as format_error:
                    logger.warning(f"Erreur formatage LaTeX: {format_error}")
                    # Utiliser le template enfant-friendly en cas d'erreur
                    if content_type in [ContentType.EXERCISE_BASIC, ContentType.EXERCISE_ADVANCED, ContentType.EXERCISE_CHALLENGE]:
                        template_name = "exercise.tex"
                    else:
                        template_name = "main.tex"
                    
                    try:
                        template = self.latex_engine.env.get_template(template_name)
                        formatted = template.render(
                            title=f"Chapitre {chapter.number} - {chapter.title}",
                            level=self.course_config.level,
                            chapter_title=chapter.title,
                            document_type=content_type.value,
                            content=content
                        )
                    except Exception as template_error:
                        logger.warning(f"Erreur template {template_name}: {template_error}")
                        # Format enfant-friendly en dernier recours avec toutes les définitions
                        formatted = self.latex_engine._create_child_friendly_fallback(
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
                    # Continue with next content type
                    
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
            # Continue without cache
            
        try:
            # Utiliser un modèle plus petit et moins de tokens pour le test
            response = await self.content_generator.client.messages.create(
                model="claude-3-haiku-20240307",  # Modèle plus petit
                max_tokens=500,  # Très limité
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = extract_text_from_response(response)
            
            # Cache result (only if it's a string)
            try:
                if isinstance(content, str):
                    await self.cache.set(cache_key, content)
            except Exception as cache_error:
                logger.warning(f"Erreur cache: {cache_error}")
            
            return content
            
        except Exception as e:
            logger.error(f"Erreur génération test: {e}")
            content = self._get_test_fallback_content(content_type)
            
        # Cache result (only if it's a string)
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
                "model": "claude-3-sonnet-20240229",
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
                structured_data,
                self.course_config
            )
            self.context_memory["program"] = program
            
            # Phase 3: Génération du contenu
            console.print("\n[yellow]Phase 3:[/yellow] Génération des contenus pédagogiques")
            await self._generate_all_content(program)
            
            # Phase 4: Compilation LaTeX (si activée)
            if not self.no_compile:
                console.print("\n[yellow]Phase 4:[/yellow] Compilation des PDFs")
                latex_compiler = LaTeXCompiler(self.course_config.output_path)
                await latex_compiler.compile_all_tex_files()
                
                # Nettoyer les fichiers auxiliaires
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
        base_path = self.course_config.output_path / f"Cours_{program.level}"
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
                chapter,
                content_type,
                self.context_memory
            )
            
            # Formater avec LaTeX
            try:
                formatted = self.latex_engine.format_content(
                    content,
                    chapter,
                    content_type,
                    level
                )
            except Exception as format_error:
                logger.warning(f"Erreur formatage LaTeX: {format_error}")
                # Utiliser le template enfant-friendly en cas d'erreur
                if content_type in [ContentType.EXERCISE_BASIC, ContentType.EXERCISE_ADVANCED, ContentType.EXERCISE_CHALLENGE]:
                    template_name = "exercise.tex"
                else:
                    template_name = "main.tex"
                
                try:
                    template = self.latex_engine.env.get_template(template_name)
                    formatted = template.render(
                        title=f"Chapitre {chapter.number} - {chapter.title}",
                        level=self.course_config.level,
                        chapter_title=chapter.title,
                        document_type=content_type.value,
                        content=content
                    )
                except Exception as template_error:
                    logger.warning(f"Erreur template {template_name}: {template_error}")
                    # Format enfant-friendly en dernier recours avec toutes les définitions
                    formatted = self.latex_engine._create_child_friendly_fallback(
                        content, chapter, content_type, self.course_config.level
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
            "model": "claude-3-sonnet-20240229",
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
            "model": "claude-3-sonnet-20240229",
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
            "model": "claude-3-sonnet-20240229",
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

# ============= Exemple de génération =============

def create_example_content():
    """Crée un exemple de contenu pour démonstration"""
    
    example_course = r"""
\section{Introduction aux nombres relatifs}

\begin{exemple}
La température à Chamonix était de $-5°C$ le matin et a augmenté de $8°C$ dans la journée. 
Quelle était la température l'après-midi ?

Pour résoudre ce problème, nous devons calculer : $-5 + 8 = 3$

La température était donc de $3°C$ l'après-midi.
\end{exemple}

\begin{definition}
Les \textbf{nombres relatifs} sont les nombres précédés d'un signe $+$ ou $-$.
\begin{itemize}
\item Les nombres positifs : $+3$, $+15,7$, $+\frac{2}{3}$
\item Les nombres négatifs : $-5$, $-12,4$, $-\frac{7}{2}$
\item Zéro n'est ni positif ni négatif
\end{itemize}
\end{definition}

\begin{propriete}
Pour additionner deux nombres relatifs :
\begin{itemize}
\item Si les nombres ont le même signe, on additionne leurs distances à zéro et on garde le signe commun
\item Si les nombres ont des signes différents, on soustrait leurs distances à zéro et on prend le signe du nombre ayant la plus grande distance à zéro
\end{itemize}
\end{propriete}
"""
    
    example_exercises = r"""
\exercice{Calculer les sommes suivantes :}
\begin{enumerate}[a)]
\item $(+7) + (+3)$
\item $(-8) + (-5)$
\item $(+12) + (-7)$
\item $(-15) + (+20)$
\end{enumerate}

\exercice{Un sous-marin se trouve à $-150$ mètres de profondeur. Il remonte de $80$ mètres. À quelle profondeur se trouve-t-il maintenant ?}

\exercice{Compléter le tableau suivant :}
\begin{center}
\begin{tabular}{|c|c|c|}
\hline
$a$ & $b$ & $a + b$ \\
\hline
$+5$ & $+8$ & \\
\hline
$-3$ & $-7$ & \\
\hline
$+9$ & $-4$ & \\
\hline
$-12$ & $+15$ & \\
\hline
\end{tabular}
\end{center}
"""
    
    return example_course, example_exercises

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
