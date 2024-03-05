# -*- coding: utf-8 -*-
# @author: leesoar

"""Voice

Based on Microsoft Azure.

See: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/index-text-to-speech

"""

import functools
import re
import time

import azure.cognitiveservices.speech as speech_sdk

__all__ = [
    "SSML",
    "Voice",
]


class Language:
    ZH_CN = "zh-CN"
    ZH_HK = "zh-HK"
    ZH_TW = "zh-TW"
    EN_US = "en-US"
    EN_GB = "en-GB"
    DE_DE = "de-DE"
    FR_FR = "fr-FR"
    JA_JP = "ja-JP"
    RU_RU = "ru-RU"
    IT_IT = "it-IT"
    ES_ES = "es-ES"


class VoiceName:
    class KID:
        EN_US_ANA = "en-US-AnaNeural"
        EN_GB_MAISIE = "en-GB-MaisieNeural"
        ZH_CN_XIAO_SHUANG = "zh-CN-XiaoshuangNeural"
        ZH_CN_XIAO_YOU = "zh-CN-XiaoyouNeural"
        DE_D_GISELA = "de-DE-GiselaNeural"
        FR_FR_ELOISE = "fr-FR-EloiseNeural"

    class MALE:
        ZH_HK_WAN_LUNG = "zh-HK-WanLungNeural"
        ZH_CN_YUN_XI = "zh-CN-YunxiNeural"
        ZH_CN_YUN_YANG = "zh-CN-YunyangNeural"
        ZH_CN_YUN_YE = "zh-CN-YunyeNeural"
        ZH_TW_YUN_JHE = "zh-TW-YunJheNeural"
        EN_GB_RYAN = "en-GB-RyanNeural"
        EN_US_BRANDON = "en-US-BrandonNeural"
        EN_US_CHRISTOPHER = "en-US-ChristopherNeural"
        EN_US_ERIC = "en-US-EricNeural"
        EN_US_GUY = "en-US-GuyNeural"
        EN_US_JACOB = "en-US-JacobNeural"
        JA_JP_KEITA = "ja-JP-KeitaNeural"
        RU_RU_DMITRY = "ru-RU-DmitryNeural"
        DE_DE_BERND = "de-DE-BerndNeural"
        DE_DE_CHRISTOPH = "de-DE-ChristophNeural"
        DE_DE_KASPER = "de-DE-KasperNeural"
        DE_D_KILLIAN = "de-DE-KillianNeural"
        DE_DE_KLAUS = "de-DE-KlausNeural"
        DE_DE_RALF = "de-DE-RalfNeural"
        FR_FR_HENRI = "fr-FR-HenriNeural"
        IT_IT_DIEGO = "it-IT-DiegoNeural"
        ES_ES_ALVARO = "es-ES-AlvaroNeural"

    class FEMALE:
        ZH_HK_HIU_GAAI = "zh-HK-HiuGaaiNeural"
        ZH_HK_HIU_MAAN = "zh-HK-HiuMaanNeural"
        ZH_CN_XIAO_CHEN = "zh-CN-XiaochenNeural"
        ZH_CN_XIAO_HAN = "zh-CN-XiaohanNeural"
        ZH_CN_XIAO_MO = "zh-CN-XiaomoNeural"
        ZH_CN_XIAO_QIU = "zh-CN-XiaoqiuNeural"
        ZH_CN_XIAO_RUI = "zh-CN-XiaoruiNeural"
        ZH_CN_XIAO_XIAO = "zh-CN-XiaoxiaoNeural"
        ZH_CN_XIAO_XUAN = "zh-CN-XiaoxuanNeural"
        ZH_CN_XIAO_YAN = "zh-CN-XiaoyanNeural"
        ZH_TW_HSIAO_CHEN = "zh-TW-HsiaoChenNeural"
        ZH_TW_HSIAO_YU = "zh-TW-HsiaoYuNeural"
        JA_JP_NANAMI = "ja-JP-NanamiNeural"
        EN_GB_LIBBY = "en-GB-LibbyNeural"
        EN_GB_SONIA = "en-GB-SoniaNeural"
        EN_US_AMBER = "en-US-AmberNeural"
        EN_US_ARIA = "en-US-AriaNeural"
        EN_US_ASHLEY = "en-US-AshleyNeural"
        EN_US_CORA = "en-US-CoraNeural"
        EN_US_ELIZABETH = "en-US-ElizabethNeural"
        EN_US_JENNY = "en-US-JennyNeural"
        EN_US_JENNY_MULTILINGUAL = "en-US-JennyMultilingualNeural"
        EN_US_MICHELLE = "en-US-MichelleNeural"
        EN_US_MONICA = "en-US-MonicaNeural"
        EN_US_SARA = "en-US-SaraNeural"
        RU_RU_DARIYA = "ru-RU-DariyaNeural"
        RU_RU_SYETLANA = "ru-RU-SvetlanaNeural"
        DE_DE_AMALA = "de-DE-AmalaNeural"
        DE_DE_ELKE = "de-DE-ElkeNeural"
        DE_DE_KLARISSA = "de-DE-KlarissaNeural"
        DE_DE_LOUISA = "de-DE-LouisaNeural"
        DE_DE_MAJA = "de-DE-MajaNeural"
        DE_DE_TANJA = "de-DE-TanjaNeural"
        DE_DE_GISELA = "de-DE-GiselaNeural"
        FR_FR_DENISE = "fr-FR-DeniseNeural"
        IT_IT_ELSA = "it-IT-ElsaNeural"
        IT_IT_ISABELLA = "it-IT-IsabellaNeural"
        ES_ES_ELVIRA = "es-ES-ElviraNeural"


