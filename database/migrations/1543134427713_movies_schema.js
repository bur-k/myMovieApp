'use strict'

/** @type {import('@adonisjs/lucid/src/Schema')} */
const Schema = use('Schema')

class MoviesSchema extends Schema {
  up () {
    this.create('movies', (table) => {
      table.increments()
      table.string('title', 126).notNullable()
      table.string('directors', 126).notNullable()
      table.string('imdbmid', 30).notNullable().unique
      table.string('year', 6).notNullable()
      table.string('budget', 14).notNullable()
      table.string('runtime', 14).notNullable()
      table.string('rating', 6).notNullable()
      table.date('releasedate', 14).notNullable()
      table.string('genre', 62).notNullable()
      table.string('plotmin', 254).notNullable()
      table.string('plot', 2046).notNullable()
      table.string('poster', 254).notNullable()
      table.string('photo1', 254).notNullable()
      table.string('photo2', 254).notNullable()
      table.string('photo3', 254).notNullable()
      table.string('trailer', 254).notNullable()
      table.decimal('price').notNullable()
      table.timestamps()
    })
  }

  down () {
    this.drop('movies')
  }
}

module.exports = MoviesSchema
