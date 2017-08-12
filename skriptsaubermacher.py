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
    :return: Dictionary der Konfigdatei
    """
    with open(configfilepath) as infile:
        config = json.load(infile)
        infile.close()
    return config


if __name__ == '__main__':
    # Argumente parsen
    parser = argparse.ArgumentParser(description='Edward simple CMS system.')
    parser.add_argument('command', metavar='command', type=str, choices=['new', 'render', 'serve'],
                        help="""Can be "new", "render" or "serve".
                        "new" will create a new edward site.
                        "render" will render the existing edward site.
                        """)
    parser.add_argument('Konfigdateipfad', action='store', type=str, dest='configpath', default='', nargs='1',
                        help='Pfad zur Textdatei die gesäubert werden soll')
    parser.add_argument('Textdateipfad', action='store', type=str, dest='inpath', default='', nargs='+',
                        help='Pfad zur Textdatei die gesäubert werden soll')
    parser.add_argument('-o', action='store', type=str, dest='outpath', default='',
                        help='Pfad zur Ausgabedatei. Default ist Ausgabe des neuen Textes nach StdOut.')
    parser.add_argument('-s', action='store_true', type=str, dest='simulate', default='',
                        help='Simulation. Ändert nichts an den Daten, sondern gibt auf StdOut aus was er tun würde')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Verbose. Zum Debuggen.')
    global VERBOSE
    args = parser.parse_args()
    if args.verbose:
        print("setting VERBOSE = True")
        VERBOSE = True
