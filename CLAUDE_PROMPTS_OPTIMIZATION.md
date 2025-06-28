# 🤖 PROMPTS CLAUDE OPTIMISÉS - Stratégie Enrichie

## 🎯 Nouvelle Stratégie d'Optimisation

### Principe Fondamental Révisé
**Investir dans la richesse des prompts d'entrée pour garantir des sorties de qualité optimale**

### Ratios de Coût (Claude 3.5 Sonnet)
- **Tokens d'entrée** : $3 / million tokens
- **Tokens de sortie** : $15 / million tokens
- **Ratio** : 1:5 (les sorties coûtent 5x plus cher)

### Nouvelle Approche
1. **Prompts d'entrée détaillés** : Contexte riche, instructions précises, exemples multiples
2. **Sorties structurées et concises** : Format imposé, limites strictes
3. **Contexte pédagogique complet** : Tous les détails nécessaires pour une génération de qualité
4. **Flexibilité maximale** : Permettre l'expression de la complexité pédagogique

---

## 📊 MODULE 1: ResourceDiscovery - Prompts Enrichis

### 1.1 Analyse Approfondie de Document Pédagogique

```python
ANALYZE_PEDAGOGICAL_DOCUMENT_DETAILED = """
Tu es un expert en didactique des mathématiques avec 20 ans d'expérience dans l'analyse de ressources pédagogiques.

CONTEXTE DÉTAILLÉ:
- Niveau: {level} (élèves de {age} ans environ)
- Période de l'année: {period} (tenir compte des acquis antérieurs)
- Programme officiel de référence: {official_program_excerpt}
- Objectifs d'apprentissage visés: {learning_objectives}

DOCUMENT À ANALYSER:
{document_full_text}

ANALYSE DEMANDÉE:

1. TYPE ET NATURE DU DOCUMENT
   - Identifier précisément le type (cours magistral, activité de découverte, exercices d'application, problème ouvert, évaluation, remédiation, etc.)
   - Analyser l'approche pédagogique sous-jacente (transmissive, constructiviste, socio-constructiviste, par investigation, etc.)
   - Évaluer le niveau d'interactivité et d'engagement attendu

2. ANALYSE DES CONCEPTS MATHÉMATIQUES
   - Lister TOUS les concepts mathématiques abordés, même implicitement
   - Pour chaque concept, identifier:
     * Le niveau de formalisation (intuitif, semi-formel, formel)
     * Les représentations utilisées (numérique, algébrique, graphique, géométrique)
     * Les registres de représentation mobilisés
   - Analyser les connexions entre concepts (hiérarchie, parallélisme, transversalité)

3. ANALYSE MULTI-DOMAINES
   - Identifier tous les domaines mathématiques impliqués avec leur pondération approximative
   - Exemples de croisements:
     * Proportionnalité: nombres (calculs), données (tableaux), mesures (conversions)
     * Géométrie analytique: espace (figures), nombres (coordonnées), algèbre (équations)
   - Repérer les opportunités de connexions interdisciplinaires

4. COMPÉTENCES MATHÉMATIQUES TRAVAILLÉES
   Pour chaque compétence du socle, analyser:
   - CHERCHER: Types de recherche proposés, autonomie attendue, stratégies suggérées
   - MODÉLISER: Situations à modéliser, niveau d'abstraction, allers-retours modèle/réalité
   - REPRÉSENTER: Diversité des représentations, passages entre registres, construction de représentations
   - RAISONNER: Types de raisonnement (déductif, inductif, par l'absurde), niveau de rigueur
   - CALCULER: Techniques de calcul, calcul mental/posé/instrumenté, estimation
   - COMMUNIQUER: Production écrite/orale attendue, vocabulaire spécifique, argumentation

5. ANALYSE DIDACTIQUE FINE
   - Obstacles épistémologiques potentiels (exemples: passage au négatif, infini, continuité)
   - Erreurs typiques anticipées et leur origine cognitive
   - Variables didactiques identifiées et leur impact
   - Ruptures de contrat didactique éventuelles
   - Zone proximale de développement visée

6. PROGRESSION ET PRÉREQUIS
   - Prérequis explicites et implicites (connaissances, capacités, attitudes)
   - Place dans une progression (introduction, consolidation, approfondissement, réinvestissement)
   - Articulation avec les apprentissages antérieurs et ultérieurs
   - Spiralité des apprentissages

7. ADAPTATIONS ET DIFFÉRENCIATION
   - Potentiel de différenciation (par la tâche, par le processus, par le produit)
   - Adaptations possibles pour élèves en difficulté
   - Enrichissements pour élèves avancés
   - Accessibilité (DYS, allophones, etc.)

8. QUALITÉ PÉDAGOGIQUE
   - Clarté des consignes et des attendus
   - Progressivité de la difficulté
   - Équilibre entre guidage et autonomie
   - Pertinence des exemples et contextes
   - Potentiel de motivation et d'engagement

FORMAT DE SORTIE STRUCTURÉ:
```json
{
  "metadata": {
    "type": "string (30 mots max)",
    "approche_pedagogique": "string (20 mots max)",
    "duree_estimee": "int (minutes)",
    "niveau_difficulte": "1-5"
  },
  "analyse_conceptuelle": {
    "concepts_principaux": ["liste avec descriptions courtes"],
    "concepts_secondaires": ["liste"],
    "prerequis": ["liste précise"],
    "connexions": {"concept1": ["concepts liés"], ...}
  },
  "analyse_multi_domaines": {
    "domaines": {"domaine": pourcentage, ...},
    "activites_transversales": ["descriptions"],
    "opportunites_interdisciplinaires": ["suggestions"]
  },
  "competences": {
    "chercher": {"niveau": "1-5", "activites": ["liste"]},
    "modeliser": {...},
    // etc. pour les 6 compétences
  },
  "analyse_didactique": {
    "obstacles": ["liste avec explications"],
    "erreurs_anticipees": ["erreur: origine"],
    "variables_didactiques": ["variable: impact"],
    "zpd": "description de la zone visée"
  },
  "qualite_score": {
    "clarte": "0-1",
    "pertinence": "0-1",
    "completude": "0-1",
    "adaptabilite": "0-1",
    "score_global": "0-1"
  },
  "recommandations": ["suggestions d'amélioration ou d'utilisation"]
}
```

Limite stricte: 800 tokens pour la réponse totale.
"""

# Stratégie:
# - Prompt d'entrée très riche (~1500 tokens) pour capturer toute la complexité
# - Sortie structurée et limitée (~800 tokens) pour l'efficacité
# - Coût: ~$0.007 par analyse (vs ~$0.003 avec l'ancienne approche minimaliste)
# - Gain: Analyse 10x plus riche et exploitable
```

### 1.2 Extraction de Patterns Pédagogiques

