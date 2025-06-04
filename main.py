import asyncio
import json
import os
from winsound import PlaySound
import colorama
from ollama import AsyncClient, Client
import ollama
import pick
import tts_with_rvc
import logging
import trans
import googletrans

for logger in logging.Logger.manager.loggerDict.values():
    if isinstance(logger, logging.Logger):
        logger.setLevel(logging.WARNING)

voices = ['af-ZA-AdriNeural', 'af-ZA-WillemNeural', 'sq-AL-AnilaNeural', 'sq-AL-IlirNeural', 'am-ET-AmehaNeural', 'am-ET-MekdesNeural', 'ar-DZ-AminaNeural', 'ar-DZ-IsmaelNeural', 'ar-BH-AliNeural', 'ar-BH-LailaNeural', 'ar-EG-SalmaNeural', 'ar-EG-ShakirNeural', 'ar-IQ-BasselNeural', 'ar-IQ-RanaNeural', 'ar-JO-SanaNeural', 'ar-JO-TaimNeural', 'ar-KW-FahedNeural', 'ar-KW-NouraNeural', 'ar-LB-LaylaNeural', 'ar-LB-RamiNeural', 'ar-LY-ImanNeural', 'ar-LY-OmarNeural', 'ar-MA-JamalNeural', 'ar-MA-MounaNeural', 'ar-OM-AbdullahNeural', 'ar-OM-AyshaNeural', 'ar-QA-AmalNeural', 'ar-QA-MoazNeural', 'ar-SA-HamedNeural', 'ar-SA-ZariyahNeural', 'ar-SY-AmanyNeural', 'ar-SY-LaithNeural', 'ar-TN-HediNeural', 'ar-TN-ReemNeural', 'ar-AE-FatimaNeural', 'ar-AE-HamdanNeural', 'ar-YE-MaryamNeural', 'ar-YE-SalehNeural', 'az-AZ-BabekNeural', 'az-AZ-BanuNeural', 'bn-BD-NabanitaNeural', 'bn-BD-PradeepNeural', 'bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural', 'bs-BA-VesnaNeural', 'bs-BA-GoranNeural', 'bg-BG-BorislavNeural', 'bg-BG-KalinaNeural', 'my-MM-NilarNeural', 'my-MM-ThihaNeural', 'ca-ES-EnricNeural', 'ca-ES-JoanaNeural', 'zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural', 'zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunyangNeural', 'zh-CN-liaoning-XiaobeiNeural', 'zh-TW-HsiaoChenNeural', 'zh-TW-YunJheNeural', 'zh-TW-HsiaoYuNeural', 'zh-CN-shaanxi-XiaoniNeural', 'hr-HR-GabrijelaNeural', 'hr-HR-SreckoNeural', 'cs-CZ-AntoninNeural', 'cs-CZ-VlastaNeural', 'da-DK-ChristelNeural', 'da-DK-JeppeNeural', 'nl-BE-ArnaudNeural', 'nl-BE-DenaNeural', 'nl-NL-ColetteNeural', 'nl-NL-FennaNeural', 'nl-NL-MaartenNeural', 'en-AU-NatashaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-HK-YanNeural', 'en-HK-SamNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-IE-ConnorNeural', 'en-IE-EmilyNeural', 'en-KE-AsiliaNeural', 'en-KE-ChilembaNeural', 'en-NZ-MitchellNeural', 'en-NZ-MollyNeural', 'en-NG-AbeoNeural', 'en-NG-EzinneNeural', 'en-PH-JamesNeural', 'en-PH-RosaNeural', 'en-US-AvaNeural', 'en-US-AndrewNeural', 'en-US-EmmaNeural', 'en-US-BrianNeural', 'en-SG-LunaNeural', 'en-SG-WayneNeural', 'en-ZA-LeahNeural', 'en-ZA-LukeNeural', 'en-TZ-ElimuNeural', 'en-TZ-ImaniNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural', 'en-GB-ThomasNeural', 'en-US-AnaNeural', 'en-US-AndrewMultilingualNeural', 'en-US-AriaNeural', 'en-US-AvaMultilingualNeural', 'en-US-BrianMultilingualNeural', 'en-US-ChristopherNeural', 'en-US-EmmaMultilingualNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural', 'et-EE-AnuNeural', 'et-EE-KertNeural', 'fil-PH-AngeloNeural', 'fil-PH-BlessicaNeural', 'fi-FI-HarriNeural', 'fi-FI-NooraNeural', 'fr-BE-CharlineNeural', 'fr-BE-GerardNeural', 'fr-CA-ThierryNeural', 'fr-CA-AntoineNeural', 'fr-CA-JeanNeural', 'fr-CA-SylvieNeural', 'fr-FR-VivienneMultilingualNeural', 'fr-FR-RemyMultilingualNeural', 'fr-FR-DeniseNeural', 'fr-FR-EloiseNeural', 'fr-FR-HenriNeural', 'fr-CH-ArianeNeural', 'fr-CH-FabriceNeural', 'gl-ES-RoiNeural', 'gl-ES-SabelaNeural', 'ka-GE-EkaNeural', 'ka-GE-GiorgiNeural', 'de-AT-IngridNeural', 'de-AT-JonasNeural', 'de-DE-SeraphinaMultilingualNeural', 'de-DE-FlorianMultilingualNeural', 'de-DE-AmalaNeural', 'de-DE-ConradNeural', 'de-DE-KatjaNeural', 'de-DE-KillianNeural', 'de-CH-JanNeural', 'de-CH-LeniNeural', 'el-GR-AthinaNeural', 'el-GR-NestorasNeural', 'gu-IN-DhwaniNeural',
          'gu-IN-NiranjanNeural', 'he-IL-AvriNeural', 'he-IL-HilaNeural', 'hi-IN-MadhurNeural', 'hi-IN-SwaraNeural', 'hu-HU-NoemiNeural', 'hu-HU-TamasNeural', 'is-IS-GudrunNeural', 'is-IS-GunnarNeural', 'id-ID-ArdiNeural', 'id-ID-GadisNeural', 'iu-Latn-CA-SiqiniqNeural', 'iu-Latn-CA-TaqqiqNeural', 'iu-Cans-CA-SiqiniqNeural', 'iu-Cans-CA-TaqqiqNeural', 'ga-IE-ColmNeural', 'ga-IE-OrlaNeural', 'it-IT-GiuseppeMultilingualNeural', 'it-IT-DiegoNeural', 'it-IT-ElsaNeural', 'it-IT-IsabellaNeural', 'ja-JP-KeitaNeural', 'ja-JP-NanamiNeural', 'jv-ID-DimasNeural', 'jv-ID-SitiNeural', 'kn-IN-GaganNeural', 'kn-IN-SapnaNeural', 'kk-KZ-AigulNeural', 'kk-KZ-DauletNeural', 'km-KH-PisethNeural', 'km-KH-SreymomNeural', 'ko-KR-HyunsuMultilingualNeural', 'ko-KR-InJoonNeural', 'ko-KR-SunHiNeural', 'lo-LA-ChanthavongNeural', 'lo-LA-KeomanyNeural', 'lv-LV-EveritaNeural', 'lv-LV-NilsNeural', 'lt-LT-LeonasNeural', 'lt-LT-OnaNeural', 'mk-MK-AleksandarNeural', 'mk-MK-MarijaNeural', 'ms-MY-OsmanNeural', 'ms-MY-YasminNeural', 'ml-IN-MidhunNeural', 'ml-IN-SobhanaNeural', 'mt-MT-GraceNeural', 'mt-MT-JosephNeural', 'mr-IN-AarohiNeural', 'mr-IN-ManoharNeural', 'mn-MN-BataaNeural', 'mn-MN-YesuiNeural', 'ne-NP-HemkalaNeural', 'ne-NP-SagarNeural', 'nb-NO-FinnNeural', 'nb-NO-PernilleNeural', 'ps-AF-GulNawazNeural', 'ps-AF-LatifaNeural', 'fa-IR-DilaraNeural', 'fa-IR-FaridNeural', 'pl-PL-MarekNeural', 'pl-PL-ZofiaNeural', 'pt-BR-ThalitaMultilingualNeural', 'pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-PT-DuarteNeural', 'pt-PT-RaquelNeural', 'ro-RO-AlinaNeural', 'ro-RO-EmilNeural', 'ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural', 'sr-RS-NicholasNeural', 'sr-RS-SophieNeural', 'si-LK-SameeraNeural', 'si-LK-ThiliniNeural', 'sk-SK-LukasNeural', 'sk-SK-ViktoriaNeural', 'sl-SI-PetraNeural', 'sl-SI-RokNeural', 'so-SO-MuuseNeural', 'so-SO-UbaxNeural', 'es-AR-ElenaNeural', 'es-AR-TomasNeural', 'es-BO-MarceloNeural', 'es-BO-SofiaNeural', 'es-CL-CatalinaNeural', 'es-CL-LorenzoNeural', 'es-CO-GonzaloNeural', 'es-CO-SalomeNeural', 'es-ES-XimenaNeural', 'es-CR-JuanNeural', 'es-CR-MariaNeural', 'es-CU-BelkysNeural', 'es-CU-ManuelNeural', 'es-DO-EmilioNeural', 'es-DO-RamonaNeural', 'es-EC-AndreaNeural', 'es-EC-LuisNeural', 'es-SV-LorenaNeural', 'es-SV-RodrigoNeural', 'es-GQ-JavierNeural', 'es-GQ-TeresaNeural', 'es-GT-AndresNeural', 'es-GT-MartaNeural', 'es-HN-CarlosNeural', 'es-HN-KarlaNeural', 'es-MX-DaliaNeural', 'es-MX-JorgeNeural', 'es-NI-FedericoNeural', 'es-NI-YolandaNeural', 'es-PA-MargaritaNeural', 'es-PA-RobertoNeural', 'es-PY-MarioNeural', 'es-PY-TaniaNeural', 'es-PE-AlexNeural', 'es-PE-CamilaNeural', 'es-PR-KarinaNeural', 'es-PR-VictorNeural', 'es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-US-AlonsoNeural', 'es-US-PalomaNeural', 'es-UY-MateoNeural', 'es-UY-ValentinaNeural', 'es-VE-PaolaNeural', 'es-VE-SebastianNeural', 'su-ID-JajangNeural', 'su-ID-TutiNeural', 'sw-KE-RafikiNeural', 'sw-KE-ZuriNeural', 'sw-TZ-DaudiNeural', 'sw-TZ-RehemaNeural', 'sv-SE-MattiasNeural', 'sv-SE-SofieNeural', 'ta-IN-PallaviNeural', 'ta-IN-ValluvarNeural', 'ta-MY-KaniNeural', 'ta-MY-SuryaNeural', 'ta-SG-AnbuNeural', 'ta-SG-VenbaNeural', 'ta-LK-KumarNeural', 'ta-LK-SaranyaNeural', 'te-IN-MohanNeural', 'te-IN-ShrutiNeural', 'th-TH-NiwatNeural', 'th-TH-PremwadeeNeural', 'tr-TR-EmelNeural', 'tr-TR-AhmetNeural', 'uk-UA-OstapNeural', 'uk-UA-PolinaNeural', 'ur-IN-GulNeural', 'ur-IN-SalmanNeural', 'ur-PK-AsadNeural', 'ur-PK-UzmaNeural', 'uz-UZ-MadinaNeural', 'uz-UZ-SardorNeural', 'vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural', 'cy-GB-AledNeural', 'cy-GB-NiaNeural', 'zu-ZA-ThandoNeural', 'zu-ZA-ThembaNeural']


