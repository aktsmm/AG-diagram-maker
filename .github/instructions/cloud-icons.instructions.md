# クラウドアイコン使用ルール (v1.1)

> **適用対象**: すべての draw.io 図面生成エージェント
> **最終更新**: 2026-01-15

このインストラクションは、Azure および AWS リソースを含む図面を生成する際のアイコン使用ルールを定義します。

---

## ⚠️ VS Code Draw.io Integration 互換性に関する重要な注意

### 問題概要

VS Code 版 Draw.io Integration では、Azure アイコンの形式によって表示の可否が異なります。

| 形式                            | Web 版 draw.io | VS Code 版 Draw.io  |
| ------------------------------- | -------------- | ------------------- |
| `shape=mxgraph.azure.*`         | ✅ 動作        | ❌ 青い四角形になる |
| `image=img/lib/azure2/**/*.svg` | ✅ 動作        | ✅ 動作             |

### 原因

- `mxgraph.azure.*` 形式は Web 版では動作するが、VS Code 版ではシェイプライブラリの読み込みが不完全
- `img/lib/azure2/` 形式は SVG 画像を直接参照するため、環境に依存せず確実に表示される

### 結論

**本リポジトリでは `img/lib/azure2/**/\*.svg` 形式を必須とする。\*\*

---

## 🔷 Azure アイコン

### 基本ルール

| ルール                 | 内容                                                            |
| ---------------------- | --------------------------------------------------------------- |
| **Azure アイコン必須** | Azure 関連の図は `img/lib/azure2/` 形式の公式アイコンを使用     |
| **汎用四角形禁止**     | Azure リソースを汎用四角形+テキストで表現してはいけない         |
| **対象スコープ**       | VNet, Firewall, VM, NSG, Storage, App Service, AKS, Entra ID 等 |

### 正式 mxCell フォーマット

```xml
<mxCell id="storage-1" value="Storage Account"
        style="image;aspect=fixed;html=1;points=[];align=center;fontSize=12;image=img/lib/azure2/storage/Storage_Accounts.svg;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="65" height="52" as="geometry"/>
</mxCell>
```

### 主要 Azure アイコンマッピング

