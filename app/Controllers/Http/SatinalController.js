'use strict'
const Database = use('Database')

class SatinalController{


  async func2({request, view, params}) {
    const film = await Database.table('movies').where({id: params.id}).first();
    return view.render('satinal', {film})
  }


  async func_insert({request, view}) {
    const ids =request.only(['fid','kid']);
    await Database.table('user_movies').insert([{ kid: 2, fid: ids.fid}]);
    const filmler = await Database.table('user_movies').join('movies', {'user_movies.fid': 'movies.id'}).where({kid: 1});
    // response.redirect(ids.trailer)
    return view.render('MovieLibrary', {filmler})
  }
}

module.exports=SatinalController
