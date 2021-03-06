#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


@contextmanager
def executeQuery(write):
    db = connect()
    c = db.cursor()
    try:
        yield c
    except:
        raise
    else:
        if write:
            db.commit()
    finally:
        c.close()
        db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with executeQuery(True) as c:
        c.execute("DELETE FROM winners")
        c.execute("DELETE FROM losers")


def deletePlayers():
    """Remove all the player records from the database."""
    with executeQuery(True) as c:
        c.execute("DELETE FROM players")


def countPlayers():
    """Returns the number of players currently registered."""
    with executeQuery(False) as c:
        query = "SELECT COUNT(*) as num_players FROM players"
        c.execute(query)
        result = c.fetchone()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with executeQuery(True) as c:
        c.execute("insert into players (name) values (%s)", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with executeQuery(False) as c:
        c.execute("select * from playerStandings")
        standings = c.fetchall()
        players = [
            (int(
                plyr[0]), str(
                plyr[1]), int(
                plyr[2]), int(
                    plyr[4])) for plyr in standings]
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with executeQuery(True) as c:
        c.execute("insert into winners (winner) values (%s)", (winner,))
        c.execute("insert into losers (loser) values (%s)", (loser,))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    # iterate through standings[x] and standings[x+1] to determine matches.
    pairings = [(plyr0[0], plyr0[1], plyr1[0], plyr1[1])
                for plyr0, plyr1 in zip(standings[::2], standings[1::2])]
    return pairings
