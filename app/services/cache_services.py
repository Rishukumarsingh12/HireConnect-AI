import json
from pathlib import Path


class CacheService:

    def __init__(self):

        self.cache_file = Path(
            "data/cache/company_cache.json"
        )

        self.cache_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.cache_file.exists():

            with open(
                self.cache_file,
                "w"
            ) as f:

                json.dump({}, f)

    def load_cache(self):

        with open(
            self.cache_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def save_cache(self, cache):

        with open(
            self.cache_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                cache,
                f,
                indent=4
            )

    def get_company(
        self,
        company_name: str
    ):

        cache = self.load_cache()

        return cache.get(
            company_name.lower()
        )

    def save_company(
        self,
        company_name: str,
        company_data: dict
    ):

        cache = self.load_cache()

        cache[
            company_name.lower()
        ] = company_data

        self.save_cache(cache)