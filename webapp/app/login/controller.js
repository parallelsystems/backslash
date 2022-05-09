import { inject as service } from '@ember/service';
import Controller from '@ember/controller';
import UnauthenticatedRouteMixin
  from "ember-simple-auth/mixins/unauthenticated-route-mixin";

export default Controller.extend(UnauthenticatedRouteMixin, {
  authenticator: "authenticator:torii",

  session: service(),

  actions: {
    login() {
      // eslint-disable-next-line no-console
      console.log("Sign in button was clicked.");
      let self = this;
      self.set("login_error", null);
      const credentials = this.getProperties(["username", "password"]);
      self.get("session").authenticate("authenticator:token", credentials).then(
        function () { },
        function () {
          self.set("login_error", "Invalid username and/or password");
        }
      );
    },

    login_google() {
      // eslint-disable-next-line no-console
      console.log("google button was clicked.");
      let self = this;
      self.set("loading", true);
      self.set("login_error", null);
      self
        .get("torii")
        .open("google-oauth2")
        .then(function (auth) {
          return self

            .get("session")
            .authenticate("authenticator:token", auth)
            .then(
              function (data) {
                return data;
              },
              function (error) {
                self.set("login_error", error.error);
              }
            );
        })
        .finally(function () {
          self.set("loading", false);
        });

      return;
    },

    login_azure() {
      let self = this;
      self.set("loading", true);
      self.set("login_error", null);
      self
        .get("torii")
        .open("azure-ad2-oauth2", { "response_type": "id_token+code" })
        .then(function (auth) {
          return self
            .get("session")
            .authenticate("authenticator:token", auth)
            .then(
              function (data) {
                return data;
              },
              function (error) {
                self.set("login_error", error.error);
              }
            );
        })
        .finally(function () {
          self.set("loading", false);
        });

      return;
    }

  }
});
