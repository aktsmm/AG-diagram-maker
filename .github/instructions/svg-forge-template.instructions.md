# SVG Forge テンプレート

> SVG Forge Agent が参照する詳細な生成ガイドライン。

## 入力要件

### 必須入力

| 項目         | 条件                    | 説明                           |
| ------------ | ----------------------- | ------------------------------ |
| マニフェスト | レビュースコア >= 90 点 | 必須項目がすべて揃っていること |
| 出力パス     | `outputs/*.drawio.svg`  | kebab-case、適切な拡張子       |

### 入力バリデーション

```yaml
validation_rules:
  manifest:
    - required:
        [
          "title",
          "purpose",
          "page_size",
          "elements",
          "connections",
          "output_path",
        ]
    - score: ">= 90"

  output_path:
    - pattern: "^outputs/[a-z0-9-]+\\.drawio\\.svg$"
    - alternatives: [".drawio.png", ".png"]

  on_invalid:
    - action: "差し戻し"
    - report: "不足項目/違反をリスト"
```

## 生成ステップ詳細

### Step 1: キャンバス設定

```yaml
canvas_configuration:
  page_sizes:
    A4_portrait:
      width: 210mm (794px at 96dpi)
      height: 297mm (1123px at 96dpi)
    A4_landscape:
      width: 297mm (1123px at 96dpi)
      height: 210mm (794px at 96dpi)
    A3_portrait:
      width: 297mm (1123px at 96dpi)
      height: 420mm (1587px at 96dpi)
    A3_landscape:
      width: 420mm (1587px at 96dpi)
      height: 297mm (1123px at 96dpi)
    Letter:
      width: 215.9mm (816px at 96dpi)
      height: 279.4mm (1056px at 96dpi)

  grid:
    enabled: true
    size: 10px
    snap_to_grid: true
    visible: false # 出力時は非表示

  margins:
    top: 20px
    right: 20px
    bottom: 20px
    left: 20px
```

### Step 2: ノード配置

