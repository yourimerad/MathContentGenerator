# Math Content Generator

Générateur automatique de contenu pédagogique mathématique utilisant l'API Claude d'Anthropic.

## 🎯 Fonctionnalités

- **Génération automatique** de cours, exercices et évaluations
- **Planification pédagogique** intelligente avec Claude
- **Formatage LaTeX** professionnel avec templates personnalisables
- **Compilation PDF** automatique
- **Cache intelligent** pour optimiser les coûts API
- **Mode test** économique pour les essais
- **Template enfant-friendly** pour les élèves de 10 ans (5ème)

## 🚀 Installation

### Prérequis

- Python 3.8+
- LaTeX (pdflatex) pour la compilation PDF
- Clé API Anthropic

### Installation des dépendances

```bash
# Cloner le projet
git clone <repository-url>
cd MathContentGenerator

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Installation de LaTeX

**macOS:**
```bash
brew install --cask mactex
```

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-full
```

**Windows:**
Télécharger et installer [MiKTeX](https://miktex.org/) ou [TeX Live](https://www.tug.org/texlive/)

## ⚙️ Configuration

### Configuration rapide

```bash
# Créer une configuration par défaut
python3 math-content-generator.py configure

# Ou configuration interactive
python3 math-content-generator.py configure --interactive
```

### Configuration manuelle

Créer un fichier `config.yaml`:

```yaml
course:
  level: "5ème"
  sessions_per_year: 120
  curriculum_sources:
    - type: "text"
      content: "Programme officiel de 5ème"
  resources: []
  output_path: "./output"

api:
  model: "claude-3-sonnet-20240229"
  max_tokens: 4000
  temperature: 0.3
  use_cache: true
  batch_processing: true
```

## 📖 Utilisation

### Génération complète

```bash
# Générer un cours complet
python3 math-content-generator.py generate --config config.yaml

# Sans compilation PDF
python3 math-content-generator.py generate --config config.yaml --no-compile
```

### Mode test économique

```bash
# Test rapide avec un chapitre
python3 math-content-generator.py test --chapter "Nombres et calculs" --level "5ème"

# Test avec dossier de sortie personnalisé
python3 math-content-generator.py test --chapter "Géométrie" --output "./test_output"

# Test sans compilation
python3 math-content-generator.py test --chapter "Fractions" --no-compile
```

## 🎨 Templates LaTeX

### Template enfant-friendly (10 ans)

Le générateur inclut un template spécialement conçu pour les élèves de 10 ans (niveau 5ème) avec :

- **Couleurs vives et amicales** : Bleu, vert, violet, orange
- **Environnements colorés** : Exemples, méthodes, astuces dans des boîtes colorées
- **Typographie adaptée** : Polices plus grandes, espacement généreux
- **Éléments visuels** : Logo mathématique, icônes, encouragements
- **Structure claire** : Page de titre attractive, table des matières, objectifs

**Environnements disponibles :**
- `\begin{exemple}` - Exemples dans des boîtes bleues
- `\begin{methode}` - Méthodes dans des boîtes vertes  
- `\begin{astuce}` - Conseils dans des boîtes violettes
- `\begin{remarque}` - Points importants dans des boîtes orange
- `\exercice{nom}` - Exercices numérotés automatiquement
- `\sectioncolor{titre}` - Sections colorées

### Template standard

Le template standard est plus sobre et professionnel, adapté aux niveaux supérieurs.

## 📁 Structure des fichiers générés

```
output/
├── Cours_5eme/
│   ├── 01_Planification/
│   │   └── planning_annuel.pdf
│   ├── 02_Chapitres/
│   │   ├── Chapitre_1_Nombres_et_calculs/
│   │   │   ├── 01_Cours/
│   │   │   │   └── cours.pdf
│   │   │   ├── 02_Exercices/
│   │   │   │   ├── 01_Entrainement/
│   │   │   │   │   └── exercices_entrainement.pdf
│   │   │   │   ├── 02_Approfondissement/
│   │   │   │   │   └── exercices_approfondissement.pdf
│   │   │   │   └── 03_Defis/
│   │   │   │       └── exercices_defis.pdf
│   │   │   └── 03_Evaluations/
│   │   │       ├── evaluation_formative.pdf
│   │   │       └── evaluation_sommative.pdf
│   │   └── ...
│   └── 04_Corrections/
│       └── corrections.pdf
```

## 💰 Optimisation des coûts

### Mode test économique

Le mode test utilise :
- Modèle Claude Haiku (plus économique)
- Tokens limités (500 max)
- Contenu de fallback pour les tests
- Pas d'analyse de ressources

### Cache intelligent

- Cache automatique des réponses API
- Évite les appels redondants
- Stockage local en JSON

## 🔧 Dépannage

### Erreurs de compilation LaTeX

1. **Vérifier l'installation LaTeX :**
   ```bash
   pdflatex --version
   ```

2. **Installer les packages manquants :**
   ```bash
   # Sur Ubuntu/Debian
   sudo apt-get install texlive-latex-extra
   
   # Sur macOS avec MacTeX
   sudo tlmgr update --self
   sudo tlmgr install tcolorbox
   ```

3. **Nettoyer les fichiers temporaires :**
   ```bash
   rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz
   ```

### Erreurs API

1. **Vérifier la clé API :**
   ```bash
   export ANTHROPIC_API_KEY="votre_clé_api"
   ```

2. **Tester la connexion :**
   ```bash
   python3 math-content-generator.py test --chapter "Test" --no-compile
   ```

## 📝 Exemples

### Test du template enfant-friendly

```bash
# Créer un test simple
python3 test_child_friendly_simple.py

# Compiler le template
pdflatex test_child_friendly_simple.tex
```

Le fichier `test_child_friendly_simple.pdf` généré montre le rendu du template enfant-friendly avec :
- Page de titre colorée avec logo
- Environnements colorés (exemples, définitions, astuces)
- Typographie adaptée aux enfants
- Messages d'encouragement

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [Anthropic](https://www.anthropic.com/) pour l'API Claude
- [Rich](https://github.com/Textualize/rich) pour l'interface console
- [Click](https://click.palletsprojects.com/) pour l'interface CLI
- [Jinja2](https://jinja.palletsprojects.com/) pour les templates LaTeX