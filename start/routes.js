'use strict'

/*
|--------------------------------------------------------------------------
| Routes
|--------------------------------------------------------------------------
|
| Http routes are entry points to your web application. You can create
| routes for different URL's and bind Controller actions to them.
|
| A complete guide on routing is available here.
| http://adonisjs.com/docs/4.1/routing
|
*/

/** @type {typeof import('@adonisjs/framework/src/Route/Manager')} */
const Route = use('Route')

Route.get('/', 'homeController.func')

Route.on('/signup').render('auth.signup')
Route.post('/signup', 'UserController.create').validator('CreateUser')

Route.on('/login').render('auth.login')
Route.post('/login', 'UserController.login').validator('LoginUser')

Route.get('/logout', 'UserController.logout')

Route.get('/admin/movie/:id', 'admin/movieController.editMovie')

Route.get('/movie/:id', 'movieController.getMov')

Route.get('/library', 'libraryController.func')
Route.post('/library', 'purchaseController.func_insert')
Route.get('/purchase/:id', 'purchaseController.func2')
