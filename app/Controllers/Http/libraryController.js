'use strict'
const Database = use('Database')


class libraryController{
  async func({request, view, auth}) {
    const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1 ;
    const filmler = await Database
      .table('user_movies').join('movies', {'user_movies.fid': 'movies.id'}).where({kid: auth.user.id})
      .paginate(pageNum, 8);

    return view.render('library', {filmler, pageNum})
   }
   async del({request, view, auth, params}) {
    await Database
      .table('user_movies').where({ fid: params.id, kid: auth.user.id }).del()
     const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1 ;
     const filmler = await Database
      .table('user_movies').join('movies', {'user_movies.fid': 'movies.id'}).where({kid: auth.user.id})
      .paginate(pageNum, 8);

    return view.render('library', {filmler, pageNum})
   }
}
module.exports=libraryController
