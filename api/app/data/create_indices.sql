-- PostgreSQL indices for Apache AGE in LightRAG
-- Replace 'embediq' with your graph name if different

-- Load AGE extension
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- Create indices for better performance
CREATE INDEX CONCURRENTLY entity_p_idx ON embediq."Entity" (id);
CREATE INDEX CONCURRENTLY vertex_p_idx ON embediq."_ag_label_vertex" (id);
CREATE INDEX CONCURRENTLY directed_p_idx ON embediq."DIRECTED" (id);
CREATE INDEX CONCURRENTLY directed_eid_idx ON embediq."DIRECTED" (end_id);
CREATE INDEX CONCURRENTLY directed_sid_idx ON embediq."DIRECTED" (start_id);
CREATE INDEX CONCURRENTLY directed_seid_idx ON embediq."DIRECTED" (start_id,end_id);
CREATE INDEX CONCURRENTLY edge_p_idx ON embediq."_ag_label_edge" (id);
CREATE INDEX CONCURRENTLY edge_sid_idx ON embediq."_ag_label_edge" (start_id);
CREATE INDEX CONCURRENTLY edge_eid_idx ON embediq."_ag_label_edge" (end_id);
CREATE INDEX CONCURRENTLY edge_seid_idx ON embediq."_ag_label_edge" (start_id,end_id);
CREATE INDEX CONCURRENTLY vertex_idx_node_id ON embediq."_ag_label_vertex" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
CREATE INDEX CONCURRENTLY entity_idx_node_id ON embediq."Entity" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
CREATE INDEX CONCURRENTLY entity_node_id_gin_idx ON embediq."Entity" USING gin(properties);
ALTER TABLE embediq."DIRECTED" CLUSTER ON directed_sid_idx;

-- In case you need to drop indices
/*
DROP INDEX entity_p_idx;
DROP INDEX vertex_p_idx;
DROP INDEX directed_p_idx;
DROP INDEX directed_eid_idx;
DROP INDEX directed_sid_idx;
DROP INDEX directed_seid_idx;
DROP INDEX edge_p_idx;
DROP INDEX edge_sid_idx;
DROP INDEX edge_eid_idx;
DROP INDEX edge_seid_idx;
DROP INDEX vertex_idx_node_id;
DROP INDEX entity_idx_node_id;
DROP INDEX entity_node_id_gin_idx;
*/ 