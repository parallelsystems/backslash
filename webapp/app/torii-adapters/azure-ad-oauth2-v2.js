import { computed } from '@ember/object';
import Oauth2 from 'torii/providers/oauth2-code';
import { configurable } from 'torii/configuration';

/**
 * This class implements authentication against AzureAD
 * using the OAuth2 authorization flow in a popup window.
 * @class
 */
var AzureAdOauth2V2 = Ember.Object.extend({
    name: 'azure-ad-oauth2-v2',

    baseUrl: computed(function () {
        return this.get('authority') + '/oauth2/v2.0/authorize';
    }),

    tennantId: configurable('tennantId', 'common'),

    // additional url params that this provider requires
    requiredUrlParams: ['client_id'],

    optionalUrlParams: ['scope', 'nonce', 'response_mode'],

    responseMode: configurable('responseMode', null),

    responseParams: computed(function () {
        return [this.get('responseType'), 'state'];
    }),

    apiVersion: '1.0',

    responseType: configurable('responseType', 'code'),
    clientId: configurable('clientId', function () {
        // A hack that allows redirectUri to be configurable
        // but default to the superclass
        return this._super();
    }),
    authority: configurable('authority', function () {
        // A hack that allows redirectUri to be configurable
        // but default to the superclass
        return this._super();
    }),

    redirectUri: configurable('redirectUri', function () {
        // A hack that allows redirectUri to be configurable
        // but default to the superclass
        return this._super();
    }),
});

export default AzureAdOauth2V2;

// export default Ember.Object.extend({
//     // credentials as passed from torii.open
//     open: function (credentials) {
//         return new Ember.RSVP.Promise(function (resolve, reject) {
//             exampleAsyncLogin(
//                 credentials.username,
//                 credentials.password,

//                 // callback function:
//                 function (error, response) {
//                     // the promise is resolved with the authorization
//                     Ember.run.bind(null, resolve, { sessionToken: response.token });
//                 }
//             );
//         });
//     }
// });