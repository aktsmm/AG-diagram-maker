# 出力形式ルール (v1.0)

> **適用対象**: すべての draw.io 図面生成エージェント
> **最終更新**: 2025-12-12

このインストラクションは、draw.io 図面の出力形式に関するルールを定義します。

---

## 形式選択ルール

### 推奨/非推奨

| 形式            | 拡張子        | 推奨度    | 理由                                             |
| --------------- | ------------- | --------- | ------------------------------------------------ |
| **draw.io XML** | `.drawio`     | ✅ 推奨   | 純粋な mxGraphModel 構造で確実に描画される       |
| draw.io SVG     | `.drawio.svg` | ⚠️ 非推奨 | content 属性のみでは描画要素が空になる場合がある |

### 問題の背景

`.drawio.svg` 形式では `content` 属性に mxCell 定義を埋め込むが、**SVG 描画要素（`<rect>`, `<path>`, `<text>` 等）が空だと draw.io で開いても何も表示されない**問題が発生する。

### 形式選択フローチャート

```
ユーザー要求
    │
    ├── SVG 形式を明示的に要求？
    │       │
    │       ├── YES → .drawio.svg を生成（注意付き）
    │       │
    │       └── NO → 既存ファイルの編集？
    │                   │
    │                   ├── YES（.drawio.svg） → .drawio.svg を維持
    │                   │
    │                   └── NO → .drawio (XML) を生成 ✅
    │
    └── デフォルト: .drawio (XML)
```

---

## `.drawio` (XML) 形式

### 構造

```xml
<mxfile host="..." modified="..." agent="...">
  <diagram id="..." name="Page-1">
    <mxGraphModel dx="..." dy="..." grid="1" gridSize="10" ...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- ノード・エッジ定義 -->
        <mxCell id="node1" value="..." style="..." vertex="1" parent="1">
          <mxGeometry x="..." y="..." width="..." height="..." as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 利点

- ✅ draw.io で確実に開ける
- ✅ mxCell 構造のみで完結
- ✅ SVG 描画要素の生成が不要
- ✅ ファイルサイズが小さい
- ✅ 生成が容易

---

## `.drawio.svg` 形式（非推奨）

### 構造

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" ...
     content="&lt;mxfile...&gt;...&lt;/mxfile&gt;">
  <!-- SVG 描画要素（rect, path, text 等） -->
  <rect x="..." y="..." width="..." height="..." />
  <text x="..." y="...">Label</text>
</svg>
```

### 問題点

- ❌ `content` 属性の mxCell 定義と SVG 描画要素の両方が必要
- ❌ SVG 描画要素が空だと draw.io で何も表示されない
- ❌ 生成が複雑（mxCell → SVG 変換が必要）

### 使用する場合の注意

`.drawio.svg` を使用する必要がある場合：

1. **既存ファイルの編集時**: 元が `.drawio.svg` なら形式を維持
2. **ブラウザ表示必須時**: Web ページで直接表示したい場合
3. **ユーザー明示要求時**: SVG を明示的に要求された場合

---

## SVG が必要な場合の推奨ワークフロー

```yaml
svg_requirement_workflow:
  step1: ".drawio (XML) 形式で図面を生成"
  step2: "draw.io デスクトップ/Webで開く"
  step3: "「ファイル」→「エクスポート」→「SVG」を選択"
  step4: "正式な SVG ファイルを取得"

  benefit: "draw.io が SVG 描画要素を正確に生成するため、表示問題なし"
```

---

## 出力パス規則

```yaml
output_path:
  base_directory: "outputs/"
  naming:
    format: "kebab-case"
    examples:
      - "azure-architecture-diagram.drawio"
      - "login-flow-chart.drawio"
      - "network-topology.drawio"

  prohibited:
    - スペースを含むファイル名
    - 日本語ファイル名（互換性のため）
    - 既存ファイルへの上書き（確認なし）
```

---

## ファイル重複チェック

```yaml
duplicate_check:
  required: true
  method: "list_dir で出力ディレクトリを確認"

  on_duplicate:
    options:
      - "上書きする（ユーザー確認後）"
      - "別名で保存（自動リネーム: _01, _02, ...）"
      - "キャンセル"

    auto_rename:
      format: "{base}_01.drawio"
      example: "azure-diagram_01.drawio"
```

---

## まとめ

| 項目               | 推奨                   |
| ------------------ | ---------------------- |
| **デフォルト形式** | `.drawio` (XML)        |
| **出力パス**       | `outputs/` 配下        |
| **命名規則**       | kebab-case             |
| **重複チェック**   | 必須                   |
| **SVG 取得方法**   | draw.io でエクスポート |
