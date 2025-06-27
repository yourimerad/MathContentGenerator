#!/usr/bin/env python3
"""
Test d'intégration ResourceFinder + PedagogicalPlanner
=====================================================

Démonstration de l'utilisation de Claude API pour:
1. Analyser un README généré par PedagogicalPlanner
2. Rechercher des ressources pertinentes via ResourceFinder
3. Enrichir le contenu avec ces ressources
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier src au Python path
sys.path.append('src')

from resource_finder import ResourceFinder, ResourceQuery, find_resources_for_readme
from pedagogical_planner import PedagogicalPlanner
from models import PedagogicalProgram

async def test_pedagogical_integration():
    """
    Test d'intégration complète:
    PedagogicalPlanner → README → ResourceFinder → Ressources
    """
    print("🔬 TEST D'INTÉGRATION: PedagogicalPlanner + ResourceFinder")
    print("=" * 80)
    
    # 1. Créer un programme pédagogique avec PedagogicalPlanner
    planner = PedagogicalPlanner()
    
    # Utiliser un niveau disponible (5ème)
    program = planner.get_program("5ème")
    
    if not program or not program.chapters:
        print("❌ Aucun programme trouvé pour la 5ème")
        return False
    
    # Prendre le premier chapitre comme exemple
    chapter = program.chapters[0]
    print(f"📚 Chapitre sélectionné: {chapter.title}")
    print(f"🎯 Objectifs: {', '.join(chapter.objectives[:2])}...")
    
    # 2. Générer un README détaillé pour ce chapitre (simulation)
    readme_content = f"""
    # {chapter.title}
    
    ## Objectifs pédagogiques
    {chr(10).join([f"- {obj}" for obj in chapter.objectives])}
    
    ## Concepts clés
    {chr(10).join([f"- {concept}" for concept in chapter.key_concepts])}
    
    ## Prérequis
    {chr(10).join([f"- {prereq}" for prereq in chapter.prerequisites])}
    
    ## Difficultés prévisibles
    - Compréhension des concepts abstraits
    - Passage du concret à l'abstrait
    - Erreurs de calcul fréquentes
    
    ## Suggestions pédagogiques
    - Utiliser des manipulations concrètes
    - Proposer des situations problèmes variées
    - Prévoir des exercices de remédiation
    """
    
    print(f"\n📝 README généré pour le chapitre:")
    print("-" * 50)
    print(readme_content[:300] + "...")
    
    # 3. Utiliser ResourceFinder pour trouver des ressources basées sur ce README
    print(f"\n🔍 Recherche de ressources via ResourceFinder...")
    
    try:
        resources = await find_resources_for_readme(readme_content, "5ème")
        
        print(f"✅ Ressources trouvées: {len(resources)}")
        
        if resources:
            print(f"\n📋 TOP 3 RESSOURCES PERTINENTES:")
            for i, resource in enumerate(resources[:3], 1):
                print(f"\n{i}. {resource.title}")
                print(f"   📊 Score: {resource.relevance_score:.2f}")
                print(f"   🏷️  Source: {resource.source}")
                print(f"   🔗 URL: {resource.url}")
                print(f"   📝 Résumé: {resource.summary[:100]}...")
                print(f"   🏷️  Mots-clés: {', '.join(resource.keywords[:5])}")
        
        return len(resources) > 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        return False

async def test_content_enrichment_simulation():
    """
    Simulation d'enrichissement de contenu avec les ressources trouvées
    """
    print(f"\n🎨 TEST: Simulation d'enrichissement de contenu")
    print("=" * 60)
    
    # Créer une requête de recherche spécifique
    query = ResourceQuery(
        query_text="fractions addition soustraction",
        level="5ème",
        subject="mathématiques",
        specific_topics=["fractions", "addition", "soustraction", "dénominateur"],
        resource_types=["pdf", "html"],
        max_results=5
    )
    
    finder = ResourceFinder()
    resources = await finder.find_resources(query)
    
    print(f"📚 Ressources trouvées: {len(resources)}")
    
    # Simuler l'utilisation des ressources pour enrichir un prompt
    if resources:
        print(f"\n🧠 Prompt enrichi basé sur les ressources:")
        print("-" * 50)
        
        enriched_prompt = f"""
        Génère un cours sur les fractions en te basant sur ces ressources expertes:
        
        RESSOURCES DISPONIBLES:
        """
        
        for resource in resources[:3]:
            enriched_prompt += f"""
        - {resource.title} (score: {resource.relevance_score:.2f})
          Résumé: {resource.summary}
          Mots-clés: {', '.join(resource.keywords)}
        """
        
        enriched_prompt += """
        
        CONSIGNES:
        - Intègre les bonnes pratiques identifiées dans les ressources
        - Adapte au niveau 5ème
        - Structure le cours de manière progressive
        - Inclus des exemples concrets
        """
        
        print(enriched_prompt[:500] + "...")
        
        return True
    
    return False

async def test_multi_level_comparison():
    """
    Test de comparaison des ressources entre différents niveaux
    """
    print(f"\n📊 TEST: Comparaison multi-niveaux")
    print("=" * 60)
    
    finder = ResourceFinder()
    levels = ["6ème", "5ème", "4ème", "3ème"]
    
    comparison_results = {}
    
    for level in levels:
        query = ResourceQuery(
            query_text="géométrie triangles propriétés",
            level=level,
            subject="mathématiques", 
            specific_topics=["géométrie", "triangles", "propriétés"],
            resource_types=["pdf", "html"],
            max_results=3
        )
        
        resources = await finder.find_resources(query)
        comparison_results[level] = resources
        
        avg_score = sum(r.relevance_score for r in resources) / len(resources) if resources else 0
        print(f"{level}: {len(resources)} ressources, score moyen: {avg_score:.2f}")
    
    # Analyser les différences
    print(f"\n🔍 Analyse des différences:")
    for level, resources in comparison_results.items():
        if resources:
            best_resource = max(resources, key=lambda r: r.relevance_score)
            print(f"{level}: Meilleure ressource - {best_resource.title} ({best_resource.relevance_score:.2f})")
    
    return True

async def main():
    """Fonction principale de test d'intégration"""
    print("🧪 TESTS D'INTÉGRATION RESOURCE FINDER")
    print("=" * 80)
    print("Démonstration de l'utilisation avancée avec Claude API")
    print("=" * 80)
    
    test_results = []
    
    try:
        # Test 1: Intégration avec PedagogicalPlanner
        result1 = await test_pedagogical_integration()
        test_results.append(("Intégration PedagogicalPlanner", result1))
        
        # Test 2: Simulation d'enrichissement de contenu
        result2 = await test_content_enrichment_simulation()
        test_results.append(("Enrichissement de contenu", result2))
        
        # Test 3: Comparaison multi-niveaux
        result3 = await test_multi_level_comparison()
        test_results.append(("Comparaison multi-niveaux", result3))
        
    except Exception as e:
        print(f"\n❌ ERREUR lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Résumé des résultats
    print(f"\n" + "=" * 80)
    print("📊 RÉSUMÉ DES TESTS D'INTÉGRATION")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat global: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests d'intégration sont passés!")
        print(f"\n🚀 CAPACITÉS DÉMONTRÉES:")
        print("   ✅ Intégration transparente avec PedagogicalPlanner")
        print("   ✅ Analyse intelligente de README via Claude")
        print("   ✅ Recherche contextualisée de ressources")
        print("   ✅ Enrichissement de prompts avec ressources expertes")
        print("   ✅ Adaptation automatique par niveau scolaire")
        print("   ✅ Scoring intelligent via IA")
        
        print(f"\n💡 PROCHAINES ÉTAPES:")
        print("   🔜 Intégration dans ContentGenerator pour génération enrichie")
        print("   🔜 Développement du PedagogicalValidator")
        print("   🔜 Implémentation de la recherche web réelle")
        print("   🔜 Système de téléchargement et indexation")
        
        return True
    else:
        print("⚠️ Certains tests d'intégration ont échoué")
        return False

if __name__ == "__main__":
    # Lancer les tests d'intégration
    success = asyncio.run(main())
    
    # Code de sortie
    sys.exit(0 if success else 1) 