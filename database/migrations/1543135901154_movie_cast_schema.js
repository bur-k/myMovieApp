'use strict'

/** @type {import('@adonisjs/lucid/src/Schema')} */
const Schema = use('Schema')

class MovieCastSchema extends Schema {
  up () {
    this.create('movie_casts', (table) => {
      table.increments()
      table.integer('mid', 80).notNullable()
      table.integer('cid', 80).notNullable()
      table.string('role', 80).notNullable()
      table.timestamps()
    })
  }

  down () {
    this.drop('movie_casts')
  }
}

module.exports = MovieCastSchema
