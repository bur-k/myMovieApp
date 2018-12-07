'use strict'
const Database = use('Database')

class homeController {
  async func({request, view}) {
    const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1;
    const filmler = await Database
      .table('movies')
      .select('*')
      .paginate(pageNum, 8);
    return view.render('home', {filmler, pageNum})
  }
}
module.exports = homeController
