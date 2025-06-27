#!/usr/bin/env python3
"""
Script de démonstration pour l'export de ressources en formats lisibles
"""

import asyncio
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resource_finder import ResourceFinder, ResourceQuery


async def demo_export_formats():
    """Démonstration des différents formats d'export"""
    print("📚 DÉMONSTRATION EXPORT RESSOURCES LISIBLES")
    print("=" * 60)
    
    # Créer le ResourceFinder
    finder = ResourceFinder()
    
    # Créer une requête de test
    query = ResourceQuery(
        query_text="théorème pythagore applications géométrie",
        level="4ème", 
        subject="mathématiques",
        specific_topics=["géométrie", "pythagore", "triangles"],
        resource_types=["pdf", "html"],
        max_results=5
    )
    
    print(f"🔍 Recherche: {query.query_text}")
    print(f"📊 Niveau: {query.level}")
    print(f"🎯 Nombre max de résultats: {query.max_results}")
    print()
    
    # Chercher les ressources
    resources = await finder.find_resources(query)
    
    if not resources:
        print("❌ Aucune ressource trouvée")
        return False
    
    # Créer le dossier d'export
    export_dir = Path("exported_resources")
    export_dir.mkdir(exist_ok=True)
    
    # Démonstration format console
    print("🖥️  FORMAT CONSOLE:")
    print("-" * 40)
    console_output = finder.format_resources_readable(resources, "console")
    print(console_output)
    print()
    
    # Export format Markdown
    print("📝 EXPORT FORMAT MARKDOWN...")
    markdown_file = export_dir / "ressources_pythagore.md"
    finder.export_resources(resources, markdown_file, "markdown")
    print(f"✅ Exporté vers: {markdown_file}")
    print()
    
    # Export format texte simple
    print("📄 EXPORT FORMAT TEXTE...")
    plain_file = export_dir / "ressources_pythagore.txt"
    finder.export_resources(resources, plain_file, "plain")
    print(f"✅ Exporté vers: {plain_file}")
    print()
    
    # Export format JSON
    print("🔢 EXPORT FORMAT JSON...")
    json_file = export_dir / "ressources_pythagore.json"
    finder.export_resources(resources, json_file, "json")
    print(f"✅ Exporté vers: {json_file}")
    print()
    
    # Afficher un aperçu du format Markdown
    print("👀 APERÇU FORMAT MARKDOWN:")
    print("-" * 40)
    markdown_content = finder.format_resources_readable(resources, "markdown")
    # Afficher seulement les premières lignes
    preview_lines = markdown_content.split('\n')[:20]
    print('\n'.join(preview_lines))
    if len(markdown_content.split('\n')) > 20:
        print("...")
    print()
    
    # Vérifier que les fichiers ont été créés
    created_files = []
    for export_file in [markdown_file, plain_file, json_file]:
        if export_file.exists():
            size_kb = export_file.stat().st_size / 1024
            created_files.append(f"✅ {export_file.name} ({size_kb:.1f} KB)")
        else:
            created_files.append(f"❌ {export_file.name} (échec)")
    
    print("📁 FICHIERS CRÉÉS:")
    for file_info in created_files:
        print(f"   {file_info}")
    
    return True


async def demo_export_different_queries():
    """Démonstration avec différents types de requêtes"""
    print("\n🔄 DÉMONSTRATION AVEC DIFFÉRENTES REQUÊTES")
    print("=" * 60)
    
    finder = ResourceFinder()
    export_dir = Path("exported_resources")
    
    queries = [
        {
            "name": "fractions_5eme",
            "query": ResourceQuery(
                query_text="fractions additions erreurs élèves",
                level="5ème",
                subject="mathématiques", 
                specific_topics=["fractions", "calculs"],
                resource_types=["pdf"],
                max_results=3
            ),
            "description": "📊 Fractions 5ème"
        },
        {
            "name": "equations_4eme", 
            "query": ResourceQuery(
                query_text="équations premier degré méthodologie",
                level="4ème",
                subject="mathématiques",
                specific_topics=["équations", "algèbre"],
                resource_types=["html", "pdf"],
                max_results=4
            ),
            "description": "🧮 Équations 4ème"
        }
    ]
    
    for query_info in queries:
        print(f"\n{query_info['description']}:")
        print("-" * 30)
        
        resources = await finder.find_resources(query_info['query'])
        
        if resources:
            # Export en Markdown
            output_file = export_dir / f"{query_info['name']}.md"
            finder.export_resources(resources, output_file, "markdown")
            
            print(f"📝 {len(resources)} ressources trouvées")
            print(f"💾 Exportées vers: {output_file.name}")
            
            # Afficher un résumé
            for i, resource in enumerate(resources[:2], 1):
                print(f"   {i}. {resource.title} (score: {resource.relevance_score:.2f})")
        else:
            print("❌ Aucune ressource")
    
    return True


async def main():
    """Fonction principale"""
    print("🚀 DÉMO EXPORT RESSOURCES PÉDAGOGIQUES")
    print("=" * 80)
    
    try:
        # Démonstration des formats d'export
        success1 = await demo_export_formats()
        
        # Démonstration avec différentes requêtes
        success2 = await demo_export_different_queries()
        
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ")
        print("=" * 80)
        
        if success1 and success2:
            print("✅ Toutes les démonstrations réussies!")
            print("\n🎉 CAPACITÉS DÉMONTRÉES:")
            print("   📝 Export format Markdown (documentation)")
            print("   📄 Export format texte simple")
            print("   🔢 Export format JSON (données)")
            print("   🖥️  Affichage console formaté")
            print("   📁 Création automatique de fichiers")
            print("   🔍 Recherche avec différentes requêtes")
            
            print("\n📂 FICHIERS CRÉÉS DANS 'exported_resources/':")
            export_dir = Path("exported_resources")
            if export_dir.exists():
                for file_path in export_dir.glob("*"):
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