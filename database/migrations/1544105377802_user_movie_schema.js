'use strict'

/** @type {import('@adonisjs/lucid/src/Schema')} */
const Schema = use('Schema')

class UserMovieSchema extends Schema {
  up () {
    this.create('user_movies', (table) => {
      table.increments()
      table.integer('fid', 80).notNullable().unique
      table.integer('kid', 80).notNullable().unique
      table.timestamps()
    })
  }

  down () {
    this.drop('user_movies')
  }
}

module.exports = UserMovieSchema
