import asyncio
from pathlib import Path
import logging
from rich.console import Console
from rich.progress import Progress

logger = logging.getLogger(__name__)
console = Console()

class LaTeXCompiler:
    """Compileur LaTeX pour générer des PDFs"""
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.compilation_log = []
    async def compile_all_tex_files(self) -> None:
        console.print("\n[yellow]Phase de compilation LaTeX...[/yellow]")
        tex_files = list(self.output_dir.rglob("*.tex"))
        if not tex_files:
            console.print("  Aucun fichier .tex trouvé à compiler")
            return
        console.print(f"  {len(tex_files)} fichiers .tex trouvés")
        with Progress(console=console) as progress:
            task = progress.add_task("Compilation PDF...", total=len(tex_files))
            for tex_file in tex_files:
                try:
                    await self._compile_single_file(tex_file, progress, task)
                except Exception as e:
                    logger.error(f"Erreur compilation {tex_file}: {e}")
                    self.compilation_log.append(f"ERREUR: {tex_file} - {e}")
                progress.advance(task)
        self._show_compilation_summary()
    async def _compile_single_file(self, tex_file: Path, progress, task) -> None:
        work_dir = tex_file.parent
        if not await self._check_pdflatex():
            raise Exception("pdflatex non trouvé. Installez LaTeX pour compiler les PDFs.")
        cmd = ["pdflatex", "-interaction=nonstopmode", str(tex_file.name)]
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=work_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            process2 = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=work_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout2, stderr2 = await process2.communicate()
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists() and pdf_file.stat().st_size > 0:
                self.compilation_log.append(f"✓ {tex_file.name} → {pdf_file.name}")
                progress.update(task, description=f"Compilé: {tex_file.name}")
                if stderr and stderr.strip():
                    stderr_text = stderr.decode('utf-8', errors='ignore').strip()
                    if stderr_text:
                        logger.warning(f"Warnings LaTeX pour {tex_file.name}: {stderr_text[:200]}...")
            else:
                error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Erreur inconnue"
                if not error_msg.strip():
                    error_msg = stdout.decode('utf-8', errors='ignore') if stdout else "Erreur inconnue"
                raise Exception(f"PDF non généré: {error_msg[:200]}...")
        except Exception as e:
            raise Exception(f"Erreur compilation: {e}")
    async def _check_pdflatex(self) -> bool:
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
    async def compile_single_file(self, tex_file: Path) -> bool:
        """Compile un seul fichier LaTeX et retourne True si succès, False sinon"""
        try:
            work_dir = tex_file.parent
            
            if not await self._check_pdflatex():
                logger.error("pdflatex non trouvé. Installez LaTeX pour compiler les PDFs.")
                return False
            
            cmd = ["pdflatex", "-interaction=nonstopmode", str(tex_file.name)]
            
            # Double compilation pour références croisées
            for i in range(2):
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=work_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
            
            # Vérifier si le PDF a été généré
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists() and pdf_file.stat().st_size > 0:
                return True
            else:
                logger.error(f"PDF non généré pour {tex_file.name}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur compilation {tex_file.name}: {e}")
            return False

    def cleanup_aux_files(self) -> None:
        aux_extensions = ['.aux', '.log', '.out', '.toc', '.nav', '.snm']
        for ext in aux_extensions:
            for aux_file in self.output_dir.rglob(f"*{ext}"):
                try:
                    aux_file.unlink()
                except Exception as e:
                    logger.warning(f"Impossible de supprimer {aux_file}: {e}") 