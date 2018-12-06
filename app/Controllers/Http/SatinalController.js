'use strict'
const Database = use('Database')

class SatinalController{
  async home ({request, view}) {

    //const pageNum = Number(request.input('page')) ? Number(request.input('page')) : 1 ;
    const filmler = await Database
      .table('movies')
      .select('*')
      //.paginate(pageNum, 4);
    const kullanicilar = await Database
      .table('kullanici')
      .select('*')



    return view.render('satinal', {filmler, kullanicilar})

  }







}

module.exports=SatinalController