class SSML:
    """Speech Synthesis Markup Language

    Generate XML for SSML.

    See: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup
    """
    from xml.etree import ElementTree as ET

    version = "1.0"

    class RATE:
        X_SLOW = "x-slow"
        SLOW = "slow"
        MEDIUM = "medium"
        FAST = "fast"
        X_FAST = "x-fast"
        DEFAULT = "default"

    class STYLE:
        # Expresses a warm and affectionate tone, with higher pitch and vocal energy.
        # The speaker is in a state of attracting the attention of the listener.
        # The personality of the speaker is often endearing in nature.
        AFFECTIONATE = "affectionate"
        # Expresses an angry and annoyed tone.
        ANGRY = "angry"
        # Expresses a warm and relaxed tone for digital assistants.
        ASSISTANT = "assistant"
        # Expresses a cool, collected, and composed attitude when speaking.
        # Tone, pitch, and prosody are more uniform compared to other types of speech.
        CALM = "calm"
        # Expresses a casual and relaxed tone.
        CHAT = "chat"
        # Expresses a positive and happy tone.
        CHEERFUL = "cheerful"
        # Expresses a friendly and helpful tone for customer support.
        CUSTOMER_SERVICE = "customerservice"
        # Expresses a melancholic and despondent tone with lower pitch and energy.
        DEPRESSED = "depressed"
        # Expresses a disdainful and complaining tone.
        # Speech of this emotion displays displeasure and contempt.
        DISGRUNTLED = "disgruntled"
        # Expresses an uncertain and hesitant tone when the speaker is feeling uncomfortable.
        EMBARRASSED = "embarrassed"
        # Expresses a sense of caring and understanding.
        EMPATHETIC = "empathetic"
        # Express a tone of admiration when you desire something that someone else has.
        ENVIOUS = "envious"
        # Expresses a scared and nervous tone, with higher pitch, higher vocal energy, and faster rate.
        # The speaker is in a state of tension and unease.
        FEARFUL = "fearful"
        # Expresses a mild, polite, and pleasant tone, with lower pitch and vocal energy.
        GENTLE = "gentle"
        # Expresses emotions in a melodic and sentimental way.
        LYRICAL = "lyrical"
        # Expresses a professional, objective tone for content reading.
        NARRATION_PROFESSIONAL = "narration-professional"
        # Express a soothing and melodious tone for content reading.
        NARRATION_RELAXED = "narration-relaxed"
        # Expresses a formal and professional tone for narrating news.
        NEWSCAST = "newscast"
        # Expresses a versatile and casual tone for general news delivery.
        NEWSCAST_CASUAL = "newscast-casual"
        # Expresses a formal, confident, and authoritative tone for news delivery.
        NEWSCAST_FORMAL = "newscast-formal"
        # Expresses a sorrowful tone.
        SAD = "sad"
        # Expresses a strict and commanding tone.
        # Speaker often sounds stiffer and much less relaxed with firm cadence.
        SERIOUS = "serious"

    class ROLE:
        GIRL = "Girl"
        BOY = "Boy"
        YOUNG_ADULT_FEMALE = "YoungAdultFemale"
        YOUNG_ADULT_MALE = "YoungAdultMale"
        OLDER_ADULT_FEMALE = "OlderAdultFemale"
        OLDER_ADULT_MALE = "OlderAdultMale"
        SENIOR_FEMALE = "SeniorFemale"
        SENIOR_MALE = "SeniorMale"

    NAME = VoiceName
    LANG = Language

    def __init__(self, lang=None, voice_name=None):
        self.lang = lang or self.LANG.EN_US
        self.voice_name = voice_name or self.NAME.FEMALE.EN_US_JENNY_MULTILINGUAL
        self.init_root()

    def init_root(self):
        self.root = self.ET.Element("speak", attrib={
            "version": self.version,
            "xmlns": "http://www.w3.org/2001/10/synthesis",
            "xmlns:mstts": "https://www.w3.org/2001/mstts",
            "xml:lang": self.lang,
        })

    @property
    def voice(self):
        voices = self.root.findall("voice") or None
        return voices and voices[-1]

    @voice.setter
    def voice(self, data):
        if isinstance(data, str):
            text = data
            data = {
                "name": self.voice_name,
            }
        else:
            text = data.get("text") and data.pop("text")
            style_degree = data.get("degree") and data.pop("degree")
            data.update({
                "name": data.get("name") or self.voice_name,
                "style": data.get("style") or "",
                "styledegree": style_degree or "",
                "role": data.get("role") or "",
                "rate": data.get("rate") or self.RATE.DEFAULT,
            })

        phonemes = data.get("phonemes") and data.pop("phonemes")
        if phonemes:
            self.__process_phonemes(phonemes, text, data)
            return

        et_voice = self.ET.Element("voice", attrib=data)
        et_voice.text = text
        self.root.append(et_voice)

    def __process_phonemes(self, phonemes: list or tuple, text: str, data: dict):
        assert isinstance(phonemes, (list, tuple)), \
            """"phonemes" has the wrong type. (need `list` or `tuple`) """

        et_voice = self.ET.Element("voice", attrib=data)
        for phoneme in phonemes:
            word = phoneme.get("word")
            alphabet = phoneme.get("alphabet", "sapi")
            ph = phoneme.get("ph")

            assert None not in [word, ph], \
                "missing `word` or `ph`."
            assert f"[{word}]" in text, \
                f'"[{word}]" is not in the text.'

            tmp_text, text = text.split(f"[{word}]", maxsplit=1)
            et_s = self.ET.Element("s")
            et_s.text = tmp_text
            et_voice.append(et_s)

            et_phoneme = self.ET.Element("phoneme", {
                "alphabet": alphabet,
                "ph": ph,
            })
            et_phoneme.text = word
            et_voice.append(et_phoneme)

            if f"[{word}]" not in text:
                et_s_end = self.ET.Element("s")
                et_s_end.text = text
                et_voice.append(et_s_end)

        self.root.append(et_voice)

    def dump(self):
        xml = self.__str__()
        if "</s>" in xml:
            voice_elems = re.findall(r"<voice.*?</voice>", xml)
            for raw_voice_elem in voice_elems:
                raw_s_elem = re.search(r"<s>(.*)</s>", raw_voice_elem)
                if not raw_s_elem:
                    continue
                raw_s_text = raw_s_elem.group(1)
                processed_s_text = raw_s_text.replace("<s>", "").replace("</s>", "")
                processed_voice_elem = raw_voice_elem.replace(raw_s_text, processed_s_text)
                xml = xml.replace(raw_voice_elem, processed_voice_elem)
        return xml

    def __str__(self):
        return self.ET.tostring(self.root, encoding="unicode", short_empty_elements=False)


