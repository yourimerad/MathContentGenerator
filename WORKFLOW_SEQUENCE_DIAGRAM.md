# 🔄 WORKFLOW & SEQUENCE DIAGRAMS - Math Content Generator

## 📊 Vue d'Ensemble du Workflow

### Principe Fondamental
Génération parallèle massive avec **prompts enrichis** pour maximiser la qualité dès la première génération.

### Métriques Clés (Nouvelle Stratégie)
- **Temps total** : < 4 heures
- **Coût total** : 45-50€
- **Appels Claude** : ~525 (incluant 5% régénération)
- **Qualité première génération** : 95%+
- **Parallélisation** : Jusqu'à 10 appels simultanés

---

## 🎭 Diagramme de Séquence Principal

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant RD as ResourceDiscovery
    participant PA as ProgramAnalyzer
    participant YP as YearPlanning
    participant CG as ContentGeneration
    participant QA as QualityAssurance
    participant OA as OutputAssembler
    participant C as Claude API
    participant Cache as Cache System

    U->>S: Input initial (niveau, contraintes)
    
    %% Phase 1: Discovery (30 min)
    S->>RD: Lance découverte ressources
    activate RD
    par Crawling parallèle
        RD->>RD: Crawl education.gouv.fr
        RD->>RD: Crawl eduscol
        RD->>RD: Crawl académies
        RD->>RD: Crawl IREM
    end
    
    RD->>Cache: Stocke ressources brutes
    
    par Analyse avec prompts enrichis
        loop Pour chaque batch de 10 documents
            RD->>C: Analyse approfondie (1500 tokens in)
            Note over C: Contexte pédagogique complet
            C-->>RD: Analyse structurée (800 tokens out)
        end
    end
    RD-->>S: 500+ ressources analysées
    deactivate RD

    %% Phase 2: Analysis (15 min)
    S->>PA: Analyse programme officiel
    activate PA
    PA->>Cache: Récupère ressources officielles
    PA->>C: Analyse complète programme (2000 tokens in)
    Note over C: Extraction exhaustive avec didactique
    C-->>PA: Structure programme (2000 tokens out)
    
    par Analyse obstacles par concept
        PA->>C: Obstacles didactiques (2000 tokens in)
        C-->>PA: Stratégies détaillées (1500 tokens out)
    end
    
    PA-->>S: Programme structuré + didactique
    deactivate PA

    %% Phase 3: Planning (20 min)
    S->>YP: Planification annuelle
    activate YP
    YP->>C: Génération planning stratégique (2500 tokens in)
    Note over C: Contexte complet + contraintes
    C-->>YP: Planning optimisé (2500 tokens out)
    
    loop Pour chaque chapitre
        YP->>C: Design séquence pédagogique (3000 tokens in)
        C-->>YP: Séquence détaillée (3000 tokens out)
    end
    
    YP-->>S: Planning 140 séances
    deactivate YP

    %% Phase 4: Generation (150 min)
    S->>CG: Génération contenus
    activate CG
    
    loop Pour chaque chapitre
        CG->>C: Analyse approfondie chapitre (3000 tokens in)
        C-->>CG: Analyse complète
        
        par Génération parallèle sessions
            loop 10 sessions en parallèle
                CG->>C: Génère cours (1500 in/1200 out)
                CG->>C: Génère exercices (1000 in/800 out)
                CG->>C: Génère évaluation (2000 in/1500 out)
            end
        end
        
        CG->>QA: Validation batch
        activate QA
        QA->>C: Validation qualité (2000 in/1000 out)
        alt Score < 95%
            QA->>CG: Demande amélioration ciblée
            CG->>C: Amélioration spécifique (500 in/400 out)
        end
        QA-->>CG: Contenu validé
        deactivate QA
    end
    
    CG-->>S: 1000+ contenus générés
    deactivate CG

    %% Phase 5: Assembly (30 min)
    S->>OA: Assemblage final
    activate OA
    OA->>OA: Structure hiérarchique
    OA->>OA: Génère métadonnées
    OA->>OA: Export multi-format
    OA-->>U: Package complet (PDF, HTML, DOCX)
    deactivate OA
