# 🤖 PROMPTS CLAUDE OPTIMISÉS - Guide Complet

## 🎯 Stratégie Globale d'Optimisation

### Principes Fondamentaux
1. **Concision maximale** : Chaque mot compte, éliminer toute redondance
2. **Structure claire** : Format standardisé pour tous les prompts
3. **Contexte minimal suffisant** : Juste assez pour la qualité
4. **Instructions précises** : Éviter l'ambiguïté
5. **Output structuré** : JSON/YAML pour parsing facile

### Économies Visées
- **Réduction tokens** : -60% vs prompts non optimisés
- **Qualité maintenue** : Score > 0.95
- **Temps de réponse** : -30% grâce à la clarté

---

## 📊 MODULE 1: ResourceDiscovery - Prompts

### 1.1 Analyse de Document Pédagogique

```python
ANALYZE_PEDAGOGICAL_DOCUMENT = """
Analyser ce document pédagogique de maths niveau {level}.

Document: {document_excerpt}

Extraire en JSON:
{
  "type": "cours|exercices|evaluation|guide",
  "concepts": ["liste des concepts mathématiques"],
  "competences": ["chercher|modeliser|representer|raisonner|calculer|communiquer"],
  "objectifs": ["objectifs pédagogiques identifiés"],
  "prerequis": ["notions requises"],
  "difficultes_anticipees": ["obstacles didactiques"],
  "progression": "description courte de la progression"
}

Être TRÈS concis. Max 100 mots par section.
"""

# Optimisation: 
# - Prompt direct sans introduction
# - Format de sortie imposé
# - Limite explicite de longueur
# Économie: ~200 tokens vs ~500 non optimisé
```

### 1.2 Extraction de Métadonnées

```python
EXTRACT_RESOURCE_METADATA = """
Métadonnées de: {resource_title}

Retourner UNIQUEMENT:
niveau: {5e|4e|3e}
domaine: {nombres|geometrie|donnees|grandeurs|algo}
type: {cours|exercice|evaluation}
duree_estimee: {minutes}
officiel: {oui|non}
qualite: {1-5}
pertinence_{chapter}: {1-5}
"""

# Optimisation:
# - Format ultra-compact
# - Valeurs énumérées prédéfinies
# - Pas de phrases complètes
# Économie: ~50 tokens vs ~150
```

---

## 📚 MODULE 2: ProgramAnalyzer - Prompts

### 2.1 Analyse Programme Officiel

```python
ANALYZE_OFFICIAL_PROGRAM = """
Programme maths {level} - Analyser structure.

Texte: {program_excerpt}

Retour JSON compact:
{
  "domaines": {
    "nom": {
      "heures": int,
      "chapitres": ["titre"],
      "competences_cibles": ["2-3 principales"],
      "periode_suggérée": [1-5]
    }
  },
  "progressions": {
    "chapitre": ["prérequis directs"]
  },
  "évaluations": {
    "type": "fréquence suggérée"
  }
}

CONCIS. Pas de descriptions.
"""

# Optimisation:
# - Structure imposée minimale
# - Pas de texte libre
# - Focus sur données essentielles
# Économie: ~300 tokens vs ~800
```

### 2.2 Analyse Didactique Ciblée

```python
ANALYZE_DIDACTIC_OBSTACLES = """
Concept: {concept} niveau {level}

Identifier:
1. Obstacle principal (1 phrase)
2. Erreur type fréquente (1 exemple)
3. Remédiation clé (1 stratégie)

Format:
- Obstacle: {description 15 mots max}
- Erreur: {exemple concret}
- Solution: {approche en 20 mots max}
"""

# Optimisation:
# - Questions ultra-ciblées
# - Limites de mots explicites
# - Format imposé minimal
# Économie: ~100 tokens vs ~400
```

---

## 📅 MODULE 3: YearPlanning - Prompts

### 3.1 Planification Annuelle Optimisée

