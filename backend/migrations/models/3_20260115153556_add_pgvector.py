from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE EXTENSION IF NOT EXISTS vector;
        ALTER TABLE "codechunk" DROP COLUMN IF EXISTS "embedding";
        ALTER TABLE "codechunk" ADD COLUMN "embedding" vector(1536);
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "codechunk" DROP COLUMN "embedding";"""


MODELS_STATE = (
    "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"
    "A1r8E5ldCkgvCM6e8x7k/f/cpbaz"
)
