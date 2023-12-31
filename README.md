# local-cq
Run locally a code quality pipeline and get the result as a static webpage

## Installation

Clone the repository and run
```bash
pip install .
```

## Usage

Navigate to the project for which you want to generate a report, then run `local-cq` specifying the source directory of your codebase and the tests directory

```bash
local-cq --source src/ --tests tests/
```

After it, a new folder called `cq-report` is created, you can open `cq-report/index.html` with a web browser. You have an overview with the badges and you have access to the reports by following the links.

!()[cq.png]