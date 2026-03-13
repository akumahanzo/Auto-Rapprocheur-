📘 Excel Reconciler - Guide Administrateur pour la Gestion des Comptes
1. Introduction

Ce document explique comment fonctionne le système de login et d’activation des comptes utilisateurs pour l’application Excel Reconciler (ISS - IngeSoft Solution).

Le système permet :

La création de comptes utilisateurs via un formulaire initial.

La validation des comptes par un administrateur.

L’activation du compte avec une clé d’activation.

La gestion sécurisée des mots de passe (hachés) et des clés.

2. Création de compte par l’utilisateur

Lorsqu’un utilisateur ouvre l’application pour la première fois, il doit créer un compte s’il n’en a pas.

Le formulaire demande les informations suivantes :

Nom complet

Email

Organisation

Solution/Logiciel (ex : Excel Reconciler)

Une fois soumis, la demande est envoyée au(x) mail(s) des administrateurs configurés dans admin_data/config.json.

⚠️ Important : Ce fichier contient les emails des admins qui recevront la demande. Ne pas exposer ce fichier publiquement.

3. Validation par l’administrateur

Les admins reçoivent la demande de création de compte.

Pour chaque demande approuvée, l’admin génère :

Nom d’utilisateur

Mot de passe (qui sera automatiquement haché)

Clé d’activation unique

Ces informations sont sauvegardées dans les fichiers JSON sécurisés :

admin_data/users.json → Stocke le nom d’utilisateur et le mot de passe haché.

admin_data/activation_keys.json → Stocke les clés d’activation valides et associées aux utilisateurs.

⚠️ Ne pas modifier directement ces fichiers sauf pour la gestion des comptes.

4. Activation du compte utilisateur

L’utilisateur reçoit par mail :

Son nom d’utilisateur

Son mot de passe

Sa clé d’activation

Lors du premier login, l’utilisateur doit :

Entrer son nom d’utilisateur et mot de passe.

Saisir la clé d’activation fournie.

Si la clé d’activation est valide, le compte est créé et activé, et l’utilisateur peut accéder à l’application.

5. Gestion des utilisateurs

Ajouter un nouvel utilisateur : suivre le processus décrit en sections 2 et 3.

Supprimer ou désactiver un utilisateur : retirer ou désactiver son entrée dans users.json et/ou activation_keys.json.

Réinitialiser un mot de passe : générer un nouveau mot de passe, le hacher et mettre à jour users.json.

Protéger les fichiers sensibles : ne jamais pousser users.json ou activation_keys.json sur un dépôt public.

6. Sécurité

Les mots de passe sont hachés avec SHA256 pour la sécurité.

Les clés d’activation sont uniques et expirables si besoin.

Les emails et informations sensibles doivent être stockés uniquement dans admin_data/ et jamais sur un dépôt public.

7. Fichiers importants
Fichier	Description
admin_data/config.json	Liste des emails administrateurs.
admin_data/users.json	Comptes utilisateurs (nom, mot de passe haché).
admin_data/activation_keys.json	Clés d’activation valides pour les utilisateurs.
8. Procédure pour un nouvel utilisateur

L’utilisateur ouvre l’application et crée une demande de compte.

L’admin reçoit l’email et génère le nom d’utilisateur, mot de passe, et clé.

L’admin envoie ces informations à l’utilisateur.

L’utilisateur se connecte avec ces informations et la clé.