def simple_mstranslate(text: str, encn=False):
    if encn:
        text = trans.translate(text, "en", "zh-Hans")
    else:
        text = trans.translate(text, "zh-Hans", "en")
    return text


async def simple_ggtranslate(text: str, encn=False):
    Translator = googletrans.Translator()
    if encn:
        result = await Translator.translate(text, dest='zh-cn')
        result = result.text
    else:
        result = await Translator.translate(text, dest='en')
        result = result.text
    return result

class Session():
    def __init__(self, model_name=None, session_name="default", need_tts=True, need_translate=True, need_two_translation=False, messages_limit=6, tts_model=None, tts_voice=None, tts_method="rmvpe"):
        if os.path.exists(f"./sessions/{session_name}.json"):
            try:
                print(f"Session {session_name} already exists. Loading session...")
                with open(f"./sessions/{session_name}.json", "r", encoding="utf-8") as f:
                    session = json.load(f)
                    self.model_name = session["model_name"]
                    self.session_name = session["session_name"]
                    self.need_tts = session["need_tts"]
                    self.need_translate = session["need_translate"]
                    self.messages = session["messages"]
                    self.translated_messages = session["translated_messages"]
                    self.messages_limit = session["messages_limit"]
                    self.need_two_translation = session["need_two_translation"]
                    self.client = Client()
                    if self.need_tts:
                        self.tts = tts_with_rvc.TTS_RVC(model_path=session["tts"]["model"],
                                        voice=session["tts"]["voice"],
                                        f0_method=session["tts"]["f0_method"])
                return
            except Exception as e:
                print(f"Error loading session {session_name}: {e}")
                print("Creating a new session...")
        assert model_name is not None, "Model name cannot be None"
        assert (tts_method in ["rmvpe", "parselmouth", "crepe"] and tts_voice in voices and tts_model is not None) or not need_tts, "TTS method, voice or model is invalid"
        self.model_name = model_name
        self.session_name = session_name
        self.need_tts = need_tts
        self.need_translate = need_translate
        self.messages = []
        self.translated_messages = []
        self.client = Client()
        self.messages_limit = messages_limit
        if self.need_tts:
            self.tts = tts_with_rvc.TTS_RVC(model_path=tts_model,
                            voice=tts_voice,
                            f0_method=tts_method)
        self.need_two_translation = need_two_translation
        self.save()

    def record(self, message, translated_message=None, role="user"):
        self.messages.append({"role": role, "content": message})
        if self.need_translate:
            self.translated_messages.append(
                {"role": role, "content": translated_message})
        self.save()

    def save(self):
        if self.need_tts:
            with open(f"./sessions/{self.session_name}.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(
                    {"model_name": self.model_name,
                    "session_name": self.session_name,
                    "need_tts": self.need_tts,
                    "need_translate": self.need_translate,
                    "tts": {
                        "model": self.tts.current_model,
                        "voice": self.tts.current_voice,
                        "f0_method": self.tts.f0_method
                        },
                    "messages_limit": self.messages_limit,
                    "messages": self.messages,
                    "translated_messages": self.translated_messages,
                    "need_two_translation": self.need_two_translation
                    }, ensure_ascii=False, indent=4))
        else:
            with open(f"./sessions/{self.session_name}.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(
                    {"model_name": self.model_name,
                    "session_name": self.session_name,
                    "need_tts": self.need_tts,
                    "need_translate": self.need_translate,
                    "messages_limit": self.messages_limit,
                    "messages": self.messages,
                    "translated_messages": self.translated_messages,
                    "need_two_translation": self.need_two_translation
                    }, ensure_ascii=False, indent=4))
    def __str__(self):
        return f"Session<{self.session_name}>:{self.model_name} with {len(self.messages)} messages, tts={self.need_tts}, translate={self.need_translate}, two_translation={self.need_two_translation}"

    def chat(self, message:str):
        if self.need_translate:
            translated_message = simple_mstranslate(message, encn=False)
            print("Translated message: ", translated_message)
            self.record(translated_message, message, role="user")
            print("Respone: \n",end="")
            result=""
            for i in self.client.chat(
                messages=self.messages[-self.messages_limit:], model=self.model_name,stream=True):
                print(i.message.content, end="", flush=True)
                result+=i.message.content
            translated_resp=""
            with open("./replacements.json", "r", encoding="utf-8") as f:
                replacements = json.loads(f.read())
            result1=result
            result2=result
            for i in replacements:
                result1 = result1.replace(
                    i[0], f'<mstrans:dictionary translation="{i[1]}">{i[0]}</mstrans:dictionary>')
                result2 = result2.replace(i[0], i[1])
            if self.need_two_translation:
                msr = simple_mstranslate(result1, encn=True)
                print("Translated response: ", msr)
                try:
                    ggr= asyncio.run(simple_ggtranslate(result2, encn=True))
                    print("Google Translate: ", ggr)
                    use=pick.pick(["Google Translate", "Microsoft Translate"], "Select a translation method", indicator="=>", default_index=0)[0]
                    if use == "Google Translate":
                        translated_resp = ggr
                    else:
                        translated_resp = msr
                except Exception as e:
                    print("Error: ", e,"Fallback to mstranslate")
                    translated_resp = msr
            else:
                translated_resp = simple_mstranslate(result1, encn=True)
            self.record(result, translated_resp, role="assistant")
            self.save()
            if self.need_tts:
                self.tts_play(translated_resp)
            print("Model: ", translated_resp)
        else:
            self.record(message, role="user")
            print("Respone: \n", end="")
            if self.need_tts:
                result = ""
                for i in self.client.chat(
                        messages=self.messages[-self.messages_limit:], model=self.model_name,
                        stream=True):
                    print(i.message.content, end="", flush=True)
                    result += i.message.content
                self.record(result, message, role="assistant")
                self.save()
                self.tts_play(result)
                print("Model: ", result)
            else:
                result = ""
                for i in self.client.chat(
                        messages=self.messages[-self.messages_limit:], model=self.model_name,
                        stream=True):
                    print(i.message.content, end="", flush=True)
                    result += i.message.content
                print()
                self.record(result, message, role="assistant")
                self.save()
    def tts_play(self, message):
        os.makedirs(f"./voices/{self.session_name}", exist_ok=True)
        self.tts.set_output_directory(f"./voices/{self.session_name}")

        message = message.replace("*", ",")
        path = self.tts(text=message, pitch=5, index_rate=0.50)
        path = os.path.normpath(path)  # Ensure the path is normalized
        new_path = os.path.join(
            os.path.dirname(path), f"{len(self.messages)}.wav")
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(path, new_path)
        PlaySound(new_path, 1)