```yaml
azure_icons:
  # Storage
  - image: "img/lib/azure2/storage/Storage_Accounts.svg"
    use_for: "ストレージアカウント, Azure Files"
  - image: "img/lib/azure2/storage/Blob_Storage.svg"
    use_for: "Blob Storage"

  # Compute
  - image: "img/lib/azure2/compute/Virtual_Machine.svg"
    use_for: "VM, 仮想マシン"
  - image: "img/lib/azure2/compute/App_Services.svg"
    use_for: "App Service, Web Apps"
  - image: "img/lib/azure2/compute/Function_Apps.svg"
    use_for: "Functions, Azure Functions"
  - image: "img/lib/azure2/compute/Kubernetes_Services.svg"
    use_for: "AKS, Azure Kubernetes Service"
  - image: "img/lib/azure2/compute/Virtual_Machine_Scale_Sets.svg"
    use_for: "VMSS, スケールセット"

  # Networking
  - image: "img/lib/azure2/networking/Virtual_Networks.svg"
    use_for: "VNet, 仮想ネットワーク"
  - image: "img/lib/azure2/networking/Azure_Firewall.svg"
    use_for: "Azure Firewall"
  - image: "img/lib/azure2/networking/Network_Security_Groups.svg"
    use_for: "NSG, ネットワークセキュリティグループ"
  - image: "img/lib/azure2/networking/Public_IP_Addresses.svg"
    use_for: "Public IP"
  - image: "img/lib/azure2/networking/Route_Tables.svg"
    use_for: "ルートテーブル, UDR"
  - image: "img/lib/azure2/networking/Load_Balancers.svg"
    use_for: "Load Balancer"
  - image: "img/lib/azure2/networking/Application_Gateways.svg"
    use_for: "Application Gateway"
  - image: "img/lib/azure2/networking/Virtual_Network_Gateways.svg"
    use_for: "VPN Gateway, ExpressRoute Gateway"
  - image: "img/lib/azure2/networking/Bastions.svg"
    use_for: "Azure Bastion"
  - image: "img/lib/azure2/networking/Private_Endpoints.svg"
    use_for: "Private Endpoint"
  - image: "img/lib/azure2/networking/Private_Link_Services.svg"
    use_for: "Private Link"

  # Identity
  - image: "img/lib/azure2/identity/Azure_Active_Directory.svg"
    use_for: "Entra ID, Azure AD, AAD"
  - image: "img/lib/azure2/identity/Managed_Identities.svg"
    use_for: "マネージド ID"

  # Security
  - image: "img/lib/azure2/security/Key_Vaults.svg"
    use_for: "Key Vault"
  - image: "img/lib/azure2/security/Azure_Defender.svg"
    use_for: "Microsoft Defender for Cloud"

  # Database
  - image: "img/lib/azure2/databases/Azure_SQL_Database.svg"
    use_for: "Azure SQL Database"
  - image: "img/lib/azure2/databases/Azure_Cosmos_DB.svg"
    use_for: "Cosmos DB"
  - image: "img/lib/azure2/databases/Azure_Database_for_PostgreSQL.svg"
    use_for: "PostgreSQL"
  - image: "img/lib/azure2/databases/Azure_Database_for_MySQL.svg"
    use_for: "MySQL"

  # AVD (Azure Virtual Desktop)
  - image: "img/lib/azure2/compute/Azure_Virtual_Desktop.svg"
    use_for: "Azure Virtual Desktop, AVD"
  - image: "img/lib/azure2/compute/Host_Pools.svg"
    use_for: "ホストプール"
  - image: "img/lib/azure2/compute/Session_Hosts.svg"
    use_for: "セッションホスト"

  # Management
  - image: "img/lib/azure2/management/Azure_Monitor.svg"
    use_for: "Azure Monitor, Log Analytics"
  - image: "img/lib/azure2/management/Azure_Policy.svg"
    use_for: "Azure Policy"
  - image: "img/lib/azure2/management/Resource_Groups.svg"
    use_for: "リソースグループ"
  - image: "img/lib/azure2/management/Subscriptions.svg"
    use_for: "サブスクリプション"

  # Integration
  - image: "img/lib/azure2/integration/API_Management_Services.svg"
    use_for: "API Management"
  - image: "img/lib/azure2/integration/Logic_Apps.svg"
    use_for: "Logic Apps"
  - image: "img/lib/azure2/integration/Service_Bus.svg"
    use_for: "Service Bus"

  # Networking (追加)
  - image: "img/lib/azure2/networking/Front_Doors.svg"
    use_for: "Front Door"
  - image: "img/lib/azure2/networking/ExpressRoute_Circuits.svg"
    use_for: "ExpressRoute"
  - image: "img/lib/azure2/networking/VPN_Gateway.svg"
    use_for: "VPN Gateway"

  # IoT
  - image: "img/lib/azure2/iot/IoT_Hub.svg"
    use_for: "IoT Hub"

  # AI & Machine Learning
  - image: "img/lib/azure2/ai_machine_learning/Azure_Machine_Learning.svg"
    use_for: "Azure Machine Learning"
  - image: "img/lib/azure2/ai_machine_learning/Cognitive_Services.svg"
    use_for: "Cognitive Services"
```

### Azure2 ライブラリのパス構造

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
│   ├── Application_Gateway.svg
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

### 非推奨フォーマット（使用禁止）

```xml
<!-- ❌ 動作しない形式（VS Code で青い四角形になる） -->
<mxCell style="shape=mxgraph.azure.Azure_Firewall;fillColor=#0078D4;..." />
<mxCell style="sketch=0;shape=mxgraph.azure.virtual_machine;fillColor=#0078D4;..." />
<mxCell style="shape=mxgraph.azure.front_door;fillColor=#0078D4;..." />

<!-- ✅ 正しい形式（推奨：VS Code + Web 両対応） -->
<mxCell style="aspect=fixed;html=1;points=[];align=center;image;fontSize=12;image=img/lib/azure2/networking/Azure_Firewall.svg;verticalLabelPosition=bottom;verticalAlign=top;" />
```

### スタイル属性の違い

| 属性          | 旧形式 (mxgraph.azure) | 新形式 (azure2)             |
| ------------- | ---------------------- | --------------------------- |
| `shape`       | `mxgraph.azure.*`      | 不要                        |
| `image`       | なし                   | `img/lib/azure2/**/*.svg`   |
| `aspect`      | なし                   | `fixed`（アスペクト比固定） |
| `fillColor`   | `#0078D4`              | 不要（SVG に含まれる）      |
| `strokeColor` | 指定                   | 不要                        |