```

---

## 🚀 Stratégie de Parallélisation Avancée

### Architecture des Appels Parallèles

```mermaid
graph TB
    subgraph "Phase Analyse (1 appel riche par chapitre)"
        A1[Analyse Chapitre 1<br/>3000 tokens in]
        A2[Analyse Chapitre 2<br/>3000 tokens in]
        A3[Analyse Chapitre N<br/>3000 tokens in]
    end
    
    subgraph "Phase Génération (10 sessions parallèles)"
        A1 --> G1[Sessions 1-10<br/>1500 tokens in each]
        A2 --> G2[Sessions 11-20<br/>1500 tokens in each]
        A3 --> G3[Sessions N-N+10<br/>1500 tokens in each]
    end
    
    subgraph "Résultats Structurés"
        G1 --> R1[Cours + Exercices<br/>1000 tokens out avg]
        G2 --> R2[Cours + Exercices<br/>1000 tokens out avg]
        G3 --> R3[Cours + Exercices<br/>1000 tokens out avg]
    end
```

### Optimisation des Batches

```python
# Configuration optimale pour la parallélisation
PARALLEL_STRATEGY = {
    "resource_analysis": {
        "batch_size": 10,
        "max_concurrent": 10,
        "tokens_in": 1500,
        "tokens_out": 800,
        "context": "full_pedagogical"
    },
    "content_generation": {
        "batch_size": 10,
        "max_concurrent": 10,
        "tokens_in": 1500,
        "tokens_out": 1200,
        "context": "chapter_analysis + session_specifics"
    },
    "quality_validation": {
        "batch_size": 5,
        "max_concurrent": 5,
        "tokens_in": 2000,
        "tokens_out": 1000,
        "context": "full_content + criteria"
    }
}
```

---

## 📈 Flux de Données Enrichi

### Nouvelle Approche : Contexte Riche

```mermaid
graph LR
    subgraph "Inputs Enrichis"
        I1[Programme Officiel<br/>Complet]
        I2[Analyse Didactique<br/>Recherche]
        I3[Profil Élèves<br/>Différenciation]
        I4[Contraintes<br/>Locales]
    end
    
    subgraph "Prompts Stratégiques"
        P1[Prompt 1500+ tokens<br/>Contexte exhaustif]
        P2[Instructions nuancées<br/>Flexibilité créative]
        P3[Format structuré<br/>Sortie optimisée]
    end
    
    subgraph "Génération Qualité"
        G1[Première génération<br/>95% qualité]
        G2[Peu de régénération<br/><5% des cas]
        G3[Cohérence garantie<br/>Multi-domaines]
    end
    
    I1 & I2 & I3 & I4 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> G1
    G1 --> G2
    G2 --> G3
```

---

## 🎯 Diagramme d'État - Génération de Contenu

```mermaid
stateDiagram-v2
    [*] --> Initialisation
    
    Initialisation --> AnalyseRessources
    
    AnalyseRessources --> AnalyseProgramme
    note right of AnalyseRessources
        Prompts enrichis ~1500 tokens
        Analyse approfondie
        Extraction patterns
    end
    
    AnalyseProgramme --> PlanificationAnnuelle
    note right of AnalyseProgramme
        Contexte didactique complet
        Obstacles et remédiations
        Multi-domaines natif
    end
    
    PlanificationAnnuelle --> GénérationChapitre
    
    state GénérationChapitre {
        [*] --> AnalyseChapitre
        AnalyseChapitre --> GénérationParallèle
        
        state GénérationParallèle {
            [*] --> Cours
            [*] --> Exercices
            [*] --> Évaluations
            
            Cours --> Validation
            Exercices --> Validation
            Évaluations --> Validation
        }
        
        Validation --> QualitéOK: Score > 95%
        Validation --> Amélioration: Score < 95%
        
        Amélioration --> Validation
        QualitéOK --> [*]
    }
    
    GénérationChapitre --> ChapitresSuivants: Plus de chapitres
    GénérationChapitre --> Assemblage: Tous générés
    
    ChapitresSuivants --> GénérationChapitre
    
    Assemblage --> Export
    Export --> [*]
