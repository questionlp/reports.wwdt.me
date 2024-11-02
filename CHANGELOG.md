# Changes

## 3.0.0

### Application Changes

- Frontend code refactor due to switching from Pure CSS to Bootstrap
  - Replacing Pure CSS frontend toolkit with Bootstrap
  - Refactor the frontend structure to use Bootstrap frontend components and conventions
  - Include the required IBM Plex web fonts with the application to remove use of Google Fonts
- User interface changes
  - Switch the design to match that of the [Wait Wait Stats Page](https://stats.wwdt.me) and the [Wait Wait Graphs Site](https://graphs.wwdt.me)
  - Make use of Bootstrap's responsive design functionality for a more consistent experience across mobile and desktop
  - Remove "Home" from all navigational breadcrumbs
  - Clean up the home page to only provide a table of contents and only display report descriptions on the index page for each section
  - Remove shading for table cells that do not contain data
  - Add tooltips to certain columns in Panelist Bluff the Listener and Show Panel Gender Mix reports to provide additional information
- Link to the corresponding location page on the Wait Wait Stats Page for each listed location in the "Locations: Average Scores" report
- Updating report method names, report template filenames and URLs for consistency
  - The following table lists the reports that have been renamed and/or had their URLs changed
  - Add the necessary redirects and update sitemap generation
  - Update test scripts to reflect new method names, routes and redirects

#### Guests

| Original Report Name | Original Report URL | New Report Name (if applicable) | New Report URL |
|----------------------|---------------------|-----------------|----------------|
| Best Of Not My Job Guests | `/guests/best-of-only` | N/A | `/guests/best-of-only-not-my-job-guests` |
| Not My Job Scoring Exceptions | `/guests/scoring-exceptions` | N/A | `/guests/not-my-job-scoring-exceptions` |
| Not My Job Three Pointers | `/guests/three-pointers` | N/A | `/guests/not-my-job-three-pointers` |

#### Locations

| Original Report Name | Original Report URL | New Report Name (if applicable) | New Report URL |
|----------------------|---------------------|-----------------|----------------|
| Average Score by Location | `/locations/average-scores` | Average Scores by Location | `/locations/average-scores-by-location` |

#### Panelists

| Original Report Name | Original Report URL | New Report Name (if applicable) | New Report URL |
|----------------------|---------------------|-----------------|----------------|
| Bluff the Listener Statistics | `/panelists/bluff-stats` | N/A | `/panelists/bluff-the-listener-statistics` |
| Bluff the Listener Statistics by Year | `/panelists/bluff-stats-by-year` | N/A | `/panelists/bluff-the-listener-statistics-by-year` |
| Debut by Year | `/panelists/debut-by-year` | Debuts by Year | `/panelists/debuts-by-year` |
| Panelist vs Panelist | `/panelists/panelist-pvp` | N/A | `/panelists/panelist-vs-panelist` |
| Panelist vs Panelist: All | `/panelists/panelist-pvp/all` | N/A | `/panelists/panelist-vs-panelist/all` |
| Perfect Score Counts | `/panelists/perfect-scores` | N/A | `/panelists/perfect-score-counts` |
| Statistics by Gender | `/panelists/gender-stats` | N/A | `/panelists/statistics-by-gender` |
| Statistics Summary | `/panelists/stats-summary` | N/A | `/panelists/statistics-summary` |

#### Scorekeepers

| Original Report Name | Original Report URL | New Report Name (if applicable) | New Report URL |
|----------------------|---------------------|-----------------|----------------|
| Introductions | `/scorekeepers/introductions` | Scorekeeper Introductions | `/scorekeepers/scorekeeper-introductions` |

#### Shows

| Original Report Name | Original Report URL | New Report Name (if applicable) | New Report URL |
|----------------------|---------------------|-----------------|----------------|
| High Scoring Shows | `/shows/high-scoring` | N/A | `/shows/high-scoring-shows` |
| Low Scoring Shows | `/shows/low-scoring` | N/A | `/shows/low-scoring-shows` |
| Not My Job Guests vs Bluff the Listener Win Ratios | `/shows/not-my-job-vs-bluffs` | N/A | `/shows/not-my-job-guests-vs-bluff-the-listener-win-ratios` |
| Search Shows by Multiple Panelists | `/shows/search-multiple-panelists` | N/A | `/shows/search-shows-by-multiple-panelists` |
| Show Counts by Year | `/shows/counts-by-year` | N/A | `/shows/show-counts-by-year` |
| Show Descriptions | `/shows/descriptions` | N/A | `/shows/show-descriptions` |
| Show Notes | `/shows/notes` | N/A | `/shows/show-notes` |
| Shows with a Guest Host | `/shows/guest-host` | N/A | `/shows/shows-with-guest-host` |
| Shows with a Guest Scorekeeper | `/shows/guest-scorekeeper` | N/A | `/shows/shows-with-guest-scorekeeper` |
| Shows with Perfect Panelist Scores | `/shows/perfect-panelist-scores` | N/A | `/shows/shows-with-perfect-panelist-scores` |

### Component Changes

- Replace Pure CSS 3.0.0 with Bootstrap 5.3.3
  - Existing Pure CSS files will be preserved to prevent cached versions of the application from breaking
  - Files related to Pure CSS will be removed in a future release

## 2.14.1

### Component Changes

- Upgrade mysql-connector-python from 8.4.0 to 9.1.0
- Upgradew numpy from 2.1.0 to 2.1.2

### Development Changes

- Upgrade black from 24.8.0 to 24.10.0
- Upgrade ruff from 0.6.9 to 0.7.0
- Increase minimum pytest version from 8.0 to 8.3 in `pyproject.toml`

## 2.14.0

### Application Changes

- Replace all references of `named_tuple=` in database cursors to `dictionary=` due to cursors using `NamedTuple` being marked for deprecation in future versions of MySQL Connector/Python
- Fix "Total Score" column for Panelist "First Appearance Wins" report where non-decimal scores were not populating

### Component Changes

- Upgrade mysql-connector-python from 8.2.0 to 8.4.0
- Upgrade numpy from 1.26.4 to 2.1.0
- Upgrade pytz from 2024.1 to 2024.2

### Development Changes

- Upgrade black from 24.4.2 to 24.8.0
- Upgrade pytest from 8.1.2 to 8.3.3
- Upgrade ruff from 0.6.7 to 0.6.9
- Add initial pytest coverage reporting using `pytest-cov`, which can be generated by running: `pytest --cov=app tests/`

## 2.13.0

### Application Changes

- Fix Guest Scoring Exceptions report where an exception does not contain any notes
- Code cleanup and fix Pylint errors and warnings

### Development Changes

- Upgrade black from 0.5.1 to 0.6.7

## 2.12.0

### Application Changes

- Add show descriptions and show notes reports
- Fix issues reported by Pylint

### Component Changes

- Upgrade gunicorn from 22.0.0 to 23.0.0

## 2.11.0

### Application Changes

- Add support for Umami web analytics via `settings.umami_analytics` config object with the following keys:

| Config Key | Description |
| ---------- | ----------- |
| `_enabled` | Set value to `true` to enable adding Umami `script` tag (default: `false`) |
| `url` | URL of the Umami analytics script |
| `data_website_id` | Umami Site ID |
| `data_auto_track` | Set value to `false` to disable auto event tracking (default: `true`) |
| `data_host_url` | Override the location where Umami data is sent to |
| `data_domains` | Comma-delimited list of domains where the Umami script should be active |

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
