/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-fo34yqh3.us', // the auth0 domain prefix
    audience: 'coffee_shop', // the audience set for the auth0 app
    clientId: '8XDqYxe7Ir44qugSTB37I0Gg3g3wBgGK', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