```yaml
node_placement:
  positioning_strategy:
    explicit: "マニフェストの x, y 座標を使用"
    auto: "レイアウトアルゴリズムで自動配置"

  auto_layout_algorithms:
    hierarchical:
      description: "階層構造（フローチャート、組織図）"
      parameters:
        direction: "TB|BT|LR|RL"
        level_spacing: 80
        node_spacing: 60

    organic:
      description: "力指向レイアウト（関係図）"
      parameters:
        attraction: 0.5
        repulsion: 100

    grid:
      description: "グリッド配置（一覧）"
      parameters:
        columns: 3
        cell_width: 150
        cell_height: 100

  shape_rendering:
    rectangle:
      default_size: { width: 120, height: 60 }
      style: "rounded=0;whiteSpace=wrap;html=1;"

    rounded_rectangle:
      default_size: { width: 120, height: 60 }
      style: "rounded=1;whiteSpace=wrap;html=1;"

    ellipse:
      default_size: { width: 80, height: 80 }
      style: "ellipse;whiteSpace=wrap;html=1;"

    diamond:
      default_size: { width: 80, height: 80 }
      style: "rhombus;whiteSpace=wrap;html=1;"

    cylinder:
      default_size: { width: 60, height: 80 }
      style: "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;"

    cloud:
      default_size: { width: 120, height: 80 }
      style: "ellipse;shape=cloud;whiteSpace=wrap;html=1;"

    actor:
      default_size: { width: 30, height: 60 }
      style: "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"

    document:
      default_size: { width: 100, height: 70 }
      style: "shape=document;whiteSpace=wrap;html=1;boundedLbl=1;"

  # ===========================================
  # Azure アイコン (mxgraph.azure.*)
  # ===========================================
  # Azure アイコンが利用可能な場合は優先使用。
  # 該当アイコンがない場合は上記の汎用形状で代替可。
  azure_icons:
    # ----- Compute -----
    virtual_machine:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;align=center;shape=mxgraph.azure.virtual_machine;"
      default_size: { width: 50, height: 43 }
      fallback: "rectangle"

    virtual_machine_scale_set:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.vm_scale_set;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    app_service:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.app_service;"
      default_size: { width: 50, height: 50 }
      fallback: "rounded_rectangle"

    function_app:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.function_apps;"
      default_size: { width: 50, height: 44 }
      fallback: "rounded_rectangle"

    container_instances:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.container_instances;"
      default_size: { width: 50, height: 42 }
      fallback: "rectangle"

    kubernetes_service:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.kubernetes;"
      default_size: { width: 50, height: 44 }
      fallback: "rectangle"

    # ----- Networking -----
    virtual_network:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.virtual_network;"
      default_size: { width: 67, height: 40 }
      fallback: "cloud"

    subnet:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.subnet;"
      default_size: { width: 50, height: 28 }
      fallback: "rounded_rectangle"

    azure_firewall:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#E65100;shape=mxgraph.azure.azure_firewall;"
      default_size: { width: 50, height: 50 }
      fallback: "diamond"

    application_gateway:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.application_gateway;"
      default_size: { width: 50, height: 50 }
      fallback: "diamond"

    load_balancer:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.load_balancer_generic;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    public_ip:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.public_ip_address;"
      default_size: { width: 50, height: 40 }
      fallback: "ellipse"

    network_security_group:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#68217A;shape=mxgraph.azure.network_security_group;"
      default_size: { width: 34, height: 40 }
      fallback: "rectangle"

    route_table:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.route_table;"
      default_size: { width: 40, height: 40 }
      fallback: "rectangle"

    vpn_gateway:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.vpn_gateway;"
      default_size: { width: 50, height: 50 }
      fallback: "diamond"

    expressroute:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.expressroute;"
      default_size: { width: 50, height: 50 }
      fallback: "diamond"

    azure_bastion:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.azure_bastion;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    dns_zone:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.dns;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    private_endpoint:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.private_endpoint;"
      default_size: { width: 40, height: 40 }
      fallback: "ellipse"

    # ----- Storage -----
    storage_account:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.storage;"
      default_size: { width: 50, height: 42 }
      fallback: "cylinder"

    blob_storage:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.blob_storage;"
      default_size: { width: 37, height: 50 }
      fallback: "cylinder"

    file_storage:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.file_storage;"
      default_size: { width: 47, height: 50 }
      fallback: "document"

    queue_storage:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.queue_storage;"
      default_size: { width: 37, height: 50 }
      fallback: "cylinder"

    # ----- Database -----
    sql_database:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.sql_database;"
      default_size: { width: 37, height: 50 }
      fallback: "cylinder"

    cosmos_db:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.cosmos_db;"
      default_size: { width: 50, height: 50 }
      fallback: "cylinder"

    redis_cache:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.cache_redis;"
      default_size: { width: 50, height: 42 }
      fallback: "cylinder"

    # ----- Security & Identity -----
    key_vault:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.key_vault;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    azure_ad:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.entra_id;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    managed_identity:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.managed_identities;"
      default_size: { width: 50, height: 50 }
      fallback: "actor"

    # ----- Integration -----
    api_management:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.api_management;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    service_bus:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.service_bus;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    event_hub:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.event_hubs;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    logic_app:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.logic_apps;"
      default_size: { width: 50, height: 50 }
      fallback: "rounded_rectangle"

    # ----- Monitoring -----
    monitor:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.monitor;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    log_analytics:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.log_analytics;"
      default_size: { width: 50, height: 44 }
      fallback: "rectangle"

    application_insights:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#68217A;shape=mxgraph.azure.application_insights;"
      default_size: { width: 50, height: 65 }
      fallback: "ellipse"

    # ----- AI & ML -----
    cognitive_services:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.cognitive_services;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    openai_service:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.azure_openai;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    machine_learning:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.machine_learning;"
      default_size: { width: 50, height: 50 }
      fallback: "ellipse"

    # ----- DevOps & Management -----
    devops:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.devops;"
      default_size: { width: 50, height: 50 }
      fallback: "rounded_rectangle"

    resource_group:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.resource_group;"
      default_size: { width: 50, height: 40 }
      fallback: "rectangle"

    subscription:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.subscriptions;"
      default_size: { width: 50, height: 35 }
      fallback: "rectangle"

    management_group:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.management_groups;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    # ----- General / Common -----
    internet:
      style: "ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;"
      default_size: { width: 120, height: 80 }
      fallback: "cloud"

    on_premises:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#505050;shape=mxgraph.azure.enterprise;"
      default_size: { width: 50, height: 50 }
      fallback: "rectangle"

    user:
      style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.user;"
      default_size: { width: 47, height: 50 }
      fallback: "actor"
```

