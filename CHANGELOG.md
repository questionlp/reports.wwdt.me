# Changes

## 2.0.0

### Component Changes

- Upgrade Flask from 2.0.2 to 2.1.2
- Upgrade Pure CSS from 2.0.6 to 2.1.0

### Application Changes

- Complete restructuring of the Flask application to use Blueprints design
  pattern
- Convert the application from using uWSGI to serve the application to
  Gunicorn to match the changes made with the Wait Wait Stats API
- Changed section names from singular to plural to match the naming convention
  used by the Wait Wait Stats Page, Wait Wait API and Wait Wait Graphs
  applications:

| v1 Section Name | v2 Section Name |
|-----------------|-----------------|
| guest           | guests          |
| host            | hosts           |
| location        | locations       |
| panelist        | panelists       |
| scorekeeper     | scorekeepers    |
| show            | shows           |

- Previously, each section's reports lived under the `reports` module at the
  top-level of the application. The reports have been moved to reside within
  their respective section's module
- Changed underscore in page name in URLs to hyphens
- Renamed `index.html` to `_index.html` in all of the template folders
- Moved the `Panel Gender Mix` report from being under the `Panelists` section
  to the more appropriate section, `Shows`
- Consolidation of CSS files to standardize column widths across all reports
- Redesign the Panelist vs Panelist report to use a dropdown to select a
  panelist rather than a side navigation menu
- Enable Markdown handling for show notes fields in the respective reports

### Development Changes

- Adding tests by way of `pytest`
