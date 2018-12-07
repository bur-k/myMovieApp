'use strict'
const Database = use('Database')

class purchaseController{

  async func2({request, view, params}) {
    const film = await Database.table('movies').where({id: params.id}).first();
    return view.render('purchase', {film})
  }

  async func_insert({request, view, auth}) {
    const ids =request.only(['fid','kid']);
    await Database.table('user_movies').insert([{ kid: ids.kid, fid: ids.fid}]);
    const pageNum = 1
    const filmler = await Database
      .table('user_movies').join('movies', {'user_movies.fid': 'movies.id'}).where({kid: auth.user.id})
      .paginate(pageNum, 8);

    return view.render('library', {filmler, pageNum})
  }
}

module.exports=purchaseController
