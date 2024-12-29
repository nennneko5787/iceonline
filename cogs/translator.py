from discord import Locale
from discord.app_commands import TranslationContext, Translator, locale_str

TLANSLATION_DATA: dict[Locale, dict[str, str]] = {
    Locale.korean: {
        "プレイヤーのプロフィールを確認します。": "플레이어의 프로필을 확인합니다.",
        "ニックネーム": "닉네임",
        "プレイヤーのニックネーム": "플레이어 닉네임",
        "サーバーとの通信に失敗しました。": "서버와의 통신에 실패했습니다.",
        "そのニックネームのプレイヤーは存在しません。": "그 닉네임의 플레이어는 존재하지 않습니다.",
        "カップル": "커플",
        "カップルなし": "커플 없음",
        "クラン": "클랜",
        "情報": "정보",
        "誕生日": "생일",
        "レベル": "레벨",
        "血液型": "혈액형",
        "MBTI": "MBTI",
        "趣味": "취미",
        "特技": "특기",
        "好きなモード": "좋아하는 모드",
        "好きな食べ物": "좋아하는 음식",
        "嫌いな食べ物": "싫어하는 음식",
        "お気に入りの曲": "좋아하는 노래",
        "これはあなたが表示させたプロフィールではありません！": "이것은 귀하가 표시한 프로필이 아닙니다!",
        "ランクマッチでの戦績": "랭크 매치 전적",
        "アカウントをリンクします。": "계정을 연결합니다.",
        "会員番号": "회원번호",
        "リンクしたいプレイヤーの会員番号(設定から確認できます)": "연동하고자 하는 플레이어의 회원번호(설정에서 확인 가능)",
        "リンクしたいプレイヤーのニックネーム": "연결하고 싶은 선수의 닉네임",
        "会員番号かニックネームが間違っています。": "회원번호 또는 닉네임이 잘못되었습니다.",
        "アカウントをリンクしました！": "계정을 연결했습니다!",
        "クイックマッチの現在の情報を取得します。アカウントをリンクする必要があります。": "퀵매치의 현재 정보를 가져옵니다. 계정을 연결해야 합니다.",
        "現在のクイックマッチの情報": "현재 퀵매치 정보",
        "クランの情報を確認します。": "클랜 정보를 확인합니다.",
        "クラン名": "클랜명",
        "クランの名前": "클랜 이름",
        "その名前のクランは存在しません。": "그 이름의 클랜은 존재하지 않습니다.",
        "クラン作成日": "클랜 생성일",
        "クラン順位": "클랜 순위",
        "クラン人員": "클랜 인원",
        "クラン点数": "클랜 점수",
        "レベル条件": "레벨 조건",
        "クランゲーム進行": "클랜 게임 진행",
        "参加可能": "참여 가능",
        "こおり鬼モード ランク条件": "얼음땡 모드 랭크 조건",
        "チームバトルモード ランク条件": "팀배틀 모드 랭크 조건",
        "1対1モード ランク条件": "1 vs 1 모드 랭크 조건",
        "旗取りモード ランク条件": "깃발뺏기 모드 랭크 조건",
        "墜落モード ランク条件": "추락 모드 랭크 조건",
        "こおり鬼(チーム) ランク条件": "얼음땡(팀)",
        "面接チャット": "인터뷰 채팅",
        "プロフィールを編集します。": "프로필을 편집합니다.",
        "一言紹介": "한마디소개",
        "誕生日の表示を切り替える": "생일표시전환",
        "誕生日の表示を切り替えるかどうか": "생일표시전환여부",
        "はい": "예",
        "いいえ": "아니요",
        "情報1": "정보1",
        "情報2": "정보2",
        "情報3": "정보3",
        "情報4": "정보4",
        "情報5": "정보5",
        "情報6": "정보6",
        "情報7": "정보7",
        "情報8": "정보8",
        "情報1の内容": "정보1의내용",
        "情報2の内容": "정보2의내용",
        "情報3の内容": "정보3의내용",
        "情報4の内容": "정보4의내용",
        "情報5の内容": "정보5의내용",
        "情報6の内容": "정보6의내용",
        "情報7の内容": "정보7의내용",
        "情報8の内容": "정보8의내용",
        "プロフィールを編集しました。": "프로필을 편집했습니다.",
        "プロフィールは何一つ編集されませんでした。": "프로필은 아무것도 편집되지 않았습니다.",
        "これはあなたが表示させたランキングではありません！": "이것은 귀하가 표시한 순위가 아닙니다!",
        "スコア": "점수",
        "各モードのランキングを確認します。": "각 모드별 순위를 확인합니다.",
        "フレンド一覧を確認します。": "친구 목록을 확인합니다.",
        "リスト": "목록",
        "確認したいリスト": "확인하고 싶은 목록",
        "友達リスト": "친구 목록",
        "受信リスト": "수신 목록",
        "送信リスト": "전송 목록",
        "フレンドがいません。": "친구가 없습니다.",
        "フレンドを選択してください": "친구를 선택하세요",
        "Discordのユーザーがアカウントをリンクしている場合、プロフィールを表示します。": "Discord 사용자가 계정을 연결한 경우 프로필을 표시합니다.",
        "ユーザー": "사용자",
        "確認したいユーザー": "확인하고 싶은 사용자",
        "週間人気度ランキングを確認します。": "주간 인기도 순위를 확인합니다.",
        "累積人気度ランキングを確認します。": "누적 인기도 순위를 확인합니다.",
        "釣りリーグシーズン(FLF)ランキングを確認します。": "낚시 리그 시즌(FLF) 랭킹을 확인합니다.",
        "既に使用されているか、クーポンがありません。": "이미 사용되었거나 쿠폰이 없습니다.",
        "クーポンを使用しました。": "쿠폰을 사용했습니다.",
        "クーポンを使用します。": "쿠폰을 사용합니다.",
        "クーポン": "쿠폰",
        "使用するクーポン": "사용 가능한 쿠폰",
        "届いているメールの一覧を確認します。": "수신된 메일 목록을 확인합니다.",
        "届いているメールはありません。": "메일이 도착하지 않았습니다.",
        "メールボックス": "우편함",
        "獲得したアイテムはゲーム内で確認してください。": "획득한 아이템은 게임 내에서 확인할 수 있습니다.",
        "週間人気度": "주간 인기도",
        "累積人気度": "누적 인기도",
        "順位を確認したいモード": "순위 확인 모드",
        "モード": "모드",
        "サーバー": "서버",
        "日本": "일본",
        "韓国": "한국",
        # アイテム
        "ゴールド": "골드",
        "アイス": "아이스",
        "マイレージ": "마일리지",
        "キューブ": "큐브",
        "高級箱": "고급 상자",
        "フリーズパス経験値": "프리즈 패스 경험치",
        # モード
        "不明": "알 수 없음",
        "こおり鬼モード": "얼음땡 모드",
        "チームバトルモード": "팀배틀 모드",
        "1対1モード": "1 vs 1 모드",
        "旗取りモード": "깃발뺏기 모드",
        "墜落モード": "추락 모드",
        "こおり鬼(チーム)": "얼음땡(팀)",
        "マラソンモード": "마라톤 모드",
        "撮影モード": "슈팅 모드",
        "ひっくり返しモード": "발판 뒤집기 모드",
        "占領モード": "점령전 모드",
        "だるまさんがころんだモード": "무궁화 꽃이 피었습니다 모드",
        "薄氷モード": "살얼음판 모드",
        "迷路エスケープモード": "미로 탈출 모드",
        "雪玉避けモード": "눈덩이 피하기 모드",
        "雪合戦モード": "눈싸움 모드",
        "超能力こおり鬼モード": "초능력 얼음땡 모드",
        "フリーズボールモード": "프리즈 볼 모드",
        "王騎士モード": "추락 왕기사 모드",
        "変身かくれんぼモード": "변신 숨바꼭질 모드",
        "爆弾モード": "폭탄 모드",
        "デスマッチモード": "데스매치 모드",
        "マフィアモード": "마피아 모드",
        "崩壊モード": "붕괴 모드",
        "宝探しモード": "보물찾기 모드",
        "墜落モード(1vs1)": "추락 모드 (1 vs 1)",
        "警察と泥棒モード": "경찰과 도둑 모드",
        "かくれんぼモード": "숨바꼭질 모드",
        "墜落モード(個人)": "추락 모드 (개인전)",
        "ゾンビモード": "좀비 모드",
        "巨人モード": "거인 모드",
        "(古い)1対1モード": "(구)1 vs 1 모드",
        "クイズモード": "퀴즈땡 모드",
        "迷路モード": "미로 탈출 모드",
    },
}

