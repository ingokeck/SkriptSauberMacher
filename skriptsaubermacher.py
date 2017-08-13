#!/usr/bin/env python3
#
#   Copyright 2017 Ingo R.Keck
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import json
import argparse
import os
import re
import sys

def load_config(configfilepath):
    """
    Konfigdatei laden. Die muss die Schlüssel "ersetzen" und "warnung" erhalten, und
    kann z.B. so aussehen:
    {
    "ersetzen":[{"regexp":"\\.\\.\\.","ziel":"…"},
              {"regexp":"([+-],[-+])","ziel":"±"},
              {"regexp":"  ","ziel":" "}],
    "warnung":[{"regexp":"[0-9] [(mm),(km),(nm),(cm)","warnung":"Leerzeichen zwischen Zahl und Einheit?"},
              {"regexp":"\\. [a-z]","warnung":"Kleiner Satzanfang?"},
              {"regexp":"\\?\\?\\?","warnung":"Fehlt da was?"}]
    }
    :param configfilepath: Pfad zur Konfigdatei
    :return: Listen der kompilierte ersetzen Muster und warnung Muster mit jeweils Ziel/Beschreibung und der
             regexp als string, alles jeweils als Liste:
             [[comp(regexp), Ziel, regexp],...], [[comp(regexp), Warnung, regexp],...]
    """
    global VERBOSE
    if isinstance(configfilepath, list):
        configfilepath = configfilepath[0]
    with open(configfilepath) as infile:
        config = json.load(infile)
        infile.close()
    # Übersetze alle regexp
    #ersetzen = [[re.compile(pattern["regexp"]),pattern["ziel"],pattern["regexp"]] for pattern in config["ersetzen"]]
    #warnung = [[re.compile(pattern["regexp"]),pattern["warnung"],pattern["regexp"]] for pattern in config["warnung"]]
    # besser Muster für Muster, damit es bei Problemen eine Fehlermeldung gibt.
    ersetzen = []
    for pattern in config["ersetzen"]:
        if VERBOSE:
            print("Überstetze Muster %s" % pattern["regexp"])
        ersetzen.append([re.compile(pattern["regexp"]),pattern["ziel"],pattern["regexp"]])
    warnung = []
    for pattern in config["warnung"]:
        if VERBOSE:
            print("Überstetze Muster %s" % pattern["regexp"])
        warnung.append([re.compile(pattern["regexp"]),pattern["warnung"],pattern["regexp"]])
    if VERBOSE:
        print("Ergebnisse: Ersetzten:")
        print(ersetzen)
        print("Warnen:")
        print(warnung)
    return ersetzen, warnung


def datei_saeubern(ersetzen, warnung, inpath, outpath=None, simulation=False):

    global VERBOSE
    if VERBOSE:
        if not outpath:
            print("Säubere Datei %s, Ausgabe zu StdOut" % inpath)
        else:
            print("Säubere Datei %s, Ausgabe zu %s" % (inpath, outpath))
    # Datei in Speicher laden
    with open(inpath) as infile:
        data = infile.read()
        infile.close()
    if not data:
        if VERBOSE:
            print("Datei %s ist leer, oder Fehler beim Lesen." % inpath)
        return False
    # zuerst ersetzen
    for pattern in ersetzen:
        newdata, times = pattern[0].subn(pattern[1], data)
        if simulation:
            print("Datei %s, Muster %s %d mal gefunden" % (inpath, pattern[2],times), file=sys.stderr)
        if VERBOSE:
            print("Datei %s, Muster %s %d mal gefunden" % (inpath, pattern[2], times), file=sys.stdout)
        if newdata:
            data = newdata
    # jetzt warnung
    # iterator?
    for pattern in warnung:
        iterator = pattern.finditer(data)
        for n in iterator:
            # Warnung nach stderr ausgeben
            print("Datei %s, position %d: %s" %(inpath, n.start(), pattern[1]), file=sys.stderr)
    if not simulation:
        if outpath:
            with open(outpath, 'w') as outfile:
                outfile.write(data)
                outfile.close()
        else:
            print(data, file=sys.stdout)
    return True


def FileTranslateTest(unittest.TestCase):
    def test_file_translate:
        global VERBOSE
        VERBOSE = True
        ersetzen, warnung = load_config('test.json')
        datei_saeubern(ersetzen, warnung, 'test.txt', outpath=None, simulation=True)


if __name__ == '__main__':
    # Argumente parsen
    parser = argparse.ArgumentParser(description='Edward simple CMS system.')
    parser.add_argument('configpath', action='store', type=str, nargs=1,
                        help='Konfigdateipfad. Pfad zur Textdatei die gesäubert werden soll')
    parser.add_argument('infilepath', action='store', type=str,  default='', nargs='+',
                        help='Textdateipfad. Pfad zur Textdatei die gesäubert werden soll')
    parser.add_argument('-o', action='store', type=str, dest='outprefix', default='',
                        help='Ausgabe des neuen Textes in eine Datei statt StdOut. Der Prefix wird vor die neue Datei gehängt. Also z.B. Prefix "neu_" macht aus "eingang.txt" ein "neu_eingang.txt". ')
    parser.add_argument('-s', action='store_true', dest='simulate',
                        help='Simulation. Ändert nichts an den Daten, sondern gibt auf StdOut aus was er tun würde')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Verbose. Zum Debuggen.')
    global VERBOSE
    VERBOSE = False
    args = parser.parse_args()
    if args.verbose:
        print("setting VERBOSE = True")
        VERBOSE = True
    # Konfigdatei laden
    ersetzen, warnung = load_config(args.configpath)
    if args.outprefix:
        # neue Ausgabedateien erzeugen
        outpaths = []
        for infile in args.infilepath:
            filenpath, filename = os.path.split(infile)
            outpaths.append(filenpath, args.outprefix+filename)
    #
    print(args.infilepath)
    # alle angebenenen Dateien säubern
    for n, infile in enumerate(args.infilepath):
        if args.outprefix:
            datei_saeubern(ersetzen, warnung, inpath=infile, outpath=outpaths[n], simulation=args.simulate)
        else:
            datei_saeubern(ersetzen, warnung, inpath=infile, simulation=args.simulate)
