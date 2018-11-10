'use strict'

class CreateUser {
  get rules () {
    return {
      'name': 'required',
      'surname': 'required',
      'username': 'required|unique:users',
      'email': 'required|unique:users',
      'password': 'required'
    }
  }

  get messages() {
    return {
      'required': '{{ field }} is required.',
      'unique': 'the {{ field }} already exists'
    }
  }

  async fails(error) {
    this.ctx.session.withErrors(error)
      .flashAll();

    return this.ctx.response.redirect('back');
  }
}

module.exports = CreateUser