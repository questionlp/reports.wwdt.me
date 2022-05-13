# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Win/Loss Streaks Report Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

#region Retrieval Functions
def retrieve_panelists(database_connection: mysql.connector.connect
                      ) -> List[Dict]:
    """Retrieve a list of panelists with their panelist ID and name"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelistid, p.panelist, p.panelistslug "
             "FROM ww_panelists p "
             "WHERE p.panelistid <> 17 "
             "ORDER BY p.panelist ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelist = OrderedDict()
        panelist["id"] = row["panelistid"]
        panelist["name"] = row["panelist"]
        panelist["slug"] = row["panelistslug"]
        panelists.append(panelist)

    return panelists

def retrieve_panelist_ranks(panelist_id: int,
                            database_connection: mysql.connector.connect
                           ) -> List[Dict]:
    """Retrieve a list of show dates and the panelist rank for the
    requested panelist ID"""

    cursor = database_connection.cursor()
    query = ("SELECT s.showid, s.showdate, pm.showpnlrank "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s "
             "AND s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND pm.panelistscore IS NOT NULL "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    ranks = []
    for row in result:
        info = OrderedDict()
        info["show_id"] = row[0]
        info["show_date"] = row[1].isoformat()
        info["rank"] = row[2]
        ranks.append(info)

    return ranks

#endregion

#region Report Functions
def calculate_panelist_losing_streaks(panelists: List[Dict],
                                      database_connection: mysql.connector.connect):
    """Retrieve panelist stats and calculate their losing streaks"""

    losing_streaks = []

    for panelist in panelists:
        longest_losing_streak = 0
        longest_losing_streak_show_dates = []
        longest_third_streak = 0
        longest_third_streak_show_dates = []
        total_losses = 0
        total_third_losses = 0

        shows = retrieve_panelist_ranks(panelist["id"], database_connection)
        if shows:
            # Calculate losing streaks
            current_streak = 0
            current_streak_show_dates = []
            for show in shows:
                if show["rank"] != "1" and show["rank"] != "1t":
                    # Placed 2nd, 2nd tied or 3rd
                    total_losses += 1
                    current_streak += 1

                    show_info = OrderedDict()
                    show_info["show_id"] = show["show_id"]
                    show_info["show_date"] = show["show_date"]
                    show_info["show_rank"] = show["rank"]
                    current_streak_show_dates.append(show_info)

                    if current_streak > longest_losing_streak:
                        longest_losing_streak = current_streak
                        longest_losing_streak_show_dates = current_streak_show_dates
                else:
                    current_streak = 0
                    current_streak_show_dates = []

            current_third_streak = 0
            current_third_streak_show_dates = []
            for show in shows:
                if show["rank"] == "3":
                    # Placed 3rd
                    total_third_losses += 1
                    current_third_streak += 1

                    show_info = OrderedDict()
                    show_info["show_id"] = show["show_id"]
                    show_info["show_date"] = show["show_date"]
                    show_info["show_rank"] = show["rank"]
                    current_third_streak_show_dates.append(show_info)

                    if current_third_streak > longest_third_streak:
                        longest_third_streak = current_third_streak
                        longest_third_streak_show_dates = current_third_streak_show_dates
                else:
                    current_third_streak = 0
                    current_third_streak_show_dates = []

            panelist["total_losses"] = total_losses
            panelist["total_third_losses"] = total_third_losses
            panelist["longest_streak"] = longest_losing_streak
            panelist["longest_streak_dates"] = longest_losing_streak_show_dates
            panelist["longest_third_streak"] = longest_third_streak
            panelist["longest_third_streak_dates"] = longest_third_streak_show_dates
            losing_streaks.append(panelist)

    return losing_streaks

def calculate_panelist_win_streaks(panelists: List[Dict],
                                   database_connection: mysql.connector.connect):
    """Retrieve panelist stats and calculate their win streaks"""

    win_streaks = []

    for panelist in panelists:
        longest_streak = 0
        longest_streak_show_dates = []
        longest_streak_with_draws = 0
        longest_streak_show_dates_with_draws = []
        total_wins = 0
        total_wins_with_draws = 0

        shows = retrieve_panelist_ranks(panelist["id"], database_connection)
        if shows:
            # Calculate win streaks
            current_streak = 0
            current_streak_show_dates = []
            for show in shows:
                if show["rank"] == "1":
                    total_wins += 1
                    current_streak += 1

                    show_info = OrderedDict()
                    show_info["show_id"] = show["show_id"]
                    show_info["show_date"] = show["show_date"]
                    show_info["show_rank"] = show["rank"]
                    current_streak_show_dates.append(show_info)

                    if current_streak > longest_streak:
                        longest_streak = current_streak
                        longest_streak_show_dates = current_streak_show_dates
                else:
                    current_streak = 0
                    current_streak_show_dates = []

            # Calculate win streaks with draws
            current_streak_with_draws = 0
            current_streak_show_dates_with_draws = []
            for show in shows:
                if show["rank"] == "1" or show["rank"] == "1t":
                    total_wins_with_draws += 1
                    current_streak_with_draws += 1

                    show_info = OrderedDict()
                    show_info["show_id"] = show["show_id"]
                    show_info["show_date"] = show["show_date"]
                    show_info["show_rank"] = show["rank"]
                    current_streak_show_dates_with_draws.append(show_info)

                    if current_streak_with_draws > longest_streak_with_draws:
                        longest_streak_with_draws = current_streak_with_draws
                        longest_streak_show_dates_with_draws = current_streak_show_dates_with_draws
                else:
                    current_streak_with_draws = 0
                    current_streak_show_dates_with_draws = []

            panelist["total_wins"] = total_wins
            panelist["total_wins_with_draws"] = total_wins_with_draws
            panelist["longest_streak"] = longest_streak
            panelist["longest_streak_dates"] = longest_streak_show_dates
            panelist["longest_streak_with_draws"] = longest_streak_with_draws
            panelist["longest_streak_with_draws_dates"] = longest_streak_show_dates_with_draws
            win_streaks.append(panelist)

    return win_streaks

#endregion
