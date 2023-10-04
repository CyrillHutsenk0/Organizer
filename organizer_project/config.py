import logging
import os
from datetime import timedelta
from typing import Optional, Union

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(
    name, silent: bool = False, default: Optional[Union[str, int]] = None
) -> Optional[Union[str, int]]:
    """
    Retrieves variable value from both os env and .env files
    :param name: variable name
    :param silent: if False, error will be raised when variable is not set or is empty string
    :param default: default value to use if env var is absent
    :return: variable value
    """
    try:
        var = os.environ[name]
        assert var is not None and var != ""
        return str(os.environ[name])
    except (KeyError, AssertionError):
        if default is not None:
            return default
        if silent:
            return None
        message = f"Expected environment variable '{name}' not set."
        raise OSError(message)


COMMON_LOG_FILENAME = f"{os.getcwd()}/logs/common.log"
if (
    (ENV_LOG_TO_FILE := get_env_variable("LOG_TO_FILE"))
    and ENV_LOG_TO_FILE.isdigit()
    and bool(int(ENV_LOG_TO_FILE))
):
    LOG_TO_FILE = True
else:
    LOG_TO_FILE = False

if LOG_TO_FILE:
    os.makedirs(os.path.dirname(COMMON_LOG_FILENAME), exist_ok=True)
    logging.basicConfig(
        filename=COMMON_LOG_FILENAME,
        filemode="a+",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

SELLER_BASE_API_URL = (
    get_env_variable("SELLER_BASE_API_URL") or "https://api.seller-online.com"
)
SELLER_API_TOKEN = get_env_variable("SELLER_API_TOKEN")
SELLER_OPERATOR_API_TOKEN = get_env_variable("SELLER_OPERATOR_API_TOKEN")

# DB configuration
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"

OLD_POSTGRES_URL = get_env_variable("OLD_POSTGRES_URL")
OLD_POSTGRES_DB = get_env_variable("OLD_POSTGRES_DB")
OLD_POSTGRES_USER = get_env_variable("OLD_POSTGRES_USER")
OLD_POSTGRES_PW = get_env_variable("OLD_POSTGRES_PW")

SELLER_PROD_DB_USER = get_env_variable("SELLER_PROD_DB_USER")
SELLER_PROD_DB_PW = get_env_variable("SELLER_PROD_DB_PW")
SELLER_PROD_DB_HOST = get_env_variable("SELLER_PROD_DB_HOST")
SELLER_PROD_DB_DB = get_env_variable("SELLER_PROD_DB_DB")

TEST_DB_USER = get_env_variable("TEST_DB_USER")
TEST_DB_PW = get_env_variable("TEST_DB_PW")
TEST_DB_HOST = get_env_variable("TEST_DB_HOST")
TEST_DB_NAME = get_env_variable("TEST_DB_NAME")
TEST_DB_URL = (
    f"postgresql://{TEST_DB_USER}:{TEST_DB_PW}@{TEST_DB_HOST}/{TEST_DB_NAME}"
    if all(
        [
            TEST_DB_USER,
            TEST_DB_PW,
            TEST_DB_HOST,
            TEST_DB_NAME,
        ]
    )
    else None
)

LOCALHOST = get_env_variable("LOCALHOST")
LOCALHOST_PORT = get_env_variable("LOCALHOST_PORT")
OLD_API_SERVER = get_env_variable("OLD_API_SERVER")
CURRENT_API_SERVER = get_env_variable("CURRENT_API_SERVER")

SENTRY_DSN = get_env_variable("SENTRY_DSN")

JWT_SECRET_KEY = get_env_variable("JWT_SECRET") or os.urandom(64)
FERNET_KEY = get_env_variable("FERNET_KEY").encode("UTF-8")

DEV = get_env_variable("FLASK_ENV") == "development"

DEBUG = True

STATIC_FOLDER = "static"

IMAGE_STORING_FOLDER = "images"

UPLOADS_STORING_FOLDER = "uploads"

TEMP_FILES_FOLDER = "temp"

DEFAULT_IMAGE_EXTENSIONS = ["JPEG", "JPG", "WEBP"]

UPLOAD_IMAGE_EXTENSIONS = ["WEBP", "JPEG", "JPG", "PNG"]

DIGITAL_FILE_EXTENSIONS = [
    "WEBP",
    "JPEG",
    "JPG",
    "RAR",
    "7z",
    "ZIP",
    "PNG",
    "JP2",
    "GIF",
    "BMP",
    "TIFF",
    "RAW",
    "PDF",
    "DJVU",
    "CGM",
]

FILE_MAX_SIZE = 100000000

JWT_SESSION_DURATION = 1

FLASK_TEST_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": TEST_DB_URL,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/test-seller_api-docs",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    "SQLALCHEMY_ECHO": False,
    "API_TITLE": "TEST SOM API",
    "API_VERSION": "v1",
    "SCHEDULER_API_ENABLED": False,
    "CORS_METHODS": ["GET", "OPTIONS", "POST", "HEAD", "PUT", "DELETE"],
    "CORS_SEND_WILDCARD": False,
    "CORS_SUPPORTS_CREDENTIALS": True,
    "CORS_ALLOW_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
        "content-type",
        "x-proxysession-id",
        "multipart/form-data",
    ],
    "CORS_EXPOSE_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
    ],
    "CORS_ORIGINS": [
        r"^.*192.168.*$",
        r"^.*192.168.*$",
        r"^.*client-dev.handmade-seller.com*$",
        r"^.*client-chat.handmade-seller.com*$",
        r"^.*localhost:8080*$",
    ],
    "CORS_AUTOMATIC_OPTIONS": True,
    "JWT_SECRET_KEY": JWT_SECRET_KEY,
    "JWT_COOKIE_SECURE": not DEV,
    "JWT_HEADER_TYPE": "JWT",
    "JWT_TOKEN_LOCATION": ["cookies"],
    "JWT_COOKIE_SAMESITE": "Lax" if DEV else None,
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=JWT_SESSION_DURATION),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(days=30),
    "JWT_ACCESS_CSRF_HEADER_NAME": "X-CSRF-TOKEN-ACCESS",
    "JWT_REFRESH_CSRF_HEADER_NAME": "X-CSRF-TOKEN-REFRESH",
    "JWT_COOKIE_CSRF_PROTECT": False,
}