FMT_TLANSLATION_DATA: dict[Locale, dict[str, str]] = {
    Locale.korean: {
        "{nickname} のプロフィール": "{nickname} 의 프로필",
        "{rank}位": "{rank}위",
        "ランクゲームシーズン {season}": "랭크 게임 시즌 {season}",
        "{cmd}を使用して、アカウントをリンクしてください。": "{cmd}를 사용하여 계정을 연결하세요.",
        "現在のモード: {mode}\n次のモード切り替えの時間: {switchTime}": "현재 모드: {mode}\n 다음 모드 전환 시간: {switchTime}",
        "{clanname} クランの情報": "{clanname} 클랜 정보",
        "{member}人 (最大{maxMember}人)": "{member}명 (최대 {maxMember}명)",
        "{score}点": "{score}점",
        "最終接続: {datetime}": "최종 연결: {datetime}",
        "その人はこおり鬼 Online!のアカウントをリンクしていません\nその人がこおり鬼 Online!をやっているのであれば「{command} を使って！」と言ってあげてください。": "그 사람은 얼음땡 온라인 계정을 연결하지 않았습니다\n 그 사람이 얼음땡 온라인을 플레이하고 있다면 “{command}를 사용하세요!” 라고 말해 주세요.",
        "ページ {page} / 3": "페이지 {page} / 3",
        "受け取り期限: {datetime}": "수령 기한: {datetime}",
        "{bosang} を受け取りました！": "{bosang}을 받았습니다!",
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