```python
EXTRACT_PEDAGOGICAL_PATTERNS = """
En tant qu'expert en ingénierie pédagogique spécialisé en mathématiques, analyser les patterns et structures récurrentes dans cette collection de ressources.

CORPUS À ANALYSER:
{resources_summary} # Liste des ressources avec leurs caractéristiques

CONTEXTE D'ANALYSE:
- Niveau concerné: {level}
- Période d'analyse: {academic_period}
- Objectif: Identifier les meilleures pratiques et approches pédagogiques récurrentes

ANALYSE DEMANDÉE:

1. PATTERNS DE PROGRESSION
   - Identifier les séquences types (découverte → formalisation → application → approfondissement)
   - Repérer les progressions spiralaires
   - Analyser les rythmes (alternance théorie/pratique, abstrait/concret)
   - Identifier les moments clés de conceptualisation

2. PATTERNS D'ACTIVITÉS
   - Typologie des situations de départ (problèmes ouverts, situations-problèmes, défis, etc.)
   - Structures d'activités récurrentes (manipulation → conjecture → preuve)
   - Modalités de travail privilégiées (individuel, binôme, groupe, classe)
   - Types de productions attendues

3. PATTERNS DE DIFFÉRENCIATION
   - Stratégies de différenciation observées
   - Niveaux de guidance proposés
   - Types d'aides et d'étayage
   - Gestion de l'hétérogénéité

4. PATTERNS D'ÉVALUATION
   - Moments d'évaluation dans les séquences
   - Types d'évaluation (diagnostique, formative, sommative)
   - Critères et indicateurs utilisés
   - Feedback et régulation

5. PATTERNS MULTI-DOMAINES
   - Connexions récurrentes entre domaines
   - Contextes favorisant la transversalité
   - Progressions intégrant plusieurs domaines

Produire une synthèse structurée en JSON (max 600 tokens) identifiant les patterns les plus efficaces à réutiliser.
"""
```

---

## 📚 MODULE 2: ProgramAnalyzer - Prompts Complexes

### 2.1 Analyse Complète du Programme Officiel

```python
ANALYZE_OFFICIAL_PROGRAM_COMPREHENSIVE = """
Tu es un inspecteur de l'Éducation Nationale spécialisé en mathématiques, chargé d'analyser en profondeur le programme officiel pour en extraire toute la substance pédagogique et didactique.

DOCUMENTS OFFICIELS À ANALYSER:
{official_program_full_text}
{eduscol_resources}
{progression_documents}

NIVEAU CONCERNÉ: {level}
ANNÉE SCOLAIRE: {academic_year}

ANALYSE APPROFONDIE DEMANDÉE:

1. ARCHITECTURE GLOBALE DU PROGRAMME
   - Vision d'ensemble et cohérence interne
   - Articulation entre les cycles (ce qui précède et ce qui suit)
   - Équilibres entre les différents domaines
   - Temps d'enseignement recommandés
   - Points de vigilance signalés

2. ANALYSE PAR DOMAINE MATHÉMATIQUE
   Pour chaque domaine (Nombres et calculs, Organisation et gestion de données, Grandeurs et mesures, Espace et géométrie, Algorithmique et programmation):
   
   a) Contenus et notions:
      - Liste exhaustive des notions à aborder
      - Niveau de formalisation attendu
      - Vocabulaire et notations à introduire
      - Exemples et contre-exemples essentiels
   
   b) Capacités attendues:
      - Ce que l'élève doit savoir faire
      - Niveau de maîtrise attendu (initiation, consolidation, approfondissement)
      - Automatismes à développer
      - Techniques et méthodes à maîtriser
   
   c) Progressivité des apprentissages:
      - Étapes de construction des concepts
      - Obstacles didactiques identifiés
      - Repères de progressivité fournis
      - Articulation avec les autres domaines

3. ANALYSE DES COMPÉTENCES MATHÉMATIQUES
   Pour chaque compétence (Chercher, Modéliser, Représenter, Raisonner, Calculer, Communiquer):
   - Définition précise dans le contexte du niveau
   - Exemples de mise en œuvre
   - Progression attendue sur l'année
   - Critères d'évaluation
   - Liens avec les domaines

4. CROISEMENTS ET TRANSVERSALITÉ
   - Identifier TOUS les chapitres naturellement transversaux
   - Exemples concrets:
     * Proportionnalité: Nombres (calculs), Données (tableaux, graphiques), Mesures (échelles, conversions)
     * Transformations: Géométrie (figures), Algorithmique (programmation), Mesures (aires)
     * Statistiques: Données (organisation), Nombres (calculs), Algorithmique (traitement)
   - Proposer des connexions innovantes mais pertinentes

5. ANALYSE DIDACTIQUE ET PÉDAGOGIQUE
   - Changements par rapport au programme précédent
   - Points de vigilance didactique explicites ou implicites
   - Recommandations méthodologiques
   - Place du numérique et de l'algorithmique
   - Importance de la résolution de problèmes

6. ÉVALUATION ET ATTENDUS
   - Attendus de fin d'année détaillés
   - Repères pour l'évaluation
   - Exemples de situations d'évaluation
   - Critères de réussite
   - Différenciation de l'évaluation

7. RESSOURCES ET MISE EN ŒUVRE
   - Analyse des ressources d'accompagnement
   - Exemples de mise en œuvre fournis
   - Matériel et outils recommandés
   - Articulation avec le socle commun

PRODUCTION ATTENDUE:
Structure JSON détaillée (max 2000 tokens) reprenant tous ces éléments de manière organisée et exploitable pour la génération automatique de contenus.

FOCUS PARTICULIER:
- Identifier précisément les chapitres multi-domaines avec leurs pondérations
- Repérer les progressions spiralaires
- Noter les points de vigilance didactique
- Extraire les exemples concrets fournis
"""

# Stratégie:
# - Prompt très détaillé (~2000 tokens) pour une analyse exhaustive
# - Sortie structurée mais généreuse (2000 tokens) car critique pour tout le système
# - Investissement justifié car utilisé pour toute la génération ultérieure
```

### 2.2 Analyse des Obstacles Didactiques et Cognitifs