FLASK_DEV_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": DB_URL,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "OPENAPI_VERSION": "3.0.3",
    "OPENAPI_URL_PREFIX": "/",
    "OPENAPI_SWAGGER_UI_PATH": "/api-docs" or "/admin-api-docs",
    "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    "SQLALCHEMY_ECHO": True,
    "API_TITLE": "SOM API",
    "API_VERSION": "v1",
    "SCHEDULER_API_ENABLED": True,
    # "SCHEDULER_JOBSTORES": {"default": SQLAlchemyJobStore(url=DB_URL)},
    "SCHEDULER_EXECUTORS": {"default": {"type": "threadpool", "max_workers": 20}},
    "SCHEDULER_JOB_DEFAULTS": {"coalesce": False, "max_instances": 3},
    "CORS_METHODS": ["GET", "OPTIONS", "POST", "HEAD", "PUT", "DELETE", "PATCH"],
    "CORS_SEND_WILDCARD": False,
    "CORS_SUPPORTS_CREDENTIALS": True,
    "CORS_ALLOW_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
        "content-type",
        "x-proxysession-id",
        "multipart/form-data",
    ],
    "CORS_EXPOSE_HEADERS": [
        "Set-Cookie",
        "Authorization",
        "SameSite",
        "Secure",
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Request-Method",
    ],
    "CORS_ORIGINS": [
        r"^.*192.168.*$",
        r"^.*192.168.*$",
        r"^.*client-dev.handmade-seller.com*$",
        r"^.*client-chat.handmade-seller.com*$",
        r"^.*ua4us.com*$",
        r"^.*chat.ua4us.com*$",
        r"^.*admin.ua4us.com*$",
        r"^.*localhost:8080*$",
        r"^.*localhost:30511*$",
        # "http://client-dev.handmade-seller.com",
        # "http://client-chat.handmade-seller.com/",
    ],
    "CORS_AUTOMATIC_OPTIONS": True,
    "JWT_SECRET_KEY": JWT_SECRET_KEY,
    "JWT_COOKIE_SECURE": not DEV,
    "JWT_TOKEN_LOCATION": ["cookies"],
    # "JWT_COOKIE_SAMESITE": "None",
    "JWT_HEADER_TYPE": "JWT",
    "JWT_COOKIE_SAMESITE": "Lax" if DEV else "None",
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=JWT_SESSION_DURATION),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(days=30),
    "JWT_ACCESS_CSRF_HEADER_NAME": "X-CSRF-TOKEN-ACCESS",
    "JWT_REFRESH_CSRF_HEADER_NAME": "X-CSRF-TOKEN-REFRESH",
    "JWT_COOKIE_CSRF_PROTECT": False,  # temporally
    # "JWT_COOKIE_CSRF_PROTECT": True,  # temporally
}

