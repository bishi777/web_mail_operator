# 手動DB変更メモ

マイグレーションファイルは作らず、DBスキーマは手動で適用する運用。
ここに必要なスキーマ変更を記録する。

---

## 2026-06-26 PCMAX 足跡返しAI挨拶フラグ追加

### 目的
足跡返しで、キャラごとに「AI生成の1通目挨拶あり/なし」を切り替えられるようにする。
- ひより: `False`（AI挨拶スキップ、`return_foot_message` 1通だけ送信）
- その他全員: `True`（従来通り 1通目AI挨拶 + 2通目 return_foot_message）

### コード変更
- [app/models.py](app/models.py) `Pcmax` モデルに追加:
  ```python
  rf_ai_intro_flug = models.BooleanField(default=True, verbose_name="足跡返しAI挨拶フラグ(True=AI挨拶あり/False=なし)")
  ```
- [app/admin.py](app/admin.py) `PcmaxAdmin.fields` に `'rf_ai_intro_flug'` を追加（管理画面で編集可）。

### 必要なDBスキーマ変更（SQL）
```sql
ALTER TABLE "pcmax" ADD COLUMN "rf_ai_intro_flug" boolean DEFAULT true NOT NULL;
ALTER TABLE "pcmax" ALTER COLUMN "rf_ai_intro_flug" DROP DEFAULT;
```
※ デフォルト True なので既存キャラは従来通りの動作。

### 適用状況
- 本環境のDBには適用済み（既存 pcmax 10件すべて `True`）。
- マイグレーションファイルは作成しない方針のため未作成。

### 管理画面でやること
PCMAX → ひより を開いて「足跡返しAI挨拶フラグ」のチェックを外す（False）だけ。
新キャラもここで切り替え可能。

### 対応するデスクトップ側（desktop_mail_operator）
- `widget/pcmax_2.py` `return_footmessage(..., use_ai_intro=True)` 引数追加、1通目AIブロックを `if use_ai_intro:` で分岐。
- `debug_drivers_p_ch_fm.py` / `gologin_p.py` で `i.get("rf_ai_intro_flug", True)` を渡す。
