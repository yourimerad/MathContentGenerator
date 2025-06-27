from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.models import Chapter, ContentType
import re
import logging

logger = logging.getLogger(__name__)

class LaTeXEngine:
    """Moteur LaTeX pour le formatage et la compilation"""
    def __init__(self, template_dir: Path = Path("templates")):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self._create_default_templates()
    def _create_default_templates(self):
        self.template_dir.mkdir(exist_ok=True)
        # ... (templates LaTeX comme dans le code d'origine) ...
        main_template = r"""
\documentclass[12pt,a4paper]{article}
% ... (reste du template principal) ...
\end{document}
"""
        exercise_template = r"""
\documentclass[12pt,a4paper]{article}
% ... (reste du template exercices) ...
\end{document}
"""
        with open(self.template_dir / "main.tex", "w", encoding="utf-8") as f:
            f.write(main_template)
        with open(self.template_dir / "exercise.tex", "w", encoding="utf-8") as f:
            f.write(exercise_template)
    def format_content(self, content: str, chapter: Chapter, content_type: ContentType, level: str) -> str:
        content = self._clean_latex_body(content)
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
    def validate_latex(self, content: str):
        errors = []
        if content.count(r'\begin{') != content.count(r'\end{'):
            errors.append("Environnements non équilibrés")
        if content.count('{') != content.count('}'):
            errors.append("Accolades non équilibrées")
        if content.count('$') % 2 != 0:
            errors.append("Délimiteurs mathématiques non équilibrés")
        return len(errors) == 0, errors
    def _clean_latex_body(self, content: str) -> str:
        """Retire le préambule et les balises document d'un contenu LaTeX complet."""
        content = re.sub(r"\\documentclass.*?\\begin{document}", "", content, flags=re.DOTALL)
        # Remove \end{document}
        content = re.sub(r"\\end{document}", "", content)
        return content.strip()
    def _create_child_friendly_fallback(self, content: str, chapter: Chapter, content_type: ContentType, level: str) -> str:
        # ... (reprendre la logique du fallback enfant-friendly du code d'origine) ...
        return content  # à adapter selon le code d'origine
