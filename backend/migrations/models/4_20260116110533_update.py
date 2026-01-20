from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "projects" ADD "analysis_summary" JSONB;
        ALTER TABLE "projects" ADD "detected_language" VARCHAR(100);
        ALTER TABLE "projects" ADD "endpoint_count" INT NOT NULL DEFAULT 0;
        ALTER TABLE "projects" ADD "file_count" INT NOT NULL DEFAULT 0;
        ALTER TABLE "projects" ADD "detected_framework" VARCHAR(100);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "projects" DROP COLUMN "analysis_summary";
        ALTER TABLE "projects" DROP COLUMN "detected_language";
        ALTER TABLE "projects" DROP COLUMN "endpoint_count";
        ALTER TABLE "projects" DROP COLUMN "file_count";
        ALTER TABLE "projects" DROP COLUMN "detected_framework";"""


MODELS_STATE = (
    "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"
    "chR6QXC2yoP69/8Dgd3WOw=="
)
