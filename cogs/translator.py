from discord import Locale
from discord.app_commands import TranslationContext, Translator, locale_str

TLANSLATION_DATA: dict[Locale, dict[str, str]] = {
    Locale.korean: {
        "ニックネームからユーザーのプロフィールを取得します。": "닉네임에서 사용자의 프로필을 가져옵니다.",
        "ユーザーの取得に失敗しました。": "사용자 확보에 실패했습니다.",
        "そのニックネームのユーザーは存在しません。": "해당 닉네임의 사용자는 존재하지 않습니다.",
        "カップル": "커플",
        "クラン": "클랜",
        "情報": "정보",
        "誕生日": "생일",
        "レベル": "레벨",
    },
}

FMT_TLANSLATION_DATA: dict[Locale, dict[str, str]] = {
    Locale.korean: {
        "{nickname} のプロフィール": "{nickname} 의 프로필",
    },
}


class FreezeTranslator(Translator):
    async def translate(
        self,
        string: locale_str,
        locale: Locale,
        context: TranslationContext = None,
    ):
        if "fmt_arg" in string.extras:
            fmt = FMT_TLANSLATION_DATA.get(locale, {}).get(
                string.message, string.message
            )
            return fmt.format(**(string.extras["fmt_arg"]))
        return TLANSLATION_DATA.get(locale, {}).get(string.message, string.message)
