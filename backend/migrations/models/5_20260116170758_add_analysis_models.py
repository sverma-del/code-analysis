from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "api_endpoints" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "method" VARCHAR(10) NOT NULL,
    "path" VARCHAR(500) NOT NULL,
    "handler_function" VARCHAR(255),
    "request_schema" JSONB,
    "response_schema" JSONB,
    "requires_auth" BOOL NOT NULL DEFAULT False,
    "description" TEXT,
    "line_number" INT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file_metadata_id" INT NOT NULL REFERENCES "filemetadata" ("id") ON DELETE CASCADE,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "analysis_artifacts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "artifact_type" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL,
    "status" VARCHAR(11) NOT NULL DEFAULT 'pending',
    "error_message" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "analysis_artifacts"."artifact_type" IS 'ARCHITECTURE_MAP: architecture_map\nAPI_CATALOG: api_catalog\nDEPENDENCY_GRAPH: dependency_graph\nDATABASE_SCHEMA: database_schema\nSECURITY_ANALYSIS: security_analysis\nERROR_HANDLING: error_handling\nPERFORMANCE_ANALYSIS: performance_analysis\nSETUP_INSTRUCTIONS: setup_instructions';
COMMENT ON COLUMN "analysis_artifacts"."status" IS 'PENDING: pending\nIN_PROGRESS: in_progress\nCOMPLETED: completed\nFAILED: failed';
        CREATE TABLE IF NOT EXISTS "component_metadata" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "component_name" VARCHAR(255) NOT NULL,
    "component_type" VARCHAR(10) NOT NULL,
    "file_paths" JSONB NOT NULL,
    "responsibilities" TEXT,
    "dependencies" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "component_metadata"."component_type" IS 'CONTROLLER: controller\nSERVICE: service\nMODEL: model\nUTILITY: utility\nMIDDLEWARE: middleware\nREPOSITORY: repository\nHELPER: helper';
        CREATE TABLE IF NOT EXISTS "dependency_edges" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dependency_type" VARCHAR(8) NOT NULL,
    "strength" INT NOT NULL DEFAULT 1,
    "details" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE,
    "source_file_id" INT NOT NULL REFERENCES "filemetadata" ("id") ON DELETE CASCADE,
    "target_file_id" INT NOT NULL REFERENCES "filemetadata" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "dependency_edges"."dependency_type" IS 'IMPORTS: imports\nCALLS: calls\nINHERITS: inherits\nUSES: uses';
        CREATE TABLE IF NOT EXISTS "security_findings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "finding_type" VARCHAR(100) NOT NULL,
    "file_paths" JSONB NOT NULL,
    "code_snippets" JSONB,
    "description" TEXT,
    "severity" VARCHAR(20),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
        ALTER TABLE "filemetadata" ADD "contains_auth" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "filemetadata" ADD "contains_db_models" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "filemetadata" ADD "exports" JSONB;
        ALTER TABLE "filemetadata" ADD "complexity_score" INT;
        ALTER TABLE "filemetadata" ADD "imports" JSONB;
        ALTER TABLE "filemetadata" ADD "contains_api_routes" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "filemetadata" DROP COLUMN "contains_auth";
        ALTER TABLE "filemetadata" DROP COLUMN "contains_db_models";
        ALTER TABLE "filemetadata" DROP COLUMN "exports";
        ALTER TABLE "filemetadata" DROP COLUMN "complexity_score";
        ALTER TABLE "filemetadata" DROP COLUMN "imports";
        ALTER TABLE "filemetadata" DROP COLUMN "contains_api_routes";
        DROP TABLE IF EXISTS "api_endpoints";
        DROP TABLE IF EXISTS "component_metadata";
        DROP TABLE IF EXISTS "analysis_artifacts";
        DROP TABLE IF EXISTS "dependency_edges";
        DROP TABLE IF EXISTS "security_findings";"""


MODELS_STATE = (
    "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"
    "nxf4/FJhY="
)
