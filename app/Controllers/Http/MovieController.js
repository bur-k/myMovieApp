'use strict'
const Database = use('Database')
class MovieController {
    async getMov({ view,params}) {
        const film = await Database.table('movies').join('movie_casts', {'movies.id': 'movie_casts.mid'}).join('casts', {'movie_casts.cid': 'casts.id'}).where({'movies.id': params.id});
        const film3 = await Database.table('movies').join('movie_casts', {'movies.id': 'movie_casts.mid'}).join('casts', {'movie_casts.cid': 'casts.id'}).where({'movies.id': params.id});
		const film2 = await Database.table('movies').where({id: params.id}).first();

		return view.render('movie', {film, film2})
    }
}

module.exports = MovieController