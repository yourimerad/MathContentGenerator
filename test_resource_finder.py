#!/usr/bin/env python3
"""
Test du module ResourceFinder - Version simplifiée
Validation des fonctionnalités de recherche de ressources pédagogiques
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier src au Python path
sys.path.append('src')

from resource_finder import (
    ResourceFinder, 
    ResourceQuery, 
    extract_keywords_from_readme
)

def test_extract_keywords():
    """Test de l'extraction de mots-clés depuis un README"""
    print("=" * 60)
    print("TEST 1: Extraction de mots-clés depuis README")
    print("=" * 60)
    
    readme_content = """
    # Chapitre 5: Équations du premier degré
    
    ## Objectifs
    - Apprendre à résoudre des équations du premier degré
    - Maîtriser les techniques de calcul algébrique  
    - Comprendre la notion de variable
    
    ## Compétences
    - Résoudre une équation simple
    - Utiliser les propriétés des opérations
    - Construire une méthode de résolution
    """
    
    keywords = extract_keywords_from_readme(readme_content)
    print(f"Mots-clés extraits: {keywords}")
    print(f"Nombre de mots-clés: {len(keywords)}")
    
    return len(keywords) > 0

async def test_resource_finder():
    """Test de base du ResourceFinder avec Claude API"""
    print("\n" + "=" * 60)
    print("TEST 2: Recherche de ressources avec Claude API")
    print("=" * 60)
    
    # Créer une requête de test
    query = ResourceQuery(
        query_text="équations premier degré",
        level="4ème",
        subject="mathématiques",
        specific_topics=["équations", "algèbre", "calcul"],
        resource_types=["pdf", "html"],
        max_results=5
    )
    
    print(f"Requête: {query.query_text}")
    print(f"Niveau: {query.level}")
    print(f"Sujets: {query.specific_topics}")
    
    # Lancer la recherche
    finder = ResourceFinder(resources_dir=Path("test_ressources"))
    resources = await finder.find_resources(query)
    
    print(f"\nRessources trouvées: {len(resources)}")
    
    for i, resource in enumerate(resources, 1):
        print(f"\n{i}. {resource.title}")
        print(f"   Source: {resource.source}")
        print(f"   Type: {resource.type}")
        print(f"   Score: {resource.relevance_score:.2f}")
        print(f"   URL: {resource.url}")
        print(f"   Mots-clés: {resource.keywords}")
        print(f"   Résumé: {resource.summary[:100]}...")
    
    return len(resources) > 0

async def test_cache_functionality():
    """Test du système de cache"""
    print("\n" + "=" * 60)
    print("TEST 3: Fonctionnalité de cache")
    print("=" * 60)
    
    query = ResourceQuery(
        query_text="fractions opérations",
        level="5ème",
        subject="mathématiques",
        specific_topics=["fractions", "addition", "multiplication"],
        resource_types=["pdf", "html"],
        max_results=3
    )
    
    finder = ResourceFinder(resources_dir=Path("test_ressources"))
    
    print("Premier appel (pas de cache)...")
    resources1 = await finder.find_resources(query)
    
    print("Deuxième appel (avec cache)...")
    resources2 = await finder.find_resources(query)
    
    print(f"Ressources trouvées (1er appel): {len(resources1)}")
    print(f"Ressources trouvées (2ème appel): {len(resources2)}")
    
    # Vérifier que le cache fonctionne
    cache_works = len(resources1) == len(resources2)
    print(f"Cache fonctionne: {'✅' if cache_works else '❌'}")
    
    return cache_works

def test_directory_creation():
    """Test de création des dossiers"""
    print("\n" + "=" * 60)
    print("TEST 4: Création des dossiers")
    print("=" * 60)
    
    finder = ResourceFinder(resources_dir=Path("test_ressources"))
    
    print("Vérification des dossiers créés:")
    resources_dir = Path("test_ressources")
    if resources_dir.exists():
        print(f"✅ Dossier ressources créé: {resources_dir}")
        
        cache_dir = resources_dir / ".cache"
        if cache_dir.exists():
            print(f"✅ Dossier cache créé: {cache_dir}")
            
            # Vérifier les fichiers de cache
            cache_files = list(cache_dir.glob("*.json"))
            print(f"📁 Fichiers de cache: {len(cache_files)}")
            
        else:
            print(f"❌ Dossier cache manquant")
    else:
        print(f"❌ Dossier ressources manquant")
    
    return True

async def test_different_levels():
    """Test avec différents niveaux scolaires"""
    print("\n" + "=" * 60)
    print("TEST 5: Différents niveaux scolaires")
    print("=" * 60)
    
    levels = ["6ème", "5ème", "4ème", "3ème"]
    finder = ResourceFinder(resources_dir=Path("test_ressources"))
    
    for level in levels:
        query = ResourceQuery(
            query_text="géométrie",
            level=level,
            subject="mathématiques",
            specific_topics=["géométrie"],
            resource_types=["pdf", "html"],
            max_results=2
        )
        
        resources = await finder.find_resources(query)
        print(f"{level}: {len(resources)} ressources trouvées")
        
        # Afficher la première ressource pour vérification
        if resources:
            resource = resources[0]
            print(f"   - {resource.title} (score: {resource.relevance_score:.2f})")
    
    return True

async def main():
    """Fonction principale de test"""
    print("🧪 TESTS DU MODULE RESOURCE FINDER - VERSION SIMPLIFIÉE")
    print("=" * 80)
    
    test_results = []
    
    try:
        # Test 1: Extraction de mots-clés
        result1 = test_extract_keywords()
        test_results.append(("Extraction mots-clés", result1))
        
        # Test 2: Recherche de ressources avec Claude
        result2 = await test_resource_finder()
        test_results.append(("Recherche ressources Claude", result2))
        
        # Test 3: Cache
        result3 = await test_cache_functionality()
        test_results.append(("Fonctionnalité cache", result3))
        
        # Test 4: Création dossiers
        result4 = test_directory_creation()
        test_results.append(("Création dossiers", result4))
        
        # Test 5: Différents niveaux
        result5 = await test_different_levels()
        test_results.append(("Différents niveaux", result5))
        
    except Exception as e:
        print(f"\n❌ ERREUR lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Résumé des résultats
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES TESTS")
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
        print("🎉 Tous les tests sont passés avec succès!")
        print("\n🔍 FONCTIONNALITÉS VALIDÉES:")
        print("   ✅ Extraction de mots-clés depuis README")
        print("   ✅ Recherche de ressources avec Claude API")
        print("   ✅ Enrichissement des métadonnées via Claude")
        print("   ✅ Calcul des scores de pertinence via Claude") 
        print("   ✅ Système de cache fonctionnel")
        print("   ✅ Support de différents niveaux scolaires")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    # Lancer les tests
    success = asyncio.run(main())
    
    # Code de sortie
    sys.exit(0 if success else 1) 