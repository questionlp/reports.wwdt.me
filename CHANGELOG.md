# Changes

## 2.10.0

### Application Changes

- Change the database queries and application logic for the panelist "Perfect Score Counts" and "Single Appearance" reports to allow the application to experimentally support MariaDB 11.4.2

### Development Changes

- Upgrade ruff from 0.3.6 to 0.5.1
- Upgrade black from 24.3.0 to 24.4.2
- Upgrade pytest from 8.1.1 to 8.1.2

## 2.9.2

### Component Changes

- Upgrade flask from 3.0.0
- Upgrade gunicorn from 21.2.0 to 22.0.0
- Upgrade numpy from 1.26.3 to 1.26.4
- Upgrade pytz from 2023.3.post1 to 2024.1

### Development Changes

- Upgrade ruff from 0.1.13 to 0.3.6
- Upgrade pytest from 7.4.4 to 8.1.1

## 2.9.1

### Development Changes

- Upgrade black from 23.12.1 to 24.3.0

## 2.9.0

### Application Changes

- Add type hints for a majority of the return types for routes and utility modules
- Replace use of `typing.Optional` and `typing.Union` with the with the conventions documented in PEP-484 and PEP-604
- Change handling of `time_zone` configuration value to prevent use of `pytz.timezone()` in function arguments
- Add support for project sponsorship links to Patreon and GitHub via `settings.patreon_url` and `settings.github_sponsors_url` config keys

### Component Changes

- Upgrade Markdown from 3.5.1 to 3.5.2
- Upgrade numpy from 1.26.0 to 1.26.3

### Development Changes

- Switch to Ruff for code linting and formatting (with the help of Black)
- Upgrade pytest from 7.4.3 to 7.4.4
- Upgrade black from 23.11.0 to 23.12.1

## 2.8.0

### Application Changes

- Addition of Panelist Bluff the Listener Statistics by Year report
- Fix a bug in the Panelist Single Appearance report where the panelists' ranking was not being rendered

### Component Changes

- Upgrade Pure CSS from 2.3.2 to 3.0.0
- Upgrade Markdown from 3.4.3 to 3.5.1

### Development Changes

- Migrate to using Ruff for linting and formatting
- Migrate use of `typing.Dict`, `typing.List` and `typing.Union` to `dict`, `list` and `|` respectively

## 2.7.0

**Starting with version 2.7.0, support for all versions of Python prior to 3.10 have been deprecated.**

### Application Changes

- Replace `dateutil.parser.parse` with `datetime.datetime.strptime`

### Component Changes

- Upgrade MySQL Connector/Python from 8.0.33 to 8.2.0
- Upgrade numpy from 1.24.3 to 1.26.0
- Remove python-dateutil from dependencies

### Development Changes

- Upgrade black from 23.10.1 to 23.11.0
- Remove `py38` and `py39` from `tool.black` in `pyproject.toml`

## 2.6.2

### Application Changes

- Correct wording for the Low Scoring Shows report description to reflect that the report only includes shows with a panelist total score of less than 30 points

## 2.6.1

### Application Changes

- Improve handling of conditions where shows have missing hosts, scorekeepers, panelists and guests for several show reports

## 2.6.0

### Component Changes

- Upgrade Flask from 2.3.2 to 3.0.0
- Upgrade gunicorn from 20.1.0 to 21.2.0
- Upgrade pytz from 2023.3 to 2023.3.post1

### Development Changes

- Upgrade pycodestyle from 2.11.0 to 2.11.1
- Upgrade pytest from 7.4.0 to 7.4.3
- Upgrade black from 23.7.0 to 23.10.1

## 2.5.0

### Application Changes

- Add support for the new decimal panelist Lightning Fill-in-the-Blank start and correct columns, `panelistlrndstart_decimal` and `panelistlrndcorrect_decimal`, respectively
- Optimize some of the template checks for `use_decimal_scores`

## 2.4.0

### Application Changes

- Add support for the new decimal panelist score column, `panelistscore_decimal` in the `ww_showpnlmap` table of the Wait Wait Stats Database
- Add a `use_decimal_scores` setting in `config.json` to enable or disable pulling data from the new column. The default is `false`
- All calculations that use of decimal scores, versus integer scores, use the Python Decimal data type
- Change the rounding of certain stats from 4 decimal places to 5 decimal places

### Component Changes

- Upgrade NumPy from 1.24.2 to 1.24.3

### Development Changes

- Upgrade black from 23.3.0 to 23.7.0
- Upgrade flake8 from 6.0.0 to 6.1.0
- Upgrade pycodestyle from 2.10.0 to 2.11.0
- Upgrade pytest from 7.3.1 to 7.4.0

## 2.3.2

### Application Changes

- Fix issue with shows with empty details causing Low Scoring and High Scoring show reports to error out

## 2.3.1

### Application Changes

- Add filter to Panelist Average Scores by Year database query to exclude any `NULL` values for panelist scores to prevent skewing of results

## 2.3.0

### Application Changes

- Addition of Panelist Average Scores by Year and Panelist Average Scores by Year: All reports
- Modify CSS for Panelist Appearances by Year report to correct column sizes
- Add tooltips to each data cell in the Panelist Appearances by Year report to display the panelist name and year
- Fix issue where printing out Panelist Appearances by Year report from cropping out the table when page scaling is reduced
- Fixed typos in dropdown menus when choosing panelists

### Development Changes

- Added tests for Panelist Average Scores by Year and Panelist Average Scores by Year: All reports
- Updated tests for Panelist Appearances by Year and Panelist vs Panelist reports

## 2.2.5

### Component Changes

- Upgrade Flask from 2.2.3 to 2.3.2

## 2.2.4

### Application Changes

