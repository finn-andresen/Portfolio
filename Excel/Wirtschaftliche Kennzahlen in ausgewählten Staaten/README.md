# Wirtschaftliche Kennzahlen in ausgewählten Staaten (in Excel) [German]
This project was done in German.

## Tools
- Microsoft Excel

## Datensatz
In diesem Projekt wurde ein von GOVDATA veröffentlichter [Datensatz](https://www.govdata.de/web/guest/daten/-/details/flache-bevolkerung-erwerbslosenquote-inflationsrate-bruttonationaleinkommen-und-bruttoinlandspr) zu wirtschaftlichen Kennzahlen ausgewählter Staaten im Zeitraum von 2004 bis 2021 verwendet. Der Datensatz steht in verschiedenen Dateiformaten zur Verfügung. Im Projekt wurde auf die CSV-Datei zurückgegriffen. Die Daten können aber auch direkt über den Browser als [HTML](https://www.datenportal.bmbf.de/portal/de/Tabelle-0.37.html) angesehen werden.

## Ziel
Das Ziel war es, die Daten in Microsoft Excel zu importieren, für die weitere Nutzung zu reinigen und eine Auswahl an Kennzahlen in einem dynamischen Dashboard bestehend aus Pivot-Diagrammen und Slicern zu visualisieren. In der finalen Excel-Arbeitsmappe sind zur Nachvollziehbarkeit vier verschiedene Arbeitsblätter enthalten:
- Raw CSV: Vorhandene Daten nach Einlesen der CSV-Datei.
- Cleaned Data: Daten nach erfolgter Datenreinigung (siehe unten). 
- Pivot: Erstellte Pivot-Tabellen und -Diagramme zur Nutzung im Dashboard.
- Dashboard: Verschiedene Visualisierungen in Kombination mit Slicern zur interaktiven Bedienung.

<u>Hinweis:</u> Excel ist auf Englisch eingestellt, weswegen beispielsweise das Tausendertrennzeichen ein Komma (,) und das Dezimaltrennzeichen ein Punkt (.) ist.

## Datenreinigung
Zur Reinigung der Rohdaten aus der CSV-Datei wurden folgende Schritte durchgeführt:
1. Überflüssige Zeilen ober- und unterhalb der eigentlichen Daten wurden entfernt, um die Daten einem reinen Tabellenformat näherzubringen.
1. Leere Zellen in der Spalte "Staat" wurden mit dem dazugehörigen Staat gefüllt, um alle weiteren Daten in den anderen Spalten entsprechend nach Staaten gruppieren zu können.
1. Spaltenüberschriften mit Einheiten wurden mit den tatsächlichen Bezeichnungen in der Zeile darüber getauscht, um alle Spaltenüberschriften in einer Zeile direkt über den Daten zu erhalten.
1. Alle Anzeigeeinheiten (Tsd., Mrd., % etc.) wurden in die "korrekte" Zahl umgerechnet, um Missverständnisse zu vermeiden. Bei Bedarf können in den Visualisierungen Anzeigeeinheiten aus Gründen der Übersichtlichkeit separat wieder eingeführt werden.
1. Daten wurden als Tabelle formatiert.
1. Alle Zellen mit "m" wurden durch "0" ersetzt. Je nach Ansatz könnte man hier auch auf den Mittelwert, Median oder Modus zurückgreifen.
1. Alle Spalten wurden korrekt formatiert.