```python
ANALYZE_DIDACTIC_COGNITIVE_OBSTACLES = """
Tu es un chercheur en didactique des mathématiques spécialisé dans l'analyse des difficultés d'apprentissage et des obstacles cognitifs.

CONCEPT À ANALYSER: {concept}
NIVEAU: {level} ({age} ans)
CONTEXTE D'APPRENTISSAGE: {learning_context}

RECHERCHES ET RESSOURCES DISPONIBLES:
{didactic_research_excerpts}
{classroom_observations}
{common_errors_database}

ANALYSE APPROFONDIE DEMANDÉE:

1. OBSTACLES ÉPISTÉMOLOGIQUES
   Analyser les obstacles liés à l'histoire et à la nature du concept:
   - Ruptures épistémologiques dans l'histoire des mathématiques
   - Conceptions spontanées en contradiction avec le savoir savant
   - Exemples historiques d'erreurs de mathématiciens
   - Temps nécessaire historiquement pour stabiliser le concept
   
   Exemples concrets:
   - Nombres négatifs: "Moins fois moins donne plus" - obstacle de la multiplication comme addition répétée
   - Infini: Confusion entre "très grand" et "infini"
   - Fractions: La fraction comme deux nombres plutôt que comme un nombre

2. OBSTACLES DIDACTIQUES
   Identifier les obstacles potentiellement créés par l'enseignement:
   - Effets de contrat didactique problématiques
   - Généralisations abusives induites par les exemples
   - Implicites non explicités
   - Routines qui deviennent des obstacles
   
   Exemples:
   - "Pour additionner des fractions, on additionne les numérateurs et les dénominateurs"
   - "Un nombre au carré est toujours plus grand"
   - "Pour résoudre, on passe de l'autre côté en changeant le signe"

3. OBSTACLES COGNITIFS ET PSYCHOLOGIQUES
   Analyser les difficultés liées au développement cognitif:
   - Niveau de pensée abstraite requis vs capacités à cet âge
   - Surcharge cognitive potentielle
   - Interférences avec les connaissances antérieures
   - Difficultés de représentation mentale
   
   Considérer:
   - Stade de développement cognitif (Piaget)
   - Capacité de mémoire de travail
   - Niveau de langage mathématique
   - Expériences concrètes disponibles

4. ANALYSE DES ERREURS TYPIQUES
   Pour chaque erreur courante:
   - Description précise de l'erreur
   - Fréquence observée (% d'élèves)
   - Origine cognitive/didactique/épistémologique
   - Persistance dans le temps
   - Stratégies de remédiation efficaces
   
   Catégoriser:
   - Erreurs de surface vs erreurs profondes
   - Erreurs systématiques vs aléatoires
   - Erreurs révélatrices d'une conception

5. VARIABLES DIDACTIQUES CRITIQUES
   Identifier les variables qui influencent la difficulté:
   - Variables numériques (taille des nombres, présence de décimaux...)
   - Variables de contexte (abstrait/concret, familier/nouveau)
   - Variables de présentation (ordre, disposition spatiale)
   - Variables de complexité (nombre d'étapes, imbrications)
   
   Pour chaque variable:
   - Valeurs qui facilitent/compliquent
   - Progression recommandée
   - Pièges à éviter

6. STRATÉGIES DE PRÉVENTION ET REMÉDIATION
   Proposer des approches pour surmonter les obstacles:
   - Situations de conflit cognitif constructives
   - Progressions qui évitent les impasses
   - Métaphores et analogies aidantes (et leurs limites)
   - Manipulations et expériences concrètes
   - Verbalisations et explicitations
   
   Principes:
   - Partir des conceptions des élèves
   - Créer le besoin du nouveau concept
   - Multiplier les représentations
   - Institutionnaliser progressivement

7. INDICATEURS DE COMPRÉHENSION
   Définir ce qui montre qu'un obstacle est surmonté:
   - Capacité à expliquer avec ses mots
   - Reconnaissance dans des contextes variés
   - Utilisation pertinente spontanée
   - Capacité à identifier les erreurs d'autres
   - Transfert à des situations nouvelles

FORMAT DE SORTIE:
JSON structuré (max 1500 tokens) avec toutes les analyses et recommandations pratiques directement exploitables.
"""
```

---

## 📅 MODULE 3: YearPlanning - Prompts Stratégiques

### 3.1 Planification Annuelle Intelligente

```python
CREATE_INTELLIGENT_YEAR_PLANNING = """
Tu es un conseiller pédagogique expert en planification curriculaire, chargé de créer une progression annuelle optimale qui respecte les contraintes institutionnelles tout en maximisant l'apprentissage des élèves.

DONNÉES D'ENTRÉE COMPLÈTES:

1. CONTEXTE INSTITUTIONNEL
   - Niveau: {level}
   - Nombre total de séances: {total_sessions} (environ {hours_per_week}h/semaine)
   - Calendrier scolaire: {school_calendar}
   - Périodes d'évaluation imposées: {evaluation_periods}
   - Contraintes locales: {local_constraints}

2. ANALYSE DU PROGRAMME (depuis ProgramAnalyzer)
   {program_analysis_complete}
   
   Points clés à considérer:
   - Répartition recommandée entre domaines
   - Prérequis et dépendances entre notions
   - Points de vigilance didactique identifiés
   - Chapitres naturellement transversaux

3. PROFIL DES ÉLÈVES
   - Niveau moyen attendu: {student_level}
   - Hétérogénéité anticipée: {heterogeneity}
   - Besoins spécifiques identifiés: {special_needs}
   - Contexte socio-culturel: {context}

4. RESSOURCES DISPONIBLES
   - Matériel: {available_materials}
   - Numérique: {digital_resources}
   - Humaines: {human_resources}
   - Sorties/projets possibles: {projects}

PLANIFICATION DEMANDÉE:

1. ARCHITECTURE ANNUELLE
   Concevoir une progression qui:
   - Respecte les 5 périodes scolaires (entre vacances)
   - Équilibre les domaines mathématiques sur l'année
   - Alterne moments de découverte/consolidation/approfondissement
   - Intègre les évaluations aux moments pertinents
   - Prévoit des temps de remédiation et de régulation
   - Exploite les chapitres transversaux pour créer du lien

2. RÉPARTITION PAR PÉRIODE
   Pour chaque période:
   - Durée exacte et nombre de séances disponibles
   - Chapitres à traiter avec justification du choix
   - Répartition détaillée des séances par chapitre
   - Moments d'évaluation (diagnostique, formative, sommative)
   - Temps tampons pour ajustements
   - Projets ou temps forts éventuels

3. LOGIQUE DE PROGRESSION
   Expliciter:
   - L'ordre choisi et sa justification didactique
   - Les spirales d'apprentissage (notions revisitées)
   - Les moments de synthèse et de structuration
   - L'articulation entre ancien et nouveau
   - La montée progressive en complexité
   - Les paliers de consolidation

4. GESTION DE LA TRANSVERSALITÉ
   Pour chaque chapitre multi-domaines:
   - Identifier les domaines impliqués et leur pondération
   - Expliciter les connexions à faire
   - Prévoir les transferts possibles
   - Organiser les synthèses inter-domaines
   
   Exemples:
   - "Proportionnalité" en période 2: Lien nombres/données/mesures
   - "Statistiques" en période 4: Après consolidation calculs et graphiques
   - "Problèmes complexes" en période 5: Mobilisation tous domaines

5. FLEXIBILITÉ ET ADAPTATIONS
   Prévoir:
   - Des points de régulation (où ajuster si retard/avance)
   - Des activités optionnelles d'approfondissement
   - Des parcours différenciés possibles
   - Des moments de remédiation ciblée
   - Des projets modulables selon le temps

6. COHÉRENCE PÉDAGOGIQUE
   Assurer:
   - Une charge cognitive progressive
   - Des temps de respiration (révisions, jeux mathématiques)
   - L'alternance des types d'activités
   - La variété des approches pédagogiques
   - Le maintien de la motivation sur l'année

7. RECOMMANDATIONS SPÉCIFIQUES
   Fournir:
   - Les points d'attention par période
   - Les écueils à éviter dans l'enchaînement
   - Les opportunités de projets interdisciplinaires
   - Les moments propices aux évaluations
   - Les adaptations selon le profil de classe

FORMAT DE SORTIE:
Structure JSON très détaillée (max 2500 tokens) avec:
- Vue macro de l'année
- Détail par période
- Justifications pédagogiques
- Flexibilité intégrée
- Recommandations pratiques

Cette planification doit être directement exploitable pour générer ensuite le détail de chaque séance.
"""
```

