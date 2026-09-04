import aiosqlite
import os


# =========================================================
# DATABASE
# =========================================================

DB_PATH = "data/donimedia.db"


# =========================================================
# DATABASE NI YARATISH
# =========================================================

async def init_db():
    """
    Database va barcha jadvallarni yaratadi.
    """

    os.makedirs("data", exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:

        # -------------------------------------------------
        # USERS
        # -------------------------------------------------

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # -------------------------------------------------
        # MOVIES
        # -------------------------------------------------

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

        # -------------------------------------------------
        # FAVORITES
        # -------------------------------------------------

        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, movie_id),

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY(movie_id)
                    REFERENCES movies(id)
                    ON DELETE CASCADE
            )
        """)

        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        await db.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY(movie_id)
                    REFERENCES movies(id)
                    ON DELETE CASCADE
            )
        """)

        await db.commit()

    print("🗄 Database jadvallari tayyor!")


# =========================================================
# USERS
# =========================================================

async def add_user(user):
    """
    Telegram foydalanuvchisini bazaga qo‘shadi.
    Agar mavjud bo‘lsa, ma’lumotlarini yangilaydi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO users (
                id,
                username,
                first_name,
                last_name
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name
            """,
            (
                user.id,
                user.username,
                user.first_name,
                user.last_name
            )
        )

        await db.commit()


async def get_user(user_id):
    """
    Bitta foydalanuvchini olish.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return await cursor.fetchone()


async def get_users_count():
    """
    Botdagi jami foydalanuvchilar soni.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# MOVIES
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
    """
    Yangi kino qo‘shadi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            INSERT INTO movies (
                code,
                title,
                description,
                genre,
                year,
                rating,
                file_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(code).strip(),
                title,
                description,
                genre,
                year,
                rating,
                file_id
            )
        )

        await db.commit()

        return cursor.lastrowid


async def get_movie(code):
    """
    Kino kod bo‘yicha qidiriladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM movies
            WHERE code = ?
            """,
            (str(code).strip(),)
        )

        return await cursor.fetchone()


async def get_movie_by_id(movie_id):
    """
    Kino ID bo‘yicha qidiriladi.

    Bu funksiya:
    ❤️ Sevimlilar
    📜 Tarix
    kabi funksiyalar uchun kerak.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM movies
            WHERE id = ?
            """,
            (movie_id,)
        )

        return await cursor.fetchone()


async def get_all_movies():
    """
    Barcha kinolarni olish.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM movies
            ORDER BY id DESC
            """
        )

        return await cursor.fetchall()


async def delete_movie(movie_id):
    """
    Kino ID bo‘yicha o‘chiriladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            DELETE FROM movies
            WHERE id = ?
            """,
            (movie_id,)
        )

        await db.commit()


async def delete_movie_by_code(code):
    """
    Kino kodi bo‘yicha o‘chiriladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            DELETE FROM movies
            WHERE code = ?
            """,
            (str(code).strip(),)
        )

        await db.commit()


async def get_movies_count():
    """
    Jami kinolar soni.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM movies
            """
        )

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# VIEWS
# =========================================================

async def increase_views(movie_id):
    """
    Kino ko‘rilishlar sonini +1 qiladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE movies
            SET views = views + 1
            WHERE id = ?
            """,
            (movie_id,)
        )

        await db.commit()


async def get_total_views():
    """
    Barcha kinolarning umumiy ko‘rilishlari.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COALESCE(SUM(views), 0)
            FROM movies
            """
        )

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# SEARCH
# =========================================================

async def search_movies(query, limit=10):
    """
    Kino nomi, janri yoki kodi bo‘yicha qidiradi.
    """

    query = query.strip()

    if not query:
        return []

    search = f"%{query}%"

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM movies
            WHERE
                title LIKE ?
                OR description LIKE ?
                OR genre LIKE ?
                OR code LIKE ?
            ORDER BY
                views DESC,
                id DESC
            LIMIT ?
            """,
            (
                search,
                search,
                search,
                search,
                limit
            )
        )

        return await cursor.fetchall()


# =========================================================
# RANDOM MOVIE
# =========================================================

async def get_random_movie():
    """
    Tasodifiy kino qaytaradi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT *
            FROM movies
            ORDER BY RANDOM()
            LIMIT 1
            """
        )

        return await cursor.fetchone()


# =========================================================
# FAVORITES
# =========================================================

async def add_favorite(user_id, movie_id):
    """
    Kinoni sevimlilarga qo‘shadi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO favorites (
                user_id,
                movie_id
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                movie_id
            )
        )

        await db.commit()


async def remove_favorite(user_id, movie_id):
    """
    Kinoni sevimlilardan o‘chiradi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            DELETE FROM favorites
            WHERE user_id = ?
            AND movie_id = ?
            """,
            (
                user_id,
                movie_id
            )
        )

        await db.commit()


async def is_favorite(user_id, movie_id):
    """
    Kino foydalanuvchining sevimlilarida bormi?
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT id
            FROM favorites
            WHERE user_id = ?
            AND movie_id = ?
            LIMIT 1
            """,
            (
                user_id,
                movie_id
            )
        )

        result = await cursor.fetchone()

        return result is not None


async def get_favorites(user_id):
    """
    Foydalanuvchining barcha sevimli kinolarini oladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT movies.*
            FROM favorites

            INNER JOIN movies
                ON favorites.movie_id = movies.id

            WHERE favorites.user_id = ?

            ORDER BY favorites.id DESC
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def get_favorites_count(user_id):
    """
    Foydalanuvchining sevimli kinolari soni.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM favorites
            WHERE user_id = ?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# HISTORY
# =========================================================

async def add_history(user_id, movie_id):
    """
    Kino ko‘rilganini tarixga yozadi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO history (
                user_id,
                movie_id
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                movie_id
            )
        )

        await db.commit()


async def get_history(user_id, limit=20):
    """
    Foydalanuvchining ko‘rgan kinolarini oladi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """
            SELECT
                movies.*,
                history.watched_at

            FROM history

            INNER JOIN movies
                ON history.movie_id = movies.id

            WHERE history.user_id = ?

            ORDER BY history.id DESC

            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        )

        return await cursor.fetchall()


async def clear_history(user_id):
    """
    Foydalanuvchining ko‘rish tarixini tozalaydi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            DELETE FROM history
            WHERE user_id = ?
            """,
            (user_id,)
        )

        await db.commit()


async def get_history_count(user_id):
    """
    Foydalanuvchi tarixidagi kino soni.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM history
            WHERE user_id = ?
            """,
            (user_id,)
        )

        result = await cursor.fetchone()

        return result[0]


# =========================================================
# STATISTICS
# =========================================================

async def get_statistics():
    """
    Bot statistikasi.
    """

    async with aiosqlite.connect(DB_PATH) as db:

        # Users
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )
        users = (await cursor.fetchone())[0]

        # Movies
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM movies
            """
        )
        movies = (await cursor.fetchone())[0]

        # Views
        cursor = await db.execute(
            """
            SELECT COALESCE(SUM(views), 0)
            FROM movies
            """
        )
        views = (await cursor.fetchone())[0]

        # Favorites
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM favorites
            """
        )
        favorites = (await cursor.fetchone())[0]

        # History
        cursor = await db.execute(
            """
            SELECT COUNT(*)
            FROM history
            """
        )
        history = (await cursor.fetchone())[0]

        return {
            "users": users,
            "movies": movies,
            "views": views,
            "favorites": favorites,
            "history": history
        }