FLASK_PROD_CONFIG = {}

# APSCHEDULER_RUN_INTERVAL = {"minutes": 1 if DEBUG else 10}

PROCRASTINATE_SCRIPT_PATH = f"{os.getcwd()}/scripts/run_jobs_worker"

CACHING_OPTIONS = {
    "DEBUG": DEBUG,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 60,
    "CACHE_KEY_PREFIX": "som_",
    "CACHE_REDIS_HOST": get_env_variable(
        "REDIS_HOST", silent=True, default="localhost"
    ),
    "CACHE_REDIS_PORT": get_env_variable("REDIS_HOST", silent=True, default=6379),
    # "CACHE_REDIS_PASSWORD": "",
    "CACHE_REDIS_DB": 3,
    # "CACHE_REDIS_URL": "",
}


ETSY_CONF = {
    "key": get_env_variable("ETSY_KEY"),
    "secret": get_env_variable("ETSY_SECRET"),
    "scopes": (  # V3 scope
        "address_r",  # See billing and shipping addresses
        "address_w",  # Update billing and shipping addresses
        "email_r",  # Read a member's email address
        "listings_r",  # See all listings (including expired etc)
        "listings_w",  # Create/edit listings
        "listings_d",  # Delete listings
        "profile_r",  # See all profile data
        "profile_w",  # Update user profile, avatar, etc
        "shops_r",  # See private shop info
        "shops_w",  # Update shop
        "transactions_r",  # See all checkout/payment data
        "transactions_w",  # Update receipts
    ),
    "scope": ("transactions_r", "transactions_w"),  # V2 scope
    "expire_delta": 60,  # Refresh token if it expired in less than N seconds
    "rate_limits": {
        "calls_per_day": 6000,  # Use only N requests per day
    },
    "redirect_url": "https://my.seller-online.com/etsy-v3-connect.php",
    "redirect_beta_url": "https://my.seller-online.com/etsy-v3-connect-beta.php",
    "redirect_atlas_url": "https://my.seller-online.com/etsy-v3-connect-ecom.php",
    "request": {
        "timeout": 10,  # Cancel request after N seconds,
        "headers": {},  # Request headers
    },
    "available_includes": {
        "getListing": frozenset({"Shipping", "Images", "Shop", "User"}),
        "getListingsByListingIds": frozenset({"Shipping", "Images", "Shop", "User"}),
        "getListingInventory": frozenset({"Listing"}),
        "default": frozenset("Transactions"),  # included by default
    },
    "personalization_property_ids": [54, 513],
    "personalization_property_none": [
        None,
        "No personalized",
        "Not requested on this item.",
    ],
    "allowed_carriers": [
        "ups",
        "usps",
        "gls",
        "tnt",
        "fedex",
        "dhl",
        "ukrposhta",
        "magyar-posta",
        "posta-moldovei",
        "kazpost",
        "latvijas-pasts",
        "belpost",
        "landmark-global",
        "correos-de-mexico",
        "russian-post",
        "poczta-polska",
        "dhl-global-mail",
        "dpd",
    ],
}

