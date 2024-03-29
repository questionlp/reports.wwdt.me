# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Location Score Breakdown Report Functions"""

from collections import OrderedDict
from decimal import Decimal
from typing import List, Dict
import mysql.connector

#region Retrieval Functions
def retrieve_average_scores_by_location(database_connection: mysql.connector.connect
                                       ) -> List[Dict]:
    """Retrieve average scores sorted by location using a pre-written
    database query"""

    average_scores = []
    cursor = database_connection.cursor(dictionary=True)
    # Excluding 25th Anniversary Show at Chicago Theatre from calculations
    # due to non-standard number of panelist scores and score totals
    query = ("SELECT l.locationid, l.venue, l.city, l.state, "
             "AVG(pm.panelistscore) AS average_score, "
             "SUM(pm.panelistscore) / (COUNT(s.showid) / 3) AS average_total, "
             "COUNT(s.showid) / 3 AS show_count "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "join ww_showlocationmap lm ON lm.showid = pm.showid "
             "JOIN ww_locations l ON l.locationid = lm.locationid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND l.locationid <> 3 " # Ignore any TBD locations
             "AND s.showdate <> '2018-10-27' "
             "GROUP BY l.locationid "
             "ORDER BY average_score DESC, average_total DESC, "
             "show_count DESC, l.venue ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        location = OrderedDict()
        location["id"] = row["locationid"]
        location["venue"] = row["venue"]
        location["city"] = row["city"]
        location["state"] = row["state"]
        location["average_score"] = Decimal(row["average_score"]).normalize()
        location["average_total"] = Decimal(row["average_total"]).normalize()
        location["show_count"] = Decimal(row["show_count"]).normalize()
        average_scores.append(location)

    return average_scores

#endregion
