import mne

# 1. Chemin vers ton gros fichier original (celui de 200 Mo)
# Remplace par ton vrai chemin absolu
chemin_gros_fichier = r"..\6a229e72e9d7821d33c2d48d\eeg"

# 2. Chargement du fichier
print("Chargement du fichier original...")
raw = mne.io.read_raw_egi(chemin_gros_fichier, preload=True)

# 3. Raccourcir le fichier : on ne garde que les 3 premi├¿res secondes
# tmin = temps de d├®but, tmax = temps de fin en secondes
print("D├®coupage des 3 premi├¿res secondes...")
raw_crop = raw.crop(tmin=0, tmax=3)

# 4. Sauvegarde du mini-fichier au format .fif (le format standard de MNE)
# On le nomme 'mini_eeg.fif' et on le met ├á la racine de ton projet
nom_sortie = "mini_eeg.fif"
raw_crop.save(nom_sortie, overwrite=True)

print(f"Ô£à Mini-dataset cr├®├® avec succ├¿s : {nom_sortie}")
print(f"Taille du fichier : {raw_crop.get_data().nbytes / 1024:.2f} Ko")
