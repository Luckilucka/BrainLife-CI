# 🚀 Modèle d'Intégration Continue (CI) pour Applications BrainLife

Ce dépôt est un modèle clé en main pour mettre en place facilement une **Intégration Continue (CI)** via GitHub Actions sur n'importe quelle application BrainLife.

---

## 🎯 Objectif
Permettre aux développeurs de tester automatiquement la logique de leur application (robot) à chaque modification de code, en utilisant un jeu de données miniaturisé au format standard `.fif`.

---

## 📂 Structure du modèle

- `.github/workflows/ci.yml` : Le cerveau de l'automatisation.
- `mini.py` : Script utilitaire pour réduire la taille de vos jeux de données originaux.
- `test_app.py` : Script de test modulable simulant l'environnement BrainLife.

---

## 🛠️ Mode d'emploi

### 1. Préparation
Téléchargez (en format ZIP) ce dépôt modèle sur votre ordinateur.

Extrayez les fichiers dans un nouveau dossier qui portera le nom de votre projet.

Ouvrez votre terminal dans ce dossier  et tapez pour créer un dépôt Git propre :

```bash
git init
```


### 2. Importer le code de votre application

Insérer votre application à la racine de ce projet en tapant : 

```bash
git clone {votre_url.git}
```

⚠️ Attention : *Assurez-vous de bien supprimer le dossier caché .git à l'intérieur de votre dossier d'application pour éviter les conflits de dépôts imbriqués. Vous pouvez afficher celui-ci via votre Explorateur de fichiers 📂 ou en tapant :*

```bash
dir /a #Via le CMD
ls -force # via le PowerShell
ls -a # Via Linux ou MacOS
```

### 3. Créer votre mini-dataset 📊

⚠️ Attention : *Votre fichier .egi ne peut se situer dans votre dépot git car il est surement trop lourd, vérifiez bien de ne pas l'avoir mis dans votre repértoire de travail actuel.* 
*Nous vous proposons donc de le réduire à quelque Mo via "mini.py", voici la démarche...*

Ouvrez le fichier mini.py.

Modifiez la variable __chemin_gros_fichier__ pour qu'elle pointe vers votre jeu de données original sur votre ordinateur.

Exécutez python mini.py dans votre terminal.

Un fichier mini_eeg.fif (très léger) sera généré à la racine. Vous pouvez maintenant supprimer ou ignorer (via .gitignore) votre gros jeu de données ou le déplacer carrèment dans un autre dossier.



### 4. Adapter le script de test 📜

Ouvrez le fichier test_app.py.

Modifiez la variable pointant vers le dossier de votre application (cherchez la ligne :

```bash
chemin_origine_main = os.path.join(script_dir, '...', 'main.py')
```

, ce sont ces 3 petits points à modifier par votre nom de dossier.)

Ajustez le dictionnaire config pour qu'il corresponde aux entrées attendues par le config.json de votre application.

Vérifiez la section "Inspection du plateau de sortie" en bas du script pour vous assurer qu'elle teste bien les fichiers que votre application est censée générer.

### 5. Lancer l'automatisation

Ajoutez vos fichiers à Git : 

```bash
git add .

git commit -m "Mise en place de la CI"

git push -u origin main

```

Allez sur la page de votre dépôt GitHub, cliquez sur l'onglet Actions et admirez la machine virtuelle valider votre code ! En fonction du résultat du test, vous saurez si vos modification sont fonctionelles !