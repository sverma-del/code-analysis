from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "database_models" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "model_name" VARCHAR(255) NOT NULL,
    "table_name" VARCHAR(255),
    "db_fields" JSONB,
    "relationships" JSONB,
    "indexes" JSONB,
    "validators" JSONB,
    "description" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "file_metadata_id" INT REFERENCES "filemetadata" ("id") ON DELETE CASCADE,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
        ALTER TABLE "component_metadata" ADD "technologies" JSONB;
        ALTER TABLE "security_findings" ADD "owasp_category" VARCHAR(100);
        ALTER TABLE "security_findings" ADD "cwe_id" VARCHAR(20);
        ALTER TABLE "security_findings" ADD "recommendation" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "security_findings" DROP COLUMN "owasp_category";
        ALTER TABLE "security_findings" DROP COLUMN "cwe_id";
        ALTER TABLE "security_findings" DROP COLUMN "recommendation";
        ALTER TABLE "component_metadata" DROP COLUMN "technologies";
        DROP TABLE IF EXISTS "database_models";"""


MODELS_STATE = (
    "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"
    "j+fV23Nf5UN+WH7+HxSeWQA="
)
