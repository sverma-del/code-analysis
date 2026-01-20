from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(5) NOT NULL DEFAULT 'user',
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
COMMENT ON COLUMN "users"."role" IS 'USER: user\nADMIN: admin';
CREATE TABLE IF NOT EXISTS "projects" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "source_type" VARCHAR(6) NOT NULL,
    "github_url" VARCHAR(500),
    "file_path" VARCHAR(500),
    "personas" JSONB NOT NULL,
    "status" VARCHAR(11) NOT NULL DEFAULT 'initialized',
    "error_message" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "projects"."source_type" IS 'ZIP: zip\nGITHUB: github';
COMMENT ON COLUMN "projects"."status" IS 'INITIALIZED: initialized\nPROCESSING: processing\nCOMPLETED: completed\nFAILED: failed';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmetP4zgQwP+VKJ9YiUO0C+yqOp2UtgFy2wdq070VxylyE7f1rWMH21lgOf73k533o9"
    "22gqWs+oXHeCYe/yZ2ZsaPuk89iPnRhEOmt7RHnQAf6i2tID/UdBAEmVQKBJhipRhyyJQE"
    "TLlgwBV6S5sBzOGhpnuQuwwFAlGitzQSYiyF1OWCITLPRCFBtyF0BJ1DsVCO/P3PoaYj4s"
    "F7yJN/g6/ODEHsFfxEnpxbyR3xECiZRcS5UpSzTR2X4tAnmXLwIBaUpNqICCmdQwIZEFA+"
    "XrBQui+9i5eZrCjyNFOJXMzZeHAGQixyy12TgUuJ5IeIkAt+1Odylt+ajZMPJx/fn518PN"
    "R05Ukq+fAULS9be2SoCAxs/UmNAwEiDYUx4wZ9gHAVXWcBWD271KCEjwtWxpfAelV+Prh3"
    "MCRzsZDQTk9X0PpsjDqXxuigeXr6Tq6FMuBGL/cgHmpGYxJphnAB+AJ6TgA4v6PM2wRmje"
    "nzYE0EGddsL74ZsIxiWE/TJKGviFqEC0BcWCGb2P48nOoE1CtA9cnYHLU0OXhDjG7fGrQ0"
    "4PmI6FtgXgfycsQVwIg7wBXoWw3lNqUYArLk/MzblQhPKcUvhTg9G7Z6Y1ewaw+HPem0z/"
    "ktVgLLLlGc9Nvm6KCh4PJbjATMH7AZU5dBuWoHiCrULhBQIB/WUy1alrB6selR8seOngoM"
    "Am9I8EMcrRXMbatvjm2jf1UA3zVsU440lfShJD04K73c6UO0vyz7UpP/atfDgakIUi7mTM"
    "2Y6dnXuvQJhII6hN45wMt9dBJpAqYQ2DDwtgxs0XIf2FcNrHJeppGzOI1M88opcL/eAeY5"
    "hZHsBQgY/Re6gtcclrHl+acRxEChrQY6zqSvoqfsZpTjqGbSPDDapMuIVYf8pl+WAALmym"
    "s5t5ypRKSm7MjBWl555OOyO8XHZGJ1N6g+whB5R9LmZZJo/fdZSFzJQFMzyR8nf+gv8jFV"
    "Wcj7aEPnt6pa3epqRP3eIH9O9PdJc4qQ05C5MEKxZe5cesQrw9WvrauW9h0FN+TCsi8n7Z"
    "Y2R2IRTrdJoM/WAH62FPdZGXbkiBOyjUrootVWeOMN/mqv7unx8TqlyPHx8mJEjhVpzhCG"
    "TgDEYhOYBaM9yzRZgYxTAmqSlT/Hw0E9yrxNOUtFrtD+0zDiu5251BGUCy6kogm4g77xpc"
    "y00xu2yx8u+YB2+ZgVQIR86xM2tf6J/QlEkEAAo+8wCn3xlLUGlm0ZPeva7La0nOoNuRoN"
    "O+Z4bA0uWlrAqAs5R2R+QzrD/lXPtKW+S/0AQyG1zw2rJ0UzgHA80Yb7odFYYzs0Gkt3gx"
    "wqBgsyRpnjQ87BvOaraMP7JY3iiuEbOWBWVWfmF3v1bkiLs95wcJGol7fIvunxC9bG+6bH"
    "LxrY2PlcXDlkzkZ3ZjmLH1+c7Uj4nuHurNIpKjKsAjynDKI5+QQfKilAfUMouVp9O92gQ0"
    "1n4C7tg+RfDUocD8pMQOVCxrhjdE39aXl37SX7SgZkyF3UtZXikZVdJZDp7ExPaX+h/eML"
    "7W+Q8bgBu24JmTPZN5JSkHJrbAAxVn+bABtrleCNFSW4GislxZQIGO3BdSvwnMm+AOeVAn"
    "yDa5vn/7A8/Q8hnehh"
)