```

---

## 🔄 Pipeline de Validation Qualité

### Workflow de Validation Multi-Critères

```mermaid
flowchart TB
    subgraph "Entrée"
        C[Contenu Généré]
        CR[Critères Référence]
    end
    
    subgraph "Validation Parallèle"
        V1[Conformité<br/>Programme]
        V2[Qualité<br/>Pédagogique]
        V3[Cohérence<br/>Multi-domaines]
        V4[Progression<br/>Difficultés]
        V5[Accessibilité<br/>Différenciation]
    end
    
    subgraph "Analyse avec Prompts Riches"
        A1[Prompt 2000 tokens<br/>Critères exhaustifs]
        A2[Validation fine<br/>Points attention]
        A3[Suggestions<br/>Amélioration]
    end
    
    subgraph "Décision"
        D{Score Global}
        OK[Validé ✓]
        AM[Amélioration<br/>Ciblée]
        REG[Régénération<br/>Complète]
    end
    
    C --> V1 & V2 & V3 & V4 & V5
    CR --> V1 & V2 & V3 & V4 & V5
    
    V1 & V2 & V3 & V4 & V5 --> A1
    A1 --> A2
    A2 --> A3
    A3 --> D
    
    D -->|>95%| OK
    D -->|85-95%| AM
    D -->|<85%| REG
    
    AM --> A1
    REG --> C
```

---

## 💰 Analyse Coût-Performance

### Comparaison Ancienne vs Nouvelle Stratégie

```mermaid
graph LR
    subgraph "Ancienne Stratégie (Minimaliste)"
        O1[Prompts: 300 tokens]
        O2[Qualité: 70%]
        O3[Régénérations: 20%]
        O4[Coût total: 60€]
    end
    
    subgraph "Nouvelle Stratégie (Enrichie)"
        N1[Prompts: 1500 tokens]
        N2[Qualité: 95%+]
        N3[Régénérations: <5%]
        N4[Coût total: 45-50€]
    end
    
    subgraph "Gains"
        G1[Qualité +35%]
        G2[Temps -40%]
        G3[Coût -20%]
        G4[Satisfaction +++]
    end
    
    O1 -.-> N1
    O2 -.-> N2
    O3 -.-> N3
    O4 -.-> N4
    
    N1 & N2 & N3 & N4 --> G1 & G2 & G3 & G4
```

### Distribution Optimale des Tokens

| Phase | Tokens In | Tokens Out | Ratio | Justification |
|-------|-----------|------------|-------|---------------|
| Analyse Programme | 2000 | 2000 | 1:1 | Fondation critique |
| Analyse Chapitre | 3000 | 3000 | 1:1 | Contexte complet nécessaire |
| Génération Cours | 1500 | 1200 | 1.25:1 | Contexte riche, sortie structurée |
| Génération Exercices | 1000 | 800 | 1.25:1 | Instructions claires, concision |
| Validation | 2000 | 1000 | 2:1 | Analyse approfondie, synthèse |

---

## 🏃 Timeline d'Exécution Détaillée

```mermaid
gantt
    title Timeline Génération Année Complète
    dateFormat HH:mm
    axisFormat %H:%M
    
    section Phase 1 - Discovery
    Crawling sites           :p1_1, 00:00, 15m
    Analyse ressources       :p1_2, after p1_1, 15m
    
    section Phase 2 - Analysis  
    Analyse programme        :p2_1, after p1_2, 10m
    Analyse didactique       :p2_2, after p2_1, 5m
    
    section Phase 3 - Planning
    Planning annuel          :p3_1, after p2_2, 10m
    Séquences chapitres      :p3_2, after p3_1, 10m
    
    section Phase 4 - Generation
    Chapitre 1              :p4_1, after p3_2, 15m
    Chapitre 2              :p4_2, after p4_1, 15m
    Chapitres 3-12          :p4_3, after p4_2, 120m
    
    section Phase 5 - Assembly
    Validation finale        :p5_1, after p4_3, 20m
    Export multi-format      :p5_2, after p5_1, 10m
    
    section Temps Total
    Durée complète          :crit, 00:00, 3h45m
