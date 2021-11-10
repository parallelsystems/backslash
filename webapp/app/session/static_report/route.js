import { hash } from "rsvp";
import { inject as service } from '@ember/service';
import Route from "@ember/routing/route";
import ComplexModelRoute from "../../mixins/complex-model-route";

export default Route.extend(ComplexModelRoute, {
  api: service(),

  async model () {
    let self = this;
    let session_model = this.modelFor("session").session_model;
    let tests = await this.store.query("test",  {
      session_id: session_model.id,
      page_size: 1000,
    });
    let test_metadata = {}
    for await (const test of tests.content) {
      let data = await self
      .get("api")
      .call("get_metadata", {
        entity_type: "test",
        entity_id: parseInt(test.id),
      }).then(r => r.result);
      test_metadata[test.id] = data;
    };
    
    return hash({
      session_model: session_model,
      user: this.modelFor("session").user,
      timings: this.modelFor("session").timings,
      related_entities: self.store.query("entity", {
        session_id: session_model.id,
        page_size: 100,
      }),
      metadata: this.modelFor("session").metadata,
      tests: tests,
      test_metadata: test_metadata,
    });
  },
});


