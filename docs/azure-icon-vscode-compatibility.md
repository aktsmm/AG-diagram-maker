# Draw.io Azure アイコン表示問題の修正ガイド

> **作成日**: 2026 年 1 月 15 日  
> **問題発生環境**: VS Code + Draw.io Integration  
> **解決策**: Azure アイコンを `mxgraph.azure.*` から `img/lib/azure2/**/*.svg` 形式に変更

## 問題概要

VS Code 版 Draw.io Integration で Azure アイコンが**青い四角形**として表示され、正しいアイコンが表示されない問題。

### 症状

- AWS アイコン（AWS19 形式）は正常に表示される
- Azure アイコン（旧形式）が青い四角形になる

## 原因

### 旧形式（❌ 動作しない）

```xml
style="shape=mxgraph.azure.front_door;fillColor=#0078D4;..."
style="shape=mxgraph.azure.app_service;fillColor=#0078D4;..."
style="shape=mxgraph.azure.azure_active_directory;fillColor=#0078D4;..."
```

- `mxgraph.azure.*` 形式は **Web 版 draw.io** では動作するが、**VS Code 版**ではシェイプライブラリの読み込みが不完全な場合がある

### 新形式（✅ 推奨）

```xml
style="image=img/lib/azure2/networking/Front_Doors.svg;..."
style="image=img/lib/azure2/compute/App_Services.svg;..."
style="image=img/lib/azure2/identity/Azure_Active_Directory.svg;..."
```

- `img/lib/azure2/*` 形式は **SVG 画像を直接参照**するため、確実に表示される

## 修正方法

### Azure アイコンのスタイル置換ルール

| サービス        | 旧形式                                       | 新形式（Azure2）                                               |
| --------------- | -------------------------------------------- | -------------------------------------------------------------- |
| Front Door      | `shape=mxgraph.azure.front_door`             | `image=img/lib/azure2/networking/Front_Doors.svg`              |
| App Service     | `shape=mxgraph.azure.app_service`            | `image=img/lib/azure2/compute/App_Services.svg`                |
| Azure AD        | `shape=mxgraph.azure.azure_active_directory` | `image=img/lib/azure2/identity/Azure_Active_Directory.svg`     |
| Blob Storage    | `shape=mxgraph.azure.blob_storage`           | `image=img/lib/azure2/storage/Blob_Block.svg`                  |
| ExpressRoute    | `shape=mxgraph.azure.expressroute`           | `image=img/lib/azure2/networking/ExpressRoute_Circuits.svg`    |
| Virtual Network | `shape=mxgraph.azure.virtual_network`        | `image=img/lib/azure2/networking/Virtual_Networks.svg`         |
| SQL Database    | `shape=mxgraph.azure.sql_database`           | `image=img/lib/azure2/databases/SQL_Database.svg`              |
| Functions       | `shape=mxgraph.azure.function_apps`          | `image=img/lib/azure2/compute/Function_Apps.svg`               |
| Key Vault       | `shape=mxgraph.azure.key_vault`              | `image=img/lib/azure2/security/Key_Vaults.svg`                 |
| API Management  | `shape=mxgraph.azure.api_management`         | `image=img/lib/azure2/integration/API_Management_Services.svg` |

### 完全なスタイル例

#### 旧形式（❌）

```xml
<mxCell id="frontdoor" value="Azure Front Door"
        style="sketch=0;outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=0;shape=mxgraph.azure.front_door;fillColor=#0078D4;strokeColor=#ffffff;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="50" width="80" height="50" as="geometry"/>
</mxCell>
```

#### 新形式（✅）

```xml
<mxCell id="frontdoor" value="Azure Front Door"
        style="aspect=fixed;html=1;points=[];align=center;image;fontSize=11;image=img/lib/azure2/networking/Front_Doors.svg;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="50" width="68" height="52" as="geometry"/>
</mxCell>
```

### スタイル属性の違い

| 属性          | 旧形式            | 新形式                      |
| ------------- | ----------------- | --------------------------- |
| `shape`       | `mxgraph.azure.*` | 不要                        |
| `image`       | なし              | `img/lib/azure2/**/*.svg`   |
| `aspect`      | なし              | `fixed`（アスペクト比固定） |
| `fillColor`   | `#0078D4`         | 不要（SVG に含まれる）      |
| `strokeColor` | 指定              | 不要                        |

## Azure2 ライブラリのパス構造

```
img/lib/azure2/
├── ai_machine_learning/
│   ├── Azure_Machine_Learning.svg
│   └── Cognitive_Services.svg
├── analytics/
│   ├── Azure_Synapse_Analytics.svg
│   └── Event_Hubs.svg
├── compute/
│   ├── App_Services.svg
│   ├── Function_Apps.svg
│   ├── Virtual_Machine.svg
│   └── Azure_Kubernetes_Service.svg
├── containers/
│   └── Container_Instances.svg
├── databases/
│   ├── SQL_Database.svg
│   ├── Azure_Cosmos_DB.svg
│   └── Cache_for_Redis.svg
├── devops/
│   └── Azure_DevOps.svg
├── identity/
│   └── Azure_Active_Directory.svg
├── integration/
│   ├── API_Management_Services.svg
│   ├── Logic_Apps.svg
│   └── Service_Bus.svg
├── iot/
│   └── IoT_Hub.svg
├── management_governance/
│   ├── Azure_Monitor.svg
│   └── Log_Analytics_Workspaces.svg
├── networking/
│   ├── Virtual_Networks.svg
│   ├── Load_Balancers.svg
│   ├── Application_Gateways.svg
│   ├── Front_Doors.svg
│   ├── ExpressRoute_Circuits.svg
│   └── VPN_Gateway.svg
├── security/
│   ├── Key_Vaults.svg
│   └── Azure_Sentinel.svg
├── storage/
│   ├── Storage_Accounts.svg
│   └── Data_Lake_Storage.svg
└── web/
    └── App_Service_Plans.svg
```

## インストラクションへの反映内容

この修正は以下のインストラクションに反映済み：

### 1. cloud-icons.instructions.md (v1.1)

- VS Code 互換性に関する警告を冒頭に追加
- 新旧形式の対照表を追加
- Azure2 ライブラリパス構造を追加

### 2. svg-forge-template.instructions.md

- 全 Azure アイコンのスタイルを `img/lib/azure2/` 形式に変更
- `shape=mxgraph.azure.*` 形式を完全に削除

## 検証チェックリスト

生成後に以下を確認：

- [ ] Azure アイコンが `img/lib/azure2/` パスを使用している
- [ ] `shape=mxgraph.azure.*` が含まれていない
- [ ] VS Code Draw.io Integration で正しく表示される

## 参考リンク

- [Draw.io Azure Icons Library](https://github.com/jgraph/drawio/tree/dev/src/main/webapp/img/lib/azure2)
- [VS Code Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)