### Step 3: コネクタ描画

```yaml
connector_rendering:
  edge_styles:
    arrow:
      style: "endArrow=classic;html=1;"
      description: "片方向矢印"

    line:
      style: "endArrow=none;html=1;"
      description: "矢印なし直線"

    bidirectional:
      style: "endArrow=classic;startArrow=classic;html=1;"
      description: "双方向矢印"

    dashed:
      style: "endArrow=classic;dashed=1;html=1;"
      description: "破線矢印"

  routing_options:
    orthogonal:
      style: "edgeStyle=orthogonalEdgeStyle;rounded=0;"
      description: "直角ルーティング（デフォルト）"

    straight:
      style: "edgeStyle=none;"
      description: "直線接続"

    curved:
      style: "edgeStyle=elbowEdgeStyle;elbow=vertical;curved=1;"
      description: "曲線接続"

  label_positioning:
    center: "align=center;verticalAlign=middle;"
    source: "align=left;verticalAlign=bottom;"
    target: "align=right;verticalAlign=bottom;"
```

### Step 4: スタイル適用

> **Note**: カラースキーム詳細は `manifest-template.instructions.md` の「カラースキーム」セクションを参照。

````yaml
style_application:
  # カラースキーム: manifest-template.instructions.md で定義
  # corporate, azure, pastel, monochrome, custom から選択

  typography:
    default:
      family: "Helvetica, Arial, sans-serif"
      size: 12
      weight: "normal"
      color: "#000000"

    title:
      size: 16
      weight: "bold"

    label:
      size: 10
      weight: "normal"
```### Step 5: draw.io メタ情報埋め込み

> **🚨 重要: draw.io 編集可能性の条件**
>
> draw.io で編集するには、**全ての図形を `mxCell` 要素として定義**する必要があります。
> SVG ネイティブ要素（`<ellipse>`, `<path>`, `<rect>` 等）だけでは、ブラウザでは表示できても **draw.io では真っ白**になります。

#### ❌ 間違った形式（draw.io で真っ白になる）

```xml
<!-- SVG要素だけで描画 → draw.io では編集不可 -->
<svg ... content="&lt;mxfile...&gt;&lt;root&gt;&lt;mxCell id='0'/&gt;&lt;mxCell id='1'/&gt;&lt;/root&gt;...">
  <ellipse cx="250" cy="220" rx="85" ry="105" fill="#F5D0B9"/>  <!-- SVGネイティブ要素 -->
  <path d="M210 280 Q230 275..." fill="#D4707A"/>                <!-- SVGネイティブ要素 -->
</svg>
```

**問題点:**
- `content` 属性の mxfile 内は空の `<root>` だけ
- 実際の図形は SVG 要素で描画
- → ブラウザ: 表示できる ✅ / draw.io: 編集対象なし → 真っ白 ❌

#### ✅ 正しい形式（draw.io で編集可能）

**方法 A: 純粋な mxfile 形式（`.drawio` 拡張子推奨）**

```xml
<mxfile host="app.diagrams.net" modified="2025-12-10T00:00:00.000Z" agent="Copilot" version="21.0.0" generator="aktsmm/Ag-diagram-maker">
  <diagram name="Page-1" id="diagram-1">
    <mxGraphModel dx="794" dy="1123" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="794" pageHeight="1123">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 全ての図形を mxCell で定義 -->
        <mxCell id="face" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F5D0B9;strokeColor=#C8A080;" vertex="1" parent="1">
          <mxGeometry x="162" y="115" width="176" height="220" as="geometry"/>
        </mxCell>
        <mxCell id="mouth" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#D4707A;strokeColor=#B85060;" vertex="1" parent="1">
          <mxGeometry x="205" y="280" width="90" height="50" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> **⚠️ 必須**: `mxfile` タグには `generator="aktsmm/Ag-diagram-maker"` 属性を必ず設定すること。