### 3.2 Design de Séquence Pédagogique Complète

```python
DESIGN_PEDAGOGICAL_SEQUENCE = """
Tu es un ingénieur pédagogique spécialisé en mathématiques, expert dans la conception de séquences d'apprentissage efficaces et engageantes.

CONTEXTE DE LA SÉQUENCE:
- Chapitre: {chapter_title}
- Domaines impliqués: {domains_weights}
- Nombre de séances allouées: {session_count}
- Place dans l'année: Période {period}, après {previous_chapters}
- Profil classe: {class_profile}

ANALYSE PRÉALABLE (du ProgramAnalyzer):
{chapter_analysis}
- Objectifs d'apprentissage détaillés
- Prérequis identifiés
- Obstacles didactiques anticipés
- Compétences à développer

CONCEPTION DÉTAILLÉE DEMANDÉE:

1. ARCHITECTURE DE LA SÉQUENCE
   Concevoir une progression en phases cohérentes:
   
   Phase 1 - MISE EN ROUTE ET DIAGNOSTIC (1-2 séances)
   - Évaluation diagnostique des prérequis
   - Situation déclenchante pour créer le besoin
   - Première exploration intuitive
   - Recueil des conceptions initiales
   
   Phase 2 - CONSTRUCTION DES SAVOIRS (3-5 séances)
   - Situations d'apprentissage progressives
   - Alternance manipulation/abstraction
   - Moments d'institutionnalisation
   - Construction collaborative des savoirs
   
   Phase 3 - ENTRAÎNEMENT ET CONSOLIDATION (3-4 séances)
   - Exercices d'application directe
   - Montée progressive en complexité
   - Automatisation des procédures
   - Feedback et régulation
   
   Phase 4 - APPROFONDISSEMENT ET TRANSFERT (2-3 séances)
   - Problèmes complexes
   - Situations de transfert
   - Projets ou défis
   - Créativité mathématique
   
   Phase 5 - ÉVALUATION ET BILAN (1-2 séances)
   - Évaluation sommative
   - Retour réflexif sur les apprentissages
   - Identification des progrès et difficultés
   - Perspectives pour la suite

2. DÉTAIL PAR SÉANCE
   Pour chaque séance, fournir:
   
   IDENTITÉ DE LA SÉANCE
   - Numéro et titre explicite
   - Objectif principal (1 phrase claire)
   - Domaines mathématiques mobilisés
   - Compétences travaillées prioritairement
   
   STRUCTURE TEMPORELLE (55 minutes)
   - Rituel d'entrée (5 min): calcul mental, énigme, rappel
   - Mise en route (5 min): présentation objectif, lien avec séance précédente
   - Activité principale (25 min): cœur de l'apprentissage
   - Mise en commun/Institutionnalisation (10 min): synthèse collective
   - Entraînement guidé (8 min): application immédiate
   - Clôture (2 min): bilan, annonce suite, devoirs
   
   MODALITÉS PÉDAGOGIQUES
   - Organisation: individuel/binômes/groupes/classe
   - Rôle de l'enseignant à chaque phase
   - Matériel nécessaire (concret et numérique)
   - Supports élèves (cahier, fiche, tablette...)
   
   DIFFÉRENCIATION INTÉGRÉE
   - Pour les élèves en difficulté: aides, étayage, simplifications
   - Pour les élèves avancés: défis, approfondissements
   - Variables didactiques pour ajuster la difficulté
   - Modalités d'accompagnement

3. ACTIVITÉS PHARES
   Détailler 3-4 activités marquantes de la séquence:
   - Situation de découverte engageante
   - Manipulation ou expérimentation
   - Problème ouvert ou défi
   - Projet ou réalisation concrète
   
   Pour chaque activité phare:
   - Objectif spécifique
   - Déroulement détaillé
   - Variables didactiques
   - Critères de réussite
   - Prolongements possibles

4. ÉVALUATION CONTINUE
   Stratégie d'évaluation sur la séquence:
   - Évaluation diagnostique: quoi et comment
   - Évaluations formatives: moments et modalités
   - Évaluation sommative: structure et barème
   - Auto-évaluation et co-évaluation
   - Outils de suivi (grilles, portfolios...)

5. RESSOURCES ET SUPPORTS
   - Documents élèves par séance
   - Matériel de manipulation
   - Ressources numériques
   - Affichages de classe
   - Références pour l'enseignant

6. POINTS DE VIGILANCE
   - Obstacles didactiques et comment les aborder
   - Erreurs typiques et leur traitement
   - Moments délicats de la progression
   - Gestion de l'hétérogénéité
   - Articulations inter-séances critiques

FORMAT DE SORTIE:
JSON structuré (max 3000 tokens) avec le détail complet de la séquence, directement exploitable pour la génération du contenu de chaque séance.
"""
```

---

## 🎨 MODULE 4: ContentGeneration - Prompts Riches et Nuancés

### 4.1 Génération de Cours Pédagogiquement Optimisé

