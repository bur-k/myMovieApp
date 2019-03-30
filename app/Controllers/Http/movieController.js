'use strict'
const Database = use('Database')

class movieController {
  async getMov({view, params}) {
    const casts = await Database.table('movies').join('movie_casts', {'movies.id': 'movie_casts.mid'}).join('casts', {'movie_casts.cid': 'casts.id'}).where({'movies.id': params.id});
    const film = await Database.table('movies').where({id: params.id}).first();
    const film1 = await Database.table('movies').where({id: ((parseInt(params.id)+1))}).orWhere({id: 1}).last();
    const film2 = await Database.table('movies').where({id: ((parseInt(params.id)+2))}).orWhere({id: 2}).last();
    return view.render('movie', {casts, film, film1, film2})
  }
  async playMov({view, params}) {
    const film = await Database.table('movies').where({'movies.id': params.id}).first();
    const movieURL = film.imdbmid.substring(6);
    return view.render('play', {film, movieURL})
  }
}

module.exports = movieController
