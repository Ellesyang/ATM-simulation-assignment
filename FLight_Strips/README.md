1. Open INDEX.html in your browser
2. 1 person opens a server using server.py
3. server.py returns a IP that can be filled in on the site to connect to the server







\# ATC Flight Strips — Dutch FIR

\### BlueSky ATM Project



\## Installatie \& opstarten



\### Stap 1 — start server op met server.py



De server toont het IP-adres dat je aan alle andere controllers doorgeeft.



\### Stap 2 — Controllers verbinden

Open `index.html` in de browser op elke laptop.

Vul het IP-adres in de bovenbalk in, bijv: `192.168.1.5:3000`

Klik \*\*VERBIND\*\* — de groene dot bevestigt de verbinding.



---



\## CSV Importeren



Upload een CSV bestand via de \*\*IMPORTEER CSV\*\* knop. De import wordt

direct gesynchroniseerd naar alle verbonden controllers.



\### Formaat (puntkomma of komma als scheidingsteken):

```

callsign;actype;wake;from;to;sector;phase;remark

KLM1234;B738;M;EGLL;EHAM;Schiphol Approach;approach;

EZY456;A320;M;LFPG;EHAM;Schiphol Departure;departure;VFR

BAW443;B788;H;EGLL;EHAM;Noord;cruise;

AFR1890;A388;J;LFPG;EHAM;West;cruise;SUPER - extra sep!

```



\### Wake categorie (automatisch bepaald als leeg):

| Code | Categorie | Voorbeelden |

|------|-----------|-------------|

| J | Super Heavy | A380, AN-124 |

| H | Heavy | B744, B77W, A333, B787 |

| M | Medium | B738, A320, E190 |

| L | Light | C172, PC12 |



\### BlueSky .scn bestanden

Selecteer direct een .scn bestand — callsigns en vliegtuigtypes worden

automatisch uitgelezen. Sectoren staan op "Unassigned" en kunnen daarna

via handoff worden verdeeld.



---



\## Handoff

Klik \*\*HANDOFF\*\* op een strip → kies de doelsector.

De strip verdwijnt uit jouw sector en verschijnt direct bij de andere controller.



\## Shortcuts

| Toets | Actie |

|-------|-------|

| `N` | Nieuwe vlucht toevoegen |

| `F` | Zoekbalk focussen |

| `Esc` | Modals sluiten |



---



\## Sectoren

| Sector | Controller |

|--------|------------|

| Schiphol Approach | APP |

| Schiphol Departure | DEP |

| Noord | N-CTR |

| West | W-CTR |

| Zuid | Z-CTR |

| Oost | O-CTR |