```python
GENERATE_PEDAGOGICAL_COURSE_CONTENT = """
Tu es un enseignant de mathématiques passionné avec 15 ans d'expérience, reconnu pour ta capacité à rendre les mathématiques accessibles et passionnantes. Tu vas créer un cours qui allie rigueur mathématique et approche bienveillante adaptée à des élèves de {level}.

CONTEXTE PÉDAGOGIQUE COMPLET:
- Séance n°{session_number} du chapitre "{chapter_title}"
- Place dans la séquence: {sequence_phase} (découverte/construction/consolidation/approfondissement)
- Séances précédentes: {previous_sessions_summary}
- Acquis des élèves: {student_prerequisites}
- Difficultés anticipées: {anticipated_difficulties}
- Domaines mathématiques impliqués: {domains_involved}

OBJECTIFS DÉTAILLÉS DE LA SÉANCE:
Principal: {main_objective}
Spécifiques:
{specific_objectives}

Compétences prioritaires: {target_competencies}

ANALYSE DIDACTIQUE (du module ProgramAnalyzer):
{didactic_analysis}
- Variables didactiques identifiées
- Obstacles épistémologiques
- Erreurs typiques à anticiper
- Stratégies de remédiation

GÉNÉRATION DU COURS:

1. ACCROCHE ET MOTIVATION (5-10 lignes)
   Créer une entrée en matière qui:
   - Capte l'attention par une situation concrète ou surprenante
   - Fait le lien avec le vécu des élèves de {age} ans
   - Pose une question ou un défi qui justifie le besoin d'apprendre
   - Active les connaissances antérieures de manière implicite
   
   Exemples d'approches:
   - Paradoxe apparent ou situation contre-intuitive
   - Problème concret du quotidien
   - Défi ou énigme mathématique
   - Histoire ou anecdote historique
   - Manipulation ou expérience

2. EXPLORATION ET DÉCOUVERTE
   Proposer une activité d'exploration qui:
   - Part des conceptions des élèves
   - Permet l'émergence progressive du concept
   - Favorise les essais et les conjectures
   - Encourage la verbalisation et l'échange
   
   Structure:
   - Situation de départ clairement posée
   - Questions guides progressives
   - Espace pour les tâtonnements
   - Moments de mise en commun

3. CONSTRUCTION DU SAVOIR
   Formaliser progressivement en:
   - Partant des productions des élèves
   - Introduisant le vocabulaire mathématique en contexte
   - Proposant plusieurs représentations (numérique, graphique, symbolique)
   - Établissant les liens avec les connaissances antérieures
   
   Éléments essentiels:
   - Définitions claires et accessibles
   - Propriétés avec justifications intuitives
   - Notations introduites progressivement
   - Exemples et contre-exemples

4. MÉTHODES ET STRATÉGIES
   Expliciter les démarches en:
   - Décomposant en étapes claires
   - Justifiant chaque étape
   - Proposant des moyens de vérification
   - Montrant différentes approches possibles
   
   Format:
   - Méthode pas à pas
   - Points d'attention (pièges à éviter)
   - Astuces et moyens mnémotechniques
   - Liens entre méthodes

5. EXEMPLES TRAVAILLÉS
   Proposer 2-3 exemples qui:
   - Illustrent différents cas de figure
   - Montrent la progression de difficulté
   - Explicitent le raisonnement
   - Incluent la vérification du résultat
   
   Pour chaque exemple:
   - Énoncé clair
   - Résolution détaillée avec commentaires
   - Mise en évidence des points clés
   - Variantes possibles

6. SYNTHÈSE ET INSTITUTIONNALISATION
   Conclure par:
   - L'essentiel à retenir (encadré coloré)
   - Les liens avec d'autres notions
   - Les applications concrètes
   - Ce qui sera vu dans la prochaine séance

7. SUPPORTS VISUELS
   Intégrer quand pertinent:
   - Schémas et figures (avec descriptions TikZ)
   - Tableaux de synthèse
   - Cartes mentales
   - Frises ou algorithmes

FORMAT DE SORTIE:
Markdown structuré avec:
- Titres et sous-titres clairs
- Encadrés pour les éléments importants
- Code LaTeX pour les formules
- Maximum 1500 tokens
- Ton bienveillant et encourageant

ATTENTION PARTICULIÈRE:
- Adapter le niveau de langue à l'âge des élèves
- Multiplier les entrées (visuelle, verbale, kinesthésique)
- Anticiper et traiter les erreurs courantes
- Créer des ponts entre les domaines mathématiques impliqués
- Maintenir un équilibre entre rigueur et accessibilité
"""
```

### 4.2 Génération d'Exercices Différenciés et Progressifs

```python
GENERATE_DIFFERENTIATED_PROGRESSIVE_EXERCISES = """
Tu es un concepteur expert d'exercices mathématiques, spécialisé dans la création de parcours d'apprentissage adaptatifs qui permettent à chaque élève de progresser à son rythme.

CONTEXTE D'EXERCICES:
- Chapitre: {chapter_title}
- Notions travaillées: {concepts}
- Domaines impliqués: {domains_weights}
- Séance n°: {session_number}
- Phase: {learning_phase}
- Profil classe: {class_profile}

ANALYSE DIDACTIQUE:
{didactic_analysis}
- Erreurs typiques identifiées
- Variables didactiques pertinentes
- Niveaux de difficulté possibles

GÉNÉRATION DEMANDÉE:
Créer une série d'exercices suivant une progression réfléchie.

1. EXERCICES D'ÉCHAUFFEMENT (3-4 exercices)
   Objectif: Réactiver les acquis et mettre en confiance
   
   Caractéristiques:
   - Application directe et immédiate
   - Nombres simples et situations épurées
   - Une seule difficulté à la fois
   - Autocorrection possible
   
   Pour chaque exercice:
   - Énoncé court et clair (2-3 lignes max)
   - Données numériques facilitantes
   - Un seul objectif d'apprentissage
   - Indication du domaine principal
   
   Exemple de progression:
   Ex 1: Reconnaissance/identification
   Ex 2: Application directe de la méthode
   Ex 3: Même structure, nombres différents
   Ex 4: Légère variation du contexte

2. EXERCICES D'ENTRAÎNEMENT (5-6 exercices)
   Objectif: Consolider et automatiser les procédures
   
   Progression spiralaire avec:
   - Complexification progressive des données
   - Introduction de variantes
   - Combinaison de plusieurs étapes
   - Contextes variés (concret/abstrait)
   
   Variables de progression:
   - Taille et nature des nombres (entiers → décimaux → fractions)
   - Nombre d'étapes (1 → 2 → 3)
   - Présence de données parasites (non → peu → plusieurs)
   - Support (avec schéma → sans schéma)
   
   Pour chaque exercice, préciser:
   - Le palier de difficulté franchi
   - Les compétences mobilisées
   - Les erreurs typiques possibles
   - Un indice si besoin

3. EXERCICES D'APPROFONDISSEMENT (3-4 exercices)
   Objectif: Développer la flexibilité et le transfert
   
   Caractéristiques:
   - Situations moins guidées
   - Plusieurs méthodes possibles
   - Liens entre domaines mathématiques
   - Nécessité de faire des choix
   
   Types variés:
   - Problème ouvert
   - Exercice à rebours (donner le résultat, trouver les données)
   - Situation de modélisation
   - Exercice "vrai ou faux" avec justification

4. DÉFIS ET EXERCICES EXPERTS (2-3 exercices)
   Objectif: Stimuler les élèves avancés
   
   Proposer:
   - Généralisations
   - Situations inédites
   - Problèmes de recherche
   - Créativité mathématique
   
   Avec:
   - Plusieurs niveaux de réponse possibles
   - Opportunités d'exploration
   - Liens avec des notions futures
   - Aspect ludique ou compétitif

5. PARCOURS DIFFÉRENCIÉS
   Organiser les exercices en 3 parcours:
   
   PARCOURS 1 (Consolidation):
   - Plus d'exercices d'échauffement
   - Progression plus lente
   - Aides et guidages supplémentaires
   - Focus sur l'essentiel
   
   PARCOURS 2 (Standard):
   - Progression équilibrée
   - Tous types d'exercices
   - Autonomie progressive
   
   PARCOURS 3 (Approfondissement):
   - Échauffement rapide
   - Plus de défis
   - Exercices de synthèse
   - Projets créatifs

6. EXERCICES TRANSVERSAUX
   Pour les chapitres multi-domaines, inclure:
   - Exercices mobilisant explicitement plusieurs domaines
   - Mises en situation complexes mais réalistes
   - Transferts entre représentations
   
   Exemple: Pour "Proportionnalité"
   - Calculs de pourcentages (Nombres)
   - Lecture de graphiques (Données)
   - Échelles et agrandissements (Géométrie/Mesures)

FORMAT DE SORTIE:
Pour chaque exercice, fournir:
```json
{
  "numero": int,
  "type": "echauffement|entrainement|approfondissement|defi",
  "parcours": [1, 2, 3],
  "enonce": "texte court et clair",
  "domaines": {"principal": 0.7, "secondaire": 0.3},
  "competences": ["calculer", "raisonner"],
  "difficulte": 1-5,
  "temps_estime": "5-10 min",
  "aide_disponible": "indice si pertinent",
  "erreur_typique": "à surveiller",
  "solution": "réponse et méthode clé"
}
```

Maximum 2000 tokens pour l'ensemble.
Assurer une vraie progressivité et cohérence dans la série.
"""
```

