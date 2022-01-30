import Component from "@ember/component";
import EmberObject from "@ember/object";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default Component.extend({
  runtime_config: service(),

  classNames: "p-3 test-overview-full overview",

  session_model: null,
  test_metadata: null,
  test_model: null,
  show_details: false,

  slash_tags: computed("test_metadata", function() {
    let metadata = this.get("test_metadata");
    if (!metadata) {
      return null;
    }
    let tags = metadata["slash::tags"];
    if (!tags) {
      return null;
    }

    let returned = [];
    for (const [name, value] of Object.entries(tags.values)) {
      returned.push({ name: name, value: value });
    }
    for (let name of tags.names) {
      if (tags.values.hasOwnProperty(name)) {
        continue;
      }
      returned.push({ name: name, value: null });
    }
    return returned;
  }),

  docstring: computed("test_docstring", function() {
    let docstring = this.get("test_docstring");
    return docstring;
  }),

  metadata_links: computed("test_metadata", function() {
    let returned = [];
    let metadata = this.get("test_metadata");

    for (let link of this.get("runtime_config").get_cached(
      "test_metadata_links"
    )) {
      let value = metadata[link.key];
      if (value) {
        returned.push({
          name: link.name,
          url: value,
          icon: link.icon,
        });
      }
      return returned;
    }
  }),

  metadata_display_items: computed(function() {
    return this.get("runtime_config").get_cached("test_metadata_display_items");
  }),

  scm_details: computed("test_model", function() {
    let self = this;
    let test_model = self.get("test_model");

    if (!test_model.get("scm")) {
      return {};
    }

    let returned = EmberObject.create({
      Revision: test_model.get("scm_revision"),
      "File Hash": test_model.get("file_hash"),
      "Local Branch": test_model.get("scm_local_branch"),
      "Remote Branch": test_model.get("scm_remote_branch"),
    });
    return returned;
  }),
  display_params: computed("test_model.{parameters,variation}", function() {
    let seen = new Set();
    let returned = [];

    for (let params of [
      this.get("test_model.parameters"),
      this.get("test_model.variation"),
    ]) {
      if (!params) {
        continue;
      }
      for (var key in params) {
        if (params.hasOwnProperty(key)) {
          if (!seen.has(key)) {
            let parts = key.split(".");
            let short = key;
            let full = null;
            if (parts.length > 1) {
              short = parts[parts.length - 1];
              full = key;
            }
            returned.push({
              name: key,
              short_name: short,
              full_name: full,
              value: params[key],
              last: false,
            });
            seen.add(key);
          }
        }
      }
    }
    if (returned.length > 0) {
      returned[returned.length - 1].last = true;
    }
    return returned;
  }),
});
