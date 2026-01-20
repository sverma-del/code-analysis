from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "projects" ALTER COLUMN "status" TYPE VARCHAR(50) USING "status"::VARCHAR(50);
        COMMENT ON COLUMN "projects"."status" IS 'INITIALIZED: initialized
PREPROCESSING: preprocessing
PREPROCESSING_COMPLETE: preprocessing_complete
READY_FOR_AGENTS: ready_for_agents
PROCESSING: processing
COMPLETED: completed
FAILED: failed';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "projects"."status" IS 'INITIALIZED: initialized
PROCESSING: processing
COMPLETED: completed
FAILED: failed';
        ALTER TABLE "projects" ALTER COLUMN "status" TYPE VARCHAR(11) USING "status"::VARCHAR(11);"""


MODELS_STATE = (
    "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"
    "AOtJLg=="
)