```python
CREATE_YEAR_PLANNING = """
Planifier année maths {level}.
Sessions: {total_sessions}
Périodes: 5
Contraintes: {constraints_summary}

Pour chaque période, donner:
P{n}: {dates}
- Chapitres: [{titre: sessions}]
- Éval: S{num} type

Exemple format:
P1: sept-oct
- Nombres relatifs: 12
- Fractions intro: 8
- Éval: S20 formative

Utiliser abréviations. Pas de phrases.
"""

# Optimisation:
# - Format tabulaire imposé
# - Abréviations standardisées
# - Exemple concret fourni
# Économie: ~250 tokens vs ~700
```

### 3.2 Planning Détaillé Chapitre

```python
PLAN_CHAPTER_DETAILS = """
Chapitre: {title}
Sessions: {allocated_sessions}
Objectifs: {main_objectives}

Structurer en phases:
```
Phase|Sessions|Focus|Activité principale
Découverte|1-2|Intuition|{type activité}
Construction|3-5|Formalisation|{type}
Entraînement|6-8|Automatisation|{type}
Approfond.|9-10|Complexification|{type}
Évaluation|11-12|Validation|{type}
```

Une ligne par phase. Mots-clés seulement.
"""

# Optimisation:
# - Format tableau markdown
# - Pas de descriptions
# - Structure fixe imposée
# Économie: ~150 tokens vs ~500
```

### 3.3 Design de Séance Minimaliste

```python
DESIGN_SESSION = """
Séance {number}/{total} - {chapter}
Type: {session_type}

Retourner:
```yaml
titre: {15 mots max}
objectifs:
  - {objectif 1 en 10 mots}
  - {objectif 2 en 10 mots}
timing:
  accueil: 5
  activité: 25
  exercices: 20
  bilan: 5
matériel: [{item}]
différenciation: {stratégie en 15 mots}
```
"""

# Optimisation:
# - YAML plus compact que JSON
# - Limites de mots strictes
# - Structure temporelle fixe
# Économie: ~120 tokens vs ~350
```

---

## 🎨 MODULE 4: ContentGeneration - Prompts Haute Efficacité

### 4.1 Génération de Cours Structuré

```python
GENERATE_COURSE_CONTENT = """
Cours {chapter} {level}.

Générer:

## Introduction
Accroche: {1 phrase, situation concrète}
Objectif: Aujourd'hui nous allons {20 mots max}

## Définition
{Concept principal en 30 mots max}
Notation: {si applicable}

## Propriétés
1. {Propriété essentielle}
2. {Si pertinent}

## Méthode
Étapes:
1. {Action}
2. {Action}

## Exemple
{Problème simple résolu étape par étape}

Utiliser Markdown. Être CONCIS. Élève-friendly.
"""

# Optimisation:
# - Structure imposée stricte
# - Markdown direct (pas de méta)
# - Sections prédéfinies
# Économie: ~400 tokens vs ~1200
```

### 4.2 Génération d'Exercices en Batch

```python
GENERATE_EXERCISE_BATCH = """
Générer {count} exercices {topic} niveau {difficulty}.

Format par exercice:
```
EX{n}:
Énoncé: {courte situation, données, question}
Réponse: {valeur ou expression}
Indice: {si difficile}
```

Varier:
- Contextes (quotidien, géométrie, problème)
- Valeurs numériques
- Formulations

Concis. Pas de blabla.
"""

# Optimisation:
# - Batch processing
# - Format ultra-compact
# - Variations imposées
# Économie: ~50 tokens/exercice vs ~150
```

### 4.3 Génération d'Évaluation Efficace

```python
GENERATE_EVALUATION = """
Évaluation {type} - {chapter} {level}
Durée: {duration}min
Points: 20

Structure:
```
# Partie A - Automatismes (6pts)
1. (2pts) {calcul/question directe}
2. (2pts) {application simple}
3. (2pts) {conversion/transformation}

