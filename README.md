# Voted

## Projektbeschreibung:

Eine Webanwendung, die das Erstellen, Teilen und Bearbeiten von Abstimmungen, Terminplanung und Tierlists ermöglicht.

## Liste der Teammitglieder:

- Yue-Tung Cheung / 926780 / s85803@bht-berlin.de
- Johann Föll / 927615 / s85982@bht-berlin.de
- Lennart Paul Fuchs / 914135 / s84810@bht-berlin.de
- Jan Höhnen / 927099 / s86129@bht-berlin.de
- Jawad Ahmad Kobeissi / 926781 / s86083@bht-berlin.de
- Enes Sacirovic / 933907 / s87967@bht-berlin.de

## Tech Stack:

### Backend:

- Django
- SQLite

### Frontend:

- Django templates
- Bootstrap
- jQuery

## Dokumentation:

### Installation:

Zum Installieren und Ausführen des lokalen Entwicklungs-Servers wird ein Terminal bzw. eine Kommandozeilen-Applikation
benötigt.

- Python 3.11 installieren: https://www.python.org/downloads/release/python-3117/
- Poetry installieren: `pip install poetry` oder https://python-poetry.org/docs/#installation
- Git-Repository klonen: `git clone https://gitlab.bht-berlin.de/codekeepers/voted.git`
- Ins Basisverzeichnis navigieren: `cd voted/`
- Abhängigkeiten installieren: `poetry install`
- Datenbank erstellen: `poetry run python manage.py migrate`
- Entwicklungs-Server starten: `poetry run python manage.py runserver`

Der Server läuft nun lokal auf dem Port 8000: http://localhost:8000/

### User-Account:

Grundsätzlich sind in der Webanwendung alle essenziellen Funktionen für Gäste freigeschaltet. Die einzige Ausnahme sind 
persönliche Statistiken, die erst mit Erstellung eines Accounts auf der Profil-Seite sichtbar werden.

Jedoch sind bei Benutzung der Website ohne Account sämtliche Nutzerdaten an die Browser-Cookies gebunden. Diese sind 
standardmäßig für 14 Tage gültig, werden aber mit jedem erneuten Besuch der Website wieder verlängert.

Mit der Erstellung eines User-Accounts werden sämtliche Daten, wie erstellte Umfragen und abgegebene Stimmen auf den 
Account übertragen.

Durch die Verwendung von HTTPS und Passwort-Hashing sind die Daten grundsätzlich sicher gespeichert. Da es momentan 
jedoch keine Funktion zur Löschung dieser Daten gibt, wird davon abgeraten, echte Daten zu verwenden.

### Funktionsweise:

Wie in der Einleitung beschrieben, ermöglicht die Webanwendung das Erstellen von verschiedenen Abstimmungsarten. Im 
folgenden wird jede dieser Arten kurz beschrieben:

#### Umfrage:

Der einfachste Abstimmungstyp. Die Antwortmöglichkeiten bestehen aus einem kurzen Text. Die Teilnehmer müssen 
sich dann, je nach Einstellungen der Umfrage, für eine oder mehrere dieser Möglichkeiten entscheiden. Am Ende gewinnt 
die Option mit den meisten Stimmen.

#### Terminabstimmung:

Funktioniert sehr ähnlich wie die normale Umfrage, mit der Ausnahme, dass die Antwortmöglichkeiten aus einem konkreten 
Zeitstempel bestehen. Der Vorteil liegt bei der einheitlichen Darstellung für Nutzer, bspw. in verschiedenen Sprachen 
oder Zeitzonen (noch nicht implementiert).

#### Tierlist:

Besonders beim jüngeren Publikum beliebt. Eine Tierlist ist ein Stufensystem zur Einordnung von "Dingen". Diese können 
alles Mögliche sein, wie Gegenstände, Personen, oder auch abstrakte Konzepte. Die Einordnung erfolgt nach dem 
amerikanischen Schulnotensystem, von S (am besten) bis F (am schlechtesten).

Die einzelnen Objekte werden als quadratisches Bild dargestellt. Bei der Auswertung wird für jedes Objekt der Median 
ermittelt.
