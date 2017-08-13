# SkriptSauberMacher
Ein kleines Python-Skript das darauf ausgelegt ist, Texte automatisiert typographisch sauber zu machen. Die Idee ist verschiedene RegExp zu definieren die dann entweder automatisiert abgearbeitet werden, oder eine Warnung ausgeben. Warum nicht awk? Weil später wohl ein bißchen AI dazu kommen könnte.

# Aufbau
Das Skript liest die Konfiguration aus einer Konfig-Datei ein, die folgende Teile hat:

* ersetzen: Alle RegExp hier werden automatisiert durch ein Ziel pro RegExp ersetz
* warnung: Alle RegExp hier werden auf StdOut mit Dateiname und Ziele und entsprechende Warnung ausgegeben

Die Konfig-Datei ist JSON und sieht z.B. so aus:

```json
{
  "ersetzen":[{"regexp":"\\.\\.\\.","ziel":"…"},
              {"regexp":"\\+\\-","ziel":"±"},
              {"regexp":"  *","ziel":" "}],
  "warnung":[{"regexp":"[0-9] [(mm)(km)(nm)(cm)]","warnung":"Leerzeichen zwischen Zahl und Einheit?"},
              {"regexp":"[0-9][(mm)(km)(nm)(cm)]","warnung":"Kein Leerzeichen zwischen Zahl und Einheit?"},
              {"regexp":"\\. [a-z]","warnung":"Kleiner Satzanfang?"},
              {"regexp":"\\?\\?\\?","warnung":"Fehlt da was?"}]
}
```

# Aufruf
Das Skript wird so aufgerufen:

```
skriptsaubermacher [option] Konfigdateipfad Textdateipfad
```

Optionen:
<dl>
  <dt>-v</dt>
  <dd>Verbose. Erzählt was es macht.</dd>
  <dt>-o Ausgabedatei-Prefix:</dt>
  <dd>Ausgabe des neuen Textes in eine Datei statt StdOut. Der Prefix wird vor die neue Datei gehängt. 
      Also z.B. Prefix 'neu_' macht aus 'eingang.txt' ein 'neu_eingang.txt'.</dd>
  <dt>-s:</dt>
  <dd>Simulation: Gibt auf StdOut aus was es tun würde, macht aber nichts.</dd>
</dl>

# Lizenz
GNU AFFERO GENERAL PUBLIC LICENSE Version 3
