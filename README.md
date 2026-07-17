# DD_scuola

Workstream DD (collegato a ORA) sulla **riforma della scuola italiana** —
in particolare il **ciclo unico scolastico** (ciclo unico di 12 anni: 5 primaria
+ 5 secondaria + 2 liceo unico, obbligo a 18 anni, superamento della
separazione precoce tra licei / tecnici / professionali).

## Struttura del repository

Questo repo segue lo stesso schema del workstream `DD_pensioni`:

```
DD_scuola/
  lavoro_dd/                 <- il NOSTRO lavoro (analisi, note, output)
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

Pin corrente: vedi `lavoro_dd/note/pin_upstream.md`.

## Regola operativa
Tutto ciò che produciamo noi va **solo dentro `lavoro_dd/`**. Il codice di
Nazareno non si modifica: è materiale upstream di sola lettura.
