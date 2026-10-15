# Stempeluhr

Arbeitszeit am Handy stempeln: Arbeitsbeginn, Mittag Anfang, Mittag Ende, Arbeitsende. Dazu Urlaub, Krankenstand, Arztbesuche und andere Abwesenheiten, Urlaubskonto, Zeitkonto und ein Monatsbericht als CSV für die Buchhaltung.

- `docs/` – die App als Web-App (GitHub Pages). Einmal mit Internet öffnen und „Zum Startbildschirm hinzufügen“, danach läuft sie ohne Internet.
- `android/Stempeluhr.apk` – dieselbe App als Android-Datei. Jeder Push legt sie unter **Releases → app** ab.

Die Zeiten werden nur auf dem Handy gespeichert. Unter **Profil → Sicherung herunterladen** regelmäßig eine Sicherung machen.

## Neu bauen

`android/stempeluhr-source.html` ist die gemeinsame Quelle. `python3 android/build_web.py android/stempeluhr-source.html` erzeugt die Web-App (Ordner `android/web`, nach `docs/` kopieren) und die APK-Oberfläche, `python3 android/build.py <schlüssel.pem>` baut und signiert die APK. Der Signaturschlüssel liegt nicht im Repository; Updates müssen mit demselben Schlüssel signiert werden.
