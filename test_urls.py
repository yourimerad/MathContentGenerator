#!/usr/bin/env python3
"""
Test simple pour déboguer la génération d'URLs
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resource_finder import ResourceFinder


def test_url_generation():
    """Test de la génération d'URLs"""
    print("🔍 TEST GÉNÉRATION URLS")
    print("=" * 50)
    
    # Test mode démo
    print("\n🔬 MODE DÉMO:")
    finder_demo = ResourceFinder(demo_mode=True)
    
    print(f"demo_mode: {finder_demo.demo_mode}")
    print(f"real_urls eduscol: {finder_demo.real_urls.get('eduscol', {})}")
    print(f"demo_urls eduscol: {finder_demo.demo_urls.get('eduscol', {})}")
    
    # Test URLs
    url1 = finder_demo._get_realistic_url('eduscol', 'programme', '4ème')
    url2 = finder_demo._get_realistic_url('eduscol', 'ressources', '4ème')
    url3 = finder_demo._get_realistic_url('irem', 'recherche', topic='géométrie')
    
    print(f"URL programme démo: {url1}")
    print(f"URL ressources démo: {url2}")
    print(f"URL recherche démo: {url3}")
    
    # Test mode production
    print("\n🌐 MODE PRODUCTION:")
    finder_prod = ResourceFinder(demo_mode=False)
    
    print(f"demo_mode: {finder_prod.demo_mode}")
    
    # Test URLs
    url1_prod = finder_prod._get_realistic_url('eduscol', 'programme', '4ème')
    url2_prod = finder_prod._get_realistic_url('eduscol', 'ressources', '4ème')
    url3_prod = finder_prod._get_realistic_url('irem', 'recherche', topic='géométrie')
    
    print(f"URL programme prod: {url1_prod}")
    print(f"URL ressources prod: {url2_prod}")
    print(f"URL recherche prod: {url3_prod}")
    
    # Comparaison
    print("\n📊 COMPARAISON:")
    print(f"Programme - Démo: {url1}")
    print(f"Programme - Prod: {url1_prod}")
    print(f"Différentes: {url1 != url1_prod}")
    
    return True


if __name__ == "__main__":
    test_url_generation() 