```

---

## 🔐 Gestion du Cache Intelligent

### Stratégie de Cache Multi-Niveaux

```mermaid
flowchart TB
    subgraph "Niveau 1 - Hot Cache"
        H1[Analyses Programme<br/>TTL: 1 mois]
        H2[Patterns Pédagogiques<br/>TTL: 1 semaine]
        H3[Templates Validés<br/>TTL: 1 jour]
    end
    
    subgraph "Niveau 2 - Warm Cache"
        W1[Ressources Crawlées<br/>TTL: 1 semaine]
        W2[Analyses Chapitres<br/>TTL: 3 jours]
        W3[Contenus Régénérables<br/>TTL: 1 jour]
    end
    
    subgraph "Niveau 3 - Cold Storage"
        C1[Historique Générations]
        C2[Versions Précédentes]
        C3[Métriques Performance]
    end
    
    subgraph "Stratégie Hit/Miss"
        S1{Cache Hit?}
        S2[Utilise Cache]
        S3[Génère + Cache]
    end
    
    H1 & H2 & H3 --> S1
    W1 & W2 & W3 --> S1
    S1 -->|Hit| S2
    S1 -->|Miss| S3
    S3 --> H1 & H2 & H3
```

---

## 📊 Dashboard de Monitoring Temps Réel

### Métriques en Direct

```mermaid
graph TB
    subgraph "Métriques Génération"
        M1[Progression: 67%<br/>94/140 sessions]
        M2[Qualité Moyenne: 96.3%]
        M3[Tokens Utilisés: 2.1M]
        M4[Coût Actuel: 31.50€]
    end
    
    subgraph "Performance API"
        P1[Appels Parallèles: 8/10]
        P2[Latence Moyenne: 3.2s]
        P3[Taux Erreur: 0.3%]
        P4[Cache Hit: 42%]
    end
    
    subgraph "Alertes"
        A1[⚠️ Qualité Chapitre 7: 89%]
        A2[✓ Budget OK: 63% utilisé]
        A3[✓ Temps OK: On track]
    end
    
    subgraph "Actions"
        AC1[Pause]
        AC2[Ajuster Qualité]
        AC3[Voir Détails]
    end
    
    M1 & M2 & M3 & M4 --> Dashboard
    P1 & P2 & P3 & P4 --> Dashboard
    A1 & A2 & A3 --> Dashboard
    Dashboard --> AC1 & AC2 & AC3
```

---

## 🎯 Points de Contrôle Qualité

### Checkpoints Automatiques

| Checkpoint | Moment | Critères | Action si Échec |
|------------|--------|----------|-----------------|
| CP1 | Post-analyse programme | Structure complète | Analyse manuelle |
| CP2 | Post-planning | Couverture 100% | Ajuster répartition |
| CP3 | Chaque 10 sessions | Qualité >95% | Amélioration ciblée |
| CP4 | Par chapitre | Cohérence domaines | Rééquilibrage |
| CP5 | Final | Conformité globale | Validation expert |

---

## 🚀 Optimisations Futures

1. **IA Prédictive** : Anticiper les besoins de régénération
2. **Templates Dynamiques** : Auto-adaptation selon succès
3. **Feedback Loop** : Intégration retours enseignants
4. **Multi-Modèle** : Combiner Claude avec autres LLMs
5. **Edge Computing** : Génération distribuée

---

*Ce document illustre le workflow complet avec la nouvelle stratégie de prompts enrichis, démontrant comment l'investissement dans la qualité des prompts d'entrée génère des gains significatifs en qualité, temps et coût.*