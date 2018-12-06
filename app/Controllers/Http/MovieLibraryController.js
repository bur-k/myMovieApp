'use strict'
const Database = use('Database')


class MovieLibraryController{
  async func({request, view, params}) {
    const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1 ;
    const filmler = await Database
      .table('user_movies').join('movies', {'user_movies.fid': 'movies.id'}).where({kid: 2})
      .paginate(pageNum, 8);


    return view.render('MovieLibrary', {filmler, pageNum})
    // return filmler;
  }




}

module.exports=MovieLibraryController
