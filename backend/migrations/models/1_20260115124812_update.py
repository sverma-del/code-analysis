from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "filemetadata" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file_path" VARCHAR(500) NOT NULL,
    "file_name" VARCHAR(255) NOT NULL,
    "extension" VARCHAR(20) NOT NULL,
    "size" INT NOT NULL,
    "is_entry_point" BOOL NOT NULL DEFAULT False,
    "content_summary" TEXT,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "codechunk" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "chunk_type" VARCHAR(50) NOT NULL,
    "start_line" INT NOT NULL,
    "end_line" INT NOT NULL,
    "file_metadata_id" INT NOT NULL REFERENCES "filemetadata" ("id") ON DELETE CASCADE,
    "project_id" UUID NOT NULL REFERENCES "projects" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "filemetadata";
        DROP TABLE IF EXISTS "codechunk";"""


MODELS_STATE = (
    "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"
    "l3FduEjF7gnK3zVuLd/7zxIQE="
)