**方法 B: SVG + mxCell 埋め込み形式（`.drawio.svg` 拡張子）**

```xml
<!-- draw.io SVG の完全な構造 -->
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     version="1.1"
     width="794px"
     height="1123px"
     viewBox="-0.5 -0.5 794 1123">

  <!-- draw.io メタデータ（編集可能性の鍵） -->
  <!-- content 属性に mxfile XML をエスケープして埋め込む -->
  <!-- ⚠️ mxfile 内に全図形の mxCell 定義を含めること -->
  <defs/>

  <g>
    <!-- 各ノードとコネクタの SVG 要素 -->
    <!-- ⚠️ これらは表示用。編集は mxCell で行われる -->
  </g>
</svg>

#### mxCell 形状スタイル一覧

| 形状タイプ | style 属性 |
|-----------|------------|
| 矩形 | `rounded=0;whiteSpace=wrap;html=1;` |
| 角丸矩形 | `rounded=1;whiteSpace=wrap;html=1;` |
| 楕円/円 | `ellipse;whiteSpace=wrap;html=1;` |
| ひし形 | `rhombus;whiteSpace=wrap;html=1;` |
| 円柱 | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` |
| 三角形 | `triangle;whiteSpace=wrap;html=1;` |
| 台形 | `shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;` |
| 雲 | `ellipse;shape=cloud;whiteSpace=wrap;html=1;` |

#### mxCell 共通属性

```yaml
mxCell_attributes:
  vertex: "1"          # ノード（図形）の場合
  edge: "1"            # エッジ（線）の場合
  parent: "1"          # 親セル（通常は "1"）
  value: "ラベル"       # 表示テキスト
  style: "..."         # スタイル文字列

mxGeometry_attributes:
  x: 100               # X座標
  y: 100               # Y座標
  width: 120           # 幅
  height: 60           # 高さ
  as: "geometry"       # 固定値
```
````

### Step 6: 保存

```yaml
save_process:
  path_validation:
    - "outputs/ ディレクトリ配下であること"
    - "ファイル名が kebab-case であること"
    - "拡張子が .drawio.svg または .drawio.png であること"

  file_operations:
    new_file:
      action: "作成"
    existing_file:
      action: "上書き確認を求める"
      alternatives: ["バージョン番号付与", "タイムスタンプ付与"]

  encoding: "UTF-8"
  line_endings: "LF"
```

---

## 🚨 重要 TIPS: draw.io 表示トラブルシューティング

### よくある失敗パターンと対策

#### パターン 1: SVG は表示されるが draw.io で真っ白

**症状:**

- ブラウザや VS Code プレビューでは画像が表示される
- draw.io で開くと何も表示されない（真っ白）

**原因:**

```xml
<!-- ❌ 失敗例: SVG の content 属性に空の mxfile -->
<svg xmlns="http://www.w3.org/2000/svg"
     content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id='0'/&gt;&lt;mxCell id='1'/&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
  <!-- 図形は SVG ネイティブ要素で描画 -->
  <ellipse cx="200" cy="180" rx="70" ry="85" fill="#F5D6C6"/>
  <path d="M 160 215 Q 200 250 240 215" fill="#D4727A"/>
</svg>
```

**問題点:**

- `content` 属性内の `mxfile` には `mxCell id="0"` と `mxCell id="1"` しかない（空のルート）
- 実際の図形（ellipse, path）は SVG 要素として描画されている
- draw.io は `mxCell` だけを読み込むので、図形データがない = 真っ白

#### パターン 1.5: draw.io で開けるが中身が空（見落としやすい！）

**症状:**

- ファイルは draw.io で開ける ✅
- しかしキャンバスが空っぽ ❌
- ブラウザで直接開くと SVG は表示される

**原因:** `content` 属性内に mxfile の構造はあるが、図形の mxCell が定義されていない