def voice_process(func):
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        cls.name = kwargs.get("voice_name") or cls.name
        cls.language = kwargs.get("lang") or cls.language

        func(cls, *args, **kwargs)

        text = kwargs.get("text") or args[0]
        if isinstance(text, SSML):
            result = cls._Voice__speech_synthesizer.speak_ssml_async(text.dump()).get()
        else:
            result = cls._Voice__speech_synthesizer.speak_text_async(text).get()
        cls.error = result.cancellation_details
        return result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted
    return wrapper


class Voice:
    NAME = VoiceName
    LANG = Language

    def __init__(self, subscription: str, region: str):
        self.__speech_config = speech_sdk.SpeechConfig(subscription=subscription, region=region)
        self.__set_output()

    def __set_speech_synthesizer(self):
        self.__speech_synthesizer = speech_sdk.SpeechSynthesizer(
            speech_config=self.__speech_config,
            audio_config=self.__audio_config
        )

    @property
    def language(self):
        return self.__speech_config.speech_synthesis_language

    @language.setter
    def language(self, lang: str):
        self.__speech_config.speech_synthesis_language = lang

    @property
    def name(self):
        return self.__speech_config.speech_synthesis_voice_name

    @name.setter
    def name(self, value: str):
        self.__speech_config.speech_synthesis_voice_name = value

    def __set_output(self, path=None):
        if not path:
            self.__audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
        else:
            self.__audio_config = speech_sdk.audio.AudioOutputConfig(filename=path)
        self.__set_speech_synthesizer()

    @voice_process
    def speak(self, text, *, voice_name=None, lang=None):
        self.__set_output()

    @voice_process
    def save(self, text, *, path=None, voice_name=None, lang=None):
        path = path or f"{int(time.time() * 1e3)}.mp3"
        self.__set_output(path)
