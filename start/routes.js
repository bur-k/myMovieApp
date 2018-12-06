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

// Route.on('/').render('welcome')
Route.on('/login').render('login')
Route.on('/signup').render('signup')

Route.get('/satinal/:id', 'SatinalController.func2')
Route.post('/satinal/:id', 'SatinalController.func_insert')

Route.get('/movie/:id','MovieController.getMov')
Route.post('/signup', 'UserController.create')

Route.on('/temp').render('temp')
Route.post('/login', 'UserController.login')

Route.get('/welcome', 'Cont4Controller.func')
Route.get('/movielibrary', 'MovieLibraryController.func')