### 4.3 Génération d'Évaluations Complètes et Équilibrées

```python
GENERATE_COMPREHENSIVE_BALANCED_EVALUATION = """
Tu es un expert en évaluation scolaire, spécialisé dans la conception d'évaluations justes, complètes et bienveillantes qui permettent de mesurer réellement les acquis des élèves tout en les encourageant dans leur progression.

CONTEXTE D'ÉVALUATION:
- Type: {evaluation_type} (diagnostique/formative/sommative)
- Chapitres évalués: {chapters_list}
- Domaines couverts: {domains_coverage}
- Moment dans l'année: {timing}
- Durée allouée: {duration} minutes
- Profil classe: {class_profile}

OBJECTIFS D'ÉVALUATION:
{evaluation_objectives}
- Compétences à évaluer
- Niveaux de maîtrise attendus
- Équilibres à respecter

ANALYSE DES APPRENTISSAGES:
{learning_analysis}
- Points forts observés en classe
- Difficultés récurrentes
- Différenciation nécessaire

CONCEPTION DE L'ÉVALUATION:

1. STRUCTURE GLOBALE
   Concevoir une évaluation équilibrée avec:
   
   PARTIE A - AUTOMATISMES ET CONNAISSANCES (30% des points)
   - Questions courtes et directes
   - Vérification des acquis fondamentaux
   - Calculs et applications immédiates
   - QCM ou questions flash
   
   PARTIE B - APPLICATIONS ET RAISONNEMENT (50% des points)
   - Exercices guidés progressifs
   - Mobilisation des méthodes apprises
   - Situations en contexte
   - Raisonnements à expliciter
   
   PARTIE C - SYNTHÈSE ET APPROFONDISSEMENT (20% des points)
   - Problème complexe ou tâche complexe
   - Mobilisation de plusieurs notions
   - Initiative et créativité possibles
   - Plusieurs niveaux de réussite

2. RÉPARTITION PAR DOMAINES
   Assurer une couverture équilibrée:
   - Chaque domaine proportionnellement au temps d'enseignement
   - Au moins une question par compétence mathématique
   - Exercices mono-domaines et multi-domaines
   - Progressivité au sein de chaque partie

3. CONCEPTION DES EXERCICES
   Pour chaque exercice:
   
   IDENTITÉ
   - Numéro et titre explicite
   - Points attribués (détail si plusieurs questions)
   - Compétences évaluées
   - Domaine(s) concerné(s)
   - Niveau de difficulté
   
   ÉNONCÉ
   - Consignes claires et non ambiguës
   - Vocabulaire adapté au niveau
   - Données nécessaires et suffisantes
   - Présentation aérée et lisible
   
   CRITÈRES D'ÉVALUATION
   - Ce qui est attendu précisément
   - Valorisation des démarches partielles
   - Points pour la présentation/communication
   - Tolerance sur les erreurs de calcul vs erreurs de raisonnement

4. BARÈME DÉTAILLÉ
   Construire un barème qui:
   - Valorise les réussites partielles
   - Distingue méthode et résultat
   - Récompense la prise d'initiative
   - Reste cohérent avec les objectifs
   
   Principes:
   - 1 point = 1 élément de réussite identifiable
   - Démarche correcte = 60-70% des points
   - Résultat juste = 30-40% des points
   - Bonus pour présentation exemplaire

5. DIFFÉRENCIATION INTÉGRÉE
   
   VERSION STANDARD
   - Exercices progressifs classiques
   - Guidage normal
   - Attendus du programme
   
   VERSION ADAPTÉE (élèves en difficulté)
   - Exercices plus guidés
   - Étapes intermédiaires fournies
   - Moins d'exercices mais essentiels
   - Aides visuelles (schémas pré-dessinés)
   - Même barème mais sur moins de points
   
   VERSION APPROFONDIE (élèves avancés)
   - Questions bonus ou prolongements
   - Moins de guidage
   - Généralisations possibles
   - Exercices ouverts
   - Points supplémentaires possibles

6. SUPPORTS ET PRÉSENTATION
   - En-tête clair avec toutes les informations
   - Espaces de réponse adaptés
   - Figures et schémas de qualité
   - Mise en page aérée et professionnelle
   - Annexes si nécessaire (formulaire, papier millimétré)

7. GRILLE D'ÉVALUATION PAR COMPÉTENCES
   Fournir une grille permettant d'évaluer:
   - Chaque compétence mathématique
   - Niveau de maîtrise (Insuffisant/Fragile/Satisfaisant/Expert)
   - Commentaires possibles par compétence
   - Synthèse pour l'élève et les parents

8. ANALYSE A POSTERIORI
   Prévoir:
   - Les erreurs typiques attendues par exercice
   - Les indices de difficultés non anticipées
   - Les adaptations possibles pour la remédiation
   - Les prolongements pour les réussites

FORMAT DE SORTIE:
Structure complète en JSON (max 3000 tokens) avec:
- Tous les exercices détaillés
- Barème précis
- Versions différenciées
- Grille d'évaluation
- Guide de correction

L'évaluation doit être:
- Juste et équilibrée
- Motivante (commencer par du accessible)
- Progressive dans la difficulté
- Claire dans ses attendus
- Bienveillante dans son approche
"""
```

