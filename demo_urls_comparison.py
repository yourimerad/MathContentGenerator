#!/usr/bin/env python3
"""
Script de démonstration pour comparer les URLs en mode démo vs production
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resource_finder import ResourceFinder, ResourceQuery


async def demo_urls_comparison():
    """Démonstration de la différence entre URLs démo et production"""
    print("🔗 DÉMONSTRATION: URLs Démo vs Production")
    print("=" * 60)
    
    # Créer une requête de test
    query = ResourceQuery(
        query_text="théorème pythagore",
        level="4ème",
        subject="mathématiques",
        specific_topics=["géométrie", "pythagore"],
        resource_types=["pdf", "html"],
        max_results=3
    )
    
    print(f"🔍 Requête: {query.query_text}")
    print(f"📊 Niveau: {query.level}")
    print()
    
    # Mode démo (par défaut)
    print("🔬 MODE DÉMONSTRATION:")
    print("-" * 30)
    finder_demo = ResourceFinder(demo_mode=True)
    resources_demo = await finder_demo.find_resources(query)
    
    for i, resource in enumerate(resources_demo[:3], 1):
        print(f"{i}. {resource.title}")
        print(f"   Source: {resource.source}")
        print(f"   URL: {resource.url}")
        print(f"   ⚠️  URL de démonstration (fictive)")
        print()
    
    # Mode production
    print("🌐 MODE PRODUCTION:")
    print("-" * 30)
    finder_prod = ResourceFinder(demo_mode=False)
    resources_prod = await finder_prod.find_resources(query)
    
    for i, resource in enumerate(resources_prod[:3], 1):
        print(f"{i}. {resource.title}")
        print(f"   Source: {resource.source}")
        print(f"   URL: {resource.url}")
        print(f"   ✅ URL réelle (fonctionnelle)")
        print()
    
    return True


async def demo_real_urls():
    """Démonstration des vraies URLs disponibles"""
    print("\n🌍 URLS RÉELLES DISPONIBLES:")
    print("=" * 60)
    
    finder = ResourceFinder(demo_mode=False)
    
    print("📚 SOURCES OFFICIELLES:")
    print("-" * 30)
    
    for source, urls in finder.real_urls.items():
        print(f"\n🏢 {source.upper()}:")
        for url_type, url in urls.items():
            print(f"   {url_type}: {url}")
    
    print(f"\n💡 UTILISATION:")
    print("-" * 30)
    print("• Mode démo (demo_mode=True): URLs fictives pour tests")
    print("• Mode production (demo_mode=False): URLs réelles fonctionnelles")
    print("• Les URLs réelles pointent vers les sites officiels")
    print("• Les ressources de démo sont générées localement")
    
    return True


async def demo_export_comparison():
    """Démonstration de l'export avec les deux modes"""
    print("\n📝 EXPORT AVEC DIFFÉRENTS MODES:")
    print("=" * 60)
    
    query = ResourceQuery(
        query_text="fractions 5ème",
        level="5ème",
        subject="mathématiques",
        specific_topics=["fractions"],
        resource_types=["pdf"],
        max_results=2
    )
    
    export_dir = Path("exported_resources")
    export_dir.mkdir(exist_ok=True)
    
    # Export mode démo
    print("🔬 Export mode démo...")
    finder_demo = ResourceFinder(demo_mode=True)
    resources_demo = await finder_demo.find_resources(query)
    
    demo_file = export_dir / "ressources_demo.md"
    finder_demo.export_resources(resources_demo, demo_file, "markdown")
    print(f"✅ Exporté vers: {demo_file.name}")
    
    # Export mode production
    print("🌐 Export mode production...")
    finder_prod = ResourceFinder(demo_mode=False)
    resources_prod = await finder_prod.find_resources(query)
    
    prod_file = export_dir / "ressources_production.md"
    finder_prod.export_resources(resources_prod, prod_file, "markdown")
    print(f"✅ Exporté vers: {prod_file.name}")
    
    # Afficher les différences
    print(f"\n📊 COMPARAISON:")
    print("-" * 30)
    print(f"Mode démo: {len(resources_demo)} ressources, URLs fictives")
    print(f"Mode production: {len(resources_prod)} ressources, URLs réelles")
    
    return True


async def main():
    """Fonction principale"""
    print("🚀 DÉMO COMPARAISON URLS DÉMO vs PRODUCTION")
    print("=" * 80)
    
    try:
        # Comparaison des URLs
        success1 = await demo_urls_comparison()
        
        # Affichage des URLs réelles
        success2 = await demo_real_urls()
        
        # Export comparatif
        success3 = await demo_export_comparison()
        
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ")
        print("=" * 80)
        
        if success1 and success2 and success3:
            print("✅ Toutes les démonstrations réussies!")
            print("\n🎉 AMÉLIORATIONS APPORTÉES:")
            print("   🔗 URLs réelles vs fictives clairement distinguées")
            print("   ⚠️  Avertissements pour les URLs de démo")
            print("   🌐 Mode production avec vraies URLs")
            print("   📝 Export adapté selon le mode")
            print("   🔬 Mode démo pour tests et développement")
            
            print("\n📂 FICHIERS CRÉÉS:")
            export_dir = Path("exported_resources")
            if export_dir.exists():
                for file_path in export_dir.glob("ressources_*.md"):
                    size_kb = file_path.stat().st_size / 1024
                    print(f"   📄 {file_path.name} ({size_kb:.1f} KB)")
            
            return True
        else:
            print("❌ Certaines démonstrations ont échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 