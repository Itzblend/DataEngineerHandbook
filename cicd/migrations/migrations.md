# Migrations


In an ideal world all the database changes go through a CI/CD system.
A production database shouldn't be touched by any human.

What steps can we take towards this?

- Version control
- SQL code parser/linter
- Migration- and Revert-scripts


How you can structure your project
```
.
└── src
    ├── db
    │   └── database.py
    └── migrations
        └── 01-add-car-type-column
            ├── migrate.sql
            └── revert.sql

4 directories, 3 files
```


## CI/CD in Database Migrations

When you push a migration into master branch in the repository, the Deployment Pipeline (DP)
should detect a version bump (assuming you remembered to bump it) and execute the migration
correlated to that version.


### Considerations:
- Migration Vs. Versioning (See DBT)


### Ideation

Detect the version change range and execute all migration or rever scripts