def get_sessions():
    sessions = []
    for file in os.listdir("./sessions"):
        if file.endswith(".json"):
            sessions.append(file[:-5])
    return sessions
def create_session_cli():
    client = ollama.Client()
    models=[i.model for i in ollama.Client().list().models]
    print("Enter the model name: ",end="")
    model_name=pick.pick(models, "Select a model", indicator="=>", default_index=0)[0]
    print(model_name)
    session_name = input("Enter the session name: ")
    need_tts = input("Need TTS? (y/n): ").lower() == "y"
    need_translate = input("Need translate? (y/n): ").lower() == "y"
    need_two_translation=False
    if need_translate:
        need_two_translation = input("Need two translation? (y/n): ").lower() == "y"
    messages_limit = int(input("Enter the messages limit: "))
    if need_tts:
        tts_model = input("Enter the TTS model path: ")
        print("",end="",flush=True)
        # tts_voice = input(f"Enter the TTS voice ({', '.join(voices)}): ")
        tts_voice= pick.pick(voices, "Select a voice", indicator="=>", default_index=0)[0]
        print("TTS voice:", tts_voice)
        tts_method = input(
            "Enter the TTS method ([r]mvpe/[p]arselmouth/[c]repe): ")
        if tts_method == "r":
            tts_method = "rmvpe"
        elif tts_method == "p":
            tts_method = "parselmouth"
        elif tts_method == "c":
            tts_method = "crepe"
        else:
            tts_method = "rmvpe"
    else:
        tts_model = None
        tts_voice = None
        tts_method = None
    return Session(model_name=model_name, session_name=session_name, need_tts=need_tts, need_translate=need_translate, messages_limit=messages_limit, tts_model=tts_model, tts_voice=tts_voice, tts_method=tts_method,need_two_translation=need_two_translation)



