````instructions
# 決定的変換ルール v5.0

> **適用対象**: IR-Renderer エージェント
> **最終更新**: 2025-12-12

このインストラクションは、DiagramIR から mxGraphModel への**完全に決定的な変換**ルールを定義します。

---

## 🎯 原則

### 決定的変換とは

```yaml
deterministic_transformation:
  definition: |
    同じ DiagramIR を入力すると、
    常に同一の mxGraphModel を出力する。

  guarantees:
    - 同一入力 → 同一出力
    - ランダム要素なし
    - 環境依存なし
    - 時刻依存なし（タイムスタンプは除く）

  prohibited:
    - レイアウトの「自動調整」
    - 「見栄え向上」のための位置変更
    - 未定義要素の補完
    - デフォルト値の推測
````

### 禁止行為

| 行為               | 理由       | 代替手段              |
| ------------------ | ---------- | --------------------- |
| 自動レイアウト調整 | 非決定的   | IR で position を指定 |
| ラベルの短縮       | 創作的判断 | IR-Builder で事前調整 |
| 色の自動選択       | 非決定的   | IR で style を指定    |
| 余白の最適化       | 創作的判断 | IR で spacing を指定  |

---

## 📐 座標計算ルール

### 自動レイアウトの決定論化

IR の `layout.type` に基づく**決定的な座標計算**:

```yaml
layout_algorithms:
  hierarchical:
    # TB (Top to Bottom) の場合
    TB:
      level_assignment: topological_sort # 決定的ソート
      x_calculation: |
        x = margin_left + (node_index_in_level * (node_width + spacing.horizontal))
      y_calculation: |
        y = margin_top + (level * (max_node_height_in_level + spacing.vertical))

    # LR (Left to Right) の場合
    LR:
      x_calculation: |
        x = margin_left + (level * (max_node_width_in_level + spacing.horizontal))
      y_calculation: |
        y = margin_top + (node_index_in_level * (node_height + spacing.vertical))

  grid:
    x_calculation: |
      x = margin_left + ((index % columns) * cell_width)
    y_calculation: |
      y = margin_top + (floor(index / columns) * cell_height)

  manual:
    # IR の position をそのまま使用
    x_calculation: element.position.x
    y_calculation: element.position.y

# ノードの出現順序は ID のアルファベット順でソート（決定的）
node_ordering:
  method: "sort by element.id ascending (lexicographic)"
```

### マージン・スペーシングのデフォルト値

```yaml
default_values:
  canvas:
    margin:
      top: 40
      right: 40
      bottom: 40
      left: 40

  spacing:
    horizontal: 60
    vertical: 80

  grid:
    columns: 3
    cell_width: 150
    cell_height: 120
# これらの値は IR で上書き可能
# IR で指定がない場合のみデフォルトを使用
```

---

## 🎨 スタイル変換ルール

### 要素タイプ → mxCell スタイル

```yaml
element_type_to_style:
  # === 基本形状 ===
  rectangle:
    base: "rounded=0;whiteSpace=wrap;html=1;"
    size: { width: 120, height: 60 }

  rounded_rectangle:
    base: "rounded=1;whiteSpace=wrap;html=1;"
    size: { width: 120, height: 60 }

  ellipse:
    base: "ellipse;whiteSpace=wrap;html=1;"
    size: { width: 80, height: 80 }

  diamond:
    base: "rhombus;whiteSpace=wrap;html=1;"
    size: { width: 80, height: 80 }

  cylinder:
    base: "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;"
    size: { width: 60, height: 80 }

  parallelogram:
    base: "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;"
    size: { width: 120, height: 60 }

  cloud:
    base: "ellipse;shape=cloud;whiteSpace=wrap;html=1;"
    size: { width: 120, height: 80 }

  actor:
    base: "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
    size: { width: 30, height: 60 }

  document:
    base: "shape=document;whiteSpace=wrap;html=1;boundedLbl=1;"
    size: { width: 100, height: 70 }

  hexagon:
    base: "shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;"
    size: { width: 100, height: 80 }

  # === Azure アイコン ===
  azure_vm:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;align=center;shape=mxgraph.azure.virtual_machine;"
    size: { width: 50, height: 43 }

  azure_vnet:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.virtual_network;"
    size: { width: 67, height: 40 }

  azure_storage:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.storage;"
    size: { width: 45, height: 38 }

  azure_sql:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.sql_database;"
    size: { width: 37, height: 50 }

  azure_app_service:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.app_service;"
    size: { width: 50, height: 50 }

  azure_function:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.function_apps;"
    size: { width: 50, height: 44 }

  azure_aks:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.kubernetes;"
    size: { width: 50, height: 44 }

  azure_firewall:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#E65100;shape=mxgraph.azure.azure_firewall;"
    size: { width: 50, height: 50 }

  azure_load_balancer:
    base: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.load_balancer_generic;"
    size: { width: 50, height: 50 }

  # === AWS アイコン ===
  aws_ec2:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#ED7100;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;"
    size: { width: 48, height: 48 }

  aws_vpc:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.vpc;"
    size: { width: 48, height: 48 }

  aws_s3:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#7AA116;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;"
    size: { width: 48, height: 48 }

  aws_rds:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#C925D1;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;"
    size: { width: 48, height: 48 }

  aws_lambda:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#ED7100;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;"
    size: { width: 48, height: 48 }

  aws_eks:
    base: "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#ED7100;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_kubernetes_service;"
    size: { width: 48, height: 48 }
