## Slow CRM 

### Technologies Used

- Python 3
- Postgres
- virtualenvwrapper

### Getting Started

- Make a virtual environment
- `pip install -r requirements.txt`
- `createdb slowcrmv2_db`
- Open the file at  `$VIRTUAL_ENV/bin/postactivate`
- Add the needed environment variables. A list of what is needed can be found in `environ.txt`

### Testing

To run the tests, you will need the environment variables setup in `$VIRTUAL_ENV/bin/postactivate`.  In the root of the project run:

```
green project/tests
```