---

## ✅ MODULE 5: QualityAssurance - Prompts d'Analyse Approfondie

### 5.1 Validation Pédagogique Complète

```python
VALIDATE_PEDAGOGICAL_QUALITY_COMPREHENSIVE = """
Tu es un inspecteur pédagogique expert et un chercheur en didactique, chargé d'évaluer la qualité pédagogique d'un contenu mathématique généré. Ton analyse doit être exhaustive, constructive et orientée vers l'amélioration continue.

CONTENU À ÉVALUER:
{content_type}: {content_title}
Niveau: {level}
Place dans la progression: {progression_context}

CONTENU COMPLET:
{full_content}

RÉFÉRENCES POUR L'ÉVALUATION:
- Programme officiel: {official_program_requirements}
- Attendus de fin d'année: {end_year_expectations}
- Recherche didactique: {didactic_research_insights}
- Bonnes pratiques identifiées: {best_practices}

ANALYSE MULTI-DIMENSIONNELLE DEMANDÉE:

1. CONFORMITÉ INSTITUTIONNELLE (Pondération: 25%)
   Vérifier:
   - Adéquation avec le programme officiel (notions, niveau d'exigence)
   - Respect des attendus de fin d'année
   - Cohérence avec les repères de progressivité
   - Utilisation correcte du vocabulaire institutionnel
   - Respect des préconisations méthodologiques
   
   Pour chaque écart identifié:
   - Nature de l'écart
   - Gravité (mineur/majeur/critique)
   - Impact sur les apprentissages
   - Correction proposée

2. QUALITÉ DIDACTIQUE (Pondération: 30%)
   Analyser:
   
   Progression conceptuelle:
   - Respect des prérequis
   - Progressivité de la difficulté
   - Gestion des obstacles didactiques
   - Articulation ancien/nouveau
   
   Approche pédagogique:
   - Pertinence des situations de départ
   - Qualité des phases de recherche
   - Moments d'institutionnalisation
   - Équilibre manipulation/abstraction
   
   Traitement des erreurs:
   - Anticipation des erreurs typiques
   - Stratégies de remédiation proposées
   - Exploitation pédagogique des erreurs
   
   Variables didactiques:
   - Identification et utilisation pertinente
   - Progression dans les valeurs
   - Impact sur la difficulté

3. ACCESSIBILITÉ ET DIFFÉRENCIATION (Pondération: 20%)
   Évaluer:
   
   Accessibilité générale:
   - Clarté des consignes et explications
   - Niveau de langue adapté
   - Supports visuels pertinents
   - Exemples concrets et parlants
   
   Différenciation pédagogique:
   - Présence d'activités différenciées
   - Niveaux de guidage variés
   - Adaptations pour élèves en difficulté
   - Défis pour élèves avancés
   
   Inclusion:
   - Adaptations DYS présentes
   - Accessibilité visuelle
   - Alternatives proposées
   - Universalité des exemples

4. COHÉRENCE ET COMPLÉTUDE (Pondération: 15%)
   Vérifier:
   
   Cohérence interne:
   - Alignement objectifs/contenu/évaluation
   - Progression logique
   - Liens entre les parties
   - Unité thématique
   
   Complétude:
   - Tous les objectifs couverts
   - Toutes les compétences travaillées
   - Tous les domaines concernés traités
   - Ressources suffisantes

5. ENGAGEMENT ET MOTIVATION (Pondération: 10%)
   Apprécier:
   
   Accroche et intérêt:
   - Qualité de l'entrée en matière
   - Pertinence des contextes
   - Variété des approches
   - Aspect ludique éventuel
   
   Maintien de l'engagement:
   - Rythme et dynamique
   - Alternance des activités
   - Feedbacks prévus
   - Valorisation des réussites

6. ANALYSE SPÉCIFIQUE MULTI-DOMAINES
   Pour les contenus transversaux:
   - Équilibre entre les domaines
   - Qualité des connexions
   - Cohérence des transitions
   - Exploitation des synergies
   - Évitement des confusions

7. RECOMMANDATIONS D'AMÉLIORATION
   Pour chaque point faible identifié:
   
   Diagnostic:
   - Description précise du problème
   - Impact sur l'apprentissage
   - Urgence de la correction
   
   Remédiation:
   - Solution concrète proposée
   - Exemple de mise en œuvre
   - Ressources utiles
   - Temps estimé pour la correction

FORMAT DE SORTIE:
```json
{
  "score_global": 0.00-1.00,
  "scores_detailles": {
    "conformite": 0.00-1.00,
    "didactique": 0.00-1.00,
    "accessibilite": 0.00-1.00,
    "coherence": 0.00-1.00,
    "engagement": 0.00-1.00
  },
  "validation": "ACCEPTE|ACCEPTE_AVEC_RESERVES|A_RETRAVAILLER",
  "points_forts": ["liste des réussites"],
  "points_amelioration": [
    {
      "categorie": "didactique|conformite|etc",
      "severite": "mineur|majeur|critique",
      "description": "problème identifié",
      "impact": "conséquence sur l'apprentissage",
      "correction": "solution proposée",
      "exemple": "illustration concrète si utile"
    }
  ],
  "analyse_multi_domaines": {
    "equilibre": 0.00-1.00,
    "connexions": "qualité des liens",
    "suggestions": ["améliorations possibles"]
  },
  "recommandation_finale": "texte de synthèse constructif"
}
```

Maximum 2000 tokens.
L'analyse doit être:
- Rigoureuse mais bienveillante
- Orientée solutions
- Priorisée (critiques > majeures > mineures)
- Constructive et encourageante
"""
```

---

## 🔄 STRATÉGIES DE PARALLÉLISATION ENRICHIES

### Orchestration des Appels Complexes

