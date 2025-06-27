#!/usr/bin/env python3
"""
DÉMONSTRATION RESOURCE FINDER 🚀
===============================

Démonstration des capacités avancées du ResourceFinder avec Claude API:
- Recherche intelligente de ressources pédagogiques
- Analyse de contenu via IA
- Scoring automatique de pertinence
- Génération de métadonnées enrichies
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier src au Python path
sys.path.append('src')

from resource_finder import ResourceFinder, ResourceQuery

async def demo_intelligent_search():
    """Démonstration de recherche intelligente avec scores IA"""
    print("🎯 DÉMONSTRATION: Recherche intelligente avec Claude")
    print("=" * 70)
    
    finder = ResourceFinder()
    
    # Différents types de recherches
    searches = [
        {
            "name": "🧮 Équations complexes (4ème)",
            "query": ResourceQuery(
                query_text="résolution équations premier degré difficultés élèves",
                level="4ème",
                subject="mathématiques",
                specific_topics=["équations", "algèbre", "variables", "didactique"],
                resource_types=["pdf", "html"],
                max_results=4
            )
        },
        {
            "name": "📐 Géométrie spatiale (3ème)",
            "query": ResourceQuery(
                query_text="géométrie espace volumes pyramide cône",
                level="3ème",
                subject="mathématiques",
                specific_topics=["géométrie", "volumes", "espace", "3D"],
                resource_types=["pdf", "html"],
                max_results=3
            )
        },
        {
            "name": "🔢 Fractions pédagogie (5ème)",
            "query": ResourceQuery(
                query_text="fractions addition soustraction erreurs typiques",
                level="5ème",
                subject="mathématiques",
                specific_topics=["fractions", "opérations", "erreurs", "remédiation"],
                resource_types=["pdf", "html"],
                max_results=3
            )
        }
    ]
    
    for search in searches:
        print(f"\n{search['name']}")
        print("-" * 50)
        
        resources = await finder.find_resources(search['query'])
        
        if resources:
            for i, resource in enumerate(resources, 1):
                print(f"\n📚 {i}. {resource.title}")
                print(f"   🏆 Score IA: {resource.relevance_score:.2f}/1.00")
                print(f"   🏢 Source: {resource.source}")
                print(f"   🔗 URL: {resource.url[:60]}...")
                print(f"   🧠 IA Keywords: {', '.join(resource.keywords[:4])}")
                print(f"   📝 Résumé: {resource.summary[:80]}...")
        else:
            print("❌ Aucune ressource trouvée")
    
    return True

async def demo_readme_analysis():
    """Démonstration d'analyse de README pédagogique"""
    print(f"\n🔍 DÉMONSTRATION: Analyse de README pédagogique")
    print("=" * 70)
    
    # Créer un README typique de chapitre
    sample_readme = """
    # Chapitre 7: Théorème de Pythagore
    
    ## Objectifs pédagogiques
    - Comprendre l'énoncé du théorème de Pythagore
    - Apprendre à calculer la longueur d'un côté dans un triangle rectangle
    - Maîtriser la réciproque du théorème de Pythagore
    - Résoudre des problèmes de géométrie utilisant Pythagore
    
    ## Concepts clés
    - Triangle rectangle, hypoténuse, côtés de l'angle droit
    - Relation a² + b² = c²
    - Réciproque et contraposée
    - Applications à la géométrie plane
    
    ## Difficultés prévisibles
    - Identifier le triangle rectangle dans une figure
    - Confusion entre théorème direct et réciproque
    - Erreurs de calcul avec les racines carrées
    - Application à des situations concrètes
    
    ## Suggestions méthodologiques
    - Commencer par des cas numériques simples (3,4,5)
    - Utiliser des manipulations concrètes et du matériel
    - Proposer des problèmes de la vie courante
    - Faire le lien avec l'histoire des mathématiques
    """
    
    print("📄 README à analyser:")
    print(sample_readme[:400] + "...\n")
    
    # Utiliser le ResourceFinder pour analyser ce README
    try:
        from resource_finder import find_resources_for_readme
        
        resources = await find_resources_for_readme(sample_readme, "4ème")
        
        print(f"🎯 Ressources trouvées pour ce README: {len(resources)}")
        
        if resources:
            print(f"\n📋 RESSOURCES RECOMMANDÉES PAR L'IA:")
            for i, resource in enumerate(resources[:3], 1):
                print(f"\n{i}. {resource.title}")
                print(f"   🎯 Pertinence IA: {resource.relevance_score:.2f}")
                print(f"   🎓 Adapté pour: Niveau {resource.source}")
                print(f"   💡 Pourquoi utile: {resource.summary[:100]}...")
                print(f"   🔑 Concepts couverts: {', '.join(resource.keywords[:5])}")
        
        return len(resources) > 0
        
    except Exception as e:
        print(f"❌ Erreur d'analyse: {e}")
        return False