# Partie B - Problèmes (10pts)
4. (5pts) {problème guidé}
   a) {sous-question}
   b) {sous-question}
5. (5pts) {problème ouvert}

# Partie C - Bonus (4pts)
6. (4pts) {défi/approfondissement}
```

Énoncés courts. Consignes claires.
"""

# Optimisation:
# - Structure fixe avec barème
# - Format imposé
# - Pas d'instructions superflues
# Économie: ~300 tokens vs ~800
```

### 4.4 Génération de Corrections Ciblées

```python
GENERATE_CORRECTION = """
Corriger: {exercise}

Format:
```
SOLUTION:
Étape 1: {action + calcul}
Étape 2: {action + calcul}
Résultat: {valeur finale}

PIÈGE: {erreur fréquente à éviter}
VÉRIF: {moyen de vérifier}
```

Ultra-concis. Focus sur méthode.
"""

# Optimisation:
# - Format fixe minimal
# - Focus sur l'essentiel
# - Pas d'explications longues
# Économie: ~100 tokens vs ~300
```

---

## ✅ MODULE 5: QualityAssurance - Prompts de Validation

### 5.1 Validation Rapide de Conformité

```python
VALIDATE_COMPLIANCE = """
Vérifier conformité programme officiel.

Contenu: {content_summary}
Attendus officiels: {official_requirements}

Évaluer (0-1):
- Couverture objectifs: 
- Niveau adapté:
- Compétences travaillées:
- Progression cohérente:

Si score < 0.9, lister 1-3 corrections prioritaires.
Format: score|correction
"""

# Optimisation:
# - Évaluation numérique directe
# - Corrections conditionnelles
# - Format compact
# Économie: ~150 tokens vs ~400
```

### 5.2 Analyse d'Erreurs Pédagogiques

```python
CHECK_PEDAGOGICAL_ISSUES = """
Scanner problèmes pédagogiques:

{content_excerpt}

Détecter:
☐ Saut conceptuel trop grand
☐ Prérequis manquant
☐ Exemple inadapté
☐ Difficulté mal calibrée
☐ Consigne ambiguë

Si problème: [Type]|Ligne|Correction suggérée (10 mots)
Sinon: "RAS"
"""

# Optimisation:
# - Checklist prédéfinie
# - Réponse conditionnelle
# - Format ligne compact
# Économie: ~100 tokens vs ~350
```

---

## 🔄 STRATÉGIES DE PARALLÉLISATION

### Batch Processing Intelligent

```python
class BatchPromptStrategy:
    """Stratégies pour appels groupés efficaces"""
    
    @staticmethod
    def create_batch_prompt(items: List[str], operation: str) -> str:
        """
        Créer un prompt pour traiter plusieurs items
        """
        if operation == "generate_exercises":
            return f"""
Générer pour CHAQUE ligne:
{chr(10).join(f'{i+1}. {item}' for i, item in enumerate(items))}

Format réponse:
1: [exercice]
2: [exercice]
...

30 mots max par exercice.
"""
        
    # Optimisation:
    # - Un appel pour N items
    # - Format de sortie parseable
    # - Limite stricte par item
    # Économie: ~80% vs appels individuels
```

### Prompts Récursifs Optimisés

```python
RECURSIVE_IMPROVEMENT = """
Score actuel: {score}
Problème principal: {main_issue}

Améliorer UNIQUEMENT ce point:
{content_excerpt}

Correction minimale:
{correction}

15 mots max. Garder le reste identique.
"""

# Optimisation:
# - Focus sur UN problème
# - Correction minimale
# - Pas de régénération complète
# Économie: ~90% vs régénération totale
```

---

## 📊 MÉTRIQUES D'OPTIMISATION

### Tableau Comparatif