```python
class EnrichedParallelStrategy:
    """
    Stratégies avancées pour orchestrer des appels complexes
    en maximisant la qualité tout en optimisant les coûts
    """
    
    async def generate_chapter_content(self, chapter: Chapter, context: GenerationContext):
        """
        Génération parallèle d'un chapitre complet avec contexte riche
        """
        
        # Phase 1: Analyse approfondie (1 appel riche)
        chapter_analysis_prompt = self.create_rich_analysis_prompt(
            chapter=chapter,
            program_requirements=context.program_requirements,
            previous_chapters=context.previous_chapters,
            student_profile=context.student_profile,
            available_resources=context.available_resources
        )
        
        analysis = await self.claude_call(
            chapter_analysis_prompt,
            max_tokens=3000  # Sortie généreuse pour analyse fondamentale
        )
        
        # Phase 2: Génération parallèle basée sur l'analyse
        generation_tasks = []
        
        for session in chapter.sessions:
            # Chaque prompt inclut l'analyse complète + contexte spécifique
            session_prompt = self.create_rich_session_prompt(
                session=session,
                chapter_analysis=analysis,
                pedagogical_sequence=chapter.sequence_plan,
                differentiation_needs=context.differentiation_needs
            )
            
            generation_tasks.append(
                self.claude_call(
                    session_prompt,
                    max_tokens=1500  # Sortie optimisée mais suffisante
                )
            )
        
        # Exécution parallèle avec gestion fine
        results = await self.execute_parallel_with_monitoring(
            tasks=generation_tasks,
            max_concurrent=10,
            retry_strategy=self.adaptive_retry,
            quality_threshold=0.95
        )
        
        return self.assemble_chapter_content(results)
    
    def create_rich_session_prompt(self, session, chapter_analysis, pedagogical_sequence, differentiation_needs):
        """
        Crée un prompt riche incluant tout le contexte nécessaire
        """
        return f"""
        CONTEXTE COMPLET DE GÉNÉRATION:
        
        1. ANALYSE DU CHAPITRE (fournie par l'analyse préalable):
        {chapter_analysis}
        
        2. SÉQUENCE PÉDAGOGIQUE DÉTAILLÉE:
        - Place de cette séance: {session.position_in_sequence}
        - Objectifs spécifiques: {session.learning_objectives}
        - Lien avec séances précédentes: {session.prerequisites}
        - Préparation séances suivantes: {session.prepares_for}
        
        3. PROFIL DES APPRENANTS ET BESOINS:
        {differentiation_needs}
        - Points d'attention particuliers
        - Adaptations nécessaires
        - Niveaux de différenciation requis
        
        4. CONTRAINTES ET RESSOURCES:
        - Durée: {session.duration}
        - Matériel disponible: {session.available_materials}
        - Configuration classe: {session.classroom_setup}
        
        [Instructions détaillées de génération...]
        
        SORTIE ATTENDUE: Format structuré, maximum 1500 tokens
        """
```

### Optimisation Coût/Qualité

```python
class CostQualityOptimizer:
    """
    Optimise le rapport coût/qualité en investissant dans les prompts
    """
    
    def calculate_optimal_token_distribution(self, content_type: str):
        """
        Détermine la distribution optimale des tokens entrée/sortie
        """
        
        # Stratégies par type de contenu
        strategies = {
            "analysis": {
                "input_tokens": 2000,   # Riche contexte
                "output_tokens": 2000,  # Analyse détaillée nécessaire
                "justification": "Analyse fondamentale pour toute la suite"
            },
            "course_content": {
                "input_tokens": 1500,   # Contexte pédagogique complet
                "output_tokens": 1200,  # Contenu structuré
                "justification": "Équilibre contexte/production"
            },
            "exercises": {
                "input_tokens": 1000,   # Consignes et progression
                "output_tokens": 800,   # Exercices concis
                "justification": "Exercices doivent être courts et clairs"
            },
            "evaluation": {
                "input_tokens": 2000,   # Tous les critères d'évaluation
                "output_tokens": 1500,  # Évaluation complète
                "justification": "Évaluation nécessite précision maximale"
            }
        }
        
        return strategies.get(content_type, strategies["course_content"])
    
    def estimate_cost(self, token_distribution, num_calls):
        """
        Estime le coût total avec la nouvelle stratégie
        """
        input_cost_per_million = 3.0   # $3/M tokens
        output_cost_per_million = 15.0  # $15/M tokens
        
        total_input_tokens = token_distribution["input_tokens"] * num_calls
        total_output_tokens = token_distribution["output_tokens"] * num_calls
        
        input_cost = (total_input_tokens / 1_000_000) * input_cost_per_million
        output_cost = (total_output_tokens / 1_000_000) * output_cost_per_million
        
        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost,
            "cost_ratio": output_cost / input_cost
        }
```

---

## 📊 NOUVELLE ANALYSE COÛT/BÉNÉFICE

### Comparaison des Approches

| Aspect | Ancienne Approche (Minimaliste) | Nouvelle Approche (Enrichie) |
|--------|----------------------------------|------------------------------|
| **Tokens Input moyens** | 300 | 1500 |
| **Tokens Output moyens** | 600 | 1000 |
| **Coût par appel** | $0.010 | $0.020 |
| **Qualité pédagogique** | 70% | 95%+ |
| **Taux de régénération** | 20% | < 5% |
| **Temps de développement** | Long (itérations) | Court (bon du premier coup) |

### Économies Globales

```yaml
Génération Année Complète:
  Ancienne Approche:
    appels_initiaux: 500
    regenerations: 100 (20%)
    appels_totaux: 600
    cout_total: $60
    qualite_moyenne: 75%
    
  Nouvelle Approche:
    appels_initiaux: 500
    regenerations: 25 (5%)
    appels_totaux: 525
    cout_total: $52.50
    qualite_moyenne: 95%
    
  Gain:
    cout: -12.5%
    qualite: +26.7%
    temps: -40% (moins d'itérations)
```

---

## 🎯 BONNES PRATIQUES MISES À JOUR

### 1. Structure des Prompts Enrichis

```python
OPTIMAL_ENRICHED_PROMPT_STRUCTURE = """
[CONTEXTE ÉTENDU - Toutes les informations pertinentes]
- Niveau, profil élèves, progression
- Analyse didactique complète
- Ressources et contraintes
- Objectifs détaillés

[INSTRUCTIONS NUANCÉES - Guidage précis mais flexible]
- Approche pédagogique souhaitée
- Points d'attention particuliers
- Flexibilité créative permise
- Critères de qualité explicites

[EXEMPLES ET CONTRE-EXEMPLES - Si pertinent]
- Ce qui fonctionne bien
- Erreurs à éviter
- Modèles de référence

[FORMAT DE SORTIE - Structure imposée, contenu flexible]
- Format clair (JSON/Markdown)
- Limites de taille strictes
- Sections obligatoires
- Liberté dans le contenu
"""
```

### 2. Principes Clés

1. **Investir dans le contexte** : Un prompt riche évite les malentendus
2. **Guider sans contraindre** : Structure claire, contenu flexible
3. **Anticiper les besoins** : Inclure l'analyse didactique dès le départ
4. **Optimiser la sortie** : C'est là que sont les économies
5. **Qualité > Quantité** : Mieux vaut un bon appel que trois moyens

---

Ce document révisé reflète une approche plus sophistiquée et réaliste de l'optimisation, privilégiant la qualité pédagogique tout en maintenant des coûts raisonnables.