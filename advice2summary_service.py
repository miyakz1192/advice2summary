#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import traceback
import uuid

# settting of import messaging
sys.path.append("messaging")
sys.path.append("messaging/service")
from messaging import *
from llm_mediator import *

class Advice2SummaryService(LLMMediatorBase):
    # サービスへの要求キューからリクエストをgetした際にそれが許容されるものかどうかを判定する
    # 許容される・・・True、されない・・・False
    def is_acceptable_request(self, rec):
        return True

    # サービスへの要求キューからメッセージを取り出し、返す
    def get_from_req_queue(self):
        return Advice2SummaryServiceReqMessaging().connect_and_basic_get_record()

    # LLMから結果を受け取り、サービスの結果返却キューにメッセージをpublishする
    def publish_to_res_queue(self, rec):
        Advice2SummaryServiceResMessaging.connect_and_basic_publish_record(rec)

    # LLMInstanceから結果が帰ってこなかったレコードを、サービスの要求キューに入れなおす
    def publish_to_req_queue(self, rec):
        Advice2SummaryServiceReqMessaging().connect_and_basic_publish_record(rec)

    # デフォルトの指示テキストを設定する
    def set_default_instruction(self):
        self.default_instruction = "以下の入力は、子育ての専門家が親と子の会話を見てアドバイスした結果です。アドバイスは親が子の自己肯定感を高めるためにはどうしたら良いのかの観点で行われています。各アドバイスは###で区切られたものがリスト化されています。アドバイスのリストを要約して総合的なアドバイスを50文字程度で作成してください。ただし、会話の修正に関する話題は明確に除外してください。"

    # LLMInstanceServiceから処理が帰ってきた後、復帰値として、
    # サービス返却キューに返すレコードを作る
    # 引数にサービス要求キューに来たoriginal_recordが渡されるので、それに結果を代入して返す
    # record種別によってメンバーの名前が変わるため、個別実装になる。
    def _make_response_record(self, original_record, llm_output_text):
        original_record.summary_text = llm_output_text
        rec = original_record
        return rec

    # LLMInstanceに渡す入力テキスト(input_example)を生成する
    # たいていの場合、サービスへの要求キューに来たrecordが
    # ネタになるため、それを入力として受け取り処理する
    def _make_llm_input_text(self, rec):
        return rec.advice_text #要求レコード内のin_text(会話の文字起こし結果)

Advice2SummaryService().main_loop()
