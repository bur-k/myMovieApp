'use strict'
const Database = use('Database')

class Cont4Controller {
  async func ({ request, view }) {
    const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1 ;
    const filmler = await Database
      .table('movies')
      .select('*')
      .paginate(pageNum, 4);
    return view.render('welcome', {filmler, pageNum})
    // return filmler;

  }
}

module.exports = Cont4Controller
