'use strict'
const Database = use('Database')

class movieController {
  async editMovie({request, view, params}) {
    const movie = await Database.table('movies').where({id: params.id}).first();
    return view.render('admin.movie', {movie})
  }
}
module.exports = movieController
