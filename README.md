# Settlers (Mini Catan) – Exemplu cu Design Patterns

## Cum rulezi proiectul

1. Instaleaza dependintele:
```sh
pip install -r requirements.txt
```

2. Ruleaza jocul:
```sh
python -m client.main
```
sau (pe unele sisteme)
```sh
py -m client.main
```

## Cerinte tehnice

- Python 3.9+
- Proiect impartit pe module si pachete (ex: `client/`, `engine/`)

## Functionalitate

Aplicatia este un mini-joc de tip Catan cu interfata grafica realizata in pygame. Jucatorul joaca impotriva unui AI cu dificultate selectabila si poate plasa drumuri, plasa asezari, arunca zarul, face trade cu banca si incheia tura.

## Design Patterns folosite

### 1. Command Pattern
- De ce: Jocul are multe actiuni diferite care sunt declansate de jucator sau de AI. Pentru a pastra codul clar, fiecare actiune este tratata separat, ca un obiect propriu.
- Unde:
`engine/game/commands/`  
`engine/services/game_service.py`
- Ce rezolva: Separa logica fiecarei actiuni de logica jocului, iar codul devine mai usor de citit, testat si extins cu actiuni noi.

### 2. State Pattern
- De ce: Jocul functioneaza pe etape diferite, iar regulile nu sunt aceleasi in fiecare etapa. Este nevoie de un mod clar de a controla ce este permis la un moment dat.

- Unde:
`engine/game/states/`

- Ce rezolva: Fiecare stare gestioneaza propriile reguli. Trecerea intre etape este clara si modificarile se fac fara a afecta restul jocului.

### 3. Factory Pattern
- De ce: Comenzile si starile sunt create in mai multe locuri. Pentru a evita cod duplicat, crearea lor este centralizata.

- Unde:
`engine/game/commands/command_factory.py`  
`engine/game/states/state_factory.py`

- Ce rezolva: Crearea obiectelor este controlata dintr-un singur loc. Adaugarea de comenzi sau stari noi se face rapid si fara modificari mari.