### 主要 Azure サービスの新旧形式対照表

| サービス        | 旧形式（❌ 禁止）                            | 新形式（✅ 必須）                                              |
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

---

## 🟠 AWS アイコン

### 基本ルール

| ルール               | 内容                                                                |
| -------------------- | ------------------------------------------------------------------- |
| **AWS アイコン必須** | AWS 関連の図は `mxgraph.aws4.resourceIcon` 形式の公式アイコンを使用 |
| **汎用四角形禁止**   | AWS リソースを汎用四角形+テキストで表現してはいけない               |
| **対象スコープ**     | EC2, VPC, S3, Lambda, RDS, ECS/EKS, CloudFront, Route 53, IAM 等    |

### 正式 mxCell フォーマット

```xml
<mxCell id="ec2-1" value="Web Server"
        style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="50" height="50" as="geometry"/>
</mxCell>
```

### AWS カテゴリ別カラー

| カテゴリ   | fillColor | 対象サービス                   |
| ---------- | --------- | ------------------------------ |
| Compute    | `#ED7100` | EC2, Lambda, ECS, EKS, Fargate |
| Storage    | `#7AA116` | S3, EBS, EFS                   |
| Database   | `#C925D1` | RDS, DynamoDB, Aurora          |
| Networking | `#8C4FFF` | VPC, ALB, CloudFront, Route 53 |
| Security   | `#DD344C` | IAM, Cognito, WAF              |
| Management | `#E7157B` | CloudWatch, SNS, SQS           |

### 主要 AWS アイコンマッピング

```yaml
aws_icons:
  style_format: "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service}"
  base_style: "sketch=0;outlineConnect=0;fontColor=#232F3E;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"

  # Compute (fillColor=#ED7100)
  - resIcon: "mxgraph.aws4.ec2"
    use_for: "EC2, 仮想サーバー"
  - resIcon: "mxgraph.aws4.lambda"
    use_for: "Lambda, サーバーレス"
  - resIcon: "mxgraph.aws4.ecs"
    use_for: "ECS, コンテナ"
  - resIcon: "mxgraph.aws4.eks"
    use_for: "EKS, Kubernetes"
  - resIcon: "mxgraph.aws4.fargate"
    use_for: "Fargate"

  # Networking (fillColor=#8C4FFF)
  - resIcon: "mxgraph.aws4.vpc"
    use_for: "VPC"
  - resIcon: "mxgraph.aws4.subnet"
    use_for: "サブネット"
  - resIcon: "mxgraph.aws4.internet_gateway"
    use_for: "Internet Gateway, IGW"
  - resIcon: "mxgraph.aws4.nat_gateway"
    use_for: "NAT Gateway"
  - resIcon: "mxgraph.aws4.application_load_balancer"
    use_for: "ALB"
  - resIcon: "mxgraph.aws4.network_load_balancer"
    use_for: "NLB"
  - resIcon: "mxgraph.aws4.route_53"
    use_for: "Route 53, DNS"
  - resIcon: "mxgraph.aws4.cloudfront"
    use_for: "CloudFront, CDN"
  - resIcon: "mxgraph.aws4.api_gateway"
    use_for: "API Gateway"
  - resIcon: "mxgraph.aws4.security_group"
    use_for: "Security Group"

  # Storage (fillColor=#7AA116)
  - resIcon: "mxgraph.aws4.s3"
    use_for: "S3, オブジェクトストレージ"
  - resIcon: "mxgraph.aws4.elastic_block_store"
    use_for: "EBS"
  - resIcon: "mxgraph.aws4.elastic_file_system"
    use_for: "EFS"

  # Database (fillColor=#C925D1)
  - resIcon: "mxgraph.aws4.rds"
    use_for: "RDS"
  - resIcon: "mxgraph.aws4.dynamodb"
    use_for: "DynamoDB"
  - resIcon: "mxgraph.aws4.aurora"
    use_for: "Aurora"
  - resIcon: "mxgraph.aws4.elasticache"
    use_for: "ElastiCache"

  # Security & Identity (fillColor=#DD344C)
  - resIcon: "mxgraph.aws4.iam"
    use_for: "IAM"
  - resIcon: "mxgraph.aws4.cognito"
    use_for: "Cognito"
  - resIcon: "mxgraph.aws4.key_management_service"
    use_for: "KMS"
  - resIcon: "mxgraph.aws4.waf"
    use_for: "WAF"

  # Others
  - resIcon: "mxgraph.aws4.cloudwatch"
    use_for: "CloudWatch"
  - resIcon: "mxgraph.aws4.sns"
    use_for: "SNS"
  - resIcon: "mxgraph.aws4.sqs"
    use_for: "SQS"
  - resIcon: "mxgraph.aws4.step_functions"
    use_for: "Step Functions"
```

