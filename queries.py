# pylint: disable=C0103, missing-docstring

import sqlite3

def detailed_movies(db:sqlite3):
    '''return the list of movies with their genres and director name'''
    query="""SELECT movies.title , movies.genres, directors.name
    FROM movies JOIN directors ON directors.id =movies.director_id"""
    db.execute(query)
    results=db.fetchall()
    return results


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query="""SELECT title
    FROM movies
    JOIN directors ON directors.id=movies.director_id
    WHERE movies.start_year > directors.death_year """
    db.execute(query)
    results=db.fetchall()
    return[movie[0] for movie in results]

def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query=f"SELECT movies.minutes FROM movies WHERE movies.genres ='{genre_name}'"
    db.row_factory=sqlite3.Row
    db.execute(query)
    results=db.fetchall()
    av_time=0
    numberofmovies=0
    for resutl in results:
        av_time+=resutl['minutes']
        numberofmovies+=1
    av_length=av_time/numberofmovies
    av_length=f"{av_length:.2f}"
    return {'genre': genre_name,'number_of_movies': numberofmovies,'avg_length':float(av_length)}


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query=f"""SELECT directors.name, COUNT(directors.id)
    FROM directors JOIN movies  ON directors.id=movies.director_id
    WHERE movies.genres ='{genre_name}'
    GROUP BY directors.name ORDER BY COUNT(directors.id) DESC, directors.name  LIMIT 5"""
    db.execute(query)
    results=db.fetchall()
    return results


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query="""SELECT (movies.minutes/30)*30 as Duration, count(*)
    FROM movies
    WHERE minutes  >0
    GROUP BY Duration
    ORDER BY movies.minutes """
    db.execute(query)
    results=db.fetchall()
    new_result=[]
    for result in results:
        new_result.append((result[0]+30,result[1]))
    return  new_result


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query="""SELECT directors.name, (movies.start_year-directors.birth_year)
    FROM directors
    JOIN movies ON directors.id=movies.director_id
    WHERE directors.birth_year >0
    ORDER BY (movies.start_year-directors.birth_year)
    LIMIT 5"""
    db.execute(query)
    results=db.fetchall()
    return  results