```xml
<!-- ❌ 失敗例: content内のrootが空 -->
<svg xmlns="http://www.w3.org/2000/svg" width="900px" height="1400px"
     content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
  <!-- SVG要素でフローチャートを描画 -->
  <ellipse cx="450" cy="80" rx="50" ry="25" fill="#d5e8d4"/>
  <text x="450" y="85">開始</text>
  <rect x="375" y="140" width="150" height="50" fill="#dae8fc"/>
  <path d="M 450 105 L 450 140" stroke="#333"/>
</svg>
```

> **🚨 重要**: draw.io は **`content` 属性内の XML だけ**を解釈する。SVG ネイティブ要素（rect, ellipse, text, path 等）は完全に無視される。

**解決策:** `content` 属性内の `<root>` に全図形を mxCell で定義

```xml
<!-- ✅ 正解: content属性内に全図形をmxCellで定義 -->
<svg xmlns="http://www.w3.org/2000/svg" width="900px" height="1400px"
     content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;start&quot; value=&quot;開始&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;400&quot; y=&quot;60&quot; width=&quot;100&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;process&quot; value=&quot;処理&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;375&quot; y=&quot;140&quot; width=&quot;150&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;e1&quot; style=&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;start&quot; target=&quot;process&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
  <defs/>
</svg>
```

**解決策:**

```xml
<!-- ✅ 正解: 純粋な mxfile 形式で出力 -->
<mxfile host="app.diagrams.net" modified="2025-12-10T00:00:00.000Z" agent="Copilot" version="21.0.0">
  <diagram name="Portrait" id="portrait-1">
    <mxGraphModel dx="400" dy="500" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="400" pageHeight="500">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 全ての図形を mxCell で定義 -->
        <mxCell id="face" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F5D6C6;strokeColor=#D4B8A8;" vertex="1" parent="1">
          <mxGeometry x="130" y="95" width="140" height="170" as="geometry"/>
        </mxCell>
        <mxCell id="mouth" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#D4727A;strokeColor=#A04040;" vertex="1" parent="1">
          <mxGeometry x="160" y="205" width="80" height="45" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

#### パターン 2: ファイル形式の選択ミス

| 拡張子        | 内容形式                         | draw.io での扱い              |
| ------------- | -------------------------------- | ----------------------------- |
| `.drawio`     | 純粋な mxfile XML                | ✅ 最も安全、推奨             |
| `.drawio.svg` | mxfile XML（SVG として認識も可） | ✅ draw.io で編集可能         |
| `.svg`        | SVG + content 属性に mxfile      | ⚠️ content 内に全 mxCell 必須 |

**推奨:**

- **ポートレート/イラスト系**: `.drawio.svg` を使用し、中身は純粋な mxfile 形式
- **技術図面**: `.drawio.svg` で mxfile 形式

#### パターン 3: mxCell で表現できない複雑な形状

**問題:** SVG の `<path>` で複雑なベジェ曲線を使いたいが、mxCell では表現できない

**解決策:** draw.io の基本図形を組み合わせる

```xml
<!-- ❌ SVG path（draw.io で編集不可） -->
<path d="M 160 215 Q 180 205 200 205 Q 220 205 240 215 Q 230 245 200 250 Q 170 245 160 215 Z"/>

<!-- ✅ mxCell の ellipse で近似 -->
<mxCell id="mouth" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#D4727A;" vertex="1" parent="1">
  <mxGeometry x="160" y="205" width="80" height="45" as="geometry"/>
</mxCell>
```

#### パターン 4: 曲線（カーブ）の描画

draw.io で曲線を描く場合は `curved=1` スタイルと `edge` を使用:

```xml
<!-- 眉毛などのアーチ型曲線 -->
<mxCell id="brow_left" value="" style="curved=1;endArrow=none;html=1;strokeColor=#2D2D2D;strokeWidth=3;endFill=0;rounded=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="150" y="135" as="sourcePoint"/>
    <mxPoint x="185" y="133" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="167" y="128"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 生成前チェックリスト