async def demo_adaptive_scoring():
    """Démonstration du scoring adaptatif par niveau"""
    print(f"\n⚖️  DÉMONSTRATION: Scoring adaptatif par niveau")
    print("=" * 70)
    
    finder = ResourceFinder()
    
    # Même requête pour différents niveaux
    base_query_text = "proportionnalité pourcentages applications"
    levels = ["6ème", "5ème", "4ème", "3ème"]
    
    print("🔬 Analyse: Même requête, niveaux différents")
    print(f"📝 Requête: '{base_query_text}'")
    
    level_results = {}
    
    for level in levels:
        query = ResourceQuery(
            query_text=base_query_text,
            level=level,
            subject="mathématiques",
            specific_topics=["proportionnalité", "pourcentages"],
            resource_types=["pdf", "html"],
            max_results=2
        )
        
        resources = await finder.find_resources(query)
        level_results[level] = resources
        
        if resources:
            avg_score = sum(r.relevance_score for r in resources) / len(resources)
            best_resource = max(resources, key=lambda r: r.relevance_score)
            print(f"\n📊 {level}:")
            print(f"   📈 Score moyen: {avg_score:.2f}")
            print(f"   🏆 Meilleure ressource: {best_resource.title}")
            print(f"   🎯 Score max: {best_resource.relevance_score:.2f}")
        else:
            print(f"\n📊 {level}: Aucune ressource")
    
    # Analyse comparative
    print(f"\n🧠 ANALYSE COMPARATIVE PAR L'IA:")
    all_scores = []
    for level, resources in level_results.items():
        if resources:
            level_max = max(r.relevance_score for r in resources)
            all_scores.append((level, level_max))
    
    if all_scores:
        all_scores.sort(key=lambda x: x[1], reverse=True)
        print(f"   🥇 Niveau le mieux adapté: {all_scores[0][0]} (score: {all_scores[0][1]:.2f})")
        print(f"   📉 Écart de pertinence: {all_scores[0][1] - all_scores[-1][1]:.2f}")
    
    return True

async def demo_caching_performance():
    """Démonstration des performances avec cache"""
    print(f"\n⚡ DÉMONSTRATION: Performance avec cache intelligent")
    print("=" * 70)
    
    finder = ResourceFinder()
    
    query = ResourceQuery(
        query_text="statistiques moyennes médianes",
        level="3ème",
        subject="mathématiques",
        specific_topics=["statistiques", "moyennes", "médianes"],
        resource_types=["pdf", "html"],
        max_results=4
    )
    
    print("🚀 Premier appel (génération IA + cache)...")
    import time
    start_time = time.time()
    
    resources1 = await finder.find_resources(query)
    
    first_call_time = time.time() - start_time
    print(f"   ⏱️  Temps: {first_call_time:.2f}s")
    print(f"   📚 Ressources: {len(resources1)}")
    
    print(f"\n💨 Deuxième appel (depuis cache)...")
    start_time = time.time()
    
    resources2 = await finder.find_resources(query)
    
    second_call_time = time.time() - start_time
    print(f"   ⏱️  Temps: {second_call_time:.2f}s")
    print(f"   📚 Ressources: {len(resources2)}")
    
    if first_call_time > 0:
        speedup = first_call_time / max(second_call_time, 0.001)
        print(f"\n🏎️  Accélération cache: x{speedup:.1f}")
        print(f"   💡 Le cache évite les appels IA répétés")
    
    return len(resources1) == len(resources2)

async def main():
    """Démonstration complète du ResourceFinder"""
    print("🚀 DÉMONSTRATION RESOURCE FINDER AVEC CLAUDE API")
    print("=" * 80)
    print("🤖 Intelligence artificielle au service de la pédagogie")
    print("=" * 80)
    
    demos = [
        ("🎯 Recherche intelligente", demo_intelligent_search),
        ("🔍 Analyse de README", demo_readme_analysis),
        ("⚖️  Scoring adaptatif", demo_adaptive_scoring),
        ("⚡ Performance cache", demo_caching_performance)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n" + "🔸" * 40)
            result = await demo_func()
            results.append((demo_name, result))
            print(f"✅ {demo_name} terminé avec succès")
        except Exception as e:
            print(f"❌ Erreur dans {demo_name}: {e}")
            results.append((demo_name, False))
    
    # Résumé final
    print(f"\n" + "=" * 80)
    print("🏁 RÉSUMÉ DE LA DÉMONSTRATION")
    print("=" * 80)
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for demo_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {demo_name}")
    
    print(f"\n📊 Résultat: {success_count}/{total_count} démonstrations réussies")
    
    if success_count == total_count:
        print(f"\n🎉 DÉMONSTRATION COMPLÈTE RÉUSSIE!")
        print(f"\n🌟 CAPACITÉS DÉMONTRÉES:")
        print("   🧠 IA Claude pour analyse de pertinence")
        print("   🎯 Scoring intelligent adaptatif par niveau")
        print("   📚 Génération automatique de métadonnées")
        print("   🔍 Analyse sémantique de contenus pédagogiques")
        print("   ⚡ Cache intelligent pour performance")
        print("   🎓 Adaptation automatique aux niveaux scolaires")
        
        print(f"\n🚀 APPLICATIONS CONCRÈTES:")
        print("   📖 Enrichissement automatique de cours")
        print("   🔧 Aide à la préparation pédagogique")
        print("   📊 Recommandations personnalisées")
        print("   🎯 Recherche contextualisée de ressources")
        
        return True
    else:
        print(f"\n⚠️  Certaines démonstrations ont échoué")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 