def loop():
    sessions = get_sessions()
    session:Session
    if len(sessions) == 0:
        session=create_session_cli()
    elif len(sessions) == 1:
        session=Session(session_name=sessions[0])
    else:
        session = Session(session_name=pick.pick(sessions, "Select a session",
                          indicator="=>", default_index=0)[0])
    while True:
        user_input = input(">>> ")
        user_input = user_input.strip()
        input_role = "user"

        if user_input == "":
            print(colorama.Fore.RED+"请输入内容" +
                  colorama.Style.RESET_ALL)
            continue
        try:
            # 命令截获
            if user_input.startswith("/"):
                if user_input.lower() in ["退出", "quit", "stop", "bye", "拜拜", "/bye", "/quit"]:
                    print(
                        f"{colorama.Fore.YELLOW}退出与 {session.session_name} 对话。{colorama.Style.RESET_ALL}")
                    break
                elif user_input.lower().startswith("/save"):
                    session.save()
                    continue
                elif user_input.lower().startswith("/load"):
                    if len(get_sessions()) == 1 :
                        print(colorama.Fore.RED+"无更多对话" +
                              colorama.Style.RESET_ALL)
                        continue
                    else:
                        new_name = pick.pick(
                            get_sessions(), "Select a session", indicator="=>", default_index=0)[0]
                        session = Session(session_name=new_name)
                    continue
                elif user_input.lower().startswith("/new"):
                    create_session_cli()
                    continue
                elif user_input.lower().startswith("/show"):
                    item = user_input.split(" ")[1]
                    if item.lower() == "summary":
                        print(
                            f"{colorama.Fore.YELLOW}=========={session.session_name}=========={colorama.Style.RESET_ALL}")
                        print(
                            f"{colorama.Fore.YELLOW}模型名：{session.model_name}{colorama.Style.RESET_ALL}")
                        print(
                            f"{colorama.Fore.YELLOW}对话条数：{len(session.messages)}{colorama.Style.RESET_ALL}")
                        # print
                    elif item.lower() == "messages":
                        print(
                            f"{colorama.Fore.YELLOW}=========={session.session_name}=========={colorama.Style.RESET_ALL}")
                        for i in session.messages:
                            print(
                                f"{colorama.Fore.YELLOW}{i['role']}：{i['content']}{colorama.Style.RESET_ALL}")
                    elif item.lower() == "translated":
                        if not session.need_translate:
                            print(colorama.Fore.RED+"未启用翻译功能" +
                                  colorama.Style.RESET_ALL)
                            continue
                        print(
                            f"{colorama.Fore.YELLOW}=========={session.session_name}=========={colorama.Style.RESET_ALL}")
                        for i in session.translated_messages:
                            print(
                                f"{colorama.Fore.YELLOW}{i['role']}：{i['content']}{colorama.Style.RESET_ALL}")
                    continue
                elif user_input.lower().startswith("/system"):
                    data = user_input.split(" ")
                    if len(data) == 1:
                        print(colorama.Fore.RED+"请输入系统消息内容" +
                              colorama.Style.RESET_ALL)
                        continue
                    user_input = data[1]
                    input_role = "system"
                else:
                    print(""+colorama.Fore.RED+"无此命令\n" +
                          colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED+"命令格式错误，请检查输入.\nError: " +
                  repr(e)+colorama.Style.RESET_ALL)
            continue
        session.chat(user_input)

if __name__ == "__main__":
    os.makedirs("./sessions", exist_ok=True)
    loop()