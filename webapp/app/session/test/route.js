import Ember from "ember";

import ComplexModelRoute from "../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {

  api: Ember.inject.service(),
  favicon: Ember.inject.service(),

  parent_controller: function() {
    return this.controllerFor("session");
  }.property(),

  setupController(controller, model) {
    this._super(...arguments);
    this.get("parent_controller").set("current_test", model.test_model);
  },

  model({test_id}) {
    let self = this;
    let session = self.modelFor("session").session_model;

    return self.store.query('test', {id: test_id}).then(function(tests) {
      let test = tests.get('firstObject');
      if (!test) {
        return Ember.RSVP.reject({not_found: true});
      }

      return Ember.RSVP.hash({
        session_model: session,
        test_metadata: (self.get("api")
                        .call("get_metadata", {
                          entity_type: "test",
                          entity_id: parseInt(test.id)
                        })
                        .then(r => r.result)),
        test_model: test,
      });

    });
  },

  afterModel({test_model}) {
    let favicon = this.get('favicon');
    favicon.set_by_test(test_model);
  },

  deactivate() {
    this.get('favicon').set_by_session(this.modelFor('session').session_model);
  },

});
