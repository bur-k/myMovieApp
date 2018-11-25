'use strict'

/** @type {import('@adonisjs/lucid/src/Schema')} */
const Schema = use('Schema')

class CastsSchema extends Schema {
  up () {
    this.create('casts', (table) => {
      table.increments()
      table.string('imdbcid', 30).notNullable().unique()
      table.string('fullname', 126).notNullable()
      table.string('photo', 254).notNullable()
      table.timestamps()
    })
  }

  down () {
    this.drop('casts')
  }
}

module.exports = CastsSchema
