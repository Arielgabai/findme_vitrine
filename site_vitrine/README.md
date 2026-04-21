# Site vitrine local

Premiere version du site vitrine statique, separee de l'app web existante.

## Ouvrir le site

Pour la version purement statique, ouvrir `site_vitrine/index.html` directement dans un navigateur.

Pour utiliser le formulaire de contact avec envoi d'e-mail direct, lancer le mini backend SMTP de cette vitrine :

```bash
cd site_vitrine
python server.py
```

Puis ouvrir `http://localhost:10000`.

## Structure

- `index.html` : contenu marketing
- `styles.css` : design premium inspire de l'app user HTML
- `app.js` : menu mobile, FAQ et animations d'apparition
- `server.py` : serveur leger pour servir la vitrine et envoyer les demandes de contact

## Variables d'environnement SMTP

Le formulaire envoie les demandes a `ariel.gabai@hotmail.fr` par defaut.

Variables a renseigner :

- `SMTP_HOST`
- `SMTP_PORT` (par defaut `587`)
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL` (optionnel, par defaut `SMTP_USERNAME`)
- `SMTP_FROM_NAME` (optionnel, par defaut `FindMe`)
- `SMTP_USE_TLS` (par defaut `true`)
- `SMTP_USE_SSL` (par defaut `false`)
- `CONTACT_TO_EMAIL` (optionnel, par defaut `ariel.gabai@hotmail.fr`)
- `PORT` (par defaut `10000`)
