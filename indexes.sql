
CREATE INDEX eutr__entity__idx ON eutr__entity USING GIN(_fts);
CREATE INDEX eutr__entity__cid ON eutr__entity (id, current);
CREATE INDEX eutr__entity__sid ON eutr__entity (id, "serial");
CREATE INDEX eutr__relation__cid ON eutr__relation (id, current);
CREATE INDEX eutr__relation__sid ON eutr__relation (id, "serial");

CREATE INDEX eutr__entity__actor__sid ON eutr__entity__actor (id, "serial");
CREATE INDEX eutr__relation__associated__sid ON eutr__relation__associated (id, "serial");
CREATE INDEX eutr__entity__interest__sid ON eutr__entity__interest (id, "serial");
CREATE INDEX eutr__entity__action_field__sid ON eutr__entity__action_field (id, "serial");
CREATE INDEX eutr__relation__employment__sid ON eutr__relation__employment (id, "serial");
CREATE INDEX eutr__relation__member__sid ON eutr__relation__member (id, "serial");
CREATE INDEX eutr__relation__topic__sid ON eutr__relation__topic (id, "serial");
CREATE INDEX eutr__relation__turnover__sid ON eutr__relation__turnover (id, "serial");