### 非推奨フォーマット（使用禁止）

```xml
<!-- ❌ 動作しない形式 -->
<mxCell style="shape=mxgraph.aws4.ec2;fillColor=#FF9900;" />

<!-- ✅ 正しい形式（resourceIcon + resIcon の組み合わせ必須） -->
<mxCell style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#ED7100;..." />
```

---

## 禁止事項（共通）

- ❌ クラウドリソースを**汎用四角形**で表現
- ❌ クラウドリソースを**単純な図形+テキスト**で代用
- ❌ 古い/非推奨のフォーマットを使用
- ✅ 必ず上記の正式フォーマットを使用すること

---

## 📋 draw.io でのライブラリ有効化（事前設定）

> **⚠️ 重要**: この設定をしないと、生成した `.drawio` ファイルを開いてもアイコンが正しく表示されない場合があります。

### 設定手順

#### VS Code Draw.io Integration の場合

1. draw.io エディタで任意の `.drawio` ファイルを開く
2. 左下の「**+ その他の図形**」（または「+ More Shapes」）をクリック
3. 「**ネットワーク**」カテゴリを展開
4. 以下にチェックを入れる：
   - ✅ **Azure** - Azure アイコンライブラリ
   - ✅ **AWS17** / **AWS18** / **AWS 2026** - AWS アイコンライブラリ（必要に応じて）
5. 「**設定を保存**」にチェックが入っていることを確認
6. 「**適用**」をクリック

#### Web 版 draw.io (app.diagrams.net) の場合

1. https://app.diagrams.net を開く
2. 左下の「**+ その他の図形**」をクリック
3. 「**ネットワーク**」セクションで **Azure** / **AWS** にチェック
4. 「**適用**」をクリック

### 設定画面イメージ

```
┌─────────────────────────────────────┐
│ 図形                            × │
├─────────────────────────────────────┤
│ ネットワーク                        │
│  ☐ Alibaba Cloud                   │
│  ☐ Allied Telesis                  │
│  ☑ AWS17                           │
│  ☑ AWS18                           │
│  ☑ AWS 2026                        │
│  ☐ AWS 3D                          │
│  ☑ Azure        ← ★必須★          │
│  ☐ Cloud & Enterprise              │
│  ☐ Cisco                           │
│  ...                               │
├─────────────────────────────────────┤
│ ☐ Labels  ☑ 設定を保存   [適用]    │
└─────────────────────────────────────┘
```

### 設定が反映されない場合

| 症状                       | 対処法                                                                 |
| -------------------------- | ---------------------------------------------------------------------- |
| Azure アイコンが青い四角形 | 「Azure」ライブラリにチェックが入っているか確認                        |
| 設定が保存されない         | 「設定を保存」にチェックを入れて再度適用                               |
| VS Code 再起動後に戻る     | VS Code の設定で `hediet.vscode-drawio.customLibraries` を確認         |
| それでも表示されない       | `img/lib/azure2/` 形式を使用しているか確認（本インストラクション準拠） |

### 補足: AWS アイコンライブラリの違い

| ライブラリ | 説明                               |
| ---------- | ---------------------------------- |
| AWS17      | 2017 年版 AWS アイコン（レガシー） |
| AWS18      | 2018 年版 AWS アイコン             |
| AWS 2026   | 最新版 AWS アイコン（推奨）        |
| AWS 3D     | 3D スタイルの AWS アイコン         |

---

## 関連ドキュメント

- [Azure アイコン VS Code 互換性修正ガイド](../../docs/azure-icon-vscode-compatibility.md)
- [Draw.io Azure Icons Library (GitHub)](https://github.com/jgraph/drawio/tree/dev/src/main/webapp/img/lib/azure2)
- [VS Code Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)
