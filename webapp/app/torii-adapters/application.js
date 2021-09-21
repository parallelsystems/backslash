export default Ember.Route.extend({
    actions: {
        openGeocities: function (username, password) {
            var route = this;
            var providerName = 'geocities';

            // The options to `this.get('torii').open(providerName, options)` will
            // be passed to the provider's `open` method.
            var options = {
                username: username,
                password: password
            };

            this.get('torii').open(providerName, options).then(function (authorization) {
                // authorization as returned by the provider
                route.somethingWithGeocitiesToken(authorization.sessionToken);
            });
        }
    }
});