```

### カラースキーム → 色定義

```yaml
color_schemes:
  corporate:
    primary: "#dae8fc"
    secondary: "#f5f5f5"
    accent: "#d5e8d4"
    success: "#d5e8d4"
    warning: "#fff2cc"
    error: "#f8cecc"
    stroke:
      primary: "#6c8ebf"
      secondary: "#666666"
      accent: "#82b366"
      success: "#82b366"
      warning: "#d6b656"
      error: "#b85450"

  pastel:
    primary: "#e1d5e7"
    secondary: "#fff2cc"
    accent: "#d5e8d4"
    success: "#d5e8d4"
    warning: "#ffe6cc"
    error: "#f8cecc"
    stroke:
      primary: "#9673a6"
      secondary: "#d6b656"
      accent: "#82b366"
      success: "#82b366"
      warning: "#d79b00"
      error: "#b85450"

  monochrome:
    primary: "#f5f5f5"
    secondary: "#e6e6e6"
    accent: "#cccccc"
    success: "#d9d9d9"
    warning: "#bfbfbf"
    error: "#a6a6a6"
    stroke:
      primary: "#333333"
      secondary: "#666666"
      accent: "#999999"
      success: "#666666"
      warning: "#666666"
      error: "#333333"

  azure:
    primary: "#0078D4"
    secondary: "#50E6FF"
    accent: "#773ADC"
    success: "#107C10"
    warning: "#FFB900"
    error: "#D13438"
    stroke:
      primary: "#005A9E"
      secondary: "#3BC5EF"
      accent: "#5C2D91"
      success: "#0B5C0B"
      warning: "#D48C00"
      error: "#A4262C"

  aws:
    primary: "#FF9900"
    secondary: "#232F3E"
    accent: "#1A73E8"
    success: "#7AA116"
    warning: "#FF9900"
    error: "#D13212"
    stroke:
      primary: "#CC7A00"
      secondary: "#1A1F28"
      accent: "#1557B0"
      success: "#5C7C12"
      warning: "#CC7A00"
      error: "#A5280F"
```

### スタイル文字列の組み立て

```yaml
style_assembly:
  # 基本スタイル + 色 + オプション の順で結合
  formula: |
    base_style + color_style + optional_style

  color_style_format: |
    fillColor={fill_color};strokeColor={stroke_color};fontColor={font_color};

  optional_style_keys:
    - opacity
    - fontSize
    - fontStyle # 0=normal, 1=bold, 2=italic, 3=bold+italic
    - shadow

  example:
    element:
      type: "rectangle"
      style:
        fill_color: "#dae8fc"
        stroke_color: "#6c8ebf"

    output: |
      rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

---

## 🔗 接続（エッジ）変換ルール