UKTVED_SELECTABLE_LENGTH = 10

RENAME_SHOP_REQUEST_STATUS = ["pending", "accepted", "rejected"]

SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 30, "max_overflow": 60}


VARIATION_QUERY_PER_PAGE_LIMIT = 10

AWS_TLD = "amazonaws.com"
AWS_S3 = "s3"
AWS_S3_REGION = "us-east-2"

S3_ACCESS_KEY_ID = get_env_variable("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = get_env_variable("S3_SECRET_ACCESS_KEY")

S3_IMAGE_BUCKET = get_env_variable("S3_IMAGE_BUCKET")
S3_DIGITAL_PRODUCT_BUCKET = get_env_variable("S3_DIGITAL_PRODUCT_BUCKET")

BETA_S3_IMAGE_BUCKET = get_env_variable("BETA_S3_IMAGE_BUCKET")
BETA_S3_DIGITAL_PRODUCT_BUCKET = get_env_variable("BETA_S3_DIGITAL_PRODUCT_BUCKET")

EXPIRE_DIGITAL_PRODUCT_MONTH = 6

SELLER_LOG_IN_REDIRECT = get_env_variable("SELLER_LOG_IN_REDIRECT")
CUSTOMER_LOG_IN_REDIRECT = get_env_variable("CUSTOMER_LOG_IN_REDIRECT")

SELLER_ONLINE_STORAGE_PATH = get_env_variable("SELLER_ONLINE_STORAGE_PATH")

SELLER_ONLINE_HOST = get_env_variable("SELLER_ONLINE_HOST")
MARKET_RSA_USER = get_env_variable("MARKET_RSA_USER")
MARKET_RSA_FILE_PATH = get_env_variable("MARKET_RSA_FILE_PATH")
MARKET_RSA_SECRET = get_env_variable("MARKET_RSA_SECRET")


USER_REGISTRATION_NAME_FIELD_MAX_CHARACTERS = 255
USER_REGISTRATION_LAST_NAME_FIELD_MAX_CHARACTERS = 255

RSA_PUBLIC_KEY = get_env_variable("RSA_PUBLIC_KEY")
RSA_PRIVATE_KEY = get_env_variable("RSA_PRIVATE_KEY")

MAIL_DRIVER = get_env_variable("MAIL_DRIVER")
MAIL_HOST = get_env_variable("MAIL_HOST")
MAIL_PORT = get_env_variable("MAIL_PORT")
MAIL_USERNAME = get_env_variable("MAIL_USERNAME")
MAIL_PASSWORD = get_env_variable("MAIL_PASSWORD")
MAIL_ENCRYPTION = get_env_variable("MAIL_ENCRYPTION")
MAIL_FROM_NAME = get_env_variable("MAIL_FROM_NAME")

SMTP = {
    "host": MAIL_HOST,
    "port": MAIL_PORT,
    "login": MAIL_USERNAME,
    "password": MAIL_PASSWORD,
    "use_tls": True if MAIL_ENCRYPTION == "tls" else False,
}

DEFAULT_FROM = {"name": MAIL_FROM_NAME, "email": MAIL_USERNAME}
WEBHOOK_ATTEMPTS_TIME_DELAY_DICT = {1: None, 2: 1, 3: 1, 4: 10, 5: 60}

IMAGES_PROXY = get_env_variable("IMAGES_PROXY")

PRODUCT_CATEGORY_SEARCH_LIMIT = 5

TASK_LIST = []