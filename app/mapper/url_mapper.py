from urllib.parse import urlencode


class URLMapper:
    BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    OPTIONS = {
        "producao": 2,
        "processamento": 3,
        "comercializacao": 4,
        "importacao": 5,
        "exportacao": 6,
    }

    SUBOPTIONS = {
        "processamento": {
            "viniferas": 1,
            "americanas_hibridas": 2,
            "uvas_de_mesa": 3,
            "sem_classificacao": 4,
        },
        "importacao": {
            "vinhos_de_mesa": 1,
            "espumantes": 2,
            "uvas_frescas": 3,
            "uvas_passas": 4,
            "suco_de_uva": 5,
        },
        "exportacao": {
            "vinhos_de_mesa": 1,
            "espumantes": 2,
            "uvas_frescas": 3,
            "suco_de_uva": 4,
        },
    }

    @classmethod
    def build_url(cls, option, suboption=None, year=None):
        if option not in cls.OPTIONS:
            raise ValueError(f"Invalid option: {option}")

        params = {"opcao": f"opt_{cls.OPTIONS[option]:02}"}

        if suboption:
            if (
                option not in cls.SUBOPTIONS
                or suboption not in cls.SUBOPTIONS[option]
            ):
                raise ValueError(
                    f"Invalid suboption: {suboption} for option: {option}"
                )
            params["subopcao"] = (
                f"subopt_{cls.SUBOPTIONS[option][suboption]:02}"
            )

        if year:
            params["ano"] = year

        return f"{cls.BASE_URL}?{urlencode(params)}"


print(URLMapper.build_url("producao", year=2023))