| Module | Tokens/Appel Non Optimisé | Tokens/Appel Optimisé | Réduction |
|--------|---------------------------|------------------------|-----------|
| ResourceDiscovery | 500 | 200 | -60% |
| ProgramAnalyzer | 800 | 300 | -62% |
| YearPlanning | 700 | 250 | -64% |
| ContentGeneration | 1200 | 400 | -67% |
| QualityAssurance | 400 | 150 | -62% |

### Économies Totales Projetées

```yaml
generation_complete:
  appels_totaux: 500
  tokens_non_optimises: 350,000
  tokens_optimises: 125,000
  economie_tokens: 225,000 (64%)
  
  cout_non_optimise: $10.50
  cout_optimise: $3.75
  economie_dollars: $6.75 (64%)
  
  temps_generation_reduit: -30%
  qualite_maintenue: 95%+
```

---

## 🎯 BONNES PRATIQUES

### 1. Structure des Prompts

```python
OPTIMAL_PROMPT_STRUCTURE = """
[CONTEXTE MINIMAL - 1 ligne]
[INSTRUCTION CLAIRE - 1 ligne]

[FORMAT DE SORTIE IMPOSÉ]

[CONTRAINTES - mots/longueur]
"""
```

### 2. Mots-Clés d'Efficacité

- ❌ "Pourriez-vous s'il vous plaît..."
- ✅ "Générer:"

- ❌ "Fournir une explication détaillée de..."
- ✅ "Expliquer en 20 mots:"

- ❌ "Il serait préférable de..."
- ✅ "Format: X|Y|Z"

### 3. Formats de Sortie Optimaux

1. **YAML** pour structures simples (30% plus compact que JSON)
2. **Tableaux Markdown** pour données tabulaires
3. **Listes numérotées** pour séquences
4. **Pipes** pour données inline

### 4. Techniques Avancées

```python
# Compression par référence
"Comme Ex1 mais avec x=5 au lieu de x=3"

# Abréviations standards
"Éval form S15" au lieu de "Évaluation formative à la séance 15"

# Templates implicites
"Format: [Type]|[Durée]|[Points]" 
# Claude comprend et suit le pattern
```

---

## 🚀 IMPLÉMENTATION

### Classe de Gestion des Prompts

```python
class PromptOptimizer:
    """Gestionnaire central des prompts optimisés"""
    
    def __init__(self):
        self.token_counter = TokenCounter()
        self.cache = PromptCache()
        
    def optimize_prompt(self, 
                       template: str, 
                       variables: Dict[str, Any],
                       max_tokens: int = 500) -> str:
        """
        Optimise un prompt en:
        1. Injectant les variables
        2. Supprimant les espaces inutiles
        3. Appliquant les abréviations
        4. Vérifiant la limite de tokens
        """
        prompt = template.format(**variables)
        prompt = self._compress_whitespace(prompt)
        prompt = self._apply_abbreviations(prompt)
        
        if self.token_counter.count(prompt) > max_tokens:
            prompt = self._truncate_smart(prompt, max_tokens)
            
        return prompt
    
    def batch_prompts(self, 
                     prompts: List[str], 
                     max_batch_size: int = 10) -> List[str]:
        """
        Regroupe plusieurs prompts en batches optimaux
        """
        batches = []
        current_batch = []
        current_tokens = 0
        
        for prompt in prompts:
            tokens = self.token_counter.count(prompt)
            if current_tokens + tokens > 3000 or len(current_batch) >= max_batch_size:
                batches.append(self._merge_batch(current_batch))
                current_batch = [prompt]
                current_tokens = tokens
            else:
                current_batch.append(prompt)
                current_tokens += tokens
                
        if current_batch:
            batches.append(self._merge_batch(current_batch))
            
        return batches
```

---

Ce guide d'optimisation des prompts permet d'atteindre l'objectif de génération complète d'une année scolaire pour moins de 50€, tout en maintenant une qualité exceptionnelle du contenu généré.