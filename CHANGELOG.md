# Changes

## 2.0.0 (Future Release)

### Component Changes

- Upgrade Flask from 2.0.2 to 2.1.3
- Upgrade Pure CSS from 2.0.6 to 2.1.0
  - Include Grid (Responsive) module
- Set Werkzeug specifically to 2.2.1

### Application Changes

- Complete restructuring of the Flask application to use Blueprints design
  pattern
  - This includes moving each section's template directories to live their
    respective section
  - Core templates including core templates, errors and sitemaps still reside
    within the top-level templates directory
- Change `app.url_map.strict_slashes` from `False` to `True`
- Convert the application from using uWSGI to serve the application to
  Gunicorn to match the changes made with the Wait Wait Stats applications
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

- Add appropriate redirects for v1 to v2 URLs
- Previously, each section's reports code files lived under the `reports`
  module at the top-level of the application. The report code files now reside
  within their respective section
- Changed underscore in page name in URLs to hyphens
- Renamed `index.html` to `_index.html` in all of the template folders
- Moved the `Panel Gender Mix` report from being under the `Panelists` section
  to the more appropriate section, `Shows`
- Consolidation of report CSS files into global `style.css`
- Standardize column widths across all reports
- Redesign the Panelist vs Panelist report use the same base temlate as other
  reports
- Enable Markdown handling for show notes fields in the respective reports
- Display `-` for table cells containing no data

### Development Changes

- Adding tests by way of `pytest`
