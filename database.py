import aiosqlite
import os


DB_PATH = "data/donimedia.db"


async def init_db():
    os.makedirs("data", exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:

        # 👤 Foydalanuvchilar
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 🎬 Kinolar
        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            genre TEXT,
            year INTEGER,
            rating REAL DEFAULT 0,
            file_id TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ❤️ Sevimlilar
        await db.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            movie_id INTEGER,
            UNIQUE(user_id, movie_id)
        )
        """)

        # 🕐 Ko‘rish tarixi
        await db.execute("""
        CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER,
            movie_id INTEGER,
            watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


# =========================================================
# 👤 USERS
# =========================================================

async def add_user(user):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        INSERT OR IGNORE INTO users
        (id, username, first_name)
        VALUES (?, ?, ?)
        """, (
            user.id,
            user.username,
            user.first_name
        ))

        await db.commit()


async def get_users_count():
    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute("""
        SELECT COUNT(*) FROM users
        """)

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# 🎬 MOVIES
# =========================================================

async def add_movie(
    code,
    title,
    description,
    genre,
    year,
    rating,
    file_id
):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        INSERT INTO movies
        (
            code,
            title,
            description,
            genre,
            year,
            rating,
            file_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            code,
            title,
            description,
            genre,
            year,
            rating,
            file_id
        ))

        await db.commit()


async def get_movie(code):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        WHERE code = ?
        """, (code,))

        return await cursor.fetchone()


async def get_movie_by_id(movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        WHERE id = ?
        """, (movie_id,))

        return await cursor.fetchone()


async def increase_views(movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        UPDATE movies
        SET views = views + 1
        WHERE id = ?
        """, (movie_id,))

        await db.commit()


async def get_movies_count():
    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute("""
        SELECT COUNT(*) FROM movies
        """)

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# 🔥 PREMYERALAR
# =========================================================

async def get_latest_movies(limit=10):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()


# =========================================================
# ⭐ TOP KINOLAR
# =========================================================

async def get_top_movies(limit=10):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        ORDER BY views DESC, rating DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()


# =========================================================
# ❤️ FAVORITES
# =========================================================

async def add_favorite(user_id, movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        INSERT OR IGNORE INTO favorites
        (user_id, movie_id)
        VALUES (?, ?)
        """, (
            user_id,
            movie_id
        ))

        await db.commit()


async def remove_favorite(user_id, movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        DELETE FROM favorites
        WHERE user_id = ?
        AND movie_id = ?
        """, (
            user_id,
            movie_id
        ))

        await db.commit()


async def is_favorite(user_id, movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute("""
        SELECT 1
        FROM favorites
        WHERE user_id = ?
        AND movie_id = ?
        """, (
            user_id,
            movie_id
        ))

        result = await cursor.fetchone()

        return result is not None


async def get_favorites(user_id):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT movies.*
        FROM favorites
        JOIN movies
        ON favorites.movie_id = movies.id
        WHERE favorites.user_id = ?
        ORDER BY favorites.rowid DESC
        """, (user_id,))

        return await cursor.fetchall()


# =========================================================
# 🕐 HISTORY
# =========================================================

async def add_history(user_id, movie_id):
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        INSERT INTO history
        (user_id, movie_id)
        VALUES (?, ?)
        """, (
            user_id,
            movie_id
        ))

        await db.commit()


async def get_history(user_id, limit=10):
    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT movies.*
        FROM history
        JOIN movies
        ON history.movie_id = movies.id
        WHERE history.user_id = ?
        ORDER BY history.watched_at DESC
        LIMIT ?
        """, (
            user_id,
            limit
        ))

        return await cursor.fetchall()


# =========================================================
# 👀 UMUMIY KO‘RISHLAR
# =========================================================

async def get_total_views():
    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute("""
        SELECT COALESCE(SUM(views), 0)
        FROM movies
        """)

        result = await cursor.fetchone()

        return result[0]

# =========================================================
# 🔎 KINO QIDIRISH
# =========================================================

async def search_movies(query, limit=10):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        WHERE title LIKE ?
           OR genre LIKE ?
           OR code LIKE ?
        ORDER BY views DESC
        LIMIT ?
        """, (
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            limit
        ))

        return await cursor.fetchall()

        # =========================================================
# 🎯 TASODIFIY KINO
# =========================================================

async def get_random_movie():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
        SELECT *
        FROM movies
        ORDER BY RANDOM()
        LIMIT 1
        """)

        return await cursor.fetchone()