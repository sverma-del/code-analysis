from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "analysis_configs" (
    "id" UUID NOT NULL PRIMARY KEY,
    "analysis_depth" VARCHAR(20) NOT NULL DEFAULT 'standard',
    "verbosity_level" VARCHAR(20) NOT NULL DEFAULT 'medium',
    "enable_web_search" BOOL NOT NULL DEFAULT True,
    "generate_diagrams" BOOL NOT NULL DEFAULT True,
    "analyze_security" BOOL NOT NULL DEFAULT True,
    "analyze_performance" BOOL NOT NULL DEFAULT False,
    "max_parallel_agents" INT NOT NULL DEFAULT 3,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "analysis_configs" IS 'User configuration for analysis behavior';
        CREATE TABLE IF NOT EXISTS "progress_events" (
    "id" UUID NOT NULL PRIMARY KEY,
    "event_type" VARCHAR(20) NOT NULL,
    "message" VARCHAR(500) NOT NULL,
    "details" JSONB,
    "current_step" INT NOT NULL DEFAULT 0,
    "total_steps" INT NOT NULL DEFAULT 0,
    "percentage" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "agent_name" VARCHAR(100),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "progress_events"."event_type" IS 'PROCESSING: processing\nMILESTONE: milestone\nWARNING: warning\nERROR: error\nINFO: info\nAGENT_START: agent_start\nAGENT_END: agent_end\nWEB_SEARCH: web_search';
COMMENT ON TABLE "progress_events" IS 'Individual progress events during analysis';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "progress_events";
        DROP TABLE IF EXISTS "analysis_configs";"""


MODELS_STATE = (
    "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"
    "k="
)
