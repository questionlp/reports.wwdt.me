# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Core Application for Wait Wait Reports."""

import platform
from urllib.parse import ParseResult, urlparse

from flask import Flask

from app import config, utility

from .dicts import RANK_MAP
from .errors import handlers
from .guests.redirects import blueprint as guests_redirects_bp
from .guests.routes import blueprint as guests_bp
from .hosts.redirects import blueprint as hosts_redirects_bp
from .hosts.routes import blueprint as hosts_bp
from .locations.redirects import blueprint as locations_redirects_bp
from .locations.routes import blueprint as locations_bp
from .main.redirects import blueprint as redirects_bp
from .main.routes import blueprint as main_bp
from .panelists.redirects import blueprint as panelists_redirects_bp
from .panelists.routes import blueprint as panelists_bp
from .scorekeepers.redirects import blueprint as scorekeepers_redirects_bp
from .scorekeepers.routes import blueprint as scorekeepers_bp
from .shows.redirects import blueprint as shows_redirects_bp
from .shows.routes import blueprint as shows_bp
from .sitemaps.routes import blueprint as sitemaps_bp
from .version import APP_VERSION


def create_app():
    """Create Flask application."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Override base Jinja options
    app.jinja_options = Flask.jinja_options.copy()
    app.jinja_options.update({"trim_blocks": True, "lstrip_blocks": True})
    app.create_jinja_environment()

    # Register error handlers
    app.register_error_handler(404, handlers.not_found)
    app.register_error_handler(500, handlers.handle_exception)

    # Load configuration file
    _config = config.load_config()
    app.config["database"] = _config["database"]
    app.config["app_settings"] = _config["settings"]

    # Set up Jinja globals
    app.jinja_env.globals["app_version"] = APP_VERSION
    app.jinja_env.globals["current_year"] = utility.current_year
    app.jinja_env.globals["rank_map"] = RANK_MAP
    app.jinja_env.globals["rendered_at"] = utility.generate_date_time_stamp

    app.jinja_env.globals["time_zone"] = _config["settings"]["app_time_zone"]
    app.jinja_env.globals["ga_property_code"] = _config["settings"].get(
        "ga_property_code", ""
    )
    app.jinja_env.globals["umami"] = _config["settings"]["umami"]
    app.jinja_env.globals["api_url"] = _config["settings"].get("api_url", "")
    app.jinja_env.globals["blog_url"] = _config["settings"].get("blog_url", "")
    app.jinja_env.globals["graphs_url"] = _config["settings"].get("graphs_url", "")
    app.jinja_env.globals["repo_url"] = _config["settings"].get("repo_url", "")
    _site_url: str = _config["settings"].get("site_url", "")
    app.jinja_env.globals["site_url"] = _site_url

    if _site_url.startswith("http"):
        parsed_site_url: ParseResult = urlparse(_site_url)
        if parsed_site_url.hostname:
            _config["settings"]["site_hostname"] = parsed_site_url.hostname
            app.jinja_env.globals["site_hostname"] = parsed_site_url.hostname

    app.jinja_env.globals["stats_url"] = _config["settings"].get("stats_url", "")
    app.jinja_env.globals["bluesky_url"] = _config["settings"].get("bluesky_url", "")
    app.jinja_env.globals["bluesky_user"] = _config["settings"].get("bluesky_user", "")
    app.jinja_env.globals["mastodon_url"] = _config["settings"].get("mastodon_url", "")
    app.jinja_env.globals["mastodon_user"] = _config["settings"].get(
        "mastodon_user", ""
    )
    app.jinja_env.globals["support_npr_url"] = _config["settings"].get(
        "support_npr_url", ""
    )
    app.jinja_env.globals["patreon_url"] = _config["settings"].get("patreon_url", "")
    app.jinja_env.globals["github_sponsor_url"] = _config["settings"].get(
        "github_sponsor_url", ""
    )
    app.jinja_env.globals["block_ai_scrapers"] = bool(
        _config["settings"].get("block_ai_scrapers", False)
    )
    app.jinja_env.globals["use_minified_css"] = bool(
        _config["settings"].get("use_minified_css", False)
    )

    app.jinja_env.globals["node_name"] = (
        platform.node().split(".")[0] if platform.node() else None
    )

    # Register Jinja template filters
    app.jinja_env.filters["markdown"] = utility.md_to_html

    # Register application blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(redirects_bp)
    app.register_blueprint(sitemaps_bp)
    app.register_blueprint(guests_redirects_bp)
    app.register_blueprint(guests_bp, url_prefix="/guests")
    app.register_blueprint(hosts_redirects_bp)
    app.register_blueprint(hosts_bp, url_prefix="/hosts")
    app.register_blueprint(locations_redirects_bp)
    app.register_blueprint(locations_bp, url_prefix="/locations")
    app.register_blueprint(panelists_redirects_bp)
    app.register_blueprint(panelists_bp, url_prefix="/panelists")
    app.register_blueprint(scorekeepers_redirects_bp)
    app.register_blueprint(scorekeepers_bp, url_prefix="/scorekeepers")
    app.register_blueprint(shows_redirects_bp)
    app.register_blueprint(shows_bp, url_prefix="/shows")

    return app
