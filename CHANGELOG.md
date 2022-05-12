# Changes

## 2.0.0

### Component Changes

- Upgrade Flask from 2.0.2 to 2.1.2
- Replace Pure CSS with Bulma

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

- Changed underlines in page name in URLs to hyphens
- Consolidation of CSS files to standardize column widths across reports
- Redesign the Panelist vs Panelist report to use a dropdown to select a
  panelist rather than a side navigation menu

### Development Changes

- Adding tests by way of `pytest`