- Correct sorting of "All Women Panel" report to sort by date

### Component Changes

- Upgrade MySQL Connector/Python from 8.0.30 to 8.0.33
- Upgrade NumPy from 1.23.2 to 1.24.2
- Upgrade pytz from 2022.6 to 2023.3
- Upgrade Markdown from 3.4.1 to 3.4.3

### Development Changes

- Move pytest configuration from `pytest.ini` into `pyproject.toml`
- Upgrade flake8 from 5.0.4 to 6.0.0
- Upgrade pycodestyle from 2.9.1 to 2.10.0
- Upgrade pytest from 7.2.0 to 7.3.1
- Upgrade black from 22.10.0 to 23.3.0

## 2.2.3

### Component Changes

- Upgrade Pure CSS from 2.1.0 to 2.2.0

## 2.2.2

### Application Changes

- Fix an issue in which adding a new host or scorekeeper entry in the database without a corresponding appearance record would cause the Host or Scorekeeper Appearances Summary reports to throw an error

## 2.2.1

### Component Changes

- Upgrade Flask from 2.2.2 to 2.2.3
- Upgrade Werkzeug from 2.2.2 to 2.2.3 to fix a security vulnerability

## 2.2.0

### Application Changes

- Addition of Not My Job Guests vs Bluff the Listener Win Ratios report
- Add missing sitemap entry for Panelists First Appearance Wins report
- Add missing entries into the panelists and shows sitemap template files
- Fix issues with sitemap generation and XML syntax in `shows.xml` and `sitemap.xml`

## 2.1.1

### Application Changes

- Correct spelling of `app.shows.reports.search_multiple_panelists` module and references
- Remove unnecessary comments and general formatting clean-up

## 2.1.0

### Application Changes

- Use `dict.get(key, default_value)` in `app/__init__.py` to get/set configuration values in order to avoid application startup errors if configuration keys are not set
  - Default value for `time_zone` is `UTC`
  - Default values for any URL is an empty string
- Addition of Panelists First Appearance Wins report
- Adding `mastodon_url` and `mastodon_user` configuration keys in the `settings` section of the config file
- If the `mastodon_url` and `mastodon_user` keys contain a value, insert a link with `rel="me"` attribute for profile link validation, in the page footer

### Component Changes

- Upgrade Flask from 2.2.0 to 2.2.2
- Upgrade Werkzeug from 2.2.1 to 2.2.2
- Upgrade pytz from 2022.2.1 to 2022.6

### Development Changes

- Upgrade flake8 from 4.0.1 to 5.0.4
- Upgrade pycodestyle from 2.8.0 to 2.9.1
- Upgrade pytest from 7.1.2 to 7.2.0
- Upgrade black from 22.6.0 to 22.10.0

## 2.0.6

### Application Changes

- Removed the unused `app/templates/core` directory and blank HTML files
- Updated Panelist Debut by Year report to include a list of years as part of a side navigation that appears on medium-sized and larger screens (>= 768 px)

## 2.0.5

### Bugfix

- Fix an issue where the `time_zone` configuration value was being assigned to `settings_config` twice, instead of being assigned to both `settings_config` and `database_config`

## 2.0.4

### Component Changes

- Upgrade MySQL Connector/Python from 8.0.28 to 8.0.30
- Upgrade NumPy from 1.22.3 to 1.23.2
- Upgrade pytz from 2022.1 to 2022.2.1

### Application Changes

- Update SQL queries in panelists and shows reports to be compatible with the MySQL flag `ONLY_FULL_GROUP_BY`

## 2.0.3

### Application Changes

- Made changes to how gender is referenced in the Panel Gender Mix report and update the corresponding test
- Simplify the logic of the backing function for Panel Gender Mix report and template file

### Development Changes

- Replace use of `FLASK_ENV` with `FLASK_DEBUG` in `runner.sh`

## 2.0.2

### Component Changes

- Upgrade Flask from 2.1.3 to 2.2.0

## 2.0.1

### Content Changes

- Update blurb on the main index page

## 2.0.0

### Component Changes

- Upgrade Flask from 2.0.2 to 2.1.3
- Upgrade Pure CSS from 2.0.6 to 2.1.0
  - Include Grid (Responsive) module
- Use Werkzeug version 2.2.1

### Application Changes

- Complete restructuring of the Flask application to use Blueprints design pattern
  - This includes moving each section's template directories to live their respective section
  - Core templates including core templates, errors and sitemaps still reside within the top-level templates directory
- Convert the application from using uWSGI to serve the application to Gunicorn to match the changes made with the Wait Wait Stats applications
- Changed section names from singular to plural to match the naming convention used by the Wait Wait Stats Page, Wait Wait API and Wait Wait Graphs applications:

| v1 Section Name | v2 Section Name |
|-----------------|-----------------|
| guest           | guests          |
| host            | hosts           |
| location        | locations       |
| panelist        | panelists       |
| scorekeeper     | scorekeepers    |
| show            | shows           |

- Add appropriate redirects for v1 to v2 URLs
- Previously, each section's reports code files lived under the `reports` module at the top-level of the application. The report code files now reside within their respective section
- Changed underscore in page name in URLs to hyphens
- Renamed `index.html` to `_index.html` in all of the template folders
- Moved the `Panel Gender Mix` report from being under the `Panelists` section to the more appropriate section, `Shows`
- Consolidation of report CSS files into global `style.css`
- Standardize column widths across all reports
- Redesign the Panelist vs Panelist report use the same base temlate as other reports
- Enable Markdown handling for show notes fields in the respective reports
- Display `-` for table cells containing no data
- Change MySQL Connector cursor return type from `dict` to `NamedTuple` where applicable

### Development Changes

- Addition of `pytest` testing
