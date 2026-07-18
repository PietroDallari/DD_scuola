# DD_scuola

Workstream DD (collegato a ORA) sulla **riforma dell'istruzione italiana**.
Il primo filone è il **ciclo unico scolastico** (ciclo unico di 12 anni: 5 primaria
+ 5 secondaria + 2 liceo unico, obbligo a 18 anni, superamento della separazione
precoce tra licei / tecnici / professionali); a seguire un filone su **università
e ricerca**.

## Struttura del repository

Il nostro lavoro è organizzato per filone tematico:

```
DD_scuola/
  ciclo_unico/               <- il NOSTRO lavoro sul ciclo unico (analisi, docs, note)
  universita/                <- filone università / ricerca (position paper)
  Ciclo_unico_scolastico/    <- clone locale del repo di Nazareno Lecis
                                (GITIGNORATO: non ridistribuito qui, vedi sotto)
```

### Il codice di Nazareno resta separato e di sola lettura

Il repo di Nazareno Lecis non viene copiato dentro questo repository. Va clonato
localmente come cartella nidificata (ignorata da git):

```bash
git clone https://github.com/NazarenoLecis/Ciclo_unico_scolastico.git
```

Lo teniamo **fissato (pin) su un commit specifico** per lavorare su una base
riproducibile. Per adottare gli aggiornamenti di Nazareno:

```bash
cd Ciclo_unico_scolastico
git fetch origin
git checkout <nuovo_commit>     # si "adotta" un pin più recente, in modo esplicito
```

Pin corrente: vedi `ciclo_unico/note/pin_upstream.md`.

## Regola operativa
Tutto ciò che produciamo noi va nelle **cartelle tematiche** (`ciclo_unico/`, poi
`universita/`), mai dentro il clone. Il codice di Nazareno non si modifica: è
materiale upstream di sola lettura, usato solo tramite driver esterni.
