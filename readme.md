## Slow CRM

### About

Slow CRM is a Rithm-inspired project designed to create a CRM system customized for the Slow Venture VC partners. The CRM supports invite-only users, universal taggable entries, and a quick-search/quick-create search function. Within the application, users can track companies, persons of interest, and a live-updating news feed from authorized users. All companies, entries, and persons can be tagged with multiple tags through a polymorphic tag-table. A news-feed entry can also be "tagged" with relevant companies or persons, which will all show up in an individual entry's detail page. The app currently supports quick-nav tags for "New Leads", "Live Deals", "Needs Discussion", and a catch-all "Portfolio". Quick search functionality allows a user to search through all items for a specific person, company, or tag, and create a new item if the search term does not exist.

### Things To Be Aware Of

- Entries currently use jinja "safe" to show internal links to a tagged person, company, or tag. Make sure your environment is safe from cross site scripting attacks!

### Technologies Used

- Python 3.6.0
- PostgreSQL 9.6.1
- Virtualenvwrapper 15.1.0

### Getting Started

- Make a virtual environment with `mkvirtualenv <Your Environment Name Here>`
- `pip install -r requirements.txt`
- `createdb slowcrmv2-db`
- Open the file at  `$VIRTUAL_ENV/bin/postactivate`
- Add the needed environment variables. A list of what is needed can be found in `environ.txt`
- Migrate the database `python manager.py db upgrade`
- Seed the database `python seed.py`
- Start the server `python app.py`
- App defaults to run at `localhost:3001`

### Testing

To run the tests, you will need the environment variables setup in `$VIRTUAL_ENV/bin/postactivate`.  In the root of the project run:

```
green
```
You can also run individual test files with:
```
green project.tests.<test_filename>
```

### Initial Login

You can login after running `seed.py` with the seeded users using 'aricliesenfelt@gmail.com' and 'password1', or 'tommyhopkins@gmail.com' and 'password2'.

If you want to use your own email/password combo, you can send an invite to an email of your choice by navigating to one of the initial logged-in users' "My Profile" page in the navbar.