```yaml
pre_generation_checklist:
  format:
    - "出力形式は純粋な mxfile XML か？"
    - "全ての図形を mxCell で定義しているか？"
    - "SVG ネイティブ要素（ellipse, path, rect）を直接使っていないか？"

  structure:
    - "mxCell id='0' と id='1' がルートに存在するか？"
    - "全ての図形に parent='1' が設定されているか？"
    - "vertex='1'（図形）または edge='1'（線）が設定されているか？"

  style:
    - "fillColor, strokeColor は #RRGGBB 形式か？"
    - "gradientColor を使う場合、gradientDirection も指定したか？"
```

### draw.io 形状変換早見表

| 描きたいもの | SVG 要素          | mxCell style                                    |
| ------------ | ----------------- | ----------------------------------------------- |
| 円/楕円      | `<ellipse>`       | `ellipse;whiteSpace=wrap;html=1;`               |
| 矩形         | `<rect>`          | `rounded=0;whiteSpace=wrap;html=1;`             |
| 角丸矩形     | `<rect rx="...">` | `rounded=1;whiteSpace=wrap;html=1;`             |
| 三角形       | `<polygon>`       | `triangle;whiteSpace=wrap;html=1;`              |
| 台形         | `<polygon>`       | `shape=trapezoid;perimeter=trapezoidPerimeter;` |
| 曲線         | `<path>`          | `curved=1;endArrow=none;` (edge)                |
| 直線         | `<line>`          | `endArrow=none;html=1;` (edge)                  |
| 矢印         | `<line>` + marker | `endArrow=classic;html=1;` (edge)               |

---

## 事後チェック

### 必須チェック項目

| チェック     | 方法                 | 合格基準             |
| ------------ | -------------------- | -------------------- |
| ファイル存在 | ファイルシステム確認 | ファイルが存在する   |
| サイズ確認   | ファイルサイズ取得   | 0 バイトでない       |
| XML 妥当性   | パース試行           | エラーなし           |
| draw.io 互換 | draw.io で開く       | 編集モードに入れる   |
| 要素確認     | 目視                 | 全ノード・エッジ表示 |
| 可読性       | 目視                 | テキストが読める     |

### draw.io 編集可能性の検証

```yaml
draw_io_verification:
  method: "ファイルをdraw.ioで開く"

  checks:
    - "ファイルが正常に開ける"
    - "すべてのノードが選択可能"
    - "ノードの移動・リサイズが可能"
    - "テキスト編集が可能"
    - "コネクタの再接続が可能"
    - "新規要素の追加が可能"

  common_issues:
    mxfile_missing: "mxfileメタデータが欠落 → 再生成"
    encoding_error: "文字化け → UTF-8で再保存"
    style_error: "スタイル構文エラー → スタイル修正"
```

## エラーハンドリング

| エラー           | 原因           | 対応                       |
| ---------------- | -------------- | -------------------------- |
| マニフェスト不足 | 必須項目欠落   | 差し戻し、不足項目報告     |
| スコア不足       | レビュー未完了 | マニフェストレビューへ戻す |
| パス不正         | outputs/ 外    | 正しいパスを提案           |
| 形状未サポート   | draw.io 非対応 | 代替形状を使用             |
| ファイル競合     | 既存ファイル   | 上書き確認/バージョン付与  |
| XML 不正         | 生成エラー     | 再生成                     |

## 品質基準

### 生成物の品質要件

| 項目           | 基準                        |
| -------------- | --------------------------- |
| 全ノード描画   | マニフェストの 100%をカバー |
| 全エッジ接続   | マニフェストの 100%をカバー |
| テキスト可読性 | 最小 8px、推奨 12px 以上    |
| 要素重なり     | なし                        |
| draw.io 互換   | 編集モードで全機能使用可能  |
| パス一致       | マニフェスト指定と完全一致  |

## 関連ファイル

| ファイル                              | 用途             |
| ------------------------------------- | ---------------- |
| `svg-forge.agent.md`                  | エージェント定義 |
| `manifest-template.instructions.md`   | マニフェスト仕様 |
| `svg-review-template.instructions.md` | レビュー基準     |
