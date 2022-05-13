# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panel Gender Mix Report Functions"""

from collections import OrderedDict
from typing import Dict, List, Text
import mysql.connector

#region Retrieval Functions
def retrieve_show_years(database_connection: mysql.connector.connect
                       ) -> List[int]:
    """Retrieve a list of show years available in the database"""

    years = []
    cursor = database_connection.cursor()
    query = ("SELECT DISTINCT YEAR(s.showdate) FROM ww_shows s "
             "ORDER BY YEAR(s.showdate) ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        years.append(row[0])

    return years

def retrieve_panel_gender_count_by_year(year: int,
                                        gender: Text,
                                        database_connection: mysql.connector.connect
                                       ) -> int:
    """Get a count of shows for the requested year that has the
    requested number of panelists of a given gender"""

    # panelistgender field only contains a single letter
    gender_tag = gender[0].upper()

    counts = OrderedDict()
    cursor = database_connection.cursor()

    for gender_count in range(0, 4):
        query = ("SELECT s.showdate FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
                 "AND p.panelistgender = %s "
                 "AND year(s.showdate) = %s "
                 "AND s.showdate <> '2018-10-27' " # Exclude 25th anniversary special
                 "GROUP BY s.showdate "
                 "HAVING COUNT(p.panelistgender) = %s;")
        cursor.execute(query, (gender_tag, year, gender_count, ))
        cursor.fetchall()
        counts["{}{}".format(gender_count, gender_tag)] = cursor.rowcount

    cursor.close()
    total = sum(counts.values())
    counts["total"] = total
    return counts

#endregion

#region Report Functions
def panel_gender_mix_breakdown(gender: Text,
                               database_connection=mysql.connector.connect
                              ) -> Dict:
    """Calculate the panel gender breakdown for all show years and
    return an OrderedDict containing count for each year"""

    show_years = retrieve_show_years(database_connection)

    gender_mix_breakdown = OrderedDict()
    for year in show_years:
        count = retrieve_panel_gender_count_by_year(year=year,
                                                    gender=gender,
                                                    database_connection=database_connection)
        gender_mix_breakdown[year] = count

    return gender_mix_breakdown

#endregion