### 接続タイプ → mxCell スタイル

```yaml
connection_type_to_style:
  arrow:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;"

  line:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;"

  bidirectional:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=classic;startFill=1;endArrow=classic;endFill=1;"

  dashed:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=classic;endFill=1;"

  dotted:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=1 4;endArrow=classic;endFill=1;"
```

### エッジスタイルオプション

```yaml
edge_style_options:
  curved:
    add: "curved=1;"
    remove: "orthogonalEdgeStyle"
    replace_with: "elbowEdgeStyle"

  orthogonal:
    # デフォルト、変更なし
    add: ""

  stroke_width:
    format: "strokeWidth={value};"
    default: 1

  stroke_color:
    format: "strokeColor={value};"
```

---

## 📦 グループ変換ルール

```yaml
group_to_mxcell:
  style: "swimlane;horizontal=1;startSize=30;fillColor={fill_color};strokeColor={stroke_color};"

  size_calculation:
    # グループサイズは IR で指定されている場合はそれを使用
    # 指定がない場合は、含まれる要素から決定的に計算
    auto_size:
      padding: 20
      header_height: 30
      width: max(member_max_x + member_width) - min(member_min_x) + (padding * 2)
      height: max(member_max_y + member_height) - min(member_min_y) + (padding * 2) + header_height

  member_positioning:
    # メンバーの position は親グループからの相対座標
    # parent 属性を group_id に設定
    parent: "{group_id}"
    relative_coordinates: true
```

---

## 📄 mxGraphModel テンプレート

```yaml
mxfile_template:
  structure: |
    <?xml version="1.0" encoding="UTF-8"?>
    <mxfile host="app.diagrams.net" modified="{timestamp}" agent="Ag-diagram-maker v5.0">
      <diagram id="{diagram_id}" name="{diagram_name}">
        <mxGraphModel dx="{dx}" dy="{dy}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_width}" pageHeight="{page_height}" math="0" shadow="0">
          <root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            {mxcells}
          </root>
        </mxGraphModel>
      </diagram>
    </mxfile>

  mxcell_node_template: |
    <mxCell id="{id}" value="{label}" style="{style}" vertex="1" parent="{parent}">
      <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
    </mxCell>

  mxcell_edge_template: |
    <mxCell id="{id}" value="{label}" style="{style}" edge="1" parent="{parent}" source="{source}" target="{target}">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

  mxcell_group_template: |
    <mxCell id="{id}" value="{label}" style="{style}" vertex="1" parent="{parent}">
      <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
    </mxCell>
```

---

## ✅ 出力前検証

```yaml
pre_output_validation:
  mandatory_checks:
    - name: "mxCell完全性"
      formula: "count(mxCell) >= 2 + count(elements) + count(connections)"
      on_fail: "BLOCK"

    - name: "参照整合性"
      check: "全エッジの source/target が存在する mxCell id を参照"
      on_fail: "BLOCK"

    - name: "座標非負"
      check: "全 mxGeometry の x, y >= 0"
      on_fail: "BLOCK"

    - name: "サイズ正値"
      check: "全 mxGeometry の width, height > 0"
      on_fail: "BLOCK"

  blocking_behavior:
    on_fail:
      - log_error
      - return_error_to_coordinator
      - do_not_save_file
```

---

## 🔄 変換プロセス

```yaml
transformation_process:
  steps:
    1_validate_input:
      action: "IR が ValidationResult.valid=true であることを確認"
      on_fail: "Coordinator にエラー返却"

    2_calculate_positions:
      action: "layout.type に基づき全要素の座標を決定的に計算"
      output: "positioned_elements[]"

    3_generate_mxcells:
      action: "各要素を mxCell に変換"
      order: "elements → groups → connections"
      output: "mxcells[]"

    4_assemble_mxfile:
      action: "テンプレートに mxcells を埋め込み"
      output: "mxfile_xml"

    5_pre_output_validation:
      action: "出力前検証を実行"
      on_fail: "BLOCK"

    6_produce_file:
      action: "ファイル出力"
      path: "IR.output.path"
```

```

```
