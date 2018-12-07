'use strict'
const Database = use('Database')

class movieController {
  async getMov({view, params}) {
    let movieCount = await Database.table('movies').count('id')
    const film = await Database.table('movies').join('movie_casts', {'movies.id': 'movie_casts.mid'}).join('casts', {'movie_casts.cid': 'casts.id'}).where({'movies.id': params.id});
    const film2 = await Database.table('movies').where({id: params.id}).first();
    const film3 = await Database.table('movies').where({id: ((parseInt(params.id)+1))}).orWhere({id: 1}).first();
    const film4 = await Database.table('movies').where({id: ((parseInt(params.id)+2))}).orWhere({id: 2}).first();
    return view.render('movie', {film, film2, film3, film4})
  }
}

module.exports = movieController
