# Changes

## 2.2.0

### Application Changes

- Addition of Not My Job Guests vs Bluff the Listener Win Ratios report
- Add missing sitemap entry for Panelists First Appearance Wins report

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
