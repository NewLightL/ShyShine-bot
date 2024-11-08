'''Config for bot'''

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    '''Create settings for bot'''
    bot_token: str
    admin_id1: int
    admin_id2: int
    admin_id3: int

    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')


def load_sett() -> dict[str, str|list[int]]:
    """Loading bot settings from env to main file

    Returns
    -------
    dict[str, str|list[int]]
        Settings bot
    """
    sett = Settings().model_dump()  # type: ignore
    sett['my_channel'] = {
            '@': {'pere': '@ShyShine_pere',
                  'wildberries': '@ShyShine_WB',
                  'ozon': '@ShyShine_Ozon',
                  'aliexpress': '@ShyShine_AliExpress'},

            'https': {'pere': 'https://t.me/ShyShine_pere',
                      'wildberries': 'https://t.me/ShyShine_WB',
                      'ozon': 'https://t.me/ShyShine_Ozon',
                      'aliexpress': 'https://t.me/ShyShine_AliExpress'},
                   }
    sett['admin_lst'] = [sett[f'admin_id{i}'] for i in range(1, 4)]
    return sett
