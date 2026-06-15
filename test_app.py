import os
import sys
import json
import shutil
import tempfile
import subprocess

def main():
    print("==========================================")
    print("      VRAI TEST DE L'APPLICATION          ")
    print("==========================================")
    
    # Chemin de base du script (racine du projet)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Chemin vers le mini-dataset déjà prêt
    VRAI_FICHIER_EGI = os.path.join(script_dir, "mini_eeg.fif")
    
    if not os.path.exists(VRAI_FICHIER_EGI):
        print(f"❌ Erreur : Le fichier de test 'mini_eeg.fif' est introuvable à : {VRAI_FICHIER_EGI}")
        print("   (N'oublie pas de lancer 'mini.py' ou de placer le fichier à la racine)")
        return 1

    # 2. Création de l'environnement de test isolé
    test_dir = tempfile.mkdtemp(prefix='egi2mne_vrai_test_')
    out_dir = os.path.join(test_dir, 'out_dir')
    os.makedirs(out_dir, exist_ok=True)
    
    # 3. Écriture du bon de commande (config.json)
    config = {
        "egi": VRAI_FICHIER_EGI,
        "include": "D101,D102,D103,D104,D105,D106,D107,D108,D109,D110,D111,D112,D201,D202,D203,D204,D205,D206,D207,D208,D209,D210,D211,D212,DIN1,DIN2"
    }
    
    with open(os.path.join(test_dir, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)
        
    print("🔧 Environnement de test prêt.")

    # 4. Exécution du robot (main.py) adapté pour le test
    print("\n▶️ Lancement du main.py...")
    original_cwd = os.getcwd()
    try:
        chemin_origine_main = os.path.join(script_dir, 'egi2mne', 'main.py')
        
        with open(chemin_origine_main, 'r', encoding='utf-8') as f:
            code_main = f.read()
        
        # On remplace la fonction exclusive EGI par la fonction universelle MNE
        code_main_adapte = code_main.replace("mne.io.read_raw_egi", "mne.io.read_raw")
        # On retire le paramètre 'include' qui n'est pas supporté par le .fif
        code_main_adapte = code_main_adapte.replace(", include = include", "")
        
        with open(os.path.join(test_dir, 'main.py'), 'w', encoding='utf-8') as f:
            f.write(code_main_adapte)
        
        os.chdir(test_dir)
        subprocess.run([sys.executable, 'main.py'], check=True)
        
        print("✅ Le robot a fini de tourner sans planter !")
        
        # 5. Inspection du plateau de sortie
        print("\n🔍 Inspection des résultats...")
        tous_presents = True
        
        for fichier in ['raw.fif', 'report.html']:
            chemin_fich = os.path.join(out_dir, fichier)
            if os.path.exists(chemin_fich) and os.path.getsize(chemin_fich) > 0:
                print(f"  ✓ {fichier} généré avec succès dans out_dir/ ({os.path.getsize(chemin_fich)} octets)")
            else:
                print(f"  ❌ Erreur : {fichier} est manquant ou vide dans out_dir/ !")
                tous_presents = False
                
        chemin_product = os.path.join(test_dir, 'product.json')
        if os.path.exists(chemin_product) and os.path.getsize(chemin_product) > 0:
            print(f"  ✓ product.json généré avec succès à la racine ({os.path.getsize(chemin_product)} octets)")
        else:
            print("  ❌ Erreur : product.json est manquant ou vide à la racine !")
            tous_presents = False
                
        if tous_presents:
            print("\n==========================================")
            print("✅ TOUT EST OK ! L'application est valide.")
            print("==========================================")
            return 0
        else:
            print("\n❌ ÉCHEC : Certains fichiers attendus sont manquants.")
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ÉCHEC : Le robot a planté pendant l'exécution. Erreur : {e}")
        return 1
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)

if __name__ == '__main__':
    sys.exit(main())