# AGENTS.md

## Python environment
Canonical environment: `.venv`

Run Python, tests, lint, and tooling by calling the environment's binaries directly via
their `.venv/bin/` path.

Windows
```bash
.venv/Scripts/pip
.venv/Scripts/python -m pytest
```

Unix:
```bash
.venv/bin/pip
.venv/bin/python -m pytest
```

## Setup commands
- Install deps: `pip install -r ./requirements.txt -r ./requirementsextra.txt`
- Start dev server: `python main.py run -c config.json`


## Testing instructions
- Find the CI plan in the .github/workflows folder.
- Add or update tests for the code you change, even if nobody asked.
- Install test deps: `pip install -r ./requirementstest.txt`
- Run unit tests: `python -m pytest`
- Run end to end test: Fisrt start dev server in background and then: `sh behave.sh`

## Compatibility

### Server
It can be run as a normal server.

###Desktop App
The server can be deployed but in a window independent of the browser

###Docker
It can be run as a normal server within Docker.

### Packaging
During the CI, if everything is correct, 3 packages (one for each operating system) are created using pyinstaller, so it is important that

## Tecnologies
REST and Templates: Flask
Persistence: SQLALCHEMY (sqlite, postgresl)
Logs: Loguru
WEBScrapping: Selenium
Desktop app: WebView
Packaging: pyinstaller

## Folders

### Data
This folder contains SQL instructions for creating tables and entering some fixed data.

### docker-compose
This folder contains the necessary files, such as Dockerfile, etc., to run the application in docker-compose.

### icconfig
This folder contains the configuration files for continuous integration.

### ssl 
It contains the SSL certificates for the server.

### test
It contains the test files, which are further divided between the pythest tests and the behave tests.
Within each one, there must be a directory tree identical to that of src, to know directly which part the tests correspond to with respect to SRC

### applications
It contains files that are necessary to deploy the application.
There is a REST part that follows the iapp.py interface
and a Web part, where static files and project templates are located.
In the static files within assets we can see the different components that are present, and we must pay special attention to the js folder, since it contains the logic of each page that we want to view with the corresponding template.

### src
It follows a hexagonal architecture and contains several folders.
#### configuration
Following the configuration folder

#### login
Functionality related to login or changing the password

#### persistence
Functionality for persisting the entire project, as well as data recovery. It also implements filters for performing searches. SQLAlachMey is used, but compatibility with SQLite and PostgreSQL is sought, as there are specific functionalities for each, such as date representation.

#### shared
Functionality that can be shared by all modules.
En este caso me gustaría destacar la clase src/shared/infraestructure/webscrapping/myrequestsselenium.py ya que nos permite recuperar información de páginas web para obtener datos, y debe tener compatibilidad total con todas las formas de ejecución.

#### utils
Utility files with functions that can be useful to avoid duplication.

#### finance
This is the folder for the project's important functionalities.
La idea del proyecto es llevar la contabilidad personal y una visión clara de tu ahorro y de dónde está realmente tu dinero y para qué lo necesitas.
Aspectos a tener encuenta:
- Un monedero es dónde está físicamente el dinero, ejemplos: Banco, Efectivo, Paypal...
- Una cuenta es una clasificación virtual de "dividir" el dinero total, y luego cada usuario gestiona el dinero real en los monederos sin importar si está todo junto o separado. Las cuentas sirven para darle una clasificación de para qué está reservado el dinero, por ejemplo, Ahorro, Fondo de Emergencia, Ocio...
- Las categorías indican el tipo de gasto o abono que tienen las operaciones
- Operaciones: Son las operaciones individuales de cada, gasto, ingreso o transferencia. Existe la posibilidad de guardar operaciones favoritas para que le usuario no tenga que volver a poner todos los campos.
- Inversión: Todo lo relacionado con inversiones, desde abrir posiciones, gestionar los dividendos, obtener los últimos valores de los productos, y gestionar bolsas y brokers.
- Resumenes: Una forma de separar todas las funcionalidades básicas CRUD de cada tema, con estadisticas que mezclan conceptos y que se pueden obtener con una única consulta en vez de realizar peticiones encadenadas.
- Hacienda: Una forma de calcular las posibles deducciones que se pueden tener en la declación de la renta Española.

