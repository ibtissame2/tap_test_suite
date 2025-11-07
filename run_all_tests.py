#!/usr/bin/env python3
"""
Lanceur complet de tous les tests du système TAP
"""

import sys
import os
import time

# Ajouter le chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

def run_test_suite():
    """Exécute toute la suite de tests"""
    
    print("🚀 LANCEMENT DE LA SUITE COMPLÈTE DE TESTS TAP")
    print("=" * 70)
    
    tests_results = {}
    start_time = time.time()
    
    # Liste des tests à exécuter
    test_modules = [
        ("Micro-MAC Authentication", "tests.test_micro_mac", "test_micro_mac_complet"),
        ("Timing Verification", "tests.test_timing", "test_timing_verification_complet"),
        ("Security Escalation", "tests.test_escalation", "test_security_escalation_complet"),
        ("Sensor Voting", "tests.test_voting", "test_sensor_voting_complet"),
        ("Intégration Complète", "tests.test_integration", "test_integration_complete")
    ]
    
    # Exécuter chaque test
    for test_name, module_name, function_name in test_modules:
        print(f"\n🔍 EXÉCUTION DU TEST: {test_name}")
        print("-" * 50)
        
        try:
            # Import dynamique du module
            module = __import__(module_name, fromlist=[function_name])
            test_function = getattr(module, function_name)
            
            # Exécution du test
            test_success = test_function()
            tests_results[test_name] = test_success
            
            if test_success:
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHOUÉ")
                
        except Exception as e:
            print(f"💥 {test_name}: ERREUR - {e}")
            tests_results[test_name] = False
    
    # Calcul du temps d'exécution
    execution_time = time.time() - start_time
    
    # Rapport final
    print("\n" + "=" * 70)
    print("📊 RAPPORT FINAL DE LA SUITE DE TESTS")
    print("=" * 70)
    
    tests_reussis = sum(1 for result in tests_results.values() if result)
    tests_total = len(tests_results)
    
    print(f"\n📈 RÉSULTATS PAR MODULE:")
    for test_name, success in tests_results.items():
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 SYNTHÈSE GLOBALE:")
    print(f"   Tests réussis: {tests_reussis}/{tests_total}")
    print(f"   Taux de réussite: {(tests_reussis/tests_total)*100:.1f}%")
    print(f"   Temps d'exécution: {execution_time:.2f} secondes")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if tests_reussis == tests_total:
        print("   ✅ Tous les tests sont réussis! Le système TAP est prêt pour le déploiement.")
    else:
        modules_echecs = [name for name, success in tests_results.items() if not success]
        print(f"   ⚠️  Les modules suivants nécessitent des corrections: {', '.join(modules_echecs)}")
        print("   🔧 Vérifiez les logs détaillés pour identifier les problèmes spécifiques.")
    
    # Statut de sortie
    if tests_reussis == tests_total:
        print("\n🎉 SUCCÈS: Tous les tests sont validés!")
        return True
    else:
        print("\n⚠️  ATTENTION: Certains tests ont échoué. Correction nécessaire.")
        return False

def test_individual_module(module_name):
    """Test un module individuel"""
    test_mapping = {
        "mac": ("tests.test_micro_mac", "test_micro_mac_complet"),
        "timing": ("tests.test_timing", "test_timing_verification_complet"),
        "escalation": ("tests.test_escalation", "test_security_escalation_complet"),
        "voting": ("tests.test_voting", "test_sensor_voting_complet"),
        "integration": ("tests.test_integration", "test_integration_complete")
    }
    
    if module_name in test_mapping:
        module_path, function_name = test_mapping[module_name]
        module = __import__(module_path, fromlist=[function_name])
        test_function = getattr(module, function_name)
        return test_function()
    else:
        print(f"Module inconnu: {module_name}")
        print("Modules disponibles: mac, timing, escalation, voting, integration")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Lanceur de tests du système TAP")
    parser.add_argument("--module", "-m", help="Tester un module spécifique")
    parser.add_argument("--all", "-a", action="store_true", help="Tester tous les modules")
    
    args = parser.parse_args()
    
    if args.module:
        # Test d'un module spécifique
        success = test_individual_module(args.module)
        sys.exit(0 if success else 1)
    else:
        # Test de tous les modules (par défaut)
        success = run_test_suite()
        sys.exit(0 if success else 1)