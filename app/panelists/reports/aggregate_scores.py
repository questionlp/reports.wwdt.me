# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Aggregate Scores Report Functions"""

from collections import OrderedDict
from typing import List, Dict
import mysql.connector
import numpy

#region Retrieval Functions
def retrieve_all_scores(database_connection: mysql.connector.connect
                       ) -> List[int]:
    """Retrieve a list of all panelist scores from non-Best Of and
    non-Repeat shows"""

    cursor = database_connection.cursor()
    query = ("SELECT pm.panelistscore FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND pm.panelistscore IS NOT NULL "
             "ORDER BY pm.panelistscore ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(row[0])

    return scores

def retrieve_score_spread(database_connection: mysql.connector.connect
                         ) -> List[Dict]:
    """Retrieve a list of grouped panelist scores from non-Best Of and
    non-Repeat shows"""

    cursor = database_connection.cursor()
    query = ("SELECT pm.panelistscore, COUNT(pm.panelistscore) "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistscore IS NOT NULL "
             "AND s.bestof = 0 AND s.repeatshowid IS NULL "
             "GROUP BY pm.panelistscore "
             "ORDER BY pm.panelistscore ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        score = OrderedDict()
        score["score"] = row[0]
        score["count"] = row[1]
        scores.append(score)

    return scores

#endregion

#region Results Generation Functions
def calculate_stats(scores: List[int]) -> Dict:
    """Calculate stats for all of the panelist scores"""

    stats = OrderedDict()
    stats["count"] = len(scores)
    stats["minimum"] = int(numpy.amin(scores))
    stats["maximum"] = int(numpy.amax(scores))
    stats["mean"] = round(numpy.mean(scores), 4)
    stats["median"] = int(numpy.median(scores))
    stats["standard_deviation"] = round(numpy.std(scores), 4)
    stats["sum"] = int(numpy.sum(scores))

    return stats

